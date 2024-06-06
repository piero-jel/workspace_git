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

\b file ApiErrorHandler.py
\b brief Modulo para el manejo de los response json de error
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Domingo 19 de Mayo de 2024.
\b version 0.3.8.
\b Change History:
Author         Date                 Version     Brief
JEL            2024.04.19           0.3.8       Version Inicial no release
JEL            2024.04.22           0.4.0       add function decorator for check request validate_json_request()
                                                delete objects JsonHanlderError, JsonDefaultError and
                                                functions response_json_error() with privates functions (
                                                '__get_codes_api()', '__get_message_codes()' )
                                 

"""
import functools
from flask import jsonify,abort,request


def split_name_type(data:str) -> tuple:
  ''' Funcion para el split de name type
      - data : string formato
        + <name:type>  : no se verifica el contendido
        + <name:!type> : se verifica el contenido util para str , len(lst), len(dct.items())
  '''
  idx:int = data.find(':')
  if(idx == -1):
    raise ValueError(f'argument error <{data}>, ":" not found')
  # end if
  if(idx == 0):
    return (None,data[1:],False)
  # end if  
  
  if(data[idx+1:][0] == '!'):
    return (data[0:idx] , data[idx+2:] , True)
  
  return (data[0:idx] , data[idx+1:] , False)
# end def

'''
def get_response_json(msg:str, code:int):
  return jsonify({ 'code' : code, 'message': msg})
jsonify({'code':400,'message':}  
'''
def validate_json_request(*targets):
  ''' Decorator function para validar los request json, solo 
      los item del root.
      - targets : listado de campos a validad desde el root
        Formato 
          + 'name:type': busca el name y verifica el tipo
          
          + 'name:!type': busca el name, verifica el tipo y en caso de type
          str|list|dict verifica que el mimos no este vacio

          + ':type' : 'sin name' en caso de necesitar validar el tipo del root 
          (donde type solo puede ser dict|list, o deribados de estos )
  '''
  def decorator_validate_json_request(func):
    ''' Decorador interno que recibe la fucion ('Funcion de orden Superior')
        , ya que el decorador principal recive argumentos. 
        Esta se encarga de armar y retornar el wrapper o funcion que 
        se encarga de realizar la verificacion
    '''
    @functools.wraps(func) # call decorator factory
    def wrapper_validate_json_request(*args,**kwargs):
      ''' Funcion wrapper que se encarga de la validacion
          - args: listado ordenado de argumentos 
          - kwargs : diccionario de argumentos (dupla nombre = valor )
      '''
      req = request.get_json()      
      for it in targets:        
        n,t,m = split_name_type(it)
        if(n == None):
          # root type dict or list
          if(not t in ('list','dict')):
            raise ValueError(f'type <{t}> in argument root <{it}> not supported')
          # end if
          if(type(req).__name__ != t): 
            pretty_resp:dict = {'dict':'JSON Object','list':'JSON Array'}
            abort(jsonify({'code':400,'message':f'type <{pretty_resp[type(req).__name__]}> in root, was expected <{pretty_resp[t]}>'}))            
          else:
            continue # root solo validamos tipo 
          #end if
        # end if
        if( not n in req):
          abort(jsonify({ 'code' : 400, 'message': f'object <{n}> not found in request'}))          
        # end if
        if( type(req[n]).__name__ != t ):
          abort(jsonify({'code':400,'message': f'object <{n}> is not type <{t}>' }))
        # end if
        if( m ):
          match t:
            case 'str':
              if(req[n].strip()==""):
                abort(jsonify({'code':400,'message': f'field <{n}> is empty'}))
            case 'list':
              if(len(req[n])):
                abort(jsonify({'code':400,'message': f'json array <{n}> is empty'}))
            case 'dict':
              if(len(req[n].items())):
                abort(jsonify({'code':400,'message': f'json object <{n}> is empty'}))
            case _:
              # no tenemos patron para comprobar el mandato, pasamos al proximo item
              pass
          #end match
        # end if
      # end for
      return func(*args,**kwargs)
    # end def
    return wrapper_validate_json_request
  # end def
  return decorator_validate_json_request
# end def
