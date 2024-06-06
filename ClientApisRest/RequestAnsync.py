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

\b file Propuesta_02.py
\b brief request asyncio con aiohttp, ejecuccion recurrente
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Lunes 20 de Mayo de 2024.
\b version 0.0.1.
\b pre install python packages
  python3 -m pip install aiohttp 
  
\b Change History:

Author         Date                 Version     Brief
JEL            2024.04.20           0.0.1       Version Inicial no release

"""
import aiohttp
import asyncio

from collections import namedtuple  

''' Definimos una namedtuple para majear response como estructuras 
    mediante la tupla:
      + url          str 
      + status_code  int
      + resp         JSON
'''
Response = namedtuple('Response', ['url','status_code', 'resp'])


async def session_fetch_data(session,url: str):
  ''' Function asynchronously Session fetches data from a given URL.
      and session created.

      - session : la cual debe utilizar para ejecutar el get
      - url     : string con la url sobre la cual realizara la peticion
  '''    
  try:    
    async with session.get(url) as response:      
      return Response(url,response.status, await response.json())
    # end async with
  except aiohttp.client_exceptions.ClientConnectorError as e: 
    return Response(url,-1, f'ClientConnectorError: {e}')
  except Exception as e:
    return Response(url,-1, f'Exception {type(e)} {e}')
  # end try    
# async def


async def api_request(urls:list|tuple,timeout:int=60):
  ''' Function asynchronously la cual se encarga de armar las tareas asincronicas
      a ejecutarse, con el timeout requerido y crear la session para la ejecucion 
      del get request

      - urls    : lista o tuple de urls 
      - timeout : opcional, tiempo de demora maximo por cada request a ejecutarse por session.
      
  '''
  ret:list = []  
  async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
    tasks = [asyncio.ensure_future(session_fetch_data(session, url)) for url in urls]
    ''' def asyncio.gather(*tasks)
        Return a future aggregating results from the given coroutines/futures.
        Coroutines will be wrapped in a future and scheduled in the event loop. 
        They will not necessarily be scheduled in the same order as passed in.

        All futures must share the same event loop. If all the tasks are done successfully,
        the returned future's result is the list of results (in the order of the original sequence,
        not necessarily the order of results arrival).
    '''
    responses = await asyncio.gather(*tasks)
    ret = responses      
  # end async with
  return ret
# async def


def download_data(urls:list|tuple,timeout=5)-> list:
  ''' Funcion de implementacion, punto de partida
      - urls : tuple o list con las urls
      - timeout : opcional para establecer el tiempo de demora maximo 
        por cada reques por url
  '''
  # creamos el loop para la espera del package de request para las urls

  ''' deprecate in new versions 
  loop = asyncio.get_event_loop()
  resp = loop.run_until_complete(api_request(urls,timeout=timeout))   
  '''

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  resp:list = []
  try:
    resp = loop.run_until_complete(api_request(urls,timeout=timeout))
  except KeyboardInterrupt:
    print('Peticion de cancelacion por Usuario (Ctrl+C)')    
  # end try

  ret:list = []
  for it in resp:
    '''
        Family error code for response
        + 1xx informational response : the request was received, continuing process
        + 2xx successful : the request was successfully received, understood, and accepted
        + 3xx redirection : further action needs to be taken in order to complete the request
        + 4xx client error : the request contains bad syntax or cannot be fulfilled
        + 5xx server error : the server failed to fulfil an apparently valid request
    '''
    if(it.status_code == -1 ):
      # para errores no tabulados de las familia 1xx|2xx|3xx|4xx|5xx
      print(f'Error <{it.url}>  Message <{it.resp}>')
      continue
    # end if
    if(it.status_code != 200 and it.status_code != -1 ):
      print(f'Error: url <{it.url}>  code<{it.status_code}>')
      continue
    # end if
    ret.append(it.resp)
  # end for
  return ret
# end def


''' implementacion '''
if __name__ == '__main__':
  url_base:str = 'https://jsonplaceholder.typicode.com/posts/{}'
  urls:list = [url_base.format(post) for post in range(1, 100)]
  urls.append('https://not-found-url/1')
  urls.append('http://not-found-url/2')
  
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
# end fi


