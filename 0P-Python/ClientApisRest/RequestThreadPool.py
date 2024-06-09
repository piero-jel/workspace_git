#!/bin/python3
"""@package docstring
Copyright 2024, Jesus Emanuel Luccioni
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

\b file RequestThreadPool.py
\b brief muti-theading request, uso de ThreadPool para ejecuccion recurrente
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Lunes 20 de Mayo de 2024.
\b version 0.0.1.
\b pre install python packages
  python3 -m pip install requests 
  
\b Change History:
Author         Date                 Version     Brief
JEL            2024.04.20           0.0.1       Version Inicial no release

"""
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import namedtuple  

''' Definimos una namedtuple para majear response como estructuras 
    mediante la tupla:
      + url          str 
      + status_code  int
      + resp         JSON
'''
Response = namedtuple('Response', ['url','status_code', 'resp'])

def vTask(url:str,timeout:int=60) :
  ''' Prototipo de tarea para ser ejecutada en un thread. Esta se encarga 
      de la peticion GET para un url/endpoint 
        - url : url/endpoint donde se realizar la peticion

      Return un Response relacionado al request para el cual el 
      code status es 200 (respuesta ok), y -1 con mensaje string
  '''
  if(not isinstance(url,str)):
    raise TypeError(f'urls type <{type(urls)} no string>')
  # end if

  if(not isinstance(timeout,int)):
    raise TypeError(f'timeout type <{type(timeout)} no int>')
  # end if  
  try:
    response = requests.get(url,timeout=5)
    return Response(url,response.status_code,response.json())    
  except requests.exceptions.RequestException as e:
    return Response(url,-1,f'Exception: {e}')
  # end try    
  return None
# end def


def download_data(urls:list | tuple) -> list:
  ''' Funcion para obtener los response relacionada a la peticion GET para 
      cada url/endpoint contenido dentro de las lista de urls.
        - urls : lista o tupla de url 
      
      Return el listado de response json de cada request para el cual el 
      code status es 200 (respuesta ok)
  '''
  if(not isinstance(urls,list) and not isinstance(urls,tuple)):
    raise TypeError(f'urls type <{type(urls)} no soportado>')
  # end if

  data = []
  with ThreadPoolExecutor(max_workers=len(urls)) as executor:
    futures = []
    for url in urls:        
      futures.append(executor.submit(vTask, url=url, timeout=5))
    # end for
    # waiting for the threads to finish and maybe print a result :
    for future in as_completed(futures):      
      if(future.result().status_code == 200):
        data.append(future.result().resp)
      elif(future.result().status_code == -1):
        print(f'Error: url <{future.result().url}> Message {future.result().resp}')  
      else:
        print(f'Error: url <{future.result().url}> Code {future.result().status_code}')  
      # end if      
    # end for
  return data
# end def

''' implementacion '''
if __name__ == '__main__':
  try:
    url_base:str = 'https://jsonplaceholder.typicode.com/posts/{}'
    urls:list = [url_base.format(post) for post in range(1, 100)]
    urls.append('https://not-found-url/1')
    urls.append('http://not-found-url/2')
    urls.append('https://api.coindesk.com/v1/bpi/currentprice.json')
    #urls.append(float(1))
    '''
    urls =  ( "https://httpbin.org/ip"
            , "https://httpbin.org/get"
            , "https://httpbin.org/user-agent"
            , "https://jsonplaceholder.typicode.com/posts'"
            , 'http://0.0.0.0:5000/countries'
            )
    '''

    data = download_data(urls)
    
    # print(data)
    print("\n\n")    
    for i,it in enumerate(data):
      print(f'[{i}]: {it}')
    # end for
  except Exception as e:
    print(f'Exception {type(e)}: {e}')
  # end try
# end fi
