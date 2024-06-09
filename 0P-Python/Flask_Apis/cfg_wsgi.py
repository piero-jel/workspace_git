#!/usr/bin/python3
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

\b file cfg_wsgi.py
\b brief Script con la configuracion por defecto de la insterfaces Wsgi, para deploy
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Domingo 19 de Mayo de 2024.
\b version 0.3.8.
\b Change History:
Author         Date                 Version     Brief
JEL            2024.04.19           0.3.8       Version Inicial no release

"""
import os

''' En caso que no se localicen las variables de entorno establece los valores 
    por defecto.
'''
## Nro de procesos 
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
## numero de thread 
threads = int(os.environ.get('GUNICORN_THREADS', '4'))

## timeout 'seconds', previo al close de conexion
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

## enlace de la aplicacion
# os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')
bind_ip   = os.environ.get('GUNICORN_APP_IP', '0.0.0.0')
bind_port = os.environ.get('GUNICORN_APP_PORT', '8080')
bind      = f'{bind_ip}:{bind_port}'


forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }

''' cfg_wsgi.py
  gunicorn --config cfg_wsgi.py main:app
                                       ~~~~ ~~~
                                         |   |
                                         |   +-> 
                                         |
                                         +-> Python Script containing the Root Flask Application
                                         
ENV GUNICORN_PROCESSES=2
ENV GUNICORN_THREADS=4
ENV GUNICORN_TIMEOUT=120
ENV GUNICORN_BIND='0.0.0.0:8080'
CMD ["gunicorn","--config", "cfg_wsgi.py", "main:app"]                                         
'''
