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

@file grpc_utils.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.3.
@date Sabado 16 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version      Brief
JEL            2026.04.16     0.0.3        Version Inicial no release
JEL            2026.05.17     0.0.4        Add Logger for gRPCServer y Ajustes para pylint
"""
# build-in modules
from typing import TypeAlias,Callable,overload
from abc import ABC, abstractmethod
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from logging import Logger


# third-party modules
from grpc import insecure_channel,Channel,Server,server
from google.protobuf.json_format import MessageToDict




class gRPCUtils:
    """ clase para encapsular utilidades """

    @classmethod
    def objgrpc2dict(cls,objgrpc:object)->dict:
        """ metodo para la converiosion de un objeto de protobuf a dict"""
        return MessageToDict(
            objgrpc,
            preserving_proto_field_name=True,   # Keep original field names (snake_case)
            use_integers_for_enums=False,       # Use enum names instead of integers
            always_print_fields_with_no_presence=True # los valores con 0, no lo imprime sin este
        )


# alias para el caller de metodo de un cliente
gRPCAction:TypeAlias = Callable[[Channel,dict], object]

# tupla para el registro de services
gRPCServicesReg = namedtuple('gRPCServicesReg',[ 'name','server'])

class gRPCServer(ABC):
    """clase abstracta que modela el server gRPS"""
    port:int
    pool_thread:int
    log:Logger

    def __init__(self,port:int,pool_thread:int,log:Logger=None):
        self.port = port
        self.pool_thread = pool_thread
        self._srv:Server = None
        self.log = log

    def _add(self,module:object,name:str,instance:object):
        name_fun = f"add_{name}Servicer_to_server"
        if not hasattr(module, name_fun):
            raise ValueError(f"El modulo '{module.__name__}', no tiene una funcion "\
                             f"llamada {name_fun}")

        func = getattr(module, name_fun)
        if not callable(func):
            raise TypeError(f"El attributo {name_fun} del modulo '{module.__name__}' "\
                            "no es una funcion")

        self.log.info("Add %s al services %s para el modulo '%s'",
                      type(instance).__name__,name,module.__name__)
        func(instance,self._srv)

    @overload
    def add(self,module:object,name:list[gRPCServicesReg]): ...

    @overload
    def add(self,module:object,name:str,instance:object): ...

    def add(self,module:object,name:str|list[gRPCServicesReg],instance:object=None):
        """ 
        Metodo que se encarga de agregar un service al listado

        :param module: Modulo Stub donde estan los metodos que representan los services
        :type module: object

        :param name: Si name es del tipo `str` este representa el Nombre del servicio, el mismo que
         figura en el proto file. Si name es una lista `list[gRPCServicesReg]` tuples que contienen
         el nombre e instancia del services.

        :type name: str|list[gRPCServicesReg]

        :param instance: instancia del servicio que definimos para manejar las peticiones y
          respuestas.
        :type instance: object
        """
        if isinstance(name,str):
            self._add(module,name,instance)
            return

        if isinstance(name,(list|tuple)):
            for it in name:
                self._add(module,it.name,it.server)

            return

        raise TypeError(f"El el tipo de attributo para name <{type(name).__name__}> no soportado")

    @abstractmethod
    def add_services(self):
        """ 
        Metodo Abstracto que se debera encarga de agregar los serivces usando las 
        funciones para cada services en particular, usando el gRPCStub generado desde la 
        definiciones dentro del proto file
        """

    def run(self):
        """ Metodo que inicia la ejecucion del servicio """
        self._srv = server(ThreadPoolExecutor(max_workers=self.pool_thread))
        self.add_services()
        port:int = self._srv.add_insecure_port(f"[::]:{self.port}")
        if port != self.port:
            self.port = port

        self._srv.start()

    def join(self):
        """ Metodo que permite atacharse al servicio a la espera de que el mismo finalice """
        self._srv.wait_for_termination()

    def stop(self,time:float = 1.0):
        """ Metodo para detener el servicio """
        self._srv.stop(time)


class gRPCClient:
    """ clase abstracta para modelar un Cliente gRPC"""
    url:str
    port:int
    _method:gRPCAction
    _methods:list[str] = None

    DISCARD_METHODS:tuple[str] = ('get_method','methods','run')

    def __init__(self,url:str,port:int,*args,**kwargs): #pylint:disable=unused-argument
        """
        Creacion de un objeto del tipo gRPCClient, para le manejo del cliente gRPC
        
        :param url: Opcional, url donde se localiza el services gRPC
        :type url: str

        :param port: Opcional numero de puerto en el cual se localiza el server gRPC
        :type port: int        
        """
        self.url = url
        self.port = port
        cls = type(self)
        self._methods = [ m for m in dir(self)
           if not m in cls.DISCARD_METHODS and callable(getattr(self, m)) and not m.startswith('__')
        ]

    def get_method(self,name:str)->gRPCAction:
        """
        Metodo que se encarga de localizar un metodo de la clase derivada, relacionado a una accion 
        que debe ejecutar el services.

        :param name: Nombre del metodo 
        :type name: str

        :return: objeto callable
        :rtype: gRPCAction
        """
        cls = type(self)
        method:gRPCAction = getattr(self,name,None)
        if method is None:
            raise ValueError(f"El Objeto '{cls.__name__}', no tiene un metodo llamado {name}")

        if not callable(method):
            raise TypeError(f'El attributo {cls.__name__}::{name} no es una funcion')

        return method

    def run(self,method:str,request:dict=None)->dict:
        """ 
        Metodo que se encarga de ejecutar una peticion al sevicio gRPC

        :param name: nombre del servicio dentro del proto gRPC
        :type name: str

        :param request: cuerpo de la peticion
        :type request: dict

        :return: response de la peticion
        :rtype: dict
        """
        self._method = self.get_method(method)

        with insecure_channel(f"{self.url}:{self.port}") as channel:
            if request is None:
                return gRPCUtils.objgrpc2dict(self._method(channel))

            return gRPCUtils.objgrpc2dict(self._method(channel,request))

    @property
    def methods(self)->list[str]:
        """ property para el geter del atributo con el listado de metodos"""
        return self._methods
