'''
WebSocket Server, update values, only send data .
# venv
python3 gauge.py

# sin venv
activate.sh --run gauge.py
'''
import os
from typing import Callable,TypeAlias,Iterable
from abc import ABC, abstractmethod
from logging import Logger,getLogger,basicConfig,DEBUG
from random import randrange
from time import sleep
from json import dumps as json_dumps
from subprocess import check_output
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer#,BaseRequestHandler
import functools
from multiprocessing import Process
from websockets.sync.server import ServerConnection,serve
from websockets.exceptions import ConnectionClosedOK,ConnectionClosedError

Callback:TypeAlias = Callable[[None],str|bytes|Iterable]


LOGGING:dict = {
    'level' : DEBUG,
    'filename' : 'logs/servers_gauge.log',
    'format'   : '%(asctime)s %(levelname)-5s: %(message)s'
}

class MultiProcess(ABC):
    """Clase para ejecutar una tarea baremetal sobre un proceso """    
    process:Process = None
    log:Logger = None
    
    def run(self):
        """Metodo que se encarga de armar los process para luego iniciarlos"""
        self.log.debug("%s::run() begin",type(self).__name__)
        self.process = Process(target=self.task,)
        self.process.start()
        self.log.debug("%s::run() end",type(self).__name__)
    
    def join(self):
        """ metodo para atacharnos al proceso, para evitar que el proeceso principal termine antes
        que este """
        self.log.debug("%s::join()",type(self).__name__)
        self.process.join()
        
    def terminate(self):
        """ metodo para finalizar el proceso """
        self.log.debug("%s::terminate()",type(self).__name__)
        self.process.terminate()

    @abstractmethod
    def task(self)->None:
        """metodo abstracto que ejecuta la tarea sobre un nuevo proceso"""

    def get_logger(self)->Logger:
        dir_name:str = os.path.dirname(LOGGING['filename'])
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        params:dict = {
            'level': LOGGING['level'],
            'format' : LOGGING['format'],
            'filename': f'{dir_name}/{type(self).__name__}.log'
        }
        #print(f'{type(self).__name__}::get_logger() params: {params}',flush=True)
        #log:Logger = getLogger(type(self).__name__)
        #log.debug('%s::get_logger() params: %s',type(self).__name__,params)
        #return log
        basicConfig(**params)
        return getLogger(type(self).__name__)


class ServerWebSocket(MultiProcess):
    """Server WebSocket con multiprocess """
    CONSTANTS_JS:str = 'constants.js'

    def __init__(self,url:str,port:int,log:Logger,callback:Callback=None,folder:str = None):
        """
        Server WebSocket con multiprocess

        :param url: direccion donde se establecera la url. Si esta es None trata de establecer la
         primer direccion del hostname.
        :type url: str

        :param port: numero de puerto para el servicio
        :type port: int

        :param log: logger 
        :type log: Logger

        :param callback: funcion que se invocara para obtener los datos y enviar al cliente. 
        Sginature `def fn()->str:`
        :type callback: Callback  

        :param folder: Opcional, directorio donde dejara el `CONSTANTS_JS` con la informacion de
        conexion al serivdor 
        :type folder: str      
        """
        self.log:Logger = log
        self.url:str = url
        self.port:int = port
        self.callback:Callback = callback

        if self.url is None:
            self.url = self.hostname()

        if folder is not None:
            self.dump_constants(folder,True)
    
    def hostname(self)->str:
        """
        Metodo de clase que nos permite obtener el host address

        :return: return el host addres, el primero si es un listado
        :rtype: str
        """
        try:
            cmd = check_output(['hostname','-I']).decode('utf-8')
            return cmd.split()[0]
        except Exception as e:
            self.log.error(f'{type(self).__name__}::hostname() Exception<{e.__name__}>. Detail {e}')

        return '127.0.0.1'

    def __get(self):
        if self.callback:
            return self.callback()
        return 'null'

    def __handler(self,websocket:ServerConnection):
        self.log.debug(f'{type(self).__name__} handler Begin')
        while True:
            message:str = self.__get()
            self.log.debug("%s message to send <%s>",type(self).__name__,message)
            try:
                websocket.send(message)
                message=websocket.recv()
                self.log.debug("%s ack received <%s>",type(self).__name__,message)

            except ConnectionClosedOK as e:
                self.log.info(f'\nPeticion de cierrer, {e}')
                break

            except ConnectionClosedError as e:
                # intenta enviar un frame y la conexion esta cerrada
                self.log.info('%s Cierre inesperado del lado del cliente, detail %s',
                              type(self).__name__,e)
                break

            except Exception as e:
                self.log.info('%s Exception<%s, detail: %s',type(self).__name__,type(e).__name__,e)
                break

        self.log.debug('%s handler end',type(self).__name__)
        
    
    def task(self):        
        self.log = self.get_logger()
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
    
    def __str__(self)->str:
        url:str = '127.0.0.1' if self.url == '' else self.url
        return f"{type(self).__name__} ws://{url}:{self.port}"


class HandlerHttpServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Extraemos nuestro logger de los argumentos que envía partial        
        self.logger:Logger = kwargs.pop('logger', getLogger("default"))
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        # 3. Redirigimos el log automático de HTTP a nuestra instancia de logger
        self.logger.info("%s - %s" % (self.address_string(), format % args))

class HttpServer(MultiProcess):
    """Http Server para el frontend, con multiprocess """    

    def __init__(self,url:str,port:int,log:Logger=None,folder:str=None):
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
        self.log:Logger = log
        self.url:str = "" if url is None else url
        self.port:int = 8000 if port is None else port
        self.folder:str = folder
        self.handler_cls = SimpleHTTPRequestHandler
        if folder is not None:
            #HandlerHttpServer.directory_to_serve = self.exists_folder()
            #HandlerHttpServer.logger = self.get_logger()
            #self.handler = HandlerHttpServer
            self.handler = functools.partial(
                #SimpleHTTPRequestHandler, 
                HandlerHttpServer,
                logger = self.get_logger(),
                directory=self.exists_folder(),
            )

        self.log.debug("%s folder<%s> | http://%s:%d",
                       type(self).__name__,self.folder,self.url,self.port)

    def exists_folder(self)->str:
        """ metodo que verifica si existe el direcotio """
        if not os.path.exists(self.folder):
            raise ValueError(f"{type(self).__name__}::exits_folder() Path<{self.folder}> not found")
        
        return self.folder
        
    def task(self):        
        self.log = self.get_logger()

        self.log.debug("%s::task() http://%s:%d",type(self).__name__,self.url,self.port)
        with TCPServer((self.url, self.port), self.handler) as httpd:
            #self.log.debug(f"Http Server '{path_to_serve}' en http://localhost:{port}")
            self.log.debug("Http Server en http://localhost:%s",self.port)
            httpd.serve_forever()

    def __str__(self)->str:
        url:str = '127.0.0.1' if self.url == '' else self.url
        return f"{type(self).__name__} folder={self.folder}, http://{url}:{self.port}"


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
    log_dir:str = os.path.dirname(LOGGING['filename'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    basicConfig(**LOGGING)
    log:Logger = getLogger('servers_gauges')

    host:str = None
    port:int = 8080
    http_serve_path:str = 'http_server_gauge' 
    http_serve_port:int = 8000

    servers:list[MultiProcess] = [
        ServerWebSocket(host,port,log,get_value,http_serve_path),
        HttpServer("",http_serve_port,log,http_serve_path)
    ]    
    try:
        # LAnzamos cada uno de los servicios
        for server in servers:
            server.run()
            ## print informacion
            print(f"Sevicio: '{server}'")

        # nos atachamos a los servicio, a la espera por que todos finalicen
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
