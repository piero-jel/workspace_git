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

@file client.py
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
Author         Date           Version      Brief
JEL            2026.04.16     0.0.3        Version Inicial no release
"""

# build-in modules
import sys
#from uuid import uuid4
#from typing import Callable
import json

# third-party modules
from grpc import Channel#,insecure_channel
#from google.protobuf.json_format import MessageToDict
from google.protobuf.empty_pb2 import Empty

# project modules
from settings import (GRPC_URL,GRPC_PORT)
from protobuf.pipeline_process_pb2 import (
    CreateRequest,CreateResponse,
    GetRequest,GetResponse,
    PutRequest,PutResponse,
    ListJobsRequest,ListJobsResponse,
    ListProvidersResponse
)
import protobuf.pipeline_process_pb2_grpc as gRPCStub
from grpc_utils import gRPCClient


    

class PipelineProcessClient(gRPCClient):

    def create(self,ch:Channel,request:dict)->dict:
        stub = gRPCStub.CreateStub(ch)        
        response:CreateResponse = stub.create(CreateRequest(**request))
        return response
    
    def get(self,ch:Channel,request:dict)->dict:
        stub = gRPCStub.GetStub(ch)        
        response:GetResponse = stub.get(GetRequest(**request))
        return response
    
    def put(self,ch:Channel,request:dict)->dict:
        stub = gRPCStub.PutStub(ch)        
        response:PutResponse = stub.put(PutRequest(**request))
        return response
    
    def list_jobs(self,ch:Channel,request:dict=None)->dict:
        stub = gRPCStub.ListJobsStub(ch)
        response:ListJobsResponse = None
        if request is None:
            response = stub.list_jobs(ListJobsRequest())
        else:
            response = stub.list_jobs(ListJobsRequest(**request))
        return response

    def list_providers(self,ch:Channel)->dict:
        stub = gRPCStub.ListProvidersStub(ch)        
        response:ListProvidersResponse = stub.list_providers(Empty())
        return response


def get_parmas(options:list[str])->tuple[str,dict]:
    argv:list = sys.argv
    argc:int  = len(argv)

    targets:list[str] = [f'--{x}' for x in options]

    if argc < 2: # <2
        print(f'Error en el llamado {argv[0]}, intente con las opciones:')
        #print(f'{argv[0]} {targets}')
        print(f'{argv[0]} {" [params] | ".join(targets)} [params]\n\n')
        sys.exit(0)
    
    if argv[1] not in targets:
        print(f'Error en el llamado {argv[0]}, parametro {argv[1]} invalido')        
        sys.exit(0)

    opt = options[targets.index(argv[1])]
    if argc < 3:
        return opt,None
    
    return opt,json.loads(argv[2])



def main():
    """ funcion principal del modulo """
    cliente:PipelineProcessClient = PipelineProcessClient(url=GRPC_URL,port=GRPC_PORT)
    #print(f'cliente: {cliente.methods}')
    opt,request = get_parmas(cliente.methods)
    #print(f'opt: {opt} | data: {request}')
    
    response:dict = None
    try:
        if request is None:
            response = cliente.run(opt)
        else:
            response = cliente.run(opt,request)

        print(f"{opt} Response:{json.dumps(response,indent=2)}")
    except Exception as e:
        print(f'Exception<{type(e).__name__}>, detail {e}')

    
    


if __name__ == "__main__":
    main()
