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
JEL            2026.05.17     0.0.4       Ajustes para pylint
"""
# build-in module
import unittest   
from time import sleep
import json
from uuid import uuid4

# project modules, under test
#from app.infrastructure.adapters.settings import celery
#from app.application.services import ProcessGateway
from app.domain.worker import (
    WorkerContext, WorkerId, WorkerResult,WorkerStatus
)
from app.infrastructure.adapters.worker_redis import (
    WorkerContextRedis,
    WorkerIdRedis,
    WorkerRedis,
    WorkerResultCelery    
)
from tests.config import get_log,unittest_log,Logger


class Test_WorkerIdRedis(unittest.TestCase):
    ''' Test Case For Test_WorkerId

        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis
    '''
    @classmethod
    def setUpClass(cls):
        cls.log = get_log(cls.__name__)        
        return super().setUpClass()
    
    def setUp(self):
        self.job:WorkerIdRedis = WorkerIdRedis.make(str(uuid4()))
        return super().setUp()
    
    def tearDown(self):
        self.job.delete()
        return super().tearDown()


    def test_gets_v1(self):
        ''' Test case gets class method, default params
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_gets_v1
        '''
        log:Logger = unittest_log(self)
        jobs_ids:list[str] = WorkerIdRedis.gets()
        log.info(f'job_ids in default Status: {json.dumps(jobs_ids,indent=2)}')
        self.assertIsInstance(jobs_ids,list)

        jobs_ids = WorkerIdRedis.gets(WorkerStatus.CANCELLED)
        log.info(f'job_ids in Canceled status: {json.dumps(jobs_ids,indent=2)}')
        self.assertIsInstance(jobs_ids,list)

    def test_gets_v2(self):
        ''' Test case gets class method, set status
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_gets_v2
        '''
        log:Logger = unittest_log(self)
        for it in WorkerStatus:
            task_ids:list[str] = WorkerIdRedis.gets(it)
            self.assertIsInstance(task_ids,list)
            log.info(f'{it.name.lower():10s} task_ids: {json.dumps(task_ids,indent=2)}')

    def test_gets_v3(self):
        ''' Test case gets class method, get with last
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_gets_v3
        '''
        log:Logger = unittest_log(self)
        for it in WorkerStatus:
            task_ids:list[str] = WorkerIdRedis.gets(it,4)
            self.assertIsInstance(task_ids,list)            
            log.info(f'{it.name.lower():10s} task_ids: {json.dumps(task_ids,indent=2)}')

    def test_make_v1(self):
        ''' Test case make class method
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_make_v1
        '''
        log:Logger = unittest_log(self)
        job:WorkerIdRedis = WorkerIdRedis.load(self.job.job_id)
        log.info(f'job_id: {job} | self.job: {self.job}')
        self.assertEqual(job.status,WorkerStatus.PENDING)
        self.assertEqual(job,self.job)
        self.assertIsInstance(job.get_status(),str)
        job.delete()

    def test_loads_v1(self):
        ''' Test case load class method
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_loads_v1
        '''
        log:Logger = unittest_log(self)        
        job:WorkerIdRedis = WorkerIdRedis.load(self.job.job_id)        
        log.info(f'self.job : {self.job} | job : {job}')
        self.assertIsInstance(job.job_id,str)
        self.assertIsInstance(job.status,WorkerStatus)
        self.assertEqual(job,self.job)        
        job.delete()

    def test_loads_v2(self):
        ''' Test case load class method, create flag true
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_loads_v2
        '''
        log:Logger = unittest_log(self)
        job:WorkerIdRedis = WorkerIdRedis.load(str(uuid4()),create=True)
        log.info(f'jod : {job}')
        self.assertIsInstance(job.job_id,str)
        self.assertIsInstance(job.status,WorkerStatus)
        self.assertEqual(job.status,WorkerStatus.PENDING)        
        job.delete()

    def test_change_v1(self):
        ''' Test case change status worker id
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_change_v1
        '''
        log:Logger = unittest_log(self)
        new:WorkerStatus = WorkerStatus.PROCESSING
        log.info(f'Before change to status {new}, Job : {self.job}')
        self.job.change(new)
        log.info(f'After  change to status {new}, Job : {self.job}')
        self.assertEqual(self.job.status,new)

        for st in WorkerStatus:
            log.info(f'Before change to status {st}, Job : {self.job}')
            self.job.change(st)
            log.info(f'After  change to status {st}, Job : {self.job}')
            self.assertEqual(self.job.status,st)

    def test_delete_v1(self):
        ''' Test case 
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_delete_v1
        '''
        log:Logger = unittest_log(self)
        job:WorkerIdRedis = WorkerIdRedis.make(str(uuid4()))
        log.info(f'make job: {job}')
        self.assertIsInstance(job,WorkerIdRedis)
        job2:WorkerIdRedis = WorkerIdRedis.find(job.job_id)
        # tenemos uno en el sistema persistente pero ahora dos en memoria
        log.info(f'find job2: {job2} | job {job}')
        self.assertEqual(job,job2)

        log.info(f'TO BOOL: job2<{bool(job2)}> | job<{bool(job)}>')
        self.assertTrue(job)
        self.assertTrue(job2)

        job.delete()        
        job2 = WorkerIdRedis.find(job.job_id)
        # Borramos el del sistema persistente pero nos queda uno en memoria
        log.info(f'TO BOOL: job2<{bool(job2)}> | job<{bool(job)}>')
        self.assertTrue(job)
        self.assertFalse(job2)

    def test_find_v1(self):
        ''' Test case class method find job-id
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_find_v1
        '''
        log:Logger = unittest_log(self)
        job:WorkerIdRedis = WorkerIdRedis.find(self.job.job_id)
        log.info(f'job: {job}')
        self.assertEqual(job,self.job)
        self.assertEqual(job.status,self.job.status)
        self.assertEqual(job.job_id,self.job.job_id)

    def test_in_status(self):
        ''' Test case check if the WorkerId is in states
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_in_status
        '''
        log:Logger = unittest_log(self)
        job:WorkerIdRedis = WorkerIdRedis.find(self.job.job_id)
        st:bool = job.in_status(WorkerStatus.CANCELLED)
        log.info(f'job: {job} | st:{st}')
        self.assertEqual(st,False)

        st = job.in_status(WorkerStatus.CANCELLED,WorkerStatus.FAILED)
        log.info(f'job: {job} | st:{st}')
        self.assertEqual(st,False)

        st = job.in_status(WorkerStatus.PENDING,WorkerStatus.FAILED)
        log.info(f'job: {job} | st:{st}')
        self.assertEqual(st,True)

        st = job.in_status(WorkerStatus.PENDING,WorkerStatus.PROCESSING,WorkerStatus.FAILED,
                           WorkerStatus.COMPLETED)
        log.info(f'job: {job} | st:{st}')
        self.assertEqual(st,True)
        
    def test_is_canceled(self):
        ''' Test case for method is_canceled
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_is_canceled
        '''
        log:Logger = unittest_log(self)
        self.job.change(WorkerStatus.CANCELLED)
        log.info(f'self.job: {self.job}')
        self.assertEqual(self.job.status,WorkerStatus.CANCELLED)
        st:bool = self.job.is_canceled()
        log.info(f'self.job.is_canceled() : {st}')
        self.assertTrue(st)

    def test_mark_deletion(self):
        ''' Test case for the method mark deletion
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerIdRedis.test_mark_deletion
        '''
        log:Logger = unittest_log(self)        
        job:WorkerIdRedis = WorkerIdRedis.make(str(uuid4()))
        log.info(f'job: {job}')
        self.assertEqual(job.status,WorkerStatus.PENDING)

        job.mark_for_deletion()
        log.info(f'After mark_for_deletion() job: {job}')
        st:bool = job.is_marked_for_deletion()
        self.assertTrue(st)

        job.delete_mark_deletion()
        job_find:WorkerIdRedis = WorkerIdRedis.find(job.job_id)
        log.info(f'After delete_mark_deletion() job_find: {job_find}')
        self.assertFalse(job_find)
        self.assertIsInstance(job_find,WorkerIdRedis)

        job_load:WorkerIdRedis = WorkerIdRedis.load(job.job_id)
        log.info(f'After delete_mark_deletion() job_load: {job_load}')
        self.assertIsNone(job_load)


class Test_WorkerContextRedis(unittest.TestCase):
    ''' Test Case For Test_WorkerId

        python3 -m unittest -v tests.test_worker_redis.Test_WorkerContextRedis
    '''
    @classmethod
    def setUpClass(cls):
        cls.log = get_log(cls.__name__)        
        return super().setUpClass()
    
    def setUp(self):
        self.log:Logger = type(self).log
        self.job_id:str = str(uuid4())
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()

    def test_store_load(self):
        ''' Test case store an load methods
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerContextRedis.test_store_load
        '''
        data:dict = {
            "name": "John",
            "surname": "Smith",
            "age": 29
        }
        work_ctx = WorkerContextRedis()
        
        # store
        work_ctx.store(self.job_id,data)

        # load
        load_data:dict = work_ctx.load(self.job_id)
        self.log.info(f'job_id: {self.job_id} | {load_data}')
        self.assertIsInstance(load_data,dict)
        for k,v in load_data.items():
            self.log.info(f'Key<{k} | {type(k).__name__}> = value<{v} | {type(v).__name__}> ')
            self.assertIsInstance(k,str)
            self.assertIsInstance(v,str)            
            if v.isdecimal():
                load_data[k] = int(v)

        self.assertDictEqual(data,load_data)
        work_ctx.delete(self.job_id)

    def test_store_load_v1(self):
        ''' Test case store and load with expire time
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerContextRedis.test_store_load_v1
        '''
        work_ctx = WorkerContextRedis(expire=60) 
        contex = {
            'code': 0,
            'ready': False,
            'status': 'PROGRESS',
            'result': None,
            'stages': 'processing',
            'pipeline': 'extraction',
            'job_id': 'b89e4d01-7c22-43d2-b5bd-c998873562d5'
        }

        st:bool = work_ctx.store(contex['job_id'],contex)
        self.assertTrue(st)
        load:dict = work_ctx.load(contex['job_id'])

        # recupera todos los campos como string
        load['code']  = int(load['code'])
        load['ready'] = bool(int(load['ready']))
        load['result'] = None # valores None o null los descarta        
        self.log.info(f'Load : {load}')
        self.assertEqual(contex,load)

        work_ctx.delete(contex['job_id'])

    def test_load_notfound(self):
        ''' Test case load with out store, not found 
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerContextRedis.test_load_notfound
        '''
        work_ctx = WorkerContextRedis()        
        load:dict = work_ctx.load(self.job_id)        
        self.log.info(f'self.job_id: {self.job_id} | {load} | {type(load).__name__} | bool(load): {bool(load)}')
        self.assertIsInstance(load,dict)
        self.assertFalse(load)

    def test_get(self):
        ''' Test case get item from stored context 
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerContextRedis.test_get
        '''
        work_ctx = WorkerContextRedis()
        contex:dict = {
            'code': 0,        
            'status': 'PROGRESS',        
            'stages': 'processing',
            'pipeline': 'extraction'        
        }
        work_ctx.store(self.job_id,contex)
        for k in contex.keys():
            val = work_ctx.get(self.job_id,k)
            self.log.info(f'val: {val:12s} for key: {k}')
            self.assertIsInstance(val,str)
        
        work_ctx.delete(self.job_id)

    def test_store_timeout(self):
        ''' Test case store and load test expire time
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerContextRedis.test_store_timeout
        '''
        ticks:int = 3
        work_ctx = WorkerContextRedis(ticks)
        contex:dict = {
            'code': 0,        
            'status': 'PROGRESS',        
            'stages': 'processing',
            'pipeline': 'extraction'        
        }
        work_ctx.store(self.job_id,contex)
        for i in range(ticks*2):
            val = work_ctx.load(self.job_id)
            self.log.info(f'load <{i:3d}> value: {val}')
            self.assertIsInstance(val,dict)
            if i >= ticks:
                self.assertFalse(val)
            else:
                self.assertTrue(val)

            sleep(1)
        
        work_ctx.delete(self.job_id)
        

class Test_WorkerRedis(unittest.TestCase):
    ''' Test Case For Test_WorkerId

        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis
    '''
    @classmethod
    def setUpClass(cls):
        cls.log = get_log(cls.__name__)        
        return super().setUpClass()
    
    def setUp(self):
        self.log:Logger = type(self).log
        self.job_id:str = str(uuid4())
        self.worker:WorkerRedis = WorkerRedis()
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()

    def test_find_workerid(self):
        ''' Test case method find_workerid()
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis.test_find_workerid
        '''
        # lo creo
        worker_id:WorkerId = self.worker.make_workerid(self.job_id)
        # lo busco
        workerid_find = self.worker.find_workerid(self.job_id)
        self.log.info(f'workerid_find: {workerid_find}')

        self.assertIsInstance(workerid_find,WorkerId)
        self.assertEqual(worker_id,workerid_find)

        worker_id.delete()

    def test_find_workerid_v2(self):
        ''' Test case method find_workerid(), worker id not found
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis.test_find_workerid_v2
        '''        
        # lo busco
        workerid = self.worker.find_workerid(self.job_id)
        self.log.info(f'workerid_find: {workerid}')
        self.assertFalse(workerid)
        self.assertIsNone(workerid.job_id)
        self.assertIsInstance(workerid.status,WorkerStatus)
    
    def test_make_workerid(self):
        ''' Test case method make_workerid()
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis.test_make_workerid
        '''
        worker_id:WorkerId = self.worker.make_workerid(self.job_id)
        self.log.info(f'worker_id: {worker_id}')
        self.assertIsInstance(worker_id,WorkerId)
        self.assertIsInstance(worker_id,WorkerIdRedis)
        worker_id.delete()

    def test_make_workercontext(self):
        ''' Test case method make_workerid()
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis.test_make_workercontext
        '''
        workercontext:WorkerContext = self.worker.make_workercontext()
        self.log.info(f'workercontext: {workercontext}')
        self.assertIsInstance(workercontext,WorkerContext)
        self.assertIsInstance(workercontext,WorkerContextRedis)

    def test_make_workerresult(self):
        ''' Test case method make_workerid()
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis.test_make_workerresult
        '''
        workerresult:WorkerResult = self.worker.make_workerresult(self.job_id)
        #self.log.info(f'workerresult: {workerresult}')
        self.log.info(f'workerresult: {workerresult}')
        self.log.info(f'workerresult.status(): {workerresult.status()}')
        self.log.info(f'workerresult.ready:    {workerresult.ready()}')
        self.log.info(f'workerresult.get():    {workerresult.get()}')
        self.assertIsInstance(workerresult,WorkerResult)
        self.assertIsInstance(workerresult,WorkerResultCelery)

    def test_get_workers(self):
        ''' Test case method get_workers()
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis.test_get_workers
        '''
        job_ids:dict = self.worker.get_workers()
        self.log.info(f'job_ids: {json.dumps(job_ids,indent=2)}')
        self.assertIsInstance(job_ids,dict)
        self.assertTrue(job_ids)

        job_ids = self.worker.get_workers(WorkerStatus.CANCELLED)
        self.log.info(f'CANCELLED job_ids: {json.dumps(job_ids,indent=2)}')
        self.assertIsInstance(job_ids,dict)
        self.assertTrue(job_ids)

        job_ids = self.worker.get_workers(WorkerStatus.FAILED)
        self.log.info(f'FAILED job_ids: {json.dumps(job_ids,indent=2)}')
        self.assertIsInstance(job_ids,dict)
        self.assertTrue(job_ids)

    def test_gets_workerid(self):
        ''' Test case method gets_workerid()
           
        python3 -m unittest -v tests.test_worker_redis.Test_WorkerRedis.test_gets_workerid
        '''
        job_ids:list = self.worker.gets_workerid()
        self.log.info(f'PENDING job_ids: {json.dumps(job_ids,indent=2)}')
        self.assertIsInstance(job_ids,list)

        job_ids = self.worker.gets_workerid(WorkerStatus.CANCELLED)
        self.log.info(f'CANCELLED job_ids: {json.dumps(job_ids,indent=2)}')
        self.assertIsInstance(job_ids,list)

        job_ids = self.worker.gets_workerid(WorkerStatus.COMPLETED,5)
        self.log.info(f'COMPLETED job_ids: {json.dumps(job_ids,indent=2)}')
        self.assertIsInstance(job_ids,list)
        
