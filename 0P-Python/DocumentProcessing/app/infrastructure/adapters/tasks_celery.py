
# build module
from json import dumps as json_dumps
from logging import Logger

# third-party modules
#from dotenv import dotenv_values
#from celery import Celery
from celery.utils.log import get_task_logger

# project modules
#from settings import (
#    REDIS_URL,REDIS_PORT,REDISCLI_AUTH
#)
from app.infrastructure.adapters.settings import celery
from app.infrastructure.adapters.worker_redis import WorkerRedis,WorkerStatus
from app.infrastructure.adapters.adapters import TaskPipeline
from app.domain.ports import ProviderInterfaces
from app.application.services import PROVIDERS_CLS




log:Logger = get_task_logger(__name__)



class TaskProcessingGateway(TaskPipeline):

    providers_cls:dict = PROVIDERS_CLS # ProvidersCls    
    worker:WorkerRedis = WorkerRedis()
    
    # opcionales dependen de la implememntacion concreta
    _pipeline:list[str] = None  # lista donde se almacenaran los stages ejecutas

    def beg_pipeline(self,data:dict)->dict:
        """
        data
          - pipeline_config : listado/pipeline de stages ex: `extraction, analysis, enrichment`
          - name : nombre
          - topic : topic - tema
          - compression : si desea compresion
          - content : datos a procesar 
        """   
        self.pipeline_config = data.get('pipeline_config',list(self.providers_cls.keys()))
        self._pipeline = [] # iniciamos el registro de stages ejecutados
        self.context = { # establecemso el context para localizar errores externos
            'name'        : data.get('name'),
            'topic'       : data.get('topic'),
            'compression' : data.get('compression',None), # Puede ser: none, gzip, snappy, lz4, zstd
            'stages'      : WorkerStatus.PENDING.name.lower(),
            'pipeline'    : "",#", ".join(self._pipeline),
            'job_status'  : self.work_id.get_status()
        }

        if 'content' not in data.keys():
            log.error('%s::run() No tenemos datos para procesar',type(self).__name__)
            raise Exception(f'{type(self).__name__}::run() No tenemos datos para procesar')

        return data

    def end_pipeline(self,data:dict)->str:
        ## creamos el EventPublisher
        self.eventpublisher = self.worker.make_evenpublisher()
        # actualizamos el context con el job_status
        self.context['job_status'] = self.work_id.get_status()
        self.context["stages"]   = WorkerStatus.COMPLETED.name.lower()
        #self.context['ready'] = True
        
        self.eventpublisher.publish(self.context,data)
        # armamos y serializamos el response, add del context
        #return json_dumps({**self.context,'result': data})
        return json_dumps(self.context)
    

    def run_stage(self,name:str,stage:ProviderInterfaces,data:dict):
        self._pipeline.append(name)
        self.context['pipeline'] = ", ".join(self._pipeline)
        self.context["stages"]   = name
        super().run_stage(name,stage,data)

        

       
  







# Registros de la tareas
celery.register_task(TaskProcessingGateway())

##
# celery -A app.infrastructure.adapters.tasks_celery worker --loglevel=INFO 
# celery -A app.infrastructure.adapters.tasks_celery worker --loglevel=DEBUG
##


