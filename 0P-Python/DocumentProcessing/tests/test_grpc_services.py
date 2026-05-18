"""
Copyright 2026, Jesus Emanuel Luccioni0
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

@file test_worker_redis.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.3.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version     Brief
JEL            2026.04.14     0.0.3       Version Inicial no release
JEL            2026.05.17     0.0.4       Add logger in gRPC Server, delete jobs creados y
                                          ajustes para pylint
"""
# build-in module
import unittest
from collections import namedtuple

# third-party modules
from grpc import StatusCode
from grpc_testing import server_from_dictionary, strict_real_time
from google.protobuf.empty_pb2 import Empty

# project modules, under test
from tests.config import get_log,unittest_log,Logger
from app.infrastructure.grpc.protobuf.pipeline_process_pb2 import (
    DESCRIPTOR,
    CreateRequest,
    GetRequest,
    PutRequest,
    ListJobsRequest
)

from tests.grpc_settings import (GRPC_MOCK,GRPC_URL)
from app.infrastructure.grpc.server import (
    CreateProcess,
    GetProcess,
    PutProcess,
    ListJobsProcess,
    ListProvidersProcess,
    PipelineProcessServer,
)
from app.infrastructure.grpc.client import PipelineProcessClient



ServicesReg = namedtuple('ServicesReg',[ 'name','server'])



@unittest.skipIf(not GRPC_MOCK, 'gRPC Mock Deshabilitado') # Omite si el mock esta deshabiltiado
class Test_gRPCServicesMock(unittest.TestCase):
    ''' Test Case For Test_WorkerId

        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServicesMock
    '''
    @classmethod
    def setUpClass(cls):
        cls.log = get_log(cls.__name__)
        cls.job_list:list = []
        return super().setUpClass()
    
    def setUp(self):
        self.log:Logger = type(self).log
        self.job_id:str = None
        # Creamos las instancias de todos los services
        services:list[ServicesReg] = [
            ServicesReg(name='Create'       ,server=CreateProcess(log=self.log)),
            ServicesReg(name='Get'          ,server=GetProcess(log=self.log)),
            ServicesReg(name='Put'          ,server=PutProcess()),
            ServicesReg(name='ListJobs'     ,server=ListJobsProcess(log=self.log)),
            ServicesReg(name='ListProviders',server=ListProvidersProcess()),
        ]
        # Armamos el dict con los server
        servicers:dict = {
            DESCRIPTOR.services_by_name[it.name]:it.server for it in services
        }
        # Crear el servidor para las pruebas
        self.test_server = server_from_dictionary(servicers, strict_real_time())
        return super().setUp()
    
    def tearDown(self):
        if self.job_id is not None:
            req:dict = { "job_id" : self.job_id, "status":"deleted"}
            request = PutRequest(**req)
            # Invocar el método directamente
            method = self.test_server.invoke_unary_unary(
                method_descriptor=(
                    DESCRIPTOR.services_by_name['Put'].methods_by_name['put']
                ),
                invocation_metadata={},
                request=request,
                timeout=10
            )
            # Obtener respuesta
            response, _, code, details = method.termination()

            # Verificaciones
            self.log.info(f'{type(self).__name__}::tearDown() response:\n{response}')
            if code != StatusCode.OK: 
                # en caso de timeout log el mensaje
                self.log.info(f'{type(self).__name__}::tearDown() response error details {details}')

        return super().tearDown()
    

    def test_create_v1(self):
        ''' Test case para el service Create
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServicesMock.test_create_v1
        '''        
        req:dict = {
            "name": "Archivo de test por gRPC",
            "topic": "dato-comprimidos-v1",
            "content": "string con el contenido del archivo",
            "compression": "gzip",
            "pipeline_config" : " extraction , analysis, enrichment "
        }
        request = CreateRequest(**req)
         # Invocar el método directamente
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(
                DESCRIPTOR.services_by_name['Create'].methods_by_name['create']
            ),
            invocation_metadata={},
            request=request,
            timeout=1
        )
        # Obtener respuesta
        response, metadata, code, details = method.termination()

        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_create_v1() response:\n{response}')
        self.assertEqual(code, StatusCode.OK)
        self.assertEqual(response.name, req['name'])
        self.assertEqual(response.topic, req['topic'])
        self.assertEqual(response.compression, req['compression'])
        self.assertEqual(response.pipeline_config, req['pipeline_config'])
        self.job_id = response.job_id

    def test_get_v1(self):
        ''' Test case para el service Get
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServicesMock.test_get_v1
        '''
        req:dict = {
            "job_id" : "XYZPPDADFAFDEAEFAEFEAQV" # Fake id
        }
        request = GetRequest(**req)
         # Invocar el método directamente
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(
                DESCRIPTOR.services_by_name['Get'].methods_by_name['get']
            ),
            invocation_metadata={},
            request=request,
            timeout=10 # 10 seconds 
        )
        # Obtener respuesta
        response, metadata, code, details = method.termination()
        if code != StatusCode.OK: 
            # en caso de timeout
            self.log.info(f'{type(self).__name__}::test_get_v1() response error details {details}')
            return 

        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_get_v1() response:\n{response}')
        self.assertEqual(code, StatusCode.OK)
        self.assertEqual(response.job_id, req['job_id'])
    
    def test_put_v1(self):
        ''' Test case para el service Put cancel or delete job
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServicesMock.test_put_v1
        '''
        req:dict = {
            "job_id" : "XYZPPDADFAFDEAEFAEFEAQV",
            "status":"cancelled"
        }
        request = PutRequest(**req)
         # Invocar el método directamente
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(
                DESCRIPTOR.services_by_name['Put'].methods_by_name['put']
            ),
            invocation_metadata={},
            request=request,
            timeout=10
        )
        # Obtener respuesta
        response, metadata, code, details = method.termination()
        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_put_v1() response:\n{response}')
        if code != StatusCode.OK: 
            # en caso de timeout log el mensaje
            self.log.info(f'{type(self).__name__}::test_put_v1() response error details {details}')
            return 
        
        self.assertEqual(code, StatusCode.OK)
        self.assertEqual(response.job_id, req['job_id'])

    def test_list_jobs_v1(self):
        ''' Test case para el service ListJobs cancel or delete job
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServicesMock.test_list_jobs_v1
        '''
        req:dict = {
            "status":"pending",
        }
        request = ListJobsRequest(**req)
         # Invocar el método directamente
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(
                DESCRIPTOR.services_by_name['ListJobs'].methods_by_name['list_jobs']
            ),
            invocation_metadata={},
            request=request,
            timeout=1
        )
        # Obtener respuesta
        response, metadata, code, details = method.termination()
        # Verificaciones
        state_list:tuple[str]= (
            "completed",
            "pending",
            "processing",
            "failed",
            "cancelled",
        )
        self.log.info(f'{type(self).__name__}::test_list_jobs_v1() response:\n{response}')
        self.assertEqual(code, StatusCode.OK)
        for st in state_list:
            if st == req["status"]:
                continue
            # todos los attr diferente al consultado deben esta vacio
            self.assertEqual(len(getattr(response,st)),0)

    def test_list_jobs_v2(self):
        ''' Test case para el service ListJobs por status
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServicesMock.test_list_jobs_v2
        '''        
        request = ListJobsRequest()
         # Invocar el método directamente
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(
                DESCRIPTOR.services_by_name['ListJobs'].methods_by_name['list_jobs']
            ),
            invocation_metadata={},
            request=request,
            timeout=1
        )
        # Obtener respuesta
        response, metadata, code, details = method.termination()
        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_list_jobs_v2() response:\n{response}')
        self.assertEqual(code, StatusCode.OK)

    def test_list_providers_v1(self):
        ''' Test case para el service ListProviders 
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServicesMock.test_list_providers_v1
        '''        
        # Invocar el método directamente
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(
                DESCRIPTOR.services_by_name['ListProviders'].methods_by_name['list_providers']
            ),
            invocation_metadata={},
            request=Empty(),
            timeout=1
        )
        # Obtener respuesta
        response, metadata, code, details = method.termination()
        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_list_providers_v1() response:\n{response}')
        self.assertEqual(code, StatusCode.OK)
        self.assertTrue(len(response.providers) > 0 )
        


@unittest.skipIf(GRPC_MOCK, 'gRPC Mock Habilitado') # Omite si el mock esta habiltiado
class Test_gRPCServices(unittest.TestCase):
    ''' Test Case For Test_WorkerId

        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServices
    '''
    @classmethod
    def setUpClass(cls):
        cls.log = get_log(cls.__name__)        
        return super().setUpClass()
    
    def setUp(self):
        self.log:Logger = type(self).log
        self.job_id:str = None
        # Creamos las instancias de todos los services
        self.server:PipelineProcessServer = PipelineProcessServer(port=0,pool_thread=1,
                                                                  log=type(self).log)
        self.server.run()
        self.cliente:PipelineProcessClient = PipelineProcessClient(url=GRPC_URL,
                                                                   port=self.server.port)
        return super().setUp()
    
    def tearDown(self):
        
        if self.job_id is not None:
            req:dict = { "job_id" : self.job_id, "status":"deleted"}
            response:dict = self.cliente.run('put',req)
            self.log.info(f'{type(self).__name__}::tearDown() delete {self.job_id} response:\n{response}')

        self.server.stop()
        return super().tearDown()


    def test_create_v1(self):
        ''' Test case para el service Create
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServices.test_create_v1
        '''        
        req:dict = {
            "name": "Archivo de test por gRPC",
            "topic": "dato-comprimidos-v1",
            "content": "string con el contenido del archivo",
            "compression": "gzip",
            "pipeline_config" : " extraction , analysis, enrichment "
        }
        
        # Obtener respuesta
        response:dict = self.cliente.run('create',req)

        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_create_v1() response:\n{response}')
        self.job_id = response['job_id']
        self.assertEqual(response['name'], req['name'])
        self.assertEqual(response['topic'], req['topic'])
        self.assertEqual(response['compression'], req['compression'])
        self.assertEqual(response['pipeline_config'], req['pipeline_config'])        
        self.assertEqual(response['code'], 0)

    def test_get_v1(self):
        ''' Test case para el service Get
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServices.test_get_v1
        '''
        req:dict = {
            "job_id" : "XYZPPDADFAFDEAEFAEFEAQV"
        }
        
        # Obtener respuesta        
        response:dict = self.cliente.run('get',req)
        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_get_v1() response:\n{response}')
        self.assertEqual(response['job_id'], req['job_id'])
        self.assertEqual(response['code'], 1)
    
    def test_put_v1(self):
        ''' Test case para el service Put cancel or delete job
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServices.test_put_v1
        '''
        req:dict = {
            "job_id" : "XYZPPDADFAFDEAEFAEFEAQV", # fake id
            "status":"cancelled"
        }
        # Obtener respuesta        
        response:dict = self.cliente.run('put',req)

        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_put_v1() response:\n{response}')
        self.assertEqual(response['job_id'], req['job_id'])
        self.assertEqual(response['code'], 1)

    def test_list_jobs_v1(self):
        ''' Test case para el service ListJobs cancel or delete job
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServices.test_list_jobs_v1
        '''
        req:dict = {
            "status":"pending",
        }
        # Obtener respuesta        
        response:dict = self.cliente.run('list_jobs',req)

        # Verificaciones
        state_list:tuple[str]= (
            "completed",
            "pending",
            "processing",
            "failed",
            "cancelled",
        )
        self.log.info(f'{type(self).__name__}::test_list_jobs_v1() response:\n{response}')
        self.assertEqual(response['code'], 0)
        for st in state_list:
            if st == req["status"]:
                continue
            # todos los attr diferente al consultado deben esta vacio
            self.assertEqual(len(response[st]),0)

    def test_list_jobs_v2(self):
        ''' Test case para el service ListJobs por status
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServices.test_list_jobs_v2
        '''        
         # Invocar el método directamente
        # Obtener respuesta        
        response:dict = self.cliente.run('list_jobs')
        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_list_jobs_v2() response:\n{response}')
        self.assertEqual(response['code'], 0)

    def test_list_providers_v1(self):
        ''' Test case para el service ListProviders 
           
        python3 -m unittest -v tests.test_grpc_services.Test_gRPCServices.test_list_providers_v1
        '''        
        # Invocar el método directamente
        response:dict = self.cliente.run('list_providers')
        
        # Verificaciones
        self.log.info(f'{type(self).__name__}::test_list_providers_v1() response:\n{response}')
        self.assertEqual(response['code'], 0)
        self.assertTrue(len(response['providers']) > 0 )
                
