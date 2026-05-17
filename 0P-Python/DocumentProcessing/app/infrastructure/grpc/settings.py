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

@file settings.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   setting adapter concretes
@details configuracion para los adapter concretos, configuracion de conexiones y otros.
@version 0.0.3.
@date Sabado 16 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version             Brief
JEL            2026.04.14     0.0.3               Version Inicial no release
"""

# third-party modules
from dotenv import dotenv_values
from logging import (
    Logger,Formatter,StreamHandler,
    getLogger,basicConfig,
    DEBUG,
)

import os
import sys


# agregamos el directorio root del proyecto al `sys.path` para los import de los modulos,
# ya que se invoca app/infrastructure/grpc/server.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './protobuf')))


ENV_VARS:dict = dotenv_values()
if ENV_VARS is None:
    raise ValueError('Error, enviroment file not found')


GRPC_URL:str          = ENV_VARS.get('GRPC_URL','localhost')
GRPC_PORT:int         = ENV_VARS.get('GRPC_PORT',50051)
GRPC_POLL_TRHEAD:int  = ENV_VARS.get('GRPC_POLL_TRHEAD',10)

CONFIG_LOGGING:dict = { 
    'level'    : DEBUG, # Nivel de detalle (DEBUG, INFO, WARNING, etc.)
    'filemode' : "a",
    #'format'   : "%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(funcName)s() - %(message)s",
    'format'   : "%(asctime)s.%(msecs)03d %(levelname)-8.8s- %(message)s",
    'datefmt'  : "%Y-%m-%d %H:%M:%S",
    #'filename' : f"tests/logs/test_{datetime.now().strftime('%Y%m%d')}.log"
}


def get_logger(appname:str,stdout:bool=False,config:dict=None)->Logger:
    '''Funcion para obtener el objeto de Logger
        - appname : nombre de la aplicacion
        - config : Opcional configuracion para el logger
    '''
    if config is None:
        config = CONFIG_LOGGING

    ret:Logger = getLogger(appname)
    if stdout:
        ret.setLevel(config['level'])  
        # Añadir el manejador que envía a stdout
        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setFormatter(Formatter(config['format']))
        ret.addHandler(stdout_handler)
    else:
        basicConfig(**config)

    return ret
