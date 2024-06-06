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

\b file Config.py
\b brief Modulo con la configuracion de la aplicacion
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Domingo 19 de Mayo de 2024.
\b version 0.3.8.
\b Change History:
Author         Date                 Version     Brief
JEL            2024.04.19           0.3.8       Version Inicial no release
JEL            2024.04.26           0.4.4       edit Config, quit edit set_logger() not currently in use
JEL            2024.04.26           0.4.5       change logging for native compatibility, setting dictConfig

"""
from flask import Flask
from flask_login import LoginManager
from logging.config import dictConfig


''' Definims dos hanlder consolo para debug y file 
    Para deploy solo debemos dejar uno en la lista 'handlers': ['file']

dictConfig({
    'version': 1,
    'formatters': {
      'default': {
        'format': '%(asctime)s.%(msecs)03d [%(levelname)-9s] %(module)s: %(message)s',
        "datefmt": "%Y/%m/%dT%H:%M:%S",
      }
    },
    'handlers': {
      "console": {
        "class": "logging.StreamHandler",
        "stream": "ext://sys.stdout",
        "formatter": "default",
      },
      "file": {
        "class": "logging.FileHandler",
        "filename": "logs/app.log",
        "formatter": "default",
      }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console','file']
    }
})    
'''
dictConfig({
    'version': 1,
    'formatters': {
      'default': {
        'format': '%(asctime)s.%(msecs)03d [%(levelname)-9s] %(module)s:%(lineno)d <%(message)s>',
        "datefmt": "%Y/%m/%dT%H:%M:%S",
      }
    },
    'handlers': {
      "file": {
        "class": "logging.FileHandler",
        "filename": "logs/Flask_Apis.log",
        "formatter": "default",
      }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})


'''
import logging

# Loggin configuration 
LOGIN_CFG:dict = {
    "level": logging.DEBUG
  , "filename":f'{Path(__file__).resolve().parent.parent}/logs/app.log'
  , "filemode":'w'
  , "format":'%(asctime)s : %(message)s'
}
logging.basicConfig ( **LOGIN_CFG )
'''

# Create a flask application
app = Flask(__name__)
 
# Establecemos que tipo de BBDD usara  flask-sqlalchemy, como se conectara
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# Enter a secret key, clave para los ciphers
app.config["SECRET_KEY"] = "12345"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# seting format compact in json response
app.config['RESTPLUS_JSON'] = {'indent':None, 'separators':(',',':')}
## FIXME setting version number
app.config['VERSION'] = '0.4.5'
app.config['TOKEN_USE'] = True
app.config['TOKEN_TIME'] = 1800





# LoginManager is needed for our application 
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)




