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

\b file RequestSequential.py
\b brief secuential request
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
from constants import URLS


def download_data(urls:list | tuple) -> list:
    ''' Funcion para obtener los response relacionada a la peticion GET para 
        cada url/endpoint contenido dentro de las lista de urls.
          - urls : lista o tupla de url 
        
        Return el listado de response json de cada request para el cual el 
        code status es 200 (respuesta ok)
    '''
    if not isinstance(urls,list) and not isinstance(urls,tuple):
        raise TypeError(f'urls type <{type(urls)} no soportado>')

    data:list = []
    for url in urls:
        # En este caso podemos tomar la opcion de reportar el mensaje, para
        # no cancelar todas las peticiones, o lanzar la excepcion
        if not isinstance(url,str):
            raise TypeError(f'url type <{type(url)} no soportado, debe ser string>')

        try:
            response = requests.get(url,timeout=5)
            if response.status_code == 200:
                data.append(response.json())
            else:
                print(f'Error: {response.status_code}')

        except requests.exceptions.RequestException as e:
            print(f'Exception: {e}')


    return data



def main():
    ''' implementacion '''
    try:
        data = download_data(URLS)
        print(data)
        print("\n\n")
        for i,it in enumerate(data):
            print(f'[{i}]: {it}')

    except Exception as e: # pylint: disable=broad-exception-caught
        print(f'Exception <{type(e).__name__}>: {e}')



if __name__ == '__main__':
    main()
