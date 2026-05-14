# build module
import unittest   
from time import sleep
import json



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

    #def test_(self):
    #    ''' Test case create new jobs
    #       
    #    python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_
    #    '''
    #    print(f'KAFKA_URL:{KAFKA_URL} KAFKA_PORT:{KAFKA_PORT}')

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
        print(f'st_delete: {st_delete}')

    def test_delete_v1(self):
        ''' Test case delete job, intentamos eliminar en `'status': 'processing'`
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_delete_v1
        '''
        log:Logger = unittest_log(self)
        data:dict = {
            'name' : f'{type(self).__name__}',
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
            print(f'job_list<{it.name}> : {json.dumps(job_list,indent=2)}')
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
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:list[str] = []
        for i in range(0,10):
            body_data:dict = {
                'name' : data['name'] + f' {i:4d}',
                'content' : data['content']
            }            
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
            'content' : "Datos Originales"
        }

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        job_id:list[str] = []
        for i in range(0,10):
            body_data:dict = {
                'name' : data['name'] + f' {i:4d}',
                'content' : data['content']
            }            
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
        print(f'\n:Jobs Staus: {json.dumps(st,indent=2)}')
       
    def test_get_v1(self):
        ''' Test case 
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_get_v1
        '''
        #job_id:str = '3497ded6-b63b-40de-9ce8-610529c3ead7'
        #job_id:str = 'ca10a8c4-0717-4b4f-b195-bba63d718dbe'
        #job_id:str = '525d40f4-5560-4552-ac68-2da5ed1d63f1'
        #job_id:str = '87c02ee8-e417-4805-8bf9-1816f5f2a3e2'
        #job_id:str = '500ddc94-7696-4a91-979d-8bd3daabeedf'
        job_id:str = 'c2fe0ef2-a7b9-4f7a-88bb-376f8ff75334'

        pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
        st:dict = pr_gateway.get(job_id)
        self.assertIsInstance(st,dict)
        print(f'\n:Job<{job_id}> Staus: {st}')

    def test_multithread_v1(self):
        ''' Test case 
           
        python3 -m unittest -v tests.test_process_gateway.Test_ProcessGatewayV1.test_multithread_v1

        FIXME podemos agregar al igual que el cancel el delete en ambos stages
         - en el procesado
         - al finalizar
         ambos con random

         Tambien agragar los set
          - task all
          - task canceled
          - task delete
        '''
        log:Logger = unittest_log(self)

        params:list[dict] = [
            {
                'name' : f'{type(self).__name__}-idx{i:02d}',
                'content' : f"Datos Originales-idx{i:02d}"  
            } for i in range(0,100)
        ]
        mt_test = MThread_ProcessGateway(params,log)
        print(f'Begin Test MultiThread')
        mt_test.start()        
        mt_test.join()
        print(f'End   Test MultiThread')
        