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

@file tasks_celery.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief  concrete adapter celery task/workers
@details definciion de la tareas/worker concretos que manejaran los pipelines
@version 0.0.3.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version        Brief
JEL            2026.04.14     0.0.3          Version Inicial no release
"""
# build-in module
from json import dumps as json_dumps
from logging import Logger

# third-party modules
from celery.utils.log import get_task_logger

# project modules
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
        
        # publicamos el job
        self.eventpublisher.publish(self.context,data)
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


