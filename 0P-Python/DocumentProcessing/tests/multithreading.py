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

@file multithreading.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.0.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version             Brief
JEL            2026.04.14     0.0.0               Version Inicial no release
"""
# build-in modules
from threading import Thread,Event
from queue import Queue
from time import sleep
from json import dumps as json_dumps
from logging import Logger
from dataclasses import dataclass,field
import random

# project modules
from app.application.services import ProcessGateway
from app.infrastructure.adapters.tasks_celery import TaskProcessingGateway
from app.infrastructure.adapters.worker_redis import (
    #WorkerContextRedis, 
    #WorkerIdRedis,
    WorkerRedis,
    WorkerStatus
)



@dataclass
class MTheadId:
    work_id:str
    name:str
    status:str = WorkerStatus.PENDING.name#


class MThread_ProcessGateway:

    def __init__(self,params:list[str]|list[dict],log:Logger,*args,**kwargs):
        """ """
        self.log = log
        self.queue = Queue()
        self.monitor_threads:list[Thread] = []
        self.workers_id:dict={}
        self.create_thread:list[Thread] = []
        self.th_finish:Thread = Thread(target=self.task_finish)
        self.th_create_monitor:Thread = Thread(target=self.create_monitor)
        self.key_event:Event = Event() # default is clear and flag in False
        self.ev_th_finish:Event = Event() # default is clear and flag in False

        for item in params:
            th_id = Thread(target=self.create,args=(item,))
            self.create_thread.append(th_id)

    def task_finish(self):
        """ """
        self.ev_th_finish.wait()
        # esperamos los threads
        for th in self.monitor_threads:
            th.join()

        # finalizados todos los theads
        for item in self.workers_id.values():
            print(f'{item.work_id} : {item.name} | {item.status}')

    def start(self):
        self.th_create_monitor.start()
        self.th_finish.start()
        for th in self.create_thread:
            th.start()

    def join(self):
        try:
            self.th_create_monitor.join()
            for th in self.create_thread:
                th.join()

            self.th_finish.join()
        except KeyboardInterrupt:
            self.log.error('%s::join(), KeyboardInterrupt',type(self).__name__)
            self.key_event.set()

    def create(self,item):
        """ signature para el task que crea el recurso"""
        job_id:str = ProcessGateway(WorkerRedis()).create(TaskProcessingGateway.launch(item))
        self.workers_id[job_id] = MTheadId(job_id,item['name'])
        self.queue.put(job_id)

    def create_monitor(self,*args,**kwargs):
        """ """
        while True and not self.key_event.is_set():
            # Get some data
            data:str = None
            try:
                data = self.queue.get(block=True,timeout=10)
            except Exception as e:
                self.log.error('%s::create_monitor(), exception {type(e).__name__}, detalle %s',
                               type(self).__name__,e)
                break
            
            self.log.info('%s::create_monitor(), data {data}',type(self).__name__)
            th_id = Thread(target=self.task_monitor,args=(data,))
            th_id.start()
            self.monitor_threads.append(th_id)

        #if self.key_event.is_set():
        #    return 
        self.ev_th_finish.set()

    def task_monitor(self,job_id:str,*args,**kwargs):
        """ """
        self.log.info('%s::task_monitor(), job_id %s',type(self).__name__,job_id)
        pr:ProcessGateway = ProcessGateway(WorkerRedis())
        retry:int = 0        
        while retry < 15 and not self.key_event.is_set():
            try:
                resp = pr.get(job_id)
                #self.log.info(f"Response: {json_dumps(resp,indent=2)}")
                self.log.info(f"Response: {resp}")
            except Exception as e:            
                self.log.error('%s::task_monitor(%s), exception %s, detalle %s',
                               type(self).__name__,job_id,type(e).__name__,e)

            sleep(1)
            retry += 1

        if self.key_event.is_set():
            return 

        if bool(random.getrandbits(1)):
            try:
                if bool(random.getrandbits(1)):
                    resp = pr.delete(job_id)
                    self.workers_id[job_id].status = "DELETED"
                else:
                    resp = pr.cancel(job_id)
                    self.workers_id[job_id].status = WorkerStatus.CANCELLED.name
                
                self.log.info(f"Response: {resp}")

            except Exception as e:            
                    self.log.error('%s::task_monitor(%s), exception %s, detalle %s',
                               type(self).__name__,job_id,type(e).__name__,e)
                
            retry = 0
            while retry < 10 and not self.key_event.is_set():
                try:
                    resp = pr.get(job_id)
                    #self.log.info(f"Response {retry:2d}: {json_dumps(resp,indent=2)}")
                    self.log.info(f"Response {retry:2d}: {resp}")
                except Exception as e:
                    self.log.error('%s::task_monitor(%s), exception %s, detalle %s',
                               type(self).__name__,job_id,type(e).__name__,e)

                sleep(1)
                retry += 1
        else:
            # wait for end task, no se cancelo
            resp:dict = pr.get(job_id)
            while not resp['ready'] and not self.key_event.is_set():
                self.log.info("Response: %s",resp)
                sleep(1)
                resp = pr.get(job_id)

            
            if bool(random.getrandbits(1)):
                pr.delete(job_id)
                self.workers_id[job_id].status = "DELETED"
            else:
                self.workers_id[job_id].status = WorkerStatus.COMPLETED.name
            self.log.info("End Task - Response: %s",resp)
