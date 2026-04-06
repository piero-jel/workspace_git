from __future__ import annotations
from os.path import dirname,exists
from os import remove
from logging import ( getLogger, config,basicConfig,Logger,
                      DEBUG,
                      INFO,
                      FileHandler,Formatter
                    )
from datetime import datetime
from django.test import TestCase


LOGGING_CONFIG = None
TESTS_LOCAL:bool = True

CONFIG_LOGGING:dict = { 
    'level'    : DEBUG,
    #'level'    : INFO,
    'filemode' : "a",
    #'format'   : "%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(funcName)s() - %(message)s",
    'format'   : "%(asctime)s.%(msecs)03d %(levelname)-8.8s- %(message)s",
    'datefmt'  : "%Y-%m-%d %H:%M:%S",    
}


class TestCaseLogger:
    def __init__(self,appname:str,file:str,config:dict=None,
                propagate:bool=False,remove:bool=False):
        '''
        - appname nombre de la aplicacion
        - file objeto __file__ del scrip, del cual tomara path al directorio padre
        - propagate flag opcional para habilitar la propagacion al log principal de la aplicacion
        - remove flag opcional para habilitar el remove del archivo al realizar del delete
         del logger `del instance<TestCaseLogger>`
        '''
        if config is None:
            config = CONFIG_LOGGING
        self.__remove:bool = remove
        self.__pathfile:str = f"{dirname(file)}/test_logs_{datetime.now().strftime('%Y%m%d')}.log"
        # 1. get and Configure Logger
        self.__log:Logger = getLogger(appname)
        self.__log.setLevel(config['level'])
        self.__log.propagate = propagate  # Don't send to root logger
        
        # 2. Create file handler and set formatter
        self.__handler:FileHandler = FileHandler(self.__pathfile)        
        self.__handler.setFormatter(Formatter(config['format'],
                                              datefmt=config['datefmt'])
                                    )
        # 3. Add handler to logger
        self.__log.addHandler(self.__handler)

    def __del__(self):
        self.__log.removeHandler(self.__handler)
        self.__handler.close()
        
        # Optionally remove the log file after tests
        if self.__remove and exists(self.__pathfile):
            remove(self.__pathfile)

    def debug(self,*args,**kwargs):
        self.__log.debug(*args,**kwargs)

    def info(self,*args,**kwargs):
        self.__log.info(*args,**kwargs)

    def warning(self,*args,**kwargs):
        self.__log.warning(*args,**kwargs)

    def error(self,*args,**kwargs):
        self.__log.error(*args,**kwargs)

    @classmethod
    def set(cls,appname:str,file:str,config:dict=None)->TestCaseLogger:
        '''Funcion para establecer el log del unitest case obtener el objeto de Logger
            - appname : nombre de la aplicacion
            - file : __file__
            - config : Opcional configuracion para el logger
        '''
        if config is None:
            config = CONFIG_LOGGING    
        
        return TestCaseLogger(appname,file,config)

    @classmethod
    def get(cls,obj:TestCase)->TestCaseLogger:
        '''Get logger from TestCase 
            - obj is self of the TEstCase
        '''
        cls_obj = type(obj)
        return getattr(cls_obj,'log',None)





