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

\b file main.py
\b brief script principal de la aplicacion
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Domingo 19 de Mayo de 2024.
\b version 0.3.8.
\b Change History:
Author         Date                 Version     Brief
JEL            2024.04.16           0.0.1       Version Inicial no release
JEL            2024.04.17           0.1.0       Separacion en modulos
JEL            2024.04.18           0.2.0       Agregado del modlulo ApiErrorHandler
JEL            2024.04.18           0.3.0       Add wsgi
JEL            2024.04.18           0.3.1       bug add try cath in access DDBB ('BBDD coruptas')
JEL            2024.04.19           0.3.2       bug add check in users != None
JEL            2024.04.19           0.3.3       bug ctx user None for Token validation ok table User dump
JEL            2024.04.19           0.3.4       check type datos in /api/register and /api/edit_register
JEL            2024.04.19           0.3.5       check mandatory field in request for /api/comicio
JEL            2024.04.19           0.3.6       check type object in request for /api/comicio
JEL            2024.04.19           0.3.7       add check for ret (get one register in tbl comicios) in /api/get_comicio/<string:id>
JEL            2024.04.19           0.3.8       add db.create_all(), for when the application is started by wsgi and there is no DDBB
JEL            2024.04.22           0.4.0       add function decorator for check request
JEL            2024.04.22           0.4.1       edit Models Users add instance method response_login()
JEL            2024.04.22           0.4.2       edit Models Comicios, edit instance method get_response()
JEL            2024.04.26           0.4.3       edit Models Comicios, edit instance method calcular_escanios() Performance
JEL            2024.04.26           0.4.4       edit Config, quit edit set_logger() not currently in use
JEL            2024.04.26           0.4.5       change logging for native compatibility, setting dictConfig
"""

from flask import request, jsonify, g,abort

## local modules
from Models.Models import Users,Comicios,db,auth
from Config.Config import app
from ApiErrorHandler.ApiErrorHandler import validate_json_request
from os import path

# Initialize app with extension
db.init_app(app)



@auth.verify_password
def verify_password(username_or_token, password:str=''):
  ''' Metodo que se encargara de verificar password/token
        - username_or_token : si este se corresponde a un token previamente
        generado y a un vigente usa este para la validacion. De lo contrario
        lo trata como usuario. Si el mismo es localizado se procede a validad
        la clave.

        - password : clave que se utilizara solo si username_or_token es un usuario
        localizado dentro de los registros.

      return :
        - True verificacion success
        - False verificacion no success, not authorized
  '''
  if(app.config.get('TOKEN_USE',False)):
    return Users.verify_password_with_token(g,username_or_token, password)
  # end if
  return Users.verify_username_password(g,username_or_token, password)
# end if


@app.route('/api/register', methods=['POST'])
@validate_json_request(':dict','username:!str','password:!str')
def register():
  ''' API para registra un nuevo usuario si 
      este no existe
  '''
  '''
  username = request.json.get('username',"") 
  password = request.json.get('password',"")
  if(not isinstance(username,str) or not isinstance(password,str)):
    logger.debug(f'username type <{type(username)}> or password type <{type(password)}> is not string')
    return response_json_error('register',400,2)
  #end if
  
  username = request.json.get('username',"") 
  password = request.json.get('password',"")
  # Check for blank requests  
  if (username.strip()=="" or password.strip()==""):    
    logger.debug(f'username <{username}> or password <{password}> is None or empty')
    abort(jsonify({'code':400,'message': f'username <{username}> or password <{password}> is None or empty' }))    
  # end if
  '''
  # set verify empty in decorator func @validate_json_request()
  username = request.json.get('username') 
  password = request.json.get('password')
  # Check for existing users
  user = None
  try:
    user = Users.query.filter_by(username = username).first()
  except Exception as e:
    app.logger.debug(f'Exception {type(e)}: {e}')
  # end try
  if (user):
    ''' usuario ya esta registrado '''
    app.logger.debug(f'username <{username}> ya esta registrado')
    abort(jsonify({'code':400,'message': f'username <{username}> ya esta registrado'}))
    #return response_json_error('register',400,1)
  # end if
  ## Creamos el nuevo usuario
  user = Users(username,password)
  db.session.add(user)
  db.session.commit()
  return (jsonify({'username': user.username}), 201)
# end def

@app.route('/api/register', methods=['PATCH'])
@auth.login_required
@validate_json_request(':dict','password:!str')
def edit_register():
  ''' API para registra un nuevo usuario si 
      este no existe
  '''  
  app.logger.debug(f'edit_register(): user:{g.user.username}')
  password = request.json.get('password')
  '''
  password = request.json.get('password',"")
  if(not isinstance(password,str)):
    logger.debug(f'password type <{type(password)}> is not string')
    return response_json_error('edit_register',400,1)
  #end if
  
  # Check for blank requests
  if ( password == ""):
    logger.debug(f'password <{password}> is None or empty')
    abort(jsonify({'code':400,'message': f'password <{password}> is None or empty'}))
    #return response_json_error('edit_register',400,0)    
  # end if  
  '''
  ## Editmaos la clave del usuario
  user = None
  try:
    user = Users.query.filter_by(username = g.user.username).first()
  except Exception as e:
    '''
    from inspect import currentframe, getframeinfo
    cf = currentframe()
    filename = path.basename(getframeinfo(cf).filename)
    lineno   = cf.f_lineno - 5
    logger.debug(f'{filename}:{lineno} - Exception {type(e)}: {e}')
    return (jsonify({'code':lineno,'error': 'error interno en BBDD'}),500)
    '''
    return (jsonify({'code':500,'error': 'error interno en BBDD'}),500)
  # end try
  if(not user):
    # 'username:password or token not linked to a registered user'
    abort(jsonify({'code':400,'message': 'username:password or token not linked to a registered user'}))
    #return response_json_error('edit_register',400,2)
  # end if
  user.hash_password(password)
  db.session.add(user)
  db.session.commit()
  return g.user.response_login()  
# end def


@app.route('/api/login')
@auth.login_required
def get_token():
  ''' API para obtener un nuevo token, para el usuario 
      con el cual se relaizo la peticion.
  '''
  app.logger.debug(f'get_token(): user:{g.user.username}')
  return g.user.response_login()  
# end def


@app.route('/api/HealthCheck', methods=['GET'])
@auth.login_required
def health_check():
  ''' APi para health check de la APIs '''
  app.logger.debug(f'health_check(): user:{g.user.username}')
  return jsonify({ 'version': app.config['VERSION'] })
# end if


@app.route('/api/users', methods=['GET'])
@auth.login_required
def get_users():
  ''' API para obtener un listado de users '''
  # get all users 
  users = None
  try:
    users = Users.query.all()
  except Exception as e:
    '''
    from inspect import currentframe, getframeinfo
    cf = currentframe()
    filename = path.basename(getframeinfo(cf).filename)
    lineno   = cf.f_lineno - 5
    logger.debug(f'{filename}:{lineno} - Exception {type(e)}: {e}')
    return (jsonify({'code':lineno,'error': 'error interno en BBDD'}),500)
    '''
    return (jsonify({'code':500,'error': 'error interno en BBDD'}),500)
  # end try
  app.logger.debug(f'get_users(): user:{g.user.username}')
  return (jsonify({'users': [ x.username for x in users]}),200)
# end if


@app.route('/api/comicio', methods=['POST'])
@auth.login_required
@validate_json_request(':dict','votos:list','escanios:int')
def comicio():
  ''' API para registra un nuevo comicio
      Los Siguentes Objetos son mandatorios/obligatorios
        - votos : 
        - escanios
      
      Mientras que los demas son opcionales
        - listas 

  '''
  app.logger.debug(f'comicio(): user:{g.user.username}')
  req = request.get_json()
  ## Creamos el nuevo registro
  comicio = Comicios(req=req,username= g.user.username)
  ret = comicio.calcular_escanios(req)  
  db.session.add(comicio)
  db.session.commit()
  return (jsonify({ 'id': comicio.id_hash,'comicios': ret }),200)
# end def

@app.route('/api/get_comicio/<string:id>', methods=['GET'])
@auth.login_required
def get_comicio(id):
  ''' API para obtener un comicio por id
        - id : hash id devuelto cundo se realiza un request 
        para la api '/api/comicio'
  '''    
  app.logger.debug(f'get_comicio(): user:{g.user.username}')
  # Check for existing id_hash, consideramos solo el id
  #ret = Comicios.query.filter_by(id_hash = id,user_id=g.user.id).first()
  ret = Comicios.query.filter_by(id_hash = id).first()
  if ( ret == None ): 
    ''' id hash no found  '''
    app.logger.debug(f'id <{id}> not found')
    abort(jsonify({'code':400,'message': f'id <{id}> not found' }))    
  # end if  
  return ret.get_response()
  #return (jsonify(ret.get_response()),200)
# end def

@app.route('/api/get_comicios', methods=['GET'])
@auth.login_required
def get_comicios():
  ''' API para obtener el listado de comicio asociados al usuario actual        
  '''    
  # Check for existing id_hash  
  app.logger.debug(f'get_comicio(): user:{g.user.username}')
  q = None
  try:
    q = Comicios.query.filter_by(user_id=g.user.id).all()
  except Exception as e:    
    app.logger.debug(f'Exception {type(e)}: {e}')
    return (jsonify({'code':500,'error': 'error interno en BBDD'}),500)
  # end try
  ret = [x.id_hash for x in q]
  return (jsonify({'user':g.user.username,'ids': ret}),200)
# end def



if (__name__ == "__main__"):
  ''' para testing utilizamos sqlite como BBDD '''
  if not path.exists('db.sqlite'):
    # Create database within app context 
    with app.app_context():
      db.create_all()
    # end with    
  # end if  
  ''' En debug mode los response json automaticamente 
      toman la tabulacion y newline para pretty format
  '''
  from cfg_wsgi import bind_ip,bind_port
  app.run(debug=True,host=bind_ip,port=int(bind_port))
  #app.run()
else:
  ''' run with wsgi, no lo ejecuta directamente el interprete '''
  if not path.exists('db.sqlite'):
    # Create database within app context 
    with app.app_context():
      db.create_all()
    # end with    
  # end if
# end if
