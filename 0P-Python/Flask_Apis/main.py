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
JEL            2024.04.19           0.3.3       bug ctx user None for Token validation ok table
                                                User dump
JEL            2024.04.19           0.3.4       check type datos in /api/register and
                                                /api/edit_register
JEL            2024.04.19           0.3.5       check mandatory field in request for /api/comicio
JEL            2024.04.19           0.3.6       check type object in request for /api/comicio
JEL            2024.04.19           0.3.7       add check for ret (get one register in tbl comicios)
                                                in /api/get_comicio/<string:id>
JEL            2024.04.19           0.3.8       add db.create_all(), for when the application is
                                                started by wsgi and there is no DDBB
JEL            2024.04.22           0.4.0       add function decorator for check request
JEL            2024.04.22           0.4.1       edit Models Users add instance method
                                                response_login()
JEL            2024.04.22           0.4.2       edit Models Comicios, edit instance method
                                                get_response()
JEL            2024.04.26           0.4.3       edit Models Comicios, edit instance method
                                                calcular_escanios() Performance
JEL            2024.04.26           0.4.4       edit Config, quit edit set_logger() not currently
                                                in use
JEL            2024.04.26           0.4.5       change logging for native compatibility, setting
                                                dictConfig
JEL            2026.02.02           0.4.4       add pylint style PEP8

"""
## 1° standard import
from os import path

## 2° third party imports
from flask import request, jsonify, g,abort          # type: ignore

## 3° import project module
from Models.Models import Users,Comicios,db,auth
from Config.Config import app#, DATABASE_TYPE
from ApiErrorHandler.ApiErrorHandler import validate_json_request

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
    if app.config.get('TOKEN_USE',False):
        return Users.verify_password_with_token(g,username_or_token, password)

    return Users.verify_username_password(g,username_or_token, password)


@app.route('/api/register', methods=['POST'])
@validate_json_request(':dict','username:!str','password:!str')
def register():
    ''' API para registra un nuevo usuario si 
        este no existe
    '''
    # set verify empty in decorator func @validate_json_request()
    username = request.json.get('username')
    password = request.json.get('password')
    app.logger.debug('Register usaer %s',username)

    # Check for existing users
    user = None
    try:
        user = Users.query.filter_by(username = username).first()
    except Exception as e: # pylint: disable=broad-exception-caught
        app.logger.debug('Exception %s: %s',type(e).__name__,e)


    if user:
        # usuario ya esta registrado
        app.logger.debug('username <%s> ya esta registrado',username)
        abort(jsonify({'code':400,'message': f'username <{username}> ya esta registrado'}))

    ## Creamos el nuevo usuario
    user = Users(username,password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201)


@app.route('/api/register', methods=['PATCH'])
@auth.login_required
@validate_json_request(':dict','password:!str')
def edit_register():
    ''' API para registra un nuevo usuario si 
        este no existe
    '''
    app.logger.debug('edit_register(): user: %s',g.user.username)
    password = request.json.get('password')

    ## Editmaos la clave del usuario
    user = None
    try:
        user = Users.query.filter_by(username = g.user.username).first()
    except Exception as e: # pylint: disable=broad-exception-caught
        abort(jsonify({'code':500,'error': f'error interno en BBDD, detalle: {e}'}))

    if not user:
        # 'username:password or token not linked to a registered user'
        abort(jsonify({'code':400,
                       'message': 'username:password or token not linked to a registered user'
                    }))

    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return g.user.response_login()



@app.route('/api/login')
@auth.login_required
def get_token():
    ''' API para obtener un nuevo token, para el usuario 
        con el cual se relaizo la peticion.
    '''
    app.logger.debug('get_token(): user: %s',g.user.username)
    return g.user.response_login()


@app.route('/api/HealthCheck', methods=['GET'])
@auth.login_required
def health_check():
    ''' APi para health check de la APIs '''
    app.logger.debug('health_check(): user: %s',g.user.username)
    return jsonify({ 'version': app.config['VERSION'] })



@app.route('/api/users', methods=['GET'])
@auth.login_required
def get_users():
    ''' API para obtener un listado de users '''
    # get all users
    users = None
    try:
        users = Users.query.all()
    except Exception as e: # pylint: disable=broad-exception-caught
        return (jsonify({'code':500,'error': f'error interno en BBDD, detalle: {e}'}),500)

    app.logger.debug('get_users(): user: %s',g.user.username)
    return (jsonify({'users': [ x.username for x in users]}),200)



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
    app.logger.debug('comicio(): user: %s',g.user.username)
    req = request.get_json()
    ## Creamos el nuevo registro
    com:Comicios = Comicios(req=req,username=g.user.username)
    ret = com.calcular_escanios(req)
    db.session.add(com)
    db.session.commit()
    return (jsonify({ 'id': com.id_hash,'comicios': ret }),200)



@app.route('/api/get_comicio/<string:id>', methods=['GET'])
@auth.login_required
def get_comicio(id_hash:str):
    ''' API para obtener un comicio por id
            - id : hash id devuelto cuando se realiza un request 
            para la api '/api/comicio'
    '''
    app.logger.debug('get_comicio(): user: %s',g.user.username)
    # Check for existing id_hash, consideramos solo el id
    #ret = Comicios.query.filter_by(id_hash = id,user_id=g.user.id).first()
    ret = Comicios.query.filter_by(id_hash = id_hash).first()
    if ret is None :
        # id hash no found
        app.logger.debug('id <%s> not found',id_hash)
        abort(jsonify({'code':400,'message': f'id <{id_hash}> not found' }))

    return ret.get_response()
    #return (jsonify(ret.get_response()),200)


@app.route('/api/get_comicios', methods=['GET'])
@auth.login_required
def get_comicios():
    ''' API para obtener el listado de comicio asociados al usuario actual        
    '''
    app.logger.debug('get_comicio(): user: %s',g.user.username)
    q = None
    try:
        q = Comicios.query.filter_by(user_id=g.user.id).all()
    except Exception as e: # pylint: disable=broad-exception-caught
        app.logger.debug('Exception %s : %s',type(e).__name__,e)
        return (jsonify({'code':500,'error': 'error interno en BBDD'}),500)
    # end try
    ret = [x.id_hash for x in q]
    return (jsonify({'user':g.user.username,'ids': ret}),200)




if __name__ == "__main__" :
    # para testing utilizamos sqlite como BBDD
    #if( DATABASE_TYPE == 'sqlite' and not path.exists('db.sqlite') ):
    if not path.exists('db.sqlite') :
        # Create database within app context
        with app.app_context():
            db.create_all()

        # En debug mode los response json automaticamente toman la tabulacion y newline
        # para pretty format
        from cfg_wsgi import bind_ip,bind_port
        app.run(debug=True,host=bind_ip,port=int(bind_port))
        #app.run()
    else:
        # run with wsgi, no lo ejecuta directamente el interprete
        if not path.exists('db.sqlite') :
            # Create database within app context
            with app.app_context():
                db.create_all()
