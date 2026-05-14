"""
Worker, interfaces que modela el trabajo persitente y asincronico 
para la interaccion de la aplicacion con la infraestructura
"""

from abc import ABC, abstractmethod
from enum import Enum
#from time import sleep

from app.domain.ports import EventPublisher

class WorkerStatus(Enum):
    """ Estados en los que puede estar el Task Jobs

        - PENDING
        - PROCESSING
        - COMPLETED
        - FAILED
        - CANCELLED
    """
    PENDING:int    = 0
    PROCESSING:int = 1
    COMPLETED:int  = 2
    FAILED:int     = 3
    CANCELLED:int  = 4


class WorkerContext(ABC):
    #SEC_EXPIRE:int = 604800 # 1-Semana
    SEC_EXPIRE:int = 60 # 1-Minuto
    
    @abstractmethod
    def store(self,id:str,contex:dict)->bool:
        """
        Metodo que se encarga de almacenar un contexto en funcion de una clave `job_id`

        :param id: job id para localizar y cargar en memoria el registro.
        :type id: str

        :param contex: contexto que se desea almacenar.
        :type contex: dict
                
        :return: Estado del store 
        :rtype: bool
        """
    
    @abstractmethod
    def get(self,id:str,key:str)->dict:
        """
        Metodo que se encarga de obtener un target desde un contexto, previamente salvado, medinate 
        la clave job_id` y la `key` dentro del map.

        :param id: job id para localizar y cargar en memoria el registro.
        :type id: str

        :param key: nombre del parametro a localizar dentro del contexto 'dict serializado'
        :type key: str
                
        :return: target localizado
        :rtype: dict
        """

    @abstractmethod
    def load(self,id:str)->dict:
        """
        Metodo que se encarga recuperar un contexto, previamente salvado, en funcion del `id=job_id`

        :param id: job id para localizar y cargar en memoria el registro.
        :type id: str
                
        :return: contexto, si no localiza uno retorna un dict vacio
        :rtype: dict
        """

    @abstractmethod
    def delete(self,id:str)->bool:
        """
        Metodo que se encarga de eliminar un contexto, previamente salvado, en funcion 
        del `id=job_id`

        :param id: job id para localizar y eliminar en memoria el registro.
        :type id: str
                
        :return: estado del delete
        :rtype: bool
        """


class WorkerId(ABC):
    """  """
    WORKER_STATUS:dict = {it.value:it.name.lower() for it in WorkerStatus}
    _job_id:str = None
    #_status:int = WorkerStatus.PENDING.value
    _status:WorkerStatus = WorkerStatus.PENDING

    def __bool__(self)->bool:
        return self._job_id is not None
    
    def __eq__(self, obj:WorkerId):
        return obj._job_id == self._job_id and obj._status == self._status
   
    def __str__(self)->str:
        cls = type(self)
        #return f'{cls.__name__}(job_id="{self._job_id}", status={self.get_status()})'
        return f'{cls.__name__}(job_id="{self._job_id}", status={self._status.name.lower()})'

    def get_status(self)->str:
        """ Metodo para obtner la representacion str del estado actual """
        #return type(self).WORKER_STATUS.get(self._status)
        return self._status.name.lower()
    
    @property
    #def status(self)->int:
    def status(self)->WorkerStatus:
        """ getter para el attr status """
        return self._status
    
    @property
    def job_id(self)->str:
        """ getter para el attr job id """
        return self._job_id
    
    @abstractmethod
    def in_status(self,*args:WorkerStatus)->bool:
        """
        Metodo que se encarga de verificar si el worker id se encuentra en alguno de los estados
        pasados        

        :param *args: estado/s que se desean verificar
        :type *args: WorkerStatus 

        :return: estado de la accion, True: success, False: Failure
        :rtype: bool
        """

    @abstractmethod
    def change(self,status:WorkerStatus=WorkerStatus.PENDING)->bool:
        """
        Metodo que se encarga de cambiar de estado de un WorkerId y actualizar 
        el mismo sobre el sistema persistente

        :param status: Opcional, Nuevo estado para el WorkerId. Por defecto Pending
        :type status: WorkerStatus

        :return: estado de la accion, True: success, False: Failure
        :rtype: bool
        """
    
    @abstractmethod
    def is_canceled(self)-> bool:
        """
        Metodopara verificar si el worker id fue cancelado

        :param status: Opcional, Nuevo estado para el TaskJobs. Por defecto Pending
        :type status: WorkerStatus
        
        :return: estado de la cancelacion, True: fue cancelado, False: no fue cancelado
        :rtype: bool
        """

    @abstractmethod
    def push(self)->bool:
        """
        Metodo que se encarga de insertar un item TaskJobs en el sistema persistente
        
        :return: estado de la accion, True: success, False: Failure
        :rtype: bool
        """
        
    @abstractmethod
    def delete(self)->bool:
        """
        Metodo que se encarga de quitar un item worker id del sistema persistente
        
        :return: estado de la accion, True: success, False: Failure
        :rtype: bool
        """
        
    # Para el delete de worker necesitamos tres pasos      
    @abstractmethod
    def mark_for_deletion(self)->bool:
        """
        Marcar el worker para el delete, 'mark the worker for deletion'

        :return: estado de la accion, True: success, False: Failure
        :rtype: bool
        """

    @abstractmethod
    def is_marked_for_deletion(self)->bool:
        """ 
        ¿worker esta marcado para delete?     
        'Is the worker marked for delete?'

        :return: estado de la accion, True: success, False: Failure
        :rtype: bool
        """

    @abstractmethod
    def delete_mark_deletion(self)->bool:
        """
        Delete worker marcado para delete

        :return: estado de la accion, True: success, False: Failure
        :rtype: bool            
        """


class WorkerResult(ABC):

    @abstractmethod
    def status(self)->str:
        """ 
        Metodo para obtener es estado del Result

        :return: el string que representa el estado
        :rtype: str
        """

    @abstractmethod
    def get(self)->dict:
        """ 
        Metodo para obtener es resultado, si ready es False retorna `None`.

        :return: el response/dictg que representa el resultado
        :rtype: dict
        """

    @abstractmethod
    def ready(self)->bool:
        """ 
        Metodo para verfificar el estado ready del Result

        :return: el estado ready, `True` job listo, `False` estado en ejecucion, failure, canceled
        :rtype: bool
        """


class Worker(ABC):

    @abstractmethod
    def find_workerid(self,wrk_id:str,retry:int=1,time:float=0.01)->WorkerId:
        """
        Metodo que se encarga de localiza en el sistema persistente un WorkerId desde su `job_id` 
        de manera bloqueante.

        :param wrk_id: job id para localizar y cargar en memoria el registro.
        :type wrk_id: str

        :param retry: Opcional numero de reintentos. Por defecto 1.
        :type retry: int

        :param time: Opcional, tiempo de demora entre reintetos. Por defecto 10 mS (mili segundos)
        :type time: float

        
        :return: el WorkerId localizado, de lo contrario WorkerId vacio `bool(WorkerId) == False`.
        :rtype: WorkerId
        """
        ''' esta ligado a de forma encadenada
        @classmethod
        def block_find(cls,job_id:str,retry:int=1,time:float=0.01)->WorkerId:        
        
        @classmethod
        def find(cls,job_id:str)->WorkerId:
        
        '''

    @abstractmethod
    def make_workerid(self,wrk_id:str,status:WorkerStatus=WorkerStatus.PENDING)->WorkerId:
        """ 
        Metodo Factory que se encarga de crear un nuevo WorkerId

        :param wrk_id: job id con el que se creara el nuevo WorkId sobre memoria y de forma 
        persistente.

        :type wrk_id: str

        :param status: Opcional, estado inicial para el nuevo WorkerId. Por defecto Pending.
        :type status: WorkerStatus

        :return: el WorkerId creado y persistido en el sistema.
        :rtype: WorkerId
        """

        ''' esta ligado a 
        @classmethod
        def make(cls,job_id:str,status:WorkerStatus=WorkerStatus.PENDING)->WorkerId:
        '''

    @abstractmethod
    def gets_workerid(self,status:WorkerStatus=WorkerStatus.PENDING,last:int=-1)->list[str]:
        """
        Metodo de la clase para obtener el listado de WorkerId.job_id en funcion del estado

        :param status: Opcional, Nuevo estado para el TaskJobs. Por defecto Pending
        :type status: str

        :param last: para indicar la cantidad de registros desde el mas reciente al mas
        antiguo. Por defecto `-1`, indica todos.
        :type last: int

        :return: listado de de job id en el estado especifico localizados
        :rtype: list[str]
        """

    @abstractmethod
    def make_workercontext(self,expire:int=WorkerContext.SEC_EXPIRE)->WorkerContext:
        """ 
        Metodo Factory que se encarga de crear un nuevo WorkerId

        :param wrk_id: job id con el que se creara el nuevo WorkId sobre memoria y de forma 
        persistente.

        :type wrk_id: str

        :param status: Opcional, estado inicial para el nuevo WorkerId. Por defecto Pending.
        :type status: WorkerStatus

        :return: el WorkerId creado y persistido en el sistema.
        :rtype: WorkerId
        """        

    @abstractmethod
    def make_workerresult(self,wrk_id:str)->WorkerResult:
        """ 
        Metodo Factory que se encarga de crear un nuevo WorkerResult

        :param wrk_id: job id con el que se creo el WorkerId del cual se desea obtener el resultado.
        :type wrk_id: str

        :return: el WorkerResult asociado al wrk_id.
        :rtype: WorkerResult
        """

    @abstractmethod
    def get_workers(self,status:WorkerStatus)->dict:
        """ 
        Metodo para obtener los worker_id/jobs_id en funcion del estado

        :param status: estado de los job_id que se desean obtener
        :type status: WorkerStatus

        :return: dict-json con el nombre del estado y el listado de job_id en dicho estado
        :rtype: dict
        """

    @abstractmethod
    def make_evenpublisher(self,*args,**kwargs)->EventPublisher:
        """ 
        Metodo Factory que se encarga de crear un EventPublisher, el cual se encargara
        de publicar el Worker finalizado

        :return: el EventPublisher creado
        :rtype: EventPublisher
        """