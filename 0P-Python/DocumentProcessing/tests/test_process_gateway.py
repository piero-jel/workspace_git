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

@file test_process_gateway.py
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
Author         Date           Version       Brief
JEL            2026.04.14     0.0.3         Version Inicial no release
"""

# build-in module
import unittest   
from time import sleep
import json
from uuid import uuid4



# third-party modules



# project modules, under test
from app.application.services import ProcessGateway
from app.infrastructure.adapters.worker_redis import (
    #WorkerContextRedis, 
    WorkerIdRedis,
    WorkerRedis,
    WorkerStatus,
)
from app.infrastructure.adapters.tasks_celery import TaskProcessingGateway

from app.infrastructure.adapters.settings import KAFKA_URL,KAFKA_PORT
from tests.config import get_log,unittest_log,Logger
from tests.multithreading import MThread_ProcessGateway





class Test_ProcessGatewayV1(unittest.TestCase):
    ''' Test Case For Test_ProcessGatewayV1

        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1
    '''
    @classmethod
    def setUpClass(cls):
        cls.log = get_log(cls.__name__)        
        return super().setUpClass()

    def test_create(self):
        ''' Test case create new jobs
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_create
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(data))
        log.info('job_ids: %s',job_id)
        self.assertIsInstance(job_id,str)

        resp:dict = pr_gateway.get(job_id)
        while not resp['ready']:   
            log.info("Response: %s",resp)
            self.assertIsInstance(resp,dict)
            sleep(1)
            resp = pr_gateway.get(job_id)

        self.assertIsInstance(resp,dict)
        log.info("Response: %s",json.dumps(resp,indent=2))

    def test_cancel_v1(self):
        ''' Test case cancel job, intentamos cancelar en `'status': 'processing'`
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_cancel_v1
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(data))
        log.info('job_ids: %s',job_id)        
        resp:dict = pr_gateway.get(job_id)
        while not resp['ready'] and resp['status'] != 'cancelled':
            log.info("Response: %s",resp)            
            self.assertIsInstance(resp,dict)
            if resp['status'] == 'processing':
                st_cancel = pr_gateway.cancel(job_id)
                log.info('st_cancle: %s',st_cancel)

            sleep(1)
            resp = pr_gateway.get(job_id)

        self.assertIsInstance(resp,dict)
        log.info("Response: %s",json.dumps(resp,indent=2))

    def test_cancel_v2(self):
        ''' Test case cancel job, intentamos cancelar en `'status': 'pending'`, fuera del loop
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_cancel_v2
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(data))
        log.info('job_ids: %s',job_id)
        st_cancel = pr_gateway.cancel(job_id)
        log.info('st_cancle: %s',st_cancel)
        resp:dict = pr_gateway.get(job_id)
        while not resp['ready'] and resp['status'] != 'cancelled':
            log.info("Response: %s",resp)            
            self.assertIsInstance(resp,dict)
            sleep(1)
            resp = pr_gateway.get(job_id)

        self.assertIsInstance(resp,dict)
        log.info("Response: %s",json.dumps(resp,indent=2))
        
    def test_cancel_v3(self):
        ''' Test case cancel job, intentamos cancelar en `'status': 'completed'`
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_cancel_v3
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(data))
        log.info('job_ids: %s',job_id)
        resp:dict = pr_gateway.get(job_id)
        while not resp['ready']:
            log.info("Response: %s",resp)            
            self.assertIsInstance(resp,dict)
            sleep(1)
            resp = pr_gateway.get(job_id)

        st_cancel = pr_gateway.cancel(job_id)
        log.info('st_cancle: %s',st_cancel)
        self.assertIsInstance(resp,dict)
        log.info("Response: %s",json.dumps(resp,indent=2))

    def test_delete_v0(self):
        ''' Test case delete job, intentamos eliminar en `'status': 'processing'`
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_delete_v0
        '''
        job_id:str = 'd248f073-7cb5-44fb-b711-95ea4a67cc99'
        st_delete = ProcessGateway(WorkerRedis()).delete(job_id)
        self.log.info(f'st_delete: {st_delete}')

    def test_delete_v1(self):
        ''' Test case delete job, intentamos eliminar en `'status': 'processing'`
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_delete_v1
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(data))
        log.info('job_ids: %s',job_id)        
        resp:dict = pr_gateway.get(job_id)
        while not resp['ready'] and resp['status'] != 'cancelled':
            log.info("Response: %s",resp)            
            self.assertIsInstance(resp,dict)
            if resp['status'] == 'processing':
                st_delete = pr_gateway.delete(job_id)
                log.info('st_delete: %s',st_delete)

            sleep(1)
            resp = pr_gateway.get(job_id)

        self.assertIsInstance(resp,dict)
        log.info("Response: %s",json.dumps(resp,indent=2))        
        while resp['code'] == 0:
            sleep(1)
            resp = ProcessGateway(WorkerRedis()).get(job_id)
            log.info("Response: %s",resp)

    def test_delete_v2(self):
        ''' Test case delete job, intentamos eliminar en `'status': 'pending'`, fuera del loop
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_delete_v2
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(data))
        log.info('job_ids: %s',job_id)

        st_delete = pr_gateway.delete(job_id)
        log.info('st_delete: %s',st_delete)

        resp:dict = pr_gateway.get(job_id)
        count:int = 0
        while resp['code'] == 0 and count < 10:
            log.info("Response: %s",resp)            
            self.assertIsInstance(resp,dict)
            sleep(1)
            resp = ProcessGateway(WorkerRedis()).get(job_id)
            count += 1

        self.assertIsInstance(resp,dict)
        log.info("Response: %s",json.dumps(resp,indent=2))
        
    def test_delete_v3(self):
        ''' Test case delet job, intentamos eliminar en `'status': 'completed'`
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_delete_v3
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:str = pr_gateway.create(TaskProcessingGateway.launch(data))
        log.info('job_ids: %s',job_id)
        resp:dict = pr_gateway.get(job_id)
        while not resp['ready']:
            log.info("Response: %s",resp)            
            self.assertIsInstance(resp,dict)
            sleep(1)
            resp = pr_gateway.get(job_id)

        st_delete = pr_gateway.delete(job_id)
        log.info('st_delete: %s',st_delete)
        count:int = 0
        while resp['code'] == 0 and count < 10:
            log.info("Response: %s",resp)            
            self.assertIsInstance(resp,dict)
            sleep(1)
            resp = ProcessGateway(WorkerRedis()).get(job_id)
            count += 1

        self.assertIsInstance(resp,dict)
        log.info("Response: %s",json.dumps(resp,indent=2))        

    def test_get_list(self):
        ''' Test case method get_list() 
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_get_list
        '''
        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_list:dict = pr_gateway.get_list()
        self.log.info(f'job_list: {json.dumps(job_list,indent=2)}')
        self.assertIsInstance(job_list,dict)

        job_list:dict = pr_gateway.get_list('cualquier-estado')
        self.log.info(f'job_list: {json.dumps(job_list,indent=2)}')
        self.assertIsInstance(job_list,dict)

    def test_get_list_v2(self):
        ''' Test case method get_list() 
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_get_list_v2
        '''
        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        for it in WorkerStatus:
            job_list:dict = pr_gateway.get_list(it.name)
            self.log.info(f'job_list<{it.name}> : {json.dumps(job_list,indent=2)}')
            self.assertIsInstance(job_list,dict)

    def test_multi_jobs(self):
        ''' Test case 
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_multi_jobs
        '''
        log:Logger = unittest_log(self)
        def get_status():
            for it in WorkerStatus:
                task_ids:list[str] = WorkerIdRedis.gets(it)
                log.info(f'{it.name:10s} task_ids: {task_ids}')

        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:list[str] = []
        for i in range(0,10):
            body_data:dict = { k:v for k,v in data.items()}
            body_data['name'] = data['name'] + f' {i:4d}'
            
            jid:str = pr_gateway.create(TaskProcessingGateway.launch(body_data))
            log.info('job_ids: %s',jid)
            self.assertIsInstance(jid,str)
            job_id.append(jid)

        resp:dict = pr_gateway.get(job_id[-1])
        while not resp['ready']:   
            log.info("Response: %s",resp)
            get_status()
            self.assertIsInstance(resp,dict)
            sleep(1)
            resp = pr_gateway.get(job_id[-1])

    def test_multi_jobs_v2(self):
        ''' Test case 
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_multi_jobs_v2
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
            "topic": "dato-comprimidos-v1",
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:list[str] = []
        for i in range(0,10):
            body_data:dict = { k:v for k,v in data.items()}
            body_data['name'] = data['name'] + f' {i:4d}'            
            jid:str = pr_gateway.create(TaskProcessingGateway.launch(body_data))
            log.info('job_ids: %s',jid)
            self.assertIsInstance(jid,str)
            job_id.append(jid)

        resp:dict = pr_gateway.get(job_id[-1])
        while not resp['ready']:   
            log.info("Response: %s",resp)
            st:dict = pr_gateway.get()
            self.assertIsInstance(st,dict)
            log.info(st)
            sleep(1)
            resp = pr_gateway.get(job_id[-1])

    def test_get_jobs(self):
        ''' Test case 
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_get_jobs
        '''
        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        st:dict = pr_gateway.get()
        self.assertIsInstance(st,dict)
        self.log.info(f'\n:Jobs Staus: {json.dumps(st,indent=2)}')
       
    def test_get_v1(self):
        ''' Test case get job no creado
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_get_v1
        '''        
        job_id:str = str(uuid4())
        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        st:dict = pr_gateway.get(job_id)
        self.assertIsInstance(st,dict)
        self.log.info(f'\n:Job<{job_id}> Staus: {st}')

    def test_multithread_v1(self):
        ''' Test case aplicacion multithread de job, con random para cancelar/eliminar/completar
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_multithread_v1
        '''
        log:Logger = unittest_log(self)

        params:list[dict] = [
            {
                'name' : f'{type(self).__name__}-idx{i:02d}',
                "topic": "dato-comprimidos-v1",
                'content' : f"Datos Originales-id {i:02d}"  
            } for i in range(0,10)
        ]
        mt_test = MThread_ProcessGateway(params,log)
        print(f'Begin Test MultiThread')
        mt_test.start()        
        mt_test.join()
        print(f'End   Test MultiThread')
        
    def test_get_v1(self):
        ''' Test case get job no creado
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_get_v1
        '''        
        st:dict = ProcessGateway(WorkerRedis()).get_providers()
        self.assertIsInstance(st,dict)
        self.log.info(f'\n:Providers <{st}>')
