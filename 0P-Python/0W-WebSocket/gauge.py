'''
WebSocket Server, update values, only send data .
# venv
python3 gauge.py

# sin venv
activate.sh --run gauge.py
'''
from typing import Callable,TypeAlias,Iterable
from abc import ABC, abstractmethod
import os
from random import randrange
from websockets.sync.server import ServerConnection,serve
#from websockets.sync.server import serve
#from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK,ConnectionClosedError
#import asyncio
from time import sleep
from json import dumps as json_dumps
from subprocess import check_output
#import http.server
#import socketserver
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import functools
from multiprocessing import Process
from logging import Logger,getLogger,basicConfig,DEBUG

Callback:TypeAlias = Callable[[None],str|bytes|Iterable]


LOGGING:dict = {
    'level' : DEBUG,
    'filename' : 'logs/servers_gauge.log',
    'format'   : '%(asctime)s %(levelname)-5s: %(message)s'
}

log_dir:str = os.path.dirname(LOGGING['filename'])
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

basicConfig(**LOGGING)
log:Logger = getLogger('servers_gauges')



class MultiProcess(ABC):
    """Clase para ejecutar una tarea baremetal sobre un proceso """
    process:Process = None

    def run(self):
        """Metodo que se encarga de armar los process para luego iniciarlos"""
        log.debug(f"{type(self).__name__}::run() begin")
        self.process = Process(target=self.task,)
        self.process.start()        
        log.debug(f"{type(self).__name__}::run() end") 
    
    def join(self):
        """ metodo para atacharnos al proceso, para evitar que el proeceso principal termine antes
        que este """
        log.debug(f"{type(self).__name__}::join()")
        self.process.join()
        
    def terminate(self):
        """ metodo para finalizar el proceso """
        log.debug(f"{type(self).__name__}::terminate()")
        self.process.terminate()

    @abstractmethod
    def task(self)->None:
        """metodo abstracto que ejecuta la tarea sobre un nuevo proceso"""


class ServerWebSocket(MultiProcess):
    """Server WebSocket con multiprocess """
    CONSTANTS_JS:str = 'constants.js'

    def __init__(self,url:str,port:int,callback:Callback=None,folder:str = None):
        """
        Server WebSocket con multiprocess

        :param url: direccion donde se establecera la url. Si esta es None trata de establecer la
         primer direccion del hostname.
        :type url: str

        :param port: numero de puerto para el servicio
        :type port: int

        :param callback: funcion que se invocara para obtener los datos y enviar al cliente. 
        Sginature `def fn()->str:`
        :type callback: Callback  

        :param folder: Opcional, directorio donde dejara el `CONSTANTS_JS` con la informacion de
        conexion al serivdor 
        :type folder: str      
        """
        self.url:str = url
        self.port:int = port
        self.callback:Callback = callback
        self.count:int = 0

        if self.url is None:
            self.url = type(self).hostname()

        if folder is not None:
            self.dump_constants(folder,True)

    @classmethod
    def hostname(cls)->str:
        """
        Metodo de clase que nos permite obtener el host address

        :return: return el host addres, el primero si es un listado
        :rtype: str
        """
        try:
            cmd = check_output(['hostname','-I']).decode('utf-8')
            return cmd.split()[0]
        except Exception as e:
            log.error(f'{cls.__name__}::hostname() Exception<{e.__name__}>. Detail {e}')

        return '127.0.0.1'

    def __get(self):
        self.count += 1
        if self.callback:
            return self.callback()
        return f'{self.count} null'

    def __handler(self,websocket:ServerConnection):
        log.debug(f'{type(self).__name__}::task() Begin')
        while True:
            message:str = self.__get()            
            try:
                websocket.send(message)
                websocket.recv()

            except ConnectionClosedOK as e:
                log.info(f'\nPeticion de cierrer, {e}')
                break

            except ConnectionClosedError as e:
                # intenta enviar un frame y la conexion esta cerrada
                log.info(f'\nCierre inesperado del lado del cliente, detail {e}')
                break

            except Exception as e:
                log.info(f'\nException<{type(e).__name__}, detail: {e}')
                break
            
        log.debug(f'{type(self).__name__}::task() End')
    
    def task(self):
        with serve(self.__handler, self.url,self.port) as server:
            server.serve_forever()

    def dump_constants(self,folder:str,overwrite:bool=False)->bool:
        """ """
        pathname:str = f'{folder}/{type(self).CONSTANTS_JS}'
        if os.path.exists(pathname) and not overwrite:
            return True

        content:list[str] = [
            f'const URL  = "ws://{self.url}";',
            f'const PORT = {self.port};',
            'export { URL, PORT };',
        ]        
        # Abre el archivo en modo escritura
        with open(pathname, "w", encoding="utf-8") as f2w:
            for line in content:
                f2w.write(line+'\n')
        
        return True

class HttpServer(MultiProcess):
    """Http Server para el frontend, con multiprocess """
    def __init__(self,url:str = None,port:int=8000,folder:str=None):
        """
        Http Server para el frontend, con multiprocess

        :param url: direccion donde se establecera la url. Si esta es None se toma el localhost.
        :type url: str

        :param port: numero de puerto para el servicio
        :type port: int

        :param folder: Opcional, directorio donde tomara los archivos para el servicer http. Por 
        defecto toma el root de ejecucion.
        :type folder: str
        """
        self.url:str = "" if url is None else url
        self.port:int=port
        self.folder:str = folder
        self.handler_cls = SimpleHTTPRequestHandler
        if folder is not None:
            self.handler = functools.partial(
                SimpleHTTPRequestHandler, 
                directory=self.exists_folder()
            )

        log.debug(f"{type(self).__name__} folder<{self.folder}> | http://{self.url}:{self.port}")

    def exists_folder(self)->str:
        """ metodo que verifica si existe el direcotio """
        if not os.path.exists(self.folder):
            raise ValueError(f"{type(self).__name__}::exits_folder() Path <{self.folder}> not found")
        
        return self.folder
        
    def task(self):
        log.debug(f"{type(self).__name__}::task() http://{self.url}:{self.port}")
        with TCPServer((self.url, self.port), self.handler) as httpd:
            #print(f"Http Server '{path_to_serve}' en http://localhost:{port}")
            log.debug(f"Http Server en http://localhost:{self.port}")
            httpd.serve_forever()




def get_value()->str:
    """ 
    Funcion que se encargara de generar los valores para el cliente WebSocket

    :return: valores en formato string json
    :rtype: str
    """
    colors:list[str] = ['#005578',"#22D125","#DACD11","#D20D0D"]
    sleep(1)
    message:str = json_dumps([ [col,float(f"{randrange(1,1000)*0.1:4.2f}")] for col in colors])
    print(f'\rMessage: {message:>96s}',end='')
    return message


def main():    
    #host:str = 'localhost'
    host:str = ServerWebSocket.hostname()
    port:int = 8080
    http_serve_path:str = 'http_server_gauge' 
    http_serve_port:int = 8000

    servers:list[MultiProcess] = [
        ServerWebSocket(host,port,get_value,http_serve_path),
        HttpServer("",http_serve_port,http_serve_path)
    ]    
    try:   
        for server in servers:
            server.run()

        ## print informacion
        print(f"Http Server '{http_serve_path}' en http://{host}:{http_serve_port}")
        print(f"SocketWeb Server  en ws://{host}:{port}")

        # nos atachamos al servicio del http server
        for server in servers:
            server.join()

    except Exception as e:
        print(f'Exception<{type(e).__name__}, detail: {e}')

    except OSError as e:
        print(f'Error con los Recursos del Sistema, detail: {e}')

    except KeyboardInterrupt:
        for server in servers:
            if server:
                server.terminate()

        print("\nServicios Finalizado.")



# verificamos si este script es el principal invocado desde la linea de comandos
if __name__ == "__main__":
    main()