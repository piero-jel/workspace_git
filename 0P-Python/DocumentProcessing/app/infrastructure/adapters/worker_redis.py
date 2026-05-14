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

@file worker_redis.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   redis workers
@details Definicion concreta para los Workes que dependen de la infraestructura de Redis como Queue
@version 0.0.3.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version      Brief
JEL            2026.04.14     0.0.3        Version Inicial no release
"""


# build-in modules
from time import sleep
from json import loads as json_loads, dumps as json_dumps

# third-party modules
#from redis import Redis
from celery.result import AsyncResult
from confluent_kafka import Producer

# project modules
#from settings import (REDIS_PORT,REDIS_URL,REDISCLI_AUTH,REDIS_DB)
from app.domain.ports import EventPublisher
from app.infrastructure.adapters.settings import redis,KAFKA_URL,KAFKA_PORT
from app.domain.worker import (
    Worker,WorkerContext, WorkerId, WorkerResult,WorkerStatus
)


class WorkerContextRedis(WorkerContext):
    """ """

    def __init__(self,expire:int=None):
        """
        :param expire: Opcional, tiempo que durara activo el contexto. Valor por 
        defecto `cls.SEC_EXPIRE`
        :type expire: int
        """
        cls=type(self)
        self.sec_expire = cls.SEC_EXPIRE if expire is None else expire

    def store(self,id:str,contex:dict)->bool:
        store_val = {}
        for k,v in contex.items():
            if v is None:
                continue
            elif isinstance(v,bool):
                store_val[k] = int(v)
            else:
                store_val[k] = v
            
        redis.hset(id,mapping=store_val)
        redis.expire(id,self.sec_expire)
        return True
    
    def get(self,id:str,key:str)->dict:
        return redis.hget(id,key).decode('utf-8') 
    
    def load(self,id:str)->dict:
        ret:dict = redis.hgetall(id)
        if ret is None:
            return {}
        return { k.decode('utf-8'):v.decode('utf-8') for k,v in redis.hgetall(id).items() }
    
    def delete(self,id:str)->bool:
        redis.delete(id)
        return True


class WorkerIdRedis(WorkerId):
    """ Clase concreta para manejar los worker id mediante Redis """

    @classmethod
    def make(cls,wrk_id:str,status:WorkerStatus=WorkerStatus.PENDING)->WorkerIdRedis:
        """
        Metodo de la clase que se encarga de crear un nuevo WorkerId

        :param status: Opcional,  estado para el TaskJobs. Por defecto Pending.
        :type status: WorkerStatus

        :return: el WorkerId creado y persistido en el sistema.
        :rtype: WorkerId
        """
        ret:WorkerIdRedis = WorkerIdRedis()
        ret._job_id = wrk_id
        #ret._status = status.value
        ret._status = status
        ret.push()
        return ret
    
    @classmethod
    def find(cls,job_id:str)->WorkerIdRedis:
        """
        Metodo de la clase que localiza en el sistema persistente un WorkerId desde su `job_id`

        :param job_id: job id para localizar y cargar en memoria el registro.
        :type job_id: str

        
        :return: el WorkerId localizado, de lo contrario WorkerId vacio `bool(WorkerId) == False`.
        :rtype: WorkerId
        """
        st:int = 0
        idx:bool = False    
        for id,status in cls.WORKER_STATUS.items():            
            if redis.sismember(status, job_id) == 1:
                st = id
                idx = True
                break            

        if not idx:
            return WorkerIdRedis()

        ret:WorkerIdRedis = WorkerIdRedis()
        ret._job_id = job_id
        ret._status = WorkerStatus(st)
        return ret
    
    @classmethod
    def block_find(cls,job_id:str,retry:int=1,time:float=0.01)->WorkerIdRedis:
        """
        Metodo de la clase para localiza en el sistema persistente un WorkerId desde su `job_id` 
        de manera bloqueante.

        :param job_id: job id para localizar y cargar en memoria el registro.
        :type job_id: str

        :param retry: Opcional numero de reintentos. Por defecto 1.
        :type retry: int

        :param time: Opcional, tiempo de demora entre reintetos. Por defecto 10 mS (mili segundos)
        :type time: float

        
        :return: el WorkerId localizado, de lo contrario WorkerId vacio `bool(WorkerId) == False`.
        :rtype: WorkerId
        """
        ret:WorkerIdRedis = WorkerIdRedis.find(job_id)
        while not ret and retry > 0:
            if time:
                sleep(time)

            retry -= 1
            ret = WorkerIdRedis.find(job_id)

        return ret
        
    @classmethod
    def load(cls,job_id:str,create:bool=False)->WorkerIdRedis:
        """
        Metodo de la clase que busca en el sistema persistente un WorkerId desde su `job_id`

        :param job_id: job id para localizar y cargar en memoria el registro.
        :type job_id: str

        :param create: Opcional, flag para habilitar la creacion si el `job_id` no existe
        :type create: bool

        :return: el WorkerId localizado, de lo contrario None.
        :rtype: WorkerId
        """
        ret:WorkerIdRedis = cls.find(job_id)
        if ret:
            return ret
        
        if not create:
            return None
        
        ret._job_id = job_id
        ret.push()
        return ret

    @classmethod
    def gets(cls,status:WorkerStatus=WorkerStatus.PENDING,last:int=-1)->list[str]:
        """
        Metodo de la clase para obtener el listado de WorkerId

        :param status: Opcional, Nuevo estado para el TaskJobs. Por defecto Pending
        :type status: str

        :param last: para indicar la cantidad de registros desde el mas reciente al mas
        antiguo. Por defecto `-1`, indica todos.
        :type last: int

        :return: listado de TaskJobs localizados
        :rtype: list[str]
        """
        ret = redis.smembers(status.name.lower())
        if last == -1:
            return [it.decode('utf-8') for it in ret] 

        return [it.decode('utf-8') for i,it in enumerate(ret) if i<last] 
        
    def in_status(self,*args:WorkerStatus)->bool:
        for st in args:
            if st.value == self._status.value:
                return True
            
        return False

    def change(self,status:WorkerStatus=WorkerStatus.PENDING)->bool:
        if self._status.value == status.value:
            return False

        self.delete()
        self._status = status
        self.push()
        return True
    
    def is_canceled(self)-> bool:
        return redis.sismember(WorkerStatus.CANCELLED.name.lower(), self._job_id) == 1

    def push(self)->bool:
        redis.sadd(self._status.name.lower(),self._job_id)
        return True

    def delete(self)->bool:        
        redis.srem(self._status.name.lower(), self._job_id)
        return True

    def mark_for_deletion(self)->bool:
        if self._status != WorkerStatus.CANCELLED:
            self.delete()
            self._status = WorkerStatus.CANCELLED
            self.push()

        redis.sadd('delete',self._job_id)
        return True
    
    def is_marked_for_deletion(self)->bool:
        return redis.sismember('delete', self._job_id) == 1
    
    def delete_mark_deletion(self)->bool:
        redis.srem(WorkerStatus.CANCELLED.name.lower(), self._job_id)
        redis.srem('delete', self._job_id)
        return True


class WorkerResultCelery(WorkerResult):
    """ """
    def __init__(self,wrk_id:str):
        """ 
        Metodo Factory que se encarga de crear un nuevo WorkerResult

        :param wrk_id: job id con el que se creo el WorkerId del cual se desea obtener el resultado.
        :type wrk_id: str

        :return: el WorkerResult asociado al wrk_id.
        :rtype: WorkerResult
        """
        result = AsyncResult(wrk_id)
        self._ready:bool = False
        self._status:str = ""
        self._result:dict = None

        try:
            self._ready = result.ready()
            self._status = result.status
            if not self._ready:
                return

            self._result:dict = json_loads(result.result)
        except Exception as e:
            #print(f'{type(self).__name__}({wrk_id}), Exception<{type(e).__name__}>, detail: {e}')
            return 

    def status(self)->str:
        return self._status
    
    def get(self)->dict:
        return self._result
    
    def ready(self)->bool:
        return self._ready        


class EventPublisherKafka(EventPublisher):
    
    def publish(self, header:dict, data:dict):
        params:dict = {
            'bootstrap.servers': f'{KAFKA_URL}:{KAFKA_PORT}'
        }
        compression:str = header.get('compression',None)
        topic:str       = header.get('topic')
        name:str        = header.get('name')
        pipeline:str    = header.get('pipeline')
        # Puede ser: none, gzip, snappy, lz4, zstd
        headers:list[tuple] = [
            ('name',   name.encode("utf-8")),
            ('source', pipeline.encode("utf-8"))
        ]
        if compression:
           params['compression.type'] = compression
           headers.append(('compression', compression.encode("utf-8")),)


        producer:Producer = Producer(params)
        producer.produce(
            topic=topic,
            value=json_dumps(data),
            headers=headers
        )
        producer.flush()

        


class WorkerRedis(Worker):
    
    def find_workerid(self,wrk_id:str,retry:int=1,time:float=0.01)->WorkerIdRedis:
        return WorkerIdRedis.block_find(wrk_id,retry,time)
    
    def make_workerid(self,wrk_id:str,status:WorkerStatus=WorkerStatus.PENDING)->WorkerIdRedis:
        return WorkerIdRedis.make(wrk_id,status)

    def gets_workerid(self,status:WorkerStatus=WorkerStatus.PENDING,last:int=-1)->list[str]:        
        return WorkerIdRedis.gets(status,last)
    
    def make_workercontext(self,expire:int=WorkerContext.SEC_EXPIRE)->WorkerContext:
        return WorkerContextRedis(expire) 
    
    def make_workerresult(self,wrk_id:str)->WorkerResultCelery:
        return WorkerResultCelery(wrk_id)
    
    def get_workers(self,status:WorkerStatus=None)->dict:
        if status:
            return { status.name.lower(): WorkerIdRedis.gets(status)}
        
        return { it.name.lower(): WorkerIdRedis.gets(it) for it in WorkerStatus}

    def make_evenpublisher(self, *args, **kwargs)->EventPublisherKafka:
        return EventPublisherKafka()
