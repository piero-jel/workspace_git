from enum import Enum
import socket
from os  import strerror
from abc import ABC, abstractmethod

class Byteint:
  def __init__(self,l:int = 4):
    self.len = l
  # end def

  def number2binary(self,num:int)-> bytearray:
    ret:bytearray = bytearray(self.len)
    i : int = self.len
    while(i>0):
      i -= 1
      ret[i] = num % 256
      num = int(num /256)
    # end while
    return ret
  # end def

  def binary2number(self,arrbyte:bytearray) -> int :
    ret : int = 0
    i : int = 0
    mx = len(arrbyte)
    while( i < self.len and i < mx):
      ret |= arrbyte[i]
      i += 1
      if(i != self.len):      
        ret <<= 8
      # end if
    # end while
    return ret
  # end def  
# end class

class FmtLen(int,Enum):  
  ''' Enumeration para el setting del formato length '''
  FMTNONE = 0 # sin formato length en header
  FMT2B   = 2 # formato length en header de 2-Bytes
  FMT4B   = 4 # formato length en header de 4-Bytes
# end class

class Status(int,Enum):
  ''' class enum del tipo int for status Station Host '''
  DISCONNECT = 0
  CONNECT    = 1
  ERROR      = 2
# end class for status

class Stream(ABC):
  ''' Clase Base Abstracta Para modelar un Stream Socket '''
  def __init__(self,**kwarg):
    self._ip    = kwarg.get('ip','0.0.0.0')
    self._port  = kwarg.get('port',8080)
    self.format_len = FmtLen(kwarg.get('fmt_len',4))
    self.byteint = Byteint(self.format_len)
    self._st   = Status.DISCONNECT

    # creamso el socket
    #self._fd:socket.socket = None
    self._fd = None
    self.last_error = None
    if(not isinstance(self._port,int)):
      self._port = int(self._port)
    # end if
  #end def

  @abstractmethod
  def Connect(self):
    pass
  #end def

  @abstractmethod
  def Disconnect(self):
    pass
  #end def


  @property
  def format_len(self):
    return self._fmt_len
  # end def

  @format_len.setter
  def format_len(self,f):
    if(not isinstance(f,FmtLen) and not isinstance(f,int)):
      raise TypeError(f'type format {type(f)} no permitido')
    # end if
    if(isinstance(f,int)):
      match f:
        case 2:
          self._fmt_len = FmtLen.FMT2B
        case 4:
          self._fmt_len = FmtLen.FMT4B
        case _:
          self._fmt_len = FmtLen.FMTNONE
      # end match
      return 
    # end if
    self._fmt_len = f
  # end def

  def Status(self)-> Status:
    '''Metodo para consultar el estado '''
    return self._st
  # end def

  def Send(self,msg,timeout=None,encoding='utf-8')-> int:
    ''' Metodo para el envio de un mensaje al host
        - msg : mensaje to send
        - timeout : float, tiempo de espera maximo para el envio del paquetes.
        - encoding : opcional UTF-8, encodign del msg

        return
          + Mayor a Cero la longitud del mensaje enviado
          + -1 error
    '''
    msg_len = len(msg)
    if(msg_len == 0):
      ''' Enviamos el cierre de conexion '''
      self._fd.send(self.byteint.number2binary(0) + b"")
      return 0
    # end 

    ## enviamos la longitud primero
    header = self.byteint.number2binary(msg_len)
    #print(f'header: {header}')
    sent = self._fd.send(header)
    if( sent == 0):
      self._st = Status.ERROR
      self.last_error = "socket connection broken"
      return -1        
    # end if

    
    bmsg = bytearray(msg,encoding=encoding)
    msg_len = len(bmsg)
    totalsent = 0
    if(timeout != None):
      self._fd.settimeout(timeout)
    # end fi
    while totalsent < msg_len:
      sent = self._fd.send(bmsg[totalsent:])
      if( sent == 0):
        self._st = Status.ERROR
        self.last_error = "socket connection broken"
        return -1        
      # end if 
      totalsent = totalsent + sent
    # end while
    if(timeout != None):
      self._fd.settimeout(None)
    # end fi
    return totalsent
  # end def

  def Receive(self,timeout=None,encoding='utf-8',**kwarg)-> str:
    ''' Metodo para recevir un mensja desde el host
          - timeout : float, tiempo de espera maximo para la recepcion
            de paquetes.

          - encoding : opcional UTF-8, encodign del msg
    '''    
    if(timeout != None):
      self._fd.settimeout(timeout)
    # end fi
    header = self._fd.recv(self._fmt_len)
    len_msg:int = self.byteint.binary2number(header)

    if(len_msg == 0):
      return ''
    # end if
    
    chunks = []
    bytes_recd = 0
    while bytes_recd < len_msg:
      if(timeout != None):
        self._fd.settimeout(timeout)
      # end fi
      chunk:bytes = self._fd.recv(len_msg - bytes_recd)
      if (chunk == b''):
        self._st = Status.ERROR
        self.last_error = "socket connection broken"
        return ''    
      # end if
      chunks.append(chunk.decode(encoding=encoding))
      bytes_recd += len(chunk)
    # end while
    return f''.join(chunks)    
  # end def

  def SendAndReceive(self,msg,timeout=None,encoding='utf-8',**kwarg) -> str:
    ''' Metodo para enviar y recibir un mensaje
        - timeout : timeout, tiempo de espera maximo para el envio/recepcion
          de paquetes.
    '''
    if(self.Send(msg,timeout,encoding) == -1):
      return ''
    # end if
    
    return self.Receive(timeout,encoding)      
  # end def  
  
#end class


class Client(Stream):
  ''' Client Stream Socket
      kwarg :
        - ip   : ip del host remoto, opcional por defecto localohost 127.0.0.1
        - port : puerto, por defecto 8080
        - fmt_len : formato para el set/get la longitud en el header del 
        mensaje, por defecto 4 bytes.
  '''
  
  ''' Clase para modelar la conexion al host '''
  def __init__(self,**kwarg):
    ''' Inicializacion de una instancia del tipo Client
        kwarg :
        - ip   : ip del host remoto, opcional por defecto localohost 127.0.0.1
        - port : puerto, por defecto 8080
        - fmt_len : formato para el set/get la longitud en el header del 
        mensaje, por defecto 4 bytes.
    '''
    super().__init__(**kwarg)
  # end def

  def Connect(self)->bool:
    ''' Metodo para conexion al host remoto
        - return 
          + True connect success
          + False connect failure
    '''
    #super(Stream,self)._fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ret = super()._fd.connect_ex((self._ip,self._port))
    self._fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ret = self._fd.connect_ex((self._ip,self._port))
    if(ret != 0):
      self.last_error = strerror(ret)
      self._st = Status.ERROR
      return False
    # end if
    self._st = Status.CONNECT
    return True
  # end def

  def Disconnect(self)->bool:
    ''' Metodo para la desconexion al host remoto 
        - return 
          + True connect success
          + False connect failure
    '''
    if(self._st == Status.CONNECT):
      self._fd.close()
      self._st = Status.DISCONNECT
    #end if
    return True
  # end def

  def __enter__(self):
    ''' for with context '''
    #print(f'{type(self)}.__enter__()')    
    return self
  
  def __exit__(self, *args):
    ''' for exit with context '''
    #print(f'{type(self)}.__exit__()')
    self.Disconnect()

  def __repr__(self) -> str:
    '''representacion formal del objeto mediante un string'''
    return f'{type(self).__name__}(ip={self._ip},port={self._port},fmt_len={self._fmt_len})'
  # end def
# end class


class Server(Stream):
  ''' Server Stream Socket
      kwarg :
        - ip   : ip para el Local Server, opcional por defecto localohost 127.0.0.1
        - port : puerto, por defecto 8080
        - fmt_len : formato para el set/get la longitud en el header del 
        mensaje, por defecto 4 bytes.
  '''
  
  ''' Clase para modelar la conexion al host '''
  def __init__(self,**kwarg):
    ''' Inicializacion de una instancia del tipo Server Stream Socket
        kwarg :
        - ip   : ip para el Local Server, opcional por defecto localohost 127.0.0.1
        - port : puerto, por defecto 8080
        - fmt_len : formato para el set/get la longitud en el header del 
        mensaje, por defecto 4 bytes.
    '''
    #self._fdsrv:socket.socket = None
    self._fdsrv = None

    super().__init__(**kwarg)
  # end def

  def Connect(self)->bool:
    ''' Metodo para conexion al host remoto
        - return 
          + True connect success
          + False connect failure
    '''    
    self._fdsrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._fdsrv.bind((self._ip,self._port))
    self._fdsrv.listen()
    self._st = Status.CONNECT
    return True
  # end def

  def Disconnect(self)->bool:
    ''' Metodo para la desconexion al host remoto 
        - return 
          + True connect success
          + False connect failure
    '''
    if(self._st != Status.CONNECT):
      return False
    if(self._fd):
      self._fd.close()
    #end if
    if(self._fdsrv):
      self._fdsrv.close()
    #end if
    
    self._st = Status.DISCONNECT    
    return True
  # end def

  def Accept(self)->str:
    ''' Metodo para Admitir conexion desde un cliente
        retunr el client address          
    '''
    self._fd, cliaddr = self._fdsrv.accept()
    return f'{cliaddr}'


  def __enter__(self):
    ''' for with context '''    
    return self
  
  def __exit__(self, *args):
    ''' for exit with context '''    
    self.Disconnect()

  def __repr__(self) -> str:
    '''representacion formal del objeto mediante un string'''
    return f'{type(self).__name__}(ip={self._ip},port={self._port},fmt_len={self._fmt_len})'
  # end def
# end class
