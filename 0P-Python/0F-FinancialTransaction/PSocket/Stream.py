"""@package docstring
Copyright 2022, Jesus Emanuel Luccioni
All rights reserved.

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

\b file PSocket/Stream.py
\b brief posix socket Stream Clien and Server
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Lunes 05 de Mayo de 2022.
\b version 0.0.1.
  
\b Change History:

Author         Date                 Version     Brief
JEL            2022.05.05           0.0.1       Version Inicial

"""
from socket import socket,SOCK_STREAM,AF_INET
from os  import strerror
from abc import ABC, abstractmethod
from enum import Enum

class Byteint:
    """ Class para el manejo de byte to int """
    def __init__(self,l:int=4):
        """
        Inicializacion de un objeto `Byteint`

        :param l: cnatidad de bytes
        :type l: int
        """
        self.len:int = l

    def number2binary(self,num:int)-> bytearray:
        """
        Metodo para la conversion de numero a frame de bytes

        :param num: numero a transformar
        :type num: int

        :return: return array/frame de byte
        :rtype: bytearray
        """
        ret:bytearray = bytearray(self.len)
        i : int = self.len
        while i>0:
            i -= 1
            ret[i] = num % 256
            num = int(num /256)

        return ret

    def binary2number(self,arrbyte:bytearray) -> int :
        """
        Metodo para la conversion de un frame de bytes a numero

        :param arrbyte: array/frame de bytes
        :type arrbyte: bytearray

        :return: valor numerico
        :rtype: int
        """
        ret : int = 0
        i : int = 0
        mx = len(arrbyte)
        while i < self.len and i < mx:
            ret |= arrbyte[i]
            i += 1
            if i != self.len:
                ret <<= 8

        return ret


class FmtLen(int,Enum):
    ''' Enumeration para el setting del formato length '''
    FMTNONE = 0 # sin formato length en header
    FMT2B   = 2 # formato length en header de 2-Bytes
    FMT4B   = 4 # formato length en header de 4-Bytes


class Status(int,Enum):
    ''' class enum del tipo int for status Station Host '''
    DISCONNECT = 0
    CONNECT    = 1
    ERROR      = 2


class Stream(ABC): # pylint: disable=too-many-instance-attributes
    ''' Clase Base Abstracta Para modelar un Stream Socket '''
    def __init__(self,**kwargs):
        """
        Inicializacion para Objetos derivados de Stream

        :param ip: direccion IP
        :type ip: str

        :param port: numero de puerto
        :type port: int

        :param fmt_len: numero de bytes para expresar la longitud de los mensajes
        :type fmt_len: int
        """
        self._ip:str    = kwargs.get('ip','0.0.0.0')
        self._port:int  = kwargs.get('port',8080)
        self.format_len:FmtLen = FmtLen(kwargs.get('fmt_len',4))
        self.byteint:Byteint = Byteint(self.format_len)
        self._st:Status   = Status.DISCONNECT

        # creamso el socket
        self._fd:socket = None
        self.last_error = None
        if not isinstance(self._port,int):
            self._port = int(self._port)

    @abstractmethod
    def Connect(self):
        '''Connect Method'''
        #pass

    @abstractmethod
    def Disconnect(self):
        '''Disconnect Method'''
        #pass

    @property
    def format_len(self):
        """Getter atribute format length"""
        return self._fmt_len

    @format_len.setter
    def format_len(self,f):
        """Setter atribute format length"""
        if not isinstance(f,FmtLen) and not isinstance(f,int):
            raise TypeError(f'type format {type(f)} no permitido')

        if  isinstance(f,int):
            match f:
                case 2:
                    self._fmt_len = FmtLen.FMT2B
                case 4:
                    self._fmt_len = FmtLen.FMT4B
                case _:
                    self._fmt_len = FmtLen.FMTNONE

            return

        self._fmt_len = f

    def Status(self)-> Status:
        '''Metodo para consultar el estado '''
        return self._st

    def Send(self,msg:str,timeout:float=None,encoding:str='utf-8')-> int:
        """
        Metodo para el envio de un mensaje al host

        :param msg : mensaje to send
        :type msg: str

        :param timeout : float, tiempo de espera maximo para el envio del paquetes.
        :type timeout: str

        :param encoding: opcional UTF-8, encodign del msg
        :type encoding: str

        :return: return Mayor a Cero la longitud del mensaje enviado, `-1` error
        :rtype: int
        """
        msg_len = len(msg)
        if msg_len == 0:
            # Enviamos el cierre de conexion
            self._fd.send(self.byteint.number2binary(0) + b"")
            return 0

        ## enviamos la longitud primero
        header = self.byteint.number2binary(msg_len)
        sent = self._fd.send(header)
        if sent == 0:
            self._st = Status.ERROR
            self.last_error = "socket connection broken"
            return -1

        bmsg = bytearray(msg,encoding=encoding)
        msg_len = len(bmsg)
        totalsent = 0
        if timeout is not None:
            self._fd.settimeout(timeout)

        while totalsent < msg_len:
            sent = self._fd.send(bmsg[totalsent:])
            if sent == 0:
                self._st = Status.ERROR
                self.last_error = "socket connection broken"
                return -1

            totalsent = totalsent + sent

        if timeout is not None:
            self._fd.settimeout(None)

        return totalsent

    def Receive(self,timeout:float=None,encoding:str='utf-8',**kwargs)->str:#pylint: disable=unused-argument
        """
        Metodo para recevir un mensja desde el host

        :param timeout : float, tiempo de espera maximo para la recepcion de paquetes.
        :type timeout: float

        :param encoding: opcional UTF-8, encodign del msg
        :type encoding: str

        :param kwargs: parametros opcionales
        :type kwarg: ...

        :return: return 
        :rtype: str
        """
        if timeout is not None:
            self._fd.settimeout(timeout)

        header = self._fd.recv(self._fmt_len)
        len_msg:int = self.byteint.binary2number(header)

        if len_msg == 0:
            return ''

        chunks:list = []
        bytes_recd:int = 0
        while bytes_recd < len_msg:
            if timeout is not None:
                self._fd.settimeout(timeout)

            chunk:bytes = self._fd.recv(len_msg - bytes_recd)
            if chunk == b'':
                self._st = Status.ERROR
                self.last_error = "socket connection broken"
                return ''

            chunks.append(chunk.decode(encoding=encoding))
            bytes_recd += len(chunk)

        return ''.join(chunks)

    def SendAndReceive(self,msg:str,timeout:float=None,encoding='utf-8',**kwargs)->str:#pylint: disable=unused-argument
        """
        Metodo para enviar y recibir un mensaje

        :param msg: mensaje a enviar
        :type src: str

        :param timeout: timeout, tiempo de espera maximo para el envio/recepcion de paquetes.
        :type src: float

        :return: return descripcion
        :rtype: dict
        """
        if self.Send(msg,timeout,encoding) == -1:
            return ''

        return self.Receive(timeout,encoding)


class Client(Stream):
    ''' Clase para modelar la conexion al host '''

    def Connect(self)->bool:
        """
        Metodo para conexion al host remoto

        :param src: argument descripcion 
        :type src: str

        :return: `True` connect success, `False` connect failure
        :rtype: bool
        """
        self._fd = socket(AF_INET, SOCK_STREAM)
        ret = self._fd.connect_ex((self._ip,self._port))
        if ret != 0:
            self.last_error = strerror(ret)
            self._st = Status.ERROR
            return False

        self._st = Status.CONNECT
        return True

    def Disconnect(self)->bool:
        """
        Metodo para la desconexion al host remoto 
        
        :return: `True` connect success, `False` connect failure
        :rtype: bool
        """
        if self._st == Status.CONNECT:
            self._fd.close()
            self._st = Status.DISCONNECT

        return True

    def __enter__(self):
        ''' for with context '''
        return self

    def __exit__(self, *args):
        ''' for exit with context '''        
        self.Disconnect()

    def __repr__(self) -> str:
        '''representacion formal del objeto mediante un string'''
        return f'{type(self).__name__}(ip={self._ip},port={self._port},fmt_len={self._fmt_len})'


class Server(Stream):
    ''' Clase para modelar la conexion al host '''

    def __init__(self,**kwarg):
        """
        Inicializacion de una instancia del tipo Server Stream Socket

        :param ip: ip para el Local Server, opcional por defecto localohost 127.0.0.1
        :type src: str

        :param port: puerto, por defecto 8080
        :type src: int

        :param fmt_len: formato para el set/get la longitud en el header del mensaje,
          por defecto 4 bytes.
        :type fmt_len: str
        """
        self._fdsrv:socket = None
        super().__init__(**kwarg)

    def Connect(self)->bool:
        """
        Metodo para conexion al host remoto
        
        :return: `True` connect success, `False` connect failure
        :rtype: bool
        """
        self._fdsrv = socket(AF_INET, SOCK_STREAM)
        self._fdsrv.bind((self._ip,self._port))
        self._fdsrv.listen()
        self._st = Status.CONNECT
        return True

    def Disconnect(self)->bool:
        """
        Metodo para la desconexion al host remoto 

        :param src: argument descripcion 
        :type src: str

        :return: `True` connect success, `False` connect failure
        :rtype: bool
        """
        if self._st != Status.CONNECT:
            return False

        if self._fd:
            self._fd.close()

        if self._fdsrv:
            self._fdsrv.close()

        self._st = Status.DISCONNECT
        return True

    def Accept(self)->str:
        """
        Metodo para Admitir conexion desde un cliente

        :return: el client address
        :rtype: str
        """
        self._fd, cliaddr = self._fdsrv.accept()
        return str(cliaddr)

    def __enter__(self):
        ''' for with context '''    
        return self

    def __exit__(self, *args):
        ''' for exit with context '''
        self.Disconnect()

    def __repr__(self) -> str:
        '''representacion formal del objeto mediante un string'''
        return f'{type(self).__name__}(ip={self._ip},port={self._port},fmt_len={self._fmt_len})'
