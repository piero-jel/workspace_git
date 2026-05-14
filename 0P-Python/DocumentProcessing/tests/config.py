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

@file config.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.3.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date                 Version                      Brief
JEL            2026.04.14     0.0.3   Version Inicial no release
"""

# build-in modules
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





