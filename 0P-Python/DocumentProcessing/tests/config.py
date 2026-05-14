from logging import ( getLogger, basicConfig,Logger,
                      DEBUG,
                      INFO
                    )
from datetime import datetime
from unittest import TestCase

TESTS_LOCAL:bool = True

CONFIG_LOGGING:dict = { 
    'level'    : DEBUG,
    #'level'    : INFO,
    'filemode' : "a",
    #'format'   : "%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(funcName)s() - %(message)s",
    'format'   : "%(asctime)s.%(msecs)03d %(levelname)-8.8s- %(message)s",
    'datefmt'  : "%Y-%m-%d %H:%M:%S",
    'filename' : f"tests/logs/test_{datetime.now().strftime('%Y%m%d')}.log"
}


def get_log(appname:str,config:dict=None)->Logger:
    '''Funcion para obtener el objeto de Logger
        - appname : nombre de la aplicacion
        - config : Opcional configuracion para el logger
    '''
    if config is None:
        config = CONFIG_LOGGING

    ret = getLogger(appname)
    basicConfig(**config)
    return ret


def unittest_log(obj:TestCase)->Logger:
    cls_obj = type(obj)
    return getattr(cls_obj,'log',None)





