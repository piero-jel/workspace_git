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
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version             Brief
JEL            2026.04.14     0.0.3               Version Inicial no release
JEL            2026.05.17     0.0.4               Ajustest para el modelo persistente de workers
                                                  (entre backend y broker) y correciones para pylint
"""

# third-party modules
from dotenv import dotenv_values
from celery import Celery
from redis import Redis



ENV_VARS:dict = dotenv_values()
if ENV_VARS is None:
    raise ValueError('Error, enviroment file not found')


REDISCLI_AUTH:str = ENV_VARS.get('REDISCLI_AUTH',None)
REDIS_URL:str     = ENV_VARS.get('REDIS_URL','localhost')
REDIS_PORT:int    = ENV_VARS.get('REDIS_PORT',6379)
REDIS_DB:int      = ENV_VARS.get('REDIS_DB',0)

KAFKA_URL:str     = ENV_VARS.get('KAFKA_URL','localhost')
KAFKA_PORT:int    = ENV_VARS.get('KAFKA_PORT',9092)

redis:Redis = Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    password=REDISCLI_AUTH,
    db=REDIS_DB
)

celery:Celery = Celery(
    'tasks',
    broker  = f'redis://:{REDISCLI_AUTH}@{REDIS_URL}:{REDIS_PORT}/0',
    backend = f'redis://:{REDISCLI_AUTH}@{REDIS_URL}:{REDIS_PORT}/1',
    result_extended=True
)


celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
