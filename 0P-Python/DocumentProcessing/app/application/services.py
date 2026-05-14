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

@file services.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   Logica de Negocios
@details Logica de Negocios
@version 0.0.3.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version          Brief
JEL            2026.04.14     0.0.3            Version Inicial no release
"""

# project modules
from app.application.providermocks import (
    ProviderAnalysis,ProviderExtraction,ProviderEnrichment
)

from app.domain.worker import (
    WorkerStatus,WorkerContext,WorkerId,WorkerResult,Worker
)



PROVIDERS_CLS:dict = {
    "extraction" : ProviderExtraction,
    "analysis"   : ProviderAnalysis,
    "enrichment" : ProviderEnrichment
}



class ProcessGateway:
    ''' Process Gateway Interfaces Clase '''
    retry:int = 10
    time:float = 0.1
    resp:dict = None

    worker_id:WorkerId = None

    def __init__(self,worker:Worker):
        """ 
        :param worker: Objeto concreto que modela la infraestructura usada para el backed 
        de los worker
        :type worker: Worker
        """        
        self.worker:Worker = worker
        self.work_context:WorkerContext = self.worker.make_workercontext(expire=604800)        

    def _status(self,worker_id:str)->bool:
        """ """
        self.worker_id = self.worker.find_workerid(worker_id,retry=self.retry,time=self.time)
        if self.worker_id.job_id is None :
            self.resp = {
                "code"      : 1,
                "error"     : f"worker id '{worker_id}' not found",
                "job_id"    : worker_id
            }
            return False

        if self.worker_id.status == WorkerStatus.CANCELLED.value:
            self.resp = {
                    "code"      : 0,
                    "ready"     : True,
                    "status"    : "REVOKED",                
                    "stages"    : self.worker_id.get_status(),
                    "job_id"    : worker_id
            } 
            resp = self.work_context.load(self.worker_id.job_id)
            if resp:
                self.resp.update(resp)
                
            return False
        
        return True
    
    def _get_result(self)->dict:
        result:WorkerResult = None
        tsk_status = self.work_context.load(self.worker_id.job_id)
        
        ret:dict = { 
            "code": 0,
            "job_id"    : self.worker_id.job_id,
        }
        if tsk_status:
            ret.update(**tsk_status)
        
        
        result = self.worker.make_workerresult(self.worker_id.job_id)
        return {
            **ret,
            #"ready"     : result.ready(),
            "ready"     : self.worker_id.in_status(WorkerStatus.COMPLETED), 
            #"status"    : result.status(), 
            #"stages"    : self.worker_id.get_status(), # lo toma del context
            "status"    : self.worker_id.get_status(), 
            "result"    : result.get()
        }

    def create(self,job_id:str)->str:
        """ 
        Metodo para la creacion de un procesamiento

        :param job_id: idnetificador unico para el job de procesamiento
        :type job_id: str

        :return: job_id 
        :rtype: str
        """
        wrk_id:WorkerId = self.worker.make_workerid(job_id)
        return wrk_id.job_id
    
    def get(self,job_id:str=None)->dict:
        """ 
        Metodo para obtener el estado de un procesamiento

        :param job_id: identificador unico para el job de procesamiento
        :type job_id: str

        :return: estado del proecesamineto para el `job_id` 
        :rtype: str
        """
        if job_id is None:
            return self.worker.get_workers()

        if not self._status(job_id):
            return self.resp
        
        return self._get_result()
    
    def cancel(self,worker_id:str)->bool:
        """ 
        Metodo para la peticion de cancelar un procesamiento

        :param job_id: idnetificador unico para el job de procesamiento
        :type job_id: str

        :return: estado del proecesamineto para el `job_id` 
        :rtype: str
        """
        if not self._status(worker_id):
            return self.resp
        

        if self.worker_id.in_status(WorkerStatus.COMPLETED):
            return {
                "code"      : 0,
                "job_status": self.worker_id.get_status(),
                "message"   : f"No se puede cancelar el worker id '{worker_id}', fue completado",
                "job_id"    : worker_id
            }

        if self.worker_id.in_status(WorkerStatus.FAILED):
            return {
                "code"      : 0,
                "job_status": self.worker_id.get_status(),
                "message"   : f"No se puede cancelar el worker id '{worker_id}', finalizo con errores",
                "job_id"    : worker_id
            }

        self.worker_id.change(WorkerStatus.CANCELLED)

        return {
            "code"      : 0,
            "job_status": self.worker_id.get_status(),
            "message"   : f"Abortando worker id '{worker_id}'",
            "job_id"    : worker_id
        }
    
    def delete(self,worker_id:str)->dict:
        """ 
        Metodo para eliminar una peticion procesamiento
         1° Si no esta cancelado, lo cancela.
         2° Luego lo elimina.

        :param job_id: identificador unico para el job de procesamiento
        :type job_id: str

        :return: estado de la accion para el `job_id` 
        :rtype: dict
        """
        if not self._status(worker_id) :
            return self.resp
        
        # estado intermedio, no inicio aun o esta en proceso
        if self.worker_id.in_status(WorkerStatus.PROCESSING,WorkerStatus.PENDING):
            self.worker_id.mark_for_deletion()
            return {
                "code"      : 0,
                "job_status": self.worker_id.get_status(),
                "message"   : f"Inicio del Borrado del worker id '{worker_id}'",
                "job_id"    : worker_id
            }
        
        # estado final WorkerStatus.CANCELLED,WorkerStatus.COMPLETED,WorkerStatus.FAILED
        job_status:str = self.worker_id.get_status()
        self.worker_id.delete()
        return {
            "code"      : 0,
            "job_status": job_status,
            "message"   : f"Se elimino del worker id '{worker_id}'",
            "job_id"    : worker_id
        }
        
    def get_list(self,status:str=None)->dict:
        """ 
        Metodo para obtener el listado de job en funcion del estado, los valores posibles dependen
        de WorkerStatus y estos pueden ser

        - `pending`
        - `processing`
        - `completed`
        - `failed`
        - `cancelled`

        :param status: Opcional, estado que se desea consultar. En caso de no aportarlo retorna el 
        listado de todos los estados.
        :type status: str

        :return: listado de los `job_id`  en funcion del estado.
        :rtype: dict
        """
        st:int = None
        status_map:dict = {it.name:it.value for it in WorkerStatus}
        if status:            
            st = status_map.get(status.strip().upper(),None)
        
        if st is not None:
            return self.worker.get_workers(WorkerStatus(st))
        
        if status:
            return { 
                "message": f"Estado '{status}' NO SOPORTADO, estado admisibles 'status_list'",
                "status_list": [x.lower() for x in status_map.keys()],
                    #**self.worker.get_workers()
                }
        
        return self.worker.get_workers()
