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
JEL            2026.05.17     0.0.4          Add Logger for gRPCServer y Ajustes para pylint
"""

# build-in modules
from argparse import ArgumentParser

# third-party modules
from google.protobuf.empty_pb2 import Empty #pylint:disable=no-name-in-module

# project modules
from settings import (GRPC_POLL_TRHEAD,GRPC_PORT,get_logger,Logger) #pylint:disable=import-error
from app.infrastructure.grpc.protobuf.pipeline_process_pb2 import ( #pylint:disable=no-name-in-module
    CreateRequest,CreateResponse,
    GetRequest,GetResponse,
    PutRequest,PutResponse,
    ListJobsRequest,ListJobsResponse,
    ListProvidersResponse
)
from app.infrastructure.grpc.grpc_utils import gRPCUtils,gRPCServer,gRPCServicesReg
import app.infrastructure.grpc.protobuf.pipeline_process_pb2_grpc as gRPCStub

from app.application.services import ProcessGateway
from app.infrastructure.adapters.tasks_celery import TaskProcessingGateway
from app.infrastructure.adapters.worker_redis import (
    WorkerRedis,
    #WorkerIdRedis,WorkerStatus
)

class Process: # pylint:disable=too-few-public-methods
    """ clase para agregar el manejo de log a los server"""
    log:Logger
    def __init__(self,log:Logger):
        self.log = log

class CreateProcess(gRPCStub.CreateServicer,Process):
    """ clase concreta que maneja el servicio gRPC Create"""
    def create(self, request:CreateRequest,context):#pylint:disable=unused-argument
        """ metodo create del services"""

        dct_req:dict = gRPCUtils.objgrpc2dict(request)
        dct_req['pipeline_config'] = [
            x.strip().lower() for x in request.pipeline_config.split(',')
        ]
        self.log.info(f'{type(self).__name__}::create({dct_req})')
        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(dct_req))

        return CreateResponse(
            job_id=job_id,
            name=request.name,
            topic=request.topic,
            compression=request.compression,
            pipeline_config=request.pipeline_config
        )


class GetProcess(gRPCStub.GetServicer,Process):
    """ clase concreta que maneja el servicio gRPC Get"""
    def get(self, request:GetRequest,context):#pylint:disable=unused-argument
        """ metodo get del servicio"""
        resp:dict = ProcessGateway(WorkerRedis()).get(request.job_id)
        self.log.info('%s::list_jobs(), resp: %s',type(self).__name__,resp)
        return GetResponse(**resp)


class PutProcess(gRPCStub.PutServicer):
    """ clase concreta que maneja el servicio gRPC Put"""
    def put(self, request:PutRequest,context):#pylint:disable=unused-argument
        """ metodo put del servicio"""
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


class ListJobsProcess(gRPCStub.ListJobsServicer,Process):
    """ clase concreta que maneja el servicio gRPC ListJobs"""
    def list_jobs(self, request:ListJobsRequest,context):#pylint:disable=unused-argument
        """ metodo list_jobs del servicio"""
        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        resp:dict = None

        if not request.HasField('status'):
            resp = pr_gateway.get_list()
        else:
            resp = pr_gateway.get_list(status=request.status)

        self.log.info('%s::list_jobs(), resp: %s',type(self).__name__,resp)
        return ListJobsResponse(**resp)


class ListProvidersProcess(gRPCStub.ListProvidersServicer):
    """ clase concreta que maneja el servicio gRPC ListProviders"""
    def list_providers(self,request:Empty,context):#pylint:disable=unused-argument
        """ Metodo list_provider del servicio"""
        #return ListProvidersResponse(providers=response)
        return ListProvidersResponse(**ProcessGateway(WorkerRedis()).get_providers())


class PipelineProcessServer(gRPCServer):
    """ clase concreta que modela el server gRPC, con todos los serivicios anteriores"""
    def add_services(self):
        """ metodo que agrega el listado de services al server gRPC"""
        list_services:list[gRPCServicesReg] = [
            gRPCServicesReg(name='Create'       ,server=CreateProcess(log=self.log)),
            gRPCServicesReg(name='Get'          ,server=GetProcess(log=self.log)),
            gRPCServicesReg(name='Put'          ,server=PutProcess()),
            gRPCServicesReg(name='ListJobs'     ,server=ListJobsProcess(log=self.log)),
            gRPCServicesReg(name='ListProviders',server=ListProvidersProcess()),
        ]

        self.add(gRPCStub,list_services)

def main():
    """ metodo principal del servicio a lanzar"""
    try:
        ## --port VAL:int
        ## --pool_thread VAL:int
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
                                    pool_thread=int(args.pool_thread),
                                    log=get_logger(__name__))

        srv.run()
        print(f"Server started, listening on {srv.port}, thread pool {srv.pool_thread}")
        srv.join()

    except Exception as e: #pylint:disable=broad-exception-caught
        print(f'Exception <{type(e).__name__}, detail {e}>')
    except KeyboardInterrupt:
        print('KeyboardInterrupt, end services.')


if __name__ == "__main__":
    main()
