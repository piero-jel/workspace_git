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

\b file Models.py
\b brief Modulo con los modelos ORM de las tablas del proyecto
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Domingo 19 de Mayo de 2024.
\b version 0.3.8.
\b Change History:
Author         Date                 Version     Brief
JEL            2024.04.19           0.3.8       Version Inicial no release
JEL            2024.04.22           0.4.1       edit Users add instance method response_login()
JEL            2024.04.22           0.4.2       edit Comicios edit instance method get_response(), 'encapsule response body with jsonfy()'
JEL            2024.04.26           0.4.3       edit Models Comicios, edit instance method calcular_escanios() Performance

"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash 
import jwt
import time
import hashlib
import json

from datetime import datetime  
from Config.Config import app

## cambiar para postgress from sqlalchemy.dialects.postgresql import JSON
#from sqlalchemy.dialects.sqlite import JSON,TIMESTAMP
from flask import jsonify

from operator import itemgetter # add for version 0.4.3
from itertools import groupby   # add for version 0.4.3

# Initialize flask-sqlalchemy extension
auth = HTTPBasicAuth()
db = SQLAlchemy()



# Create user model
class Users(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(250),unique=True,nullable=False,index = True)
  password = db.Column(db.String(250),nullable=False)

  def __init__(self,username:str,password:str):
    ''' Metodo/protocolo para el init de una Instancia
          - username : Nombre de usuario
          - password : clave para el usuario, se almacena cifrada.
    '''
    self.username = username
    self.password = generate_password_hash(password)
  # end def

  def hash_password(self, password):
    ''' Metodo p/generar el hash password para ser alamacenado de forma segura
          - password : con la que el usuari se loguea
    '''
    self.password = generate_password_hash(password)
  # end def

  def verify_password(self, password):
    ''' Metodo para verificacion del pass
          - password : con la que el usuari se loguea
    '''
    return check_password_hash(self.password, password)
  # end def

  def generate_auth_token(self, expires_in = 1800) -> str:
    ''' Metodo de instancia para generar un token relacionado a un usuario
          - expires_in : timeout , tiempo de vida util del token a generar
          Valor por defecto '1800'
    '''
    ret = jwt.encode( { 'id': self.id
                       , 'exp': time.time() + expires_in 
                       }
                      , app.config['SECRET_KEY'], algorithm='HS256'
                    )
    if(isinstance(ret,str)):
      return ret
    return ret.decode('ascii')  
  # end def

  def response_login(self,timeout=app.config.get('TOKEN_TIME',1800)):
    ''' Metodo de instancia que generar un token relacionado al usuario
        y arma la respuesta para el request de login
          - expires_in : timeout , tiempo de vida util del token a generar
          Valor por defecto '1800'
    '''
    token = self.generate_auth_token(timeout)
    return jsonify({ 'username': self.username
                    , 'access_token': token
                    , 'timeout': timeout
                  })
  # end def

    
  @staticmethod
  def verify_username_password(ctxg,username, password)-> bool:
    ''' Metodo estatico para verificar usuario mediane username y password 
          - ctxg : contexto global donde actualizaremos el 'user'
          - username : usario 
          - password : password del usuario    
    ''' 
    try:
      user = Users.query.filter_by(username = username).first()
    except Exception as e:
      app.logger.debug(f'Exception {type(e)}: {e}')
    #end try
    if (not user or not user.verify_password(password)):
      return False
    # end if  
    ## save user in global contex 
    ctxg.user = user
    return True
  # end def

  @staticmethod
  def verify_password_with_token(ctxg,username_or_token, password)-> bool:
    ''' 
      - ctxg: contexto global done actualizaremos el valor de usuario
      - username_or_token : user name o toek
      - password : en caso de username necesitamos la clave
    '''
    data = None
    try:
      data = jwt.decode ( username_or_token
                        , app.config['SECRET_KEY']
                        , algorithms=['HS256'])
    except jwt.exceptions.DecodeError as e:
      ''' En caso de validar un nombre de usaurio caemos en esta
          excepccion
      '''      
      app.logger.debug(f'jwt.exceptions.DecodeError: {e}')
    except Exception as e:      
      app.logger.debug(f'Exception {type(e)}: {e}')
    # end try    

    if (data):      
      ctxg.user = db.session.get(Users, data['id'])        
      app.logger.debug(f'verify_password_with_token() set context user {ctxg.user}')
      if( not ctxg.user):
        ''' valido el token pero no esta el usuario en la base'''
        return False
      # end if
      return True
    #end if

    user = None
    try:
      user = Users.query.filter_by(username = username_or_token).first()      
    except Exception as e:
      app.logger.debug(f'Exception {type(e)}: {e}')
    # end try  

    if (not user or not user.verify_password(password)):
      return False
    # end if
    ctxg.user = user
    return True
  # end def
# end class

# Create user model
class Comicios(db.Model):
  __tablename__ = 'comicios'
  id = db.Column(db.Integer, primary_key=True)
  id_hash  = db.Column(db.String(64),unique=True,nullable=False)
  user_id  = db.Column(db.Integer,db.ForeignKey('users.id'))
  #req  = db.Column(JSON)
  #resp = db.Column(JSON)
  req  = db.Column(db.String(1024),nullable=True)
  resp = db.Column(db.String(1024),nullable=True)
  timestamp = db.Column(db.DateTime)

  def __init__(self,username:str,req:dict):    
    try:
      self.user_id = Users.query.filter_by(username = username).first().id
      self.id_hash = hashlib.md5(f"{time.clock_gettime_ns(time.CLOCK_REALTIME)}".encode()).hexdigest()    
      self.req = json.dumps(req)
      self.timestamp = datetime.now()
    except Exception as e:
      app.logger.debug(f'Exception {type(e)}: {e}')
    #end try
  # end def

  def __repr__(self):
    return f"{type(self).__name__}({self.id_hash}, {self.user_id})"
  #end def

  def get_response(self):
    ''' Metodo de Instancia para armar un response relacionado a la instancia '''
    return jsonify({ 'id': self.id_hash
            , 'date': self.timestamp
            , 'request': json.loads(self.req)
            , 'response':json.loads(self.resp)
            })
  # end def

  
  def calcular_escanios(self,req:dict) -> list:
    ''' Metodo de instancia para calcular los escanios por 
        listas, este actualiza el attributo 'resp'
          - req : dicionario con la informacion +, este debe contener los objetos:
            + votos : lista
            + escanios : del tipo int

        return lista con el calculo de escanio por lista
    '''
    escanios:int = req['escanios']
    dis_votes:list = req['votos']    

    # 1° ordenamos la lista en funcion de la cantidad de votos por partido
    dis_votes.sort(reverse=True, key=itemgetter("votos"))
    ## 2° Para cada lista calculamos la distribucion de escanios
    ret : list = []
    ret_list:list = []
    for i in dis_votes:
      ''' creamos el esqueleto de la lista a retornar y la que usaremso para procesar'''   
      tmp : list = [ i["votos"]/(j+1) for j in range(0,escanios)]   
      ret += [ {"name":i["name"],"votos":ii} for ii in tmp]
      '''
      ret.append( { "name":i["name"]
                  , "cocientes": [ i["votos"]/(j+1) for j in range(0,escanios)]                  
                  })
      '''
      ret_list.append({'name':i["name"],'votos':i["votos"],'escanios':0})
    # end for
    '''
    # 3° armamos una lista desglozamos nombre con cada item de la distribucion de escaneos
    tmp : list = []
    for it in ret:
      tmp += [ {"name":it["name"],"votos":i} for i in it["cocientes"]]      
    # end for 
    '''
    ret.sort(reverse=True, key=itemgetter("votos"))
    ret = ret[0:escanios]
    
    ## antes de agrupar debemso ordenar por el mismo key
    ret.sort(reverse=True, key=itemgetter("name"))    
    result:list = []
    for k,g in groupby(ret,key=itemgetter('name')):
      result.append({'name':k,'escanios':len(list(g))})      
    # end for

    for it in ret_list:
      i = next(filter(lambda obj: obj.get('name') == it['name'], result), None)
      if( i ):
        it['escanios'] = i['escanios']
      # end if
    #end for
    ret_list.sort(reverse=True, key=itemgetter("votos"))  

    r:list = []
    for i in ret_list:
      r.append({"lista":i["name"],"escanios":i["escanios"] })      
    # end for
    self.resp = json.dumps(r)
    return r
  # end def
#end class












