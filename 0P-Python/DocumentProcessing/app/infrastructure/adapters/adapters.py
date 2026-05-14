"""
Definimos la interface de las tareas, que solo dependen de Celery, usando 
interfaces para Worquer, el cual representa el backend o el sistema de Queue
que usara Celery para la asincronia
"""
# build module
from abc import ABC, abstractmethod
#import time
#from json import dumps as json_dumps
from logging import Logger
#from typing import Any
#from collections import namedtuple

# third-party modules
from celery import Task
#from celery.contrib.abortable import AbortableTask
#from celery.result import AsyncResult
from celery.utils.log import get_task_logger

# project modules
from app.infrastructure.adapters.settings import celery
from app.domain.ports import ProviderInterfaces,EventPublisher
from app.domain.worker import (
    WorkerStatus, WorkerContext, WorkerId, Worker,
    #WorkerResult,
)



log:Logger = get_task_logger(__name__)
   

class TaskPipeline(Task,ABC):
    # atributos necesarios para la configuracion del pipeline
    providers_cls:dict = None # dict con los provider, 
                              # `Key: name stages`, `values: class services provider`
    pipeline_config:list[str] = None # lista con el nombre de los stages a ejecutar 
                                     # (sigue el orden y puedne repetirse stages
                                     #  segun requerimientos)

    # atributos abstracto que manejan la infraestructura persitente y temporal     
    worker:Worker = None # worker, este debe definirse concretamente ya que es el encargado de crear
                         # los demas atributos relacionados al contexto
    work_id:WorkerId = None    
    work_context:WorkerContext = None
    
    context:dict = None # donde se alamcenra el context data que se actualiza con los stages,
                        # este debe ser dict de un solo nivel para no romper la serializacion
                        # por temas de performan se opto por uno solo,

    eventpublisher:EventPublisher = None # El encargado de publicar el trabajo finalizado

    expire:int = 86400
    

    def __init__(self,id:str|int = 1):        
        if isinstance(id,int):
            self.name:str = f"{type(self).__name__}_{id:06d}"
        else:
            self.name:str = id
        
        super().__init__()

    def delay(self, *args, **kwargs):
        return celery.send_task(self.name, args=args, kwargs=kwargs)

    def run(self, data:dict):
        cls = type(self)
        self.work_id = self.worker.find_workerid(self.request.id,retry=100) # wait hasta 1seg
        if self.work_id.job_id is None:
            log.error('%s::run() No se localizo el id <%s>, para el worker id',
                    cls.__name__,self.request.id)
            return None

        self.work_context = self.worker.make_workercontext(expire=self.expire)
        self.work_id.change(WorkerStatus.PROCESSING)

        content:dict = self.beg_pipeline(data)        
        for stage in self.pipeline_config:
            if self.work_id.is_canceled():
                if self.work_id.is_marked_for_deletion():
                    log.info("%s::run() delete work_id %s", cls.__name__,self.work_id)
                    self.work_context.delete(self.work_id.job_id)
                    self.work_id.delete_mark_deletion()
                    return None
                # si esta solo cancelada
                log.info("%s::run() cancel work_id %s", cls.__name__,self.work_id)
                return self.cancel()

            self.run_stage(stage,self.providers_cls[stage](),content)
            
        
        log.info("%s::run() %s : self.work_id.change(WorkerStatus.COMPLETED)",
                  type(self).__name__,self.work_id)
        self.work_id.change(WorkerStatus.COMPLETED)
        #self.eventpublisher = self.worker.make_evenpublisher()
        ## para salvar el response del end en el context temporal
        ret:str = self.end_pipeline(content)
        self.work_context.store(self.work_id.job_id,self.context)

        #return self.end_pipeline(content)
        return ret

    def cancel(self):
        self.context['job_status'] = WorkerStatus.CANCELLED.name.lower()
        log.info("%s::cancel() self.work_context.store(%s,%s)",
                  type(self).__name__,self.work_id.job_id,self.context)
        self.work_context.store(self.work_id.job_id,self.context)
        #self.update_state(state='REVOKED')
        return None
    
    def run_stage(self,name:str,stage:ProviderInterfaces,data:dict):
        """
        Metodo que ejecuta un stages, este puede sobrescribirse y alfinal invocar
        el de la clase Base de la forma `super().run_stage(name,satage,data)`
        para el correcto funcionamiento. Ya que este actualiza atributos

        :param name: nombre del stages
        :type name: str

        :param stage: Satege a ejecutar
        :type stage: ProviderInterfaces

        :param data: dato que actualizara el stage
        :type data: dict        
        """
        self.work_context.store(self.work_id.job_id,self.context)
        data = stage.do_work(data)

    @abstractmethod
    def beg_pipeline(self,data:dict)->dict:
        """
        Metodo que se encarga de inicial el `context` el cual contiene la info global del pipeline 
        con la cual se establece/actualiza el WorkerContex. Util en caso de works no sastifactorios.
        Se crea `pipeline_config` si este no es constante y predefinido y se devuelve el `data` que
        representa los datos que procesara el primer stages. 

        :param data: dato que acompaña la peticion
        :type data: dict

        :return: return dato con el cual debe iniciar el pipeline, el cual recibira el primer stages
        :rtype: dict
        """

    @abstractmethod
    def end_pipeline(self,data:dict)->str:
        """
        Metodo que se encarga de realizar las acciones al finalizar el pipeline, la responsabilidad 
        principal es la conversion dict->str

        :param data: dato o resultados de la ejecucion de todos los stages del pipeline
        :type data: dict

        :return: sting con la info a serailizar para ser recolectada por el sistema
        :rtype: str
        """
        
    @classmethod
    def launch(cls,data:dict)->str:
        '''Metodo de la clase que se encarga de lanzar el worker y retorna el id del mismo'''
        return cls().s(data).apply_async().id




    
        


