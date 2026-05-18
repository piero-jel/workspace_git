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

@file test_fastapi.py
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
"""
# build-in module
import unittest   
from time import sleep
#import json
#import random
from uuid import uuid4
#from collections import namedtuple


# third-party modules
from fastapi.testclient import TestClient

# project modules, under test
from tests.config import get_log,Logger#,unittest_log
from app.infrastructure.apis.fastapi import fastapi
from app.application.services import ProcessGateway
from app.infrastructure.adapters.worker_redis import WorkerRedis

#from tests.fastapi_settings import (FAST_API_MOCK,FAST_API_PORT,FAST_API_URL)





class Test_ProcessCreate(unittest.TestCase):
    ''' Test Cases For EndPoint process_create() POST /pipeline_process/

        python3 -m unittest -v tests.test_fastapi.Test_ProcessCreate
    '''
    @classmethod
    def setUpClass(cls):
        cls.log:Logger = get_log(cls.__name__)
        cls.job_list:list = []
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        client = TestClient(fastapi)
        request:dict = {"status": "deleted"}
        for job_id in cls.job_list:
            response = client.put(f"pipeline_process/{job_id}",json=request)
            cls.log.info('%s.tearDownClass() delete %s, response: %s',
                         cls.__name__,job_id,response)

        return super().tearDownClass()
    
    def setUp(self):
        self.log = type(self).log
        self.client = TestClient(fastapi)
        self.job_id:str = None
        return super().setUp()

    def tearDown(self):
        # FIXME next step mock WorkerRedis()
        if self.job_id is not None:
            type(self).job_list.append(self.job_id)

        return super().tearDown()

    def test_post_default(self):
        ''' Test case with default body in post

        python3 -m unittest -v tests.test_fastapi.Test_ProcessCreate.test_post_default
        '''
        # compression y pipeline_config, son opcionales
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo"
        }
        response = self.client.post("pipeline_process/",json=request)
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id = resp['job_id']
        self.assertIsInstance(self.job_id,str)
        
        self.log.info(f'{type(self).__name__}::test_post_default(), response: {resp}')        
        
        # campos request idem to response
        for key in ('name','topic'):
            self.assertEqual(request[key],resp[key])
        
        # campos por defualt 
        self.assertIsNone(resp['compression'])
        self.assertEqual(resp['pipeline_config'],['extraction'])

    def test_post_compression(self):
        ''' Test case with default body in post

        python3 -m unittest -v tests.test_fastapi.Test_ProcessCreate.test_post_compression
        '''
        # compression y pipeline_config, son opcionales
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo",
            "compression" : "gzip"
        }
        response = self.client.post("pipeline_process/",json=request)

        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id = resp['job_id']
        self.assertIsInstance(self.job_id,str)
        
        self.log.info(f'{type(self).__name__}::test_post_compression(), response: {resp}')        
        
        # campos request idem to response
        for key in ('name','topic','compression'):
            self.assertEqual(request[key],resp[key])
        
        # campos por defualt         
        self.assertEqual(resp['pipeline_config'],['extraction'])

    def test_post_pipeline_config(self):
        ''' Test case with default body in post

        python3 -m unittest -v tests.test_fastapi.Test_ProcessCreate.test_post_pipeline_config
        '''
        # compression y pipeline_config, son opcionales
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo",
            "pipeline_config" : ["Extraction "," Analysis ", "Enrichment"]
        }
        response = self.client.post("pipeline_process/",json=request)

        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id = resp['job_id']
        self.assertIsInstance(self.job_id,str)
        
        self.log.info(f'{type(self).__name__}::test_post_pipeline_config(), response: {resp}')        
        
        # campos request idem to response
        for key in ('name','topic'):
            self.assertEqual(request[key],resp[key])
        
        self.assertListEqual(resp['pipeline_config'],
                            [x.strip().lower() for x in request['pipeline_config']])
        
    def test_post_pipeline_config_v2(self):
        ''' Test case with default body in post

        python3 -m unittest -v tests.test_fastapi.Test_ProcessCreate.test_post_pipeline_config_v2
        '''
        # compression y pipeline_config, son opcionales
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo",
            "pipeline_config" : " Extraction , Analysis , Enrichment "
        }
        response = self.client.post("pipeline_process/",json=request)

        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id = resp['job_id']
        self.assertIsInstance(self.job_id,str)
        
        self.log.info(f'{type(self).__name__}::test_post_pipeline_config_v2(), response: {resp}')        
        
        # campos request idem to response
        for key in ('name','topic'):
            self.assertEqual(request[key],resp[key])
        
        self.assertListEqual(resp['pipeline_config'],
                            [x.strip().lower() for x in request['pipeline_config'].split(',')])

    def test_post_all(self):
        ''' Test case with default body in post

        python3 -m unittest -v tests.test_fastapi.Test_ProcessCreate.test_post_all
        '''        
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo",
            "pipeline_config" : " Extraction , Analysis , Enrichment ",
            "compression" : "gzip"
        }
        response = self.client.post("pipeline_process/",json=request)

        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id = resp['job_id']
        self.assertIsInstance(self.job_id,str)
        
        self.log.info(f'{type(self).__name__}::test_post_all(), response: {resp}')        
        
        # campos request idem to response
        for key in ('name','topic','compression'):
            self.assertEqual(request[key],resp[key])
                
        self.assertListEqual(resp['pipeline_config'],
                            [x.strip().lower() for x in request['pipeline_config'].split(',')])
    
    def test_post_all_v2(self):
        ''' Test case with default body in post

        python3 -m unittest -v tests.test_fastapi.Test_ProcessCreate.test_post_all_v2
        '''
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo",
            "pipeline_config" : ["Extraction "," Analysis ", "Enrichment"],
            "compression" : "gzip"
        }
        response = self.client.post("pipeline_process/",json=request)
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id = resp['job_id']
        self.assertIsInstance(self.job_id,str)
        
        self.log.info(f'{type(self).__name__}::test_post_all_v2(), response: {resp}')        
        
        # campos request idem to response
        for key in ('name','topic','compression'):
            self.assertEqual(request[key],resp[key])
                
        self.assertListEqual(resp['pipeline_config'],
                            [x.strip().lower() for x in request['pipeline_config']])


class Test_ProcessGet(unittest.TestCase):
    ''' Test Cases For EndPoint process_get() GET /pipeline_process/<job_id>

        python3 -m unittest -v tests.test_fastapi.Test_ProcessGet        
    '''
    @classmethod
    def setUpClass(cls):
        cls.log:Logger = get_log(cls.__name__)
        cls.job_list:list = []
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        client = TestClient(fastapi)
        request:dict = {"status": "deleted"}
        for job_id in cls.job_list:
            response = client.put(f"pipeline_process/{job_id}",json=request)            
            cls.log.info(f'delete {job_id}, response: {response}')

        return super().tearDownClass()
    
    def setUp(self):
        self.log = type(self).log
        self.client = TestClient(fastapi)
        self.job_id:str = None
        return super().setUp()

    def tearDown(self):    
        if self.job_id is not None:
            type(self).job_list.append(self.job_id)

        return super().tearDown()
    

    def test_get_v1(self):
        ''' Test case get method

        python3 -m unittest -v tests.test_fastapi.Test_ProcessGet.test_get_v1
        '''
        # 1° creamos un job
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo"            
        }
        response = self.client.post("pipeline_process/",json=request)
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id:str = resp['job_id']
        self.assertIsInstance(self.job_id,str)

        # 2° Consultamos el estado de este 
        response = self.client.get(f"pipeline_process/{self.job_id}")
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_get_v1() response: {resp}')
        self.assertEqual(resp['code'],0)
        # campos obligatorios en localte success 'code','job_id','ready','status'
        for key in ('code','job_id','ready','status'):
            self.assertTrue( key in resp.keys() )
        
    def test_get_loop(self):
        ''' Test case get method

        python3 -m unittest -v tests.test_fastapi.Test_ProcessGet.test_get_loop
        '''
        # 1° creamos un job
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo"            
        }
        response = self.client.post("pipeline_process/",json=request)
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.job_id:str = resp['job_id']
        self.assertIsInstance(self.job_id,str)

        # 2° Consultamos el estado de este 
        response = self.client.get(f"pipeline_process/{self.job_id}")
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()        
        while not resp['ready']  :
            self.log.info(f'{type(self).__name__}::test_get_loop() response: {resp}')
            self.assertEqual(resp['code'],0)
            # campos obligatorios en localte success 'code','job_id','ready','status'
            for key in ('code','job_id','ready','status'):
                self.assertTrue( key in resp.keys() )

            sleep(1)
            response = self.client.get(f"pipeline_process/{self.job_id}")
            self.assertEqual(response.status_code, 200)
            resp = response.json()
            
    def test_get_notfound_v1(self):
        ''' Test case get method

        python3 -m unittest -v tests.test_fastapi.Test_ProcessGet.test_get_notfound_v1
        '''        
        job_id:str = str(uuid4())        
        response = self.client.get(f"pipeline_process/{job_id}")
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_get_notfound_v1() response: {resp}')
        self.assertEqual(resp['code'],1)
        # campos obligatorios
        for key in ('code','message','job_id'):
            self.assertTrue( key in resp.keys() )

        self.assertEqual(resp['job_id'],job_id)


class Test_ProcessDiscard(unittest.TestCase):
    ''' Test Cases For EndPoint process_discard() PUT /pipeline_process/<job_id>

        python3 -m unittest -v tests.test_fastapi.Test_ProcessDiscard
    '''    
    def setUp(self):
        self.log:Logger = get_log(type(self).__name__)
        self.client = TestClient(fastapi)
        request:dict = {
            "name"        : "Nombre de archivo",
            "topic"       : "dato-comprimidos-v1",            
            "content"     : "string con el contenido del archivo"
        }
        response = self.client.post("pipeline_process/",json=request)
        self.assertEqual(response.status_code, 200)
        self.job_id:str = response.json()['job_id']
        return super().setUp()

    def tearDown(self):
        if self.job_id is not None:
            request:dict = {"status": "deleted"}
            response = self.client.put(f"pipeline_process/{self.job_id}",json=request)
            self.log.info(f'{type(self).__name__}::tearDown() delete {self.job_id}, response: {response}, {response.json()}')

        return super().tearDown()

    def test_cancel_v1(self):
        ''' Test case put method cancelled

        python3 -m unittest -v tests.test_fastapi.Test_ProcessDiscard.test_cancel_v1
        '''        
        # Creado ahora lo cancelamos
        request:dict = {"status": "cancelled"}
        response = self.client.put(f"pipeline_process/{self.job_id}",json=request)
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_cancel_v1() response: {resp}')
        # campos obligatorios
        for key in ('code','message','job_id'):
            self.assertTrue( key in resp.keys() )

        self.assertEqual(resp['code'],0)

    def test_cancel_v2(self):
        ''' Test case put method cancelled, status error

        python3 -m unittest -v tests.test_fastapi.Test_ProcessDiscard.test_cancel_v2
        '''        
        # Creado ahora lo cancelamos
        request:dict = {"status": "cancel"}
        response = self.client.put(f"pipeline_process/{self.job_id}",json=request)
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_cancel_v2() response: {resp}')
        for key in ('code','message','job_id'):
            self.assertTrue( key in resp.keys() )

        self.assertEqual(resp['code'],1)
    
    def test_cancel_v3(self):
        ''' Test case put method cancelled, job_id not found

        python3 -m unittest -v tests.test_fastapi.Test_ProcessDiscard.test_cancel_v3
        '''        
        # Creado ahora lo cancelamos
        request:dict = {"status": "cancelled"}
        job_id:str = str(uuid4())
        response = self.client.put(f"pipeline_process/{job_id}",json=request)
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_cancel_v3() response: {resp}')
        for key in ('code','message','job_id'):
            self.assertTrue( key in resp.keys() )
        
        self.assertEqual(resp['code'],1)
        self.assertEqual(resp['job_id'],job_id)


class Test_ListItems(unittest.TestCase):
    ''' Test Cases For EndPoint process_discard() 
        - GET /pipeline_process/list/[<status>]
        - GET /pipeline_process/providers/

        python3 -m unittest -v tests.test_fastapi.Test_ListItems
    '''    
    def setUp(self):
        self.log:Logger = get_log(type(self).__name__)
        self.client = TestClient(fastapi)

    def test_get_process_v1(self):
        ''' Test case get process for status

        python3 -m unittest -v tests.test_fastapi.Test_ListItems.test_get_process_v1
        '''   
        status:str = 'pending'
        response = self.client.get(f"pipeline_process/list/{status}")
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_get_process_v1() response: {resp}')

        for key in ('code',status):
            self.assertTrue( key in resp.keys() )
        
        self.assertEqual(resp['code'],0)

    def test_get_process_v2(self):
        ''' Test case get process for status

        python3 -m unittest -v tests.test_fastapi.Test_ListItems.test_get_process_v2
        '''   
        status:str = 'not found'
        response = self.client.get(f"pipeline_process/list/{status}")
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_get_process_v2() response: {resp}')

        for key in ('code','message'):
            self.assertTrue( key in resp.keys() )
        
        self.assertEqual(resp['code'],1)

    def test_get_providers_v1(self):
        ''' Test case get provider

        python3 -m unittest -v tests.test_fastapi.Test_ListItems.test_get_providers_v1
        '''
        response = self.client.get(f"pipeline_process/providers/")
        self.assertEqual(response.status_code, 200)
        resp:dict = response.json()
        self.log.info(f'{type(self).__name__}::test_get_providers_v1() response: {resp}')

        for key in ('code','providers'):
            self.assertTrue( key in resp.keys() )
        
        self.assertEqual(resp['code'],0)
        

class Test_(unittest.TestCase):
    ''' 
        python3 -m unittest -v tests.test_fastapi.Test_
    '''    
    def test_get_process_v1(self):
        ''' Test case get get process for status

        python3 -m unittest -v tests.test_fastapi.Test_.test_get_process_v1
        '''        
        lst_delete = [            
            "43729b6a-a5c4-4740-b993-c24805088d01",
            "5df27255-fd90-4c17-a846-bff3f6df67ef"
        ]
        pr = ProcessGateway(WorkerRedis())
        for job_id in lst_delete:
            pr.delete(job_id)
