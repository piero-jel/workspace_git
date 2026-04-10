'''
WebSocket Server, update values, only send data .
# venv
python3 gauge.py

# sin venv
activate.sh --run gauge.py
'''
import os
from random import randrange
from websockets.sync.server import ServerConnection
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK,ConnectionClosedError
import asyncio
from typing import Callable,TypeAlias,Iterable
from time import sleep
from json import dumps as json_dumps
from subprocess import check_output
import http.server
import socketserver
import functools
from multiprocessing import Process

Callback:TypeAlias = Callable[[None],str|bytes|Iterable]

class ServerWebSocket:
    def __init__(self,url:str,port:int,callback:Callback=None):
        self.url:str = url
        self.port:int = port
        self.callback:Callback = callback
        self.count:int = 0

        if self.url is None:
            self.url = type(self).hostname()

    @classmethod
    def hostname(cls)->str:
        try:
            cmd = check_output(['hostname','-I']).decode('utf-8')
            return cmd.split()[0]
        except Exception as e:
            print(f'{cls.__name__}::hostname() Exception<{e.__name__}>. Detail {e}')

        return '127.0.0.1'

    async def get(self):
        self.count += 1
        if self.callback:
            return self.callback()
        return f'{self.count} null'

    async def handler(self,websocket:ServerConnection):
        print(f'{type(self).__name__}::task() Begin')
        while True:
            message:str = await self.get()
            print(f'\rMessage: {message:>96s}',end='')
            try:
                await websocket.send(message)
                await websocket.recv()

            except ConnectionClosedOK as e:
                print(f'\nPeticion de cierrer, {e}')
                break

            except ConnectionClosedError as e:
                # intenta enviar un frame y la conexion esta cerrada
                print(f'\nCierre inesperado del lado del cliente, detail {e}')
                break

            except Exception as e:
                print(f'\nException<{type(e).__name__}, detail: {e}')
                break
            
        print(f'{type(self).__name__}::task() End')
    
    async def __create(self):
        async with serve(self.handler, self.url,self.port) as server:
            await server.serve_forever()
    
    def run(self):
        print(f'{type(self).__name__}::run() ws://{self.url}:{self.port}')
        asyncio.run(self.__create())


def get_value()->int:            
    colors:list[str] = ['#005578',"#22D125","#DACD11","#D20D0D"]
    #sleep(0.001) # wait 1mS
    #sleep(0.500) # wait 1mS
    sleep(1)            
    return json_dumps([ [col,float(f"{randrange(1,1000)*0.1:4.2f}")] for col in colors])



def http_server(path_to_serve:str,port=8000):
    """ Idem to run
        python3 -m http.server -d ${path_to_serve}
    """
    if not os.path.exists(path_to_serve):
        raise ValueError(f"path_to_serve {path_to_serve} not found")
    
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, 
        directory=path_to_serve
    )
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Http Server '{path_to_serve}' en http://localhost:{port}")
        httpd.serve_forever()



def main():    
    #host:str = 'localhost'
    host:str = None#'192.168.0.182'
    port:int = 8080
    http_serve_path:str = 'http_server_gauge' 
    http_serve_port:int = 8000

    try:
        p = Process(target=http_server, args=(http_serve_path,http_serve_port))
        p.start()

        ServerWebSocket(host,port,get_value).run()
        p.join()

    except Exception as e:
        print(f'Exception<{type(e).__name__}, detail: {e}')

    except KeyboardInterrupt:
        p.terminate()
        print("\nServidor finalizado.")

# verificamos si este script es el principal invocado desde la linea de comandos
if __name__ == "__main__":
    main()