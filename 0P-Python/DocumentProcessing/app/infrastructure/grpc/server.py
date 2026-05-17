"""
Copyright 2026, Jesus Emanuel Luccioni
All rights reserved.

This file is part of devops for Open Container (in this case docker )

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

@file server.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.3.
@date Sabado 16 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version        Brief
JEL            2026.04.16     0.0.3          Version Inicial no release
"""

# build-in modules
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser
from uuid import uuid4

# third-party modules
from grpc import Server,server
from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict

# project modules
from settings import (GRPC_POLL_TRHEAD,GRPC_PORT,get_logger,Logger)
from protobuf.pipeline_process_pb2 import (
    CreateRequest,CreateResponse,
    GetRequest,GetResponse,
    PutRequest,PutResponse,
    ListJobsRequest,ListJobsResponse,
    ListProvidersResponse
)

from grpc_utils import gRPCUtils,gRPCServer,gRPCServicesReg
import protobuf.pipeline_process_pb2_grpc as gRPCStub
from app.application.services import ProcessGateway
from app.infrastructure.adapters.tasks_celery import TaskProcessingGateway
from app.infrastructure.adapters.worker_redis import ( WorkerRedis )

log:Logger = get_logger(__name__)

class CreateProcess(gRPCStub.CreateServicer):
    def create(self, request:CreateRequest,context):

        dct_req:dict = gRPCUtils.objgrpc2dict(request)
        dct_req['pipeline_config'] = [
            x.strip().lower() for x in request.pipeline_config.split(',')
        ]
        log.info(f'{type(self).__name__}::create({dct_req})')
        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(dct_req))

        return CreateResponse(
            job_id=job_id,
            name=request.name,
            topic=request.topic,
            compression=request.compression,
            pipeline_config=request.pipeline_config
        )


class GetProcess(gRPCStub.GetServicer):
    def get(self, request:GetRequest,context):
        resp:dict = ProcessGateway(WorkerRedis()).get(request.job_id)
        log.info('%s::list_jobs(), resp: %s',type(self).__name__,resp)
        return GetResponse(**resp)

    
class PutProcess(gRPCStub.PutServicer):
    def put(self, request:PutRequest,context):

        st:str = request.status.strip().lower()
        pr:ProcessGateway = ProcessGateway(WorkerRedis())
        resp:dict = None
        match st:
            case 'cancelled':
                resp = pr.cancel(request.job_id)

            case 'deleted':
                resp = pr.delete(request.job_id)

            case _:
                resp = {
                    "code"    : 1,
                    "job_id"  : request.job_id,
                    "status"  : request.status,
                    "message" : f"Estado '{st}' no permitido, solo 'cancelled' o 'deleted'",
                }

        return PutResponse(**resp)


class ListJobsProcess(gRPCStub.ListJobsServicer):
    def list_jobs(self, request:ListJobsRequest,context):

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        resp:dict = None
       
        if not request.HasField('status'):
            resp = pr_gateway.get_list()
        else:
            resp = pr_gateway.get_list(status=request.status)

        log.info('%s::list_jobs(), resp: %s',type(self).__name__,resp)
        return ListJobsResponse(**resp)


class ListProvidersProcess(gRPCStub.ListProvidersServicer):
    def list_providers(self,request:Empty,context):
        return ListProvidersResponse(**ProcessGateway(WorkerRedis()).get_providers())
    

class PipelineProcessServer(gRPCServer):
    list_services:list[gRPCServicesReg] = [
        gRPCServicesReg(name='Create'       ,server=CreateProcess()),
        gRPCServicesReg(name='Get'          ,server=GetProcess()),
        gRPCServicesReg(name='Put'          ,server=PutProcess()),
        gRPCServicesReg(name='ListJobs'     ,server=ListJobsProcess()),
        gRPCServicesReg(name='ListProviders',server=ListProvidersProcess()),
    ]
    
    def add_services(self):
        self.add(gRPCStub,self.list_services)

def main():
    try:
        ## --port VAL:int        
        ## --pool-thread VAL:int
        parser = ArgumentParser(description="gRPC Server")
        parser.add_argument(
            "--port",
            default=GRPC_PORT,
            required=False,
            help="Port Server."
        )
        parser.add_argument(
            "--pool_thread",
            required=False,
            default=GRPC_POLL_TRHEAD,
            help="Max number of thread for pool server."
        )
        args = parser.parse_args()
        srv = PipelineProcessServer(port=int(args.port),
                                    pool_thread=int(args.pool_thread))
        
        srv.run()
        print(f"Server started, listening on {srv.port}, thread pool {srv.pool_thread}")
        srv.join()
        
    except Exception as e:
        print(f'Exception <{type(e).__name__}, detail {e}>')
    except KeyboardInterrupt:
        print('KeyboardInterrupt, end services.')


if __name__ == "__main__":    
    main()
