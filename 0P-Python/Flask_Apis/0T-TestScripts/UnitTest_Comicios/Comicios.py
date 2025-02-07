import json


def strjson_to_dict(data:str)->dict:
  '''Funcion para convertir un json string a un dict
  Params
    data string con el json

  Return 
    dict : con la representacion del json
  '''
  return json.loads(data)
#enddef

def dict_to_strjson(data:dict,tabs=None)->str:
  '''Funcion para convertir un dict a un json string
  Params
    data dict con los datos

  Return 
    str : string con la representacion json del dict
  '''
  if(tabs):
    return json.dumps(data,indent=tabs)
  return json.dumps(data)
#enddef


def dict_to_jsonfile(data:dict,filename:str,tab:int=2) -> None:
  ''' Dictionary dump to file JSON.

  Params
    - data    : dict, data to dump in file
    - filename: str, path/file del archivo
    - tab     : identation for dump
  '''  
  with open(filename, 'w') as file2write:
    json.dump(data, file2write,indent=tab) 
# end def

def jsonfile_to_dict(path:str) -> dict|list:
  ''' Load json file in dict

  Params
    - path: str, path/file del archivo
  '''  
  from pathlib import Path
  if(not Path(path).exists()):
    return None
  content:str = ''
  ## concatenamos el contenido sin espacios
  with open(path,"r") as file2read:    
    for it in file2read:
      tmp = it.rstrip()
      content += tmp.lstrip()      
    # end for
  #endwith     
  return json.loads(content)
# end for

class BaseApis:
  ''' Interfaces Base para la verificacion de APIs
  '''  
  def get_endpoint(self,type,*args,**kwargs) -> str:
    ''' Metodo para obtener los diferentes end point disponible 
    para un comicio.

    Params
      type : tipo de endpoint
        - create_user : para crear nuevos usuarios
        + 

    '''
    name_method = f'_get_endpoint_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}> para obtener end point no disponible')
    
    method = getattr(self,name_method)
    return method(*args,**kwargs)
  #enddef

  def get_auth(self,type,*args,**kwargs) -> tuple:
    ''' Metodo para obtener la tupla p/auth

    Params
      type : tipo de endpoint
    '''
    name_method = f'_get_auth_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}> para obtener Auth no disponible')
    #endif    
    method = getattr(self,name_method)
    return method(*args,**kwargs)
  #enddef

  def get_payload(self,type,*args,**kwargs)-> dict :
    ''' Metodo para obtener el payload para los diferentes end point
    disponible.

    Params
      type : tipo de endpoint
    '''
    name_method = f'_get_payload_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}> para obtener un payload no existe')
    
    method = getattr(self,name_method)
    return method(*args,**kwargs)
  #enddef

  def get_method(self,type,*args,**kwargs)-> str :
    ''' Metodo para obtener el metodo de la APIS para los diferentes type
    disponible.

    Params
      type : tipo de accion
    '''
    name_method = f'_get_method_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}> para obtener un Metodo no existe')
    
    method = getattr(self,name_method)
    return method(*args,**kwargs)
  #enddef

  def request_method(self,type,*args,**kwargs):
    ''' Metodo para obtener el Request Method (funcion encargada de realizar la peticion a la API)
    para los diferentes type disponible.

    Params
      type : tipo de accion
    '''
    name_method = f'_request_method_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}> para obtener un Request Metodo no existe')
    
    method = getattr(self,name_method)
    return method(*args,**kwargs)
  #enddef

  def get_headers(self,type,*args,**kwargs)-> str :
    ''' Metodo para obtener el Header de la APIS para los diferentes type
    disponible.

    Params
      type : tipo de accion
    '''
    name_method = f'_get_headers_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}> para obtener un Metodo no existe')
    
    method = getattr(self,name_method)
    return method(*args,**kwargs)
  #enddef

  def get_response(self,type,*args,**kwargs)-> dict :
    ''' Metodo para obtener los response fijos, que solo depende de un template 
    mas los datos de la clase deribada, de la APIs. En contraparte contamos con 
    los metodo para el check de cada response el cual es especifico de cada objeto
    derivado y que puede variar en funcion del tipo de respuesta.

    Params
      type : tipo de accion
    '''
    name_method = f'_get_response_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}> para obtener un Response no existe')
    
    method = getattr(self,name_method)
    return method(*args,**kwargs)
  #enddef

  def verify_response(self,type,response,*args,**kwargs) -> bool:
    '''Metodo para realizar la verificacion de una response, esta es customizable 
    para cada objeto derivado y a diferencia de los get, que nos permiten obtener
    un dict y comparar este directamente del lado del test. Este recibe el objeto 
    respnse y retorna un bool.

    Params
      type : tipo de verificacion
      response : respuesta a verificar 

    Returns 
      - True : verificacion succes
      - False : verificacion failure
    '''
    name_method = f'_verify_response_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}>, para la verificacion de response no Existe')
    #endif
    if( not 200 <= response.status_code <= 210 ):
      return False
    #endif
    method = getattr(self,name_method)
    return method(response,*args,**kwargs)
  #enddef

  def verify_headers(self,type,response,*args,**kwargs) -> bool:
    '''Metodo para realizar la verificacion de tipo de header de la respuesta, este
    sigue la misma logica que ``verify_response()`` es altamente customizable del 
    lado de clase deribada.

    Params
      type : tipo de verificacion
      response : respuesta a verificar 

    Returns 
      - True : verificacion succes
      - False : verificacion failure
    '''
    name_method = f'_verify_headers_{type}'
    if( not hasattr(self,name_method)):
      raise ValueError(f'Type<{type}>, para la verificacion de Header de la response no Existe')
    
    method = getattr(self,name_method)
    return method(response,*args,**kwargs)
  #enddef
#endclass

class Comicio(BaseApis):
  '''Objeto para modelar un comicio
    - username : Nombre de usuario
    - password : password
    - jsonfile : path file json with comicio data
  '''
  IP:str   = '127.0.0.1'
  PORT:str = '8080'
  #
  URL:str  = 'http://' + IP + ':' + PORT
  APIsVERSION:str = '0.5.0'

  def __init__(self,**kwargs):
    self.username:str = kwargs.get('username','jel')
    self.password:str = kwargs.get('password','pass12345')
    self.data :dict = jsonfile_to_dict(kwargs.get('jsonfile','../post_comicio_01.json'))
    ## new_password is reverse de la original
    self.new_password:str = kwargs.get('new_password',self.password[::-1])
    self.tkn = kwargs.get('tkn',None)
    self.timeout = kwargs.get('timeout',0)
    self.ids:list = kwargs.get('ids',[])
    #super().__init__(header_uniq=True)
  #enddef

  def to_json(self)->dict:
    '''Metodo que transforma el contenido del objeto en un json/dict'''
    return {
      'username'     : self.username,
      'password'     : self.password,
      'data'         : self.data,
      'new_password' : self.new_password,
      'tkn'          : self.tkn,
      'timeout'      : self.timeout,
      'ids'          : self.ids
    }
  #endif
  """
  def token(self,tkn=None):
    '''Metodo para Obtener o establecer el token
    Params
      - token : Opcional, si lo especificamos establece el toke

    Returns
      Si no especificamos el token, este es retornado. De lo contrario None
    '''
    if(tkn):
      self.tkn = tkn
      return None
    #endif
    return self.tkn
  #enddef
  """

  """
  def __str__(self):
    '''Representacion no formal para un objeto del tipo Comicio

    Returns
      Representacion mediante un string, del objeto
    '''
    return f'Username: {self.username}, Password: {self.password}'
  #enddef
  """
  def get_method(self,type)-> str :
    ''' OVER WRITE Metodo para obtener el metodo de la APIS para los diferentes type
    disponible.

    Params
      type : tipo de funcionalidad
    '''
    match type:
      case 'create_user'|'comicio':
        return 'POST'
      case 'edit_user':
        return 'PATCH'
      case 'login'|'health_check'|'get_users'|'get_comicio'|'get_comicios':
        return 'GET'
      case _ :
        raise ValueError(f'Type<{type}> para obtener el Metodo no existe')
  #endef

  def request_method(self,type):
    ''' OVER WRITE Metodo para obtener la funcion que se encarga de realizar 
    el request.

    Params
      type : tipo de funcionalidad
    '''
    import requests
    match type:
      case 'create_user'|'comicio':
        return requests.post
      
      case 'edit_user':
        return requests.patch
      
      case 'login'|'health_check'|'get_users'|'get_comicio_id'|'get_comicios':
        return requests.get
      case _ :
        raise ValueError(f'Type<{type}> para obtener el Request Metodo no existe')
  #endef

  def get_auth(self,type) -> tuple:
    ''' OVER WRITE Metodo para obtener el auth de la APIS para los diferentes type
    disponible.

    Params
      type : tipo de funcionalidad
    '''
    match type:
      case 'create_user':
        return None
      
      case 'edit_user'|'login':
        return (self.username,self.password)
      
      case 'get_users'|'health_check'|'comicio'|'get_comicios'|'get_comicio_id':
        return (self.tkn,'notrelevant')
      
      case _ :
        raise ValueError(f'Type<{type}> para obtener el Auth no existe')
  #endef

  def get_endpoint(self, tipo, *args, **kwargs):
    match tipo:
      case 'create_user' | 'edit_user':
        return Comicio.URL + '/api/register'      
      case 'get_users':
        return Comicio.URL + '/api/users'
      case 'login':
        return Comicio.URL + '/api/login'
      case 'health_check':
        return Comicio.URL + '/api/HealthCheck'
      case 'comicio':
        return Comicio.URL + '/api/comicio'
      case 'get_comicio':
        return Comicio.URL + '/api/get_comicio'
      case 'get_comicios':
        return Comicio.URL + '/api/get_comicios'
      case 'get_comicio_id':
        return Comicio.URL + '/api/get_comicio/'+kwargs.get('id','fac0179bf7a42e755e17bab20e51f2cd')      
      case _:
        raise ValueError(f'Type<{tipo}> para obtener el End Point no existe')
      #endcase
    #endmatch  
  #enddef
  

  def _get_payload_create_user(self)-> dict :
    ''' Metodo para obtener el payload relacionado a la creacion de un usuario.
    '''    
    return {"username":self.username,"password":self.password}
  #enddef

  def _get_payload_edit_user(self)-> dict :
    ''' Metodo para obtener el payload relacionado a la edicion de un usuario.
    '''
    # hacemos el swap de claves    
    return {"password":self.new_password}
  #enddef

  def _get_payload_comicio(self,path=None)-> dict :
    ''' Metodo para obtener el payload relacionado a la creacion de un comicio.
    '''
    if(path is None):
      return self.data
    #endif
    return jsonfile_to_dict(path)
  #enddef

  def get_headers(self,type) -> str:
    '''Metodo para obtener el header de la respuestas
    Params
      type : tipo de verificacion, para todos los metodos usamos el mismo
      response : respuesta a verificar 

    Returns 
      - True : verificacion succes
      - False : verificacion failure
    '''  
    return 'application/json'
  #enddef

  def _get_response_create_user(self)-> dict :
    ''' Metodo para obtener el response relacionado a la creacion de un user.
    '''    
    return {'username':self.username}
  #enddef

  def _get_response_edit_user(self)-> dict :
    ''' Metodo para obtener el response relacionado a la edicion de un user.
    No interviene el access_token, este cambia al editar el user
    '''    
    return { 'timeout': self.timeout
            ,'username':self.username
           }
  #enddef

  def _get_response_get_user(self)-> dict :
    ''' Metodo para obtener el response relacionado a obtener la lista de user.
    No interviene el access_token, este cambia al editar el user
    '''    
    return { "users": [self.username] }
  #enddef

  def _get_response_login(self)-> dict :
    ''' Metodo para obtener el response relacionado al Login.
    No interviene el access_token, este obtiene le nuevo Token
    '''    
    return { 'timeout': self.timeout }
  #enddef

  def _get_response_health_check(self)-> dict :
    ''' Metodo para obtener el response relacionado a la health_check.
    No interviene el access_token, este obtiene le nuevo Token
    '''    
    return { "version": Comicio.APIsVERSION }
  #enddef



  def verify_headers(self,type,response) -> bool:
    '''OVER WRITE Metodo para realizar la verificacion de tipo de header 
    de la respuesta. Ya que para todos los response el header debe ser el mismo.

    Params
      type : tipo de verificacion, para todos los metodos usamos el mismo
      response : respuesta a verificar 

    Returns 
      - True : verificacion succes
      - False : verificacion failure
    '''  
    return True if response.headers["Content-Type"] == 'application/json'\
      else False
  #enddef

  def _verify_response_create_user(self,response,repeat=False):
    '''Metodo callback para verificar el response del typo ``create_user``

    Params
      response : objeto response, de 
    '''
    '''Response Type: 
      1. Case Success: { "username": "${username}" }
      2. Usuario Ya Creado: {
        "code": 400,
        "message": "username <jesus> ya esta registrado"
      }
    '''
    data = response.json()
    if(not repeat):
      if ('username' in data):
        return True if data['username'] == self.username else False
      #endif
      return False
    #endif
    if ('username' in data):
      return True if data['username'] == self.username else False
    #endif

    if (not 'code' in data or data['code'] != 400):
      return False
    
    msg = f'username <{self.username}> ya esta registrado'
    if (not 'message' in data or data['message'] != msg):
      return False
    #endif
    return True
  #endef

  def _verify_response_edit_user(self,response):
    '''Metodo callback para verificar el response del tipo ``edit_user``

    Params
      response : objeto response
    '''
    '''Response Type: {
      "access_token": "...",
      "timeout": 1800,
      "username": "jesus"
    }
    '''
    # 1° Verificamos que contenga todos los key
    dct_resp = response.json()
    if not all(key in dct_resp for key in ("access_token","timeout","username")):
      return False
    #endif
    if(len(dct_resp['access_token'])<10):
      return False
    #endif
    if(dct_resp['timeout'] != 1800):
      return False
    #endif
    
    if(dct_resp['username'] != self.username):
      return False
    #endif   

    self.password = self.new_password
    self.tkn = dct_resp['access_token']
    return True
  #enddef

  def _verify_response_get_users(self,response):
    '''Metodo callback para verificar el response del tipo ``edit_user``

    Params
      response : objeto response
    '''
    '''Response Type: {
        "users": [
          "jesus"
        ]
      }
    '''
    # 1° Verificamos que contenga todos los key
    dct_resp = response.json()
    if not 'users' in dct_resp:
      print(f'key users, not found in {dct_resp}')
      return False
    #endif
    ## recorremos la lista para buscar nuestro usuario
    if(not self.username in dct_resp['users']):
      print(f'users<{self.username}>, not found in {dct_resp}')
      return False
    #endif
    return True
  #enddef

  def _verify_response_login(self,response):
    '''Metodo callback para verificar el response del tipo ``edit_user``

    Params
      response : objeto response
    '''
    '''Response Type: {
      "access_token": "...",
      "timeout": 1800,
      "username": "jesus"
    }
    '''
    # 1° Verificamos que contenga todos los key
    dct_resp = response.json()
    if not all(key in dct_resp for key in ("access_token","timeout","username")):
      return False
    #endif
    if(len(dct_resp['access_token'])<10):
      return False
    #endif
    '''Almacenamos el token, para la session de test'''
    self.tkn = dct_resp['access_token']
    if(dct_resp['timeout'] != 1800):
      return False
    #endif
    
    if(dct_resp['username'] != self.username):
      return False
    #endif
    return True
  #enddef

  def _verify_response_health_check(self,response):
    '''Metodo callback para verificar el response del tipo ``edit_user``

    Params
      response : objeto response
    '''
    '''Response Type: {
      "version": "0.5.0"
    }
    '''
    # 1° Verificamos que contenga todos los key
    dct_resp = response.json()
    if not 'version' in dct_resp:
      print(f'key version, not found in {dct_resp}')
      return False
    #endif
    if(dct_resp['version'] != Comicio.APIsVERSION):
      return False    
    #endif
    return True
  #enddef

  def _verify_response_comicio(self,response):
    '''Metodo callback para verificar el response del tipo ``edit_user``

    Params
      response : objeto response
    '''
    '''Response Type: {
      "comicios": [
        {
          "escanios": 3,
          "lista": "Partido A"
        },
        {
          "escanios": 3,
          "lista": "Partido B"
        },
        {
          "escanios": 1,
          "lista": "Partido C"
        },
        {
          "escanios": 0,
          "lista": "Partido D"
        },
        {
          "escanios": 0,
          "lista": "Partido E"
        }
      ],
      "id": "1d746807e4a828c64eedb824423aa9b8"
    }
    '''
    # 1° Verificamos que contenga todos los key
    dct_resp = response.json()
    if not all(key in dct_resp for key in ("comicios","id")):
      print(f'keys:{("comicios","id")} not found in {dct_resp}')
      return False
    #endif
    if(len(dct_resp['comicios'])<1):
      print(f'comicios len menor a uno, en {dct_resp}')
      return False
    #endif

    if(len(dct_resp['id'])<10):
      print(f'ID de Comicio len menor a 10, en {dct_resp}')
      return False
    #endif

    dct_resp = dct_resp['comicios'][0]
    if not all(key in dct_resp for key in ("escanios","lista")):
      return False
    #endif    
    return True
  #enddef

  def _verify_response_get_comicios(self,response):
    '''
    Metodo callback para verificar el response del tipo ``edit_user``

    Params
      response : objeto response
    
    '''
    ''' Response {
      "ids": [
        "1d746807e4a828c64eedb824423aa9b8",
        "34a869c0440813c2764f053696ac2c2b",
        "97f1d1254c3241adf0ac5e58031a80a1",
        "130233468fd4ea383afee0b98f82aeec",
        "685c3d982b3d339c129b31339ff3b538",
        "52c2126b6512c934c12bec30d0e3e2e8"
      ],
      "user": "jesus"
    }
    '''
    # 1° Verificamos que contenga todos los key
    dct_resp = response.json()
    if not all(key in dct_resp for key in ("ids","user")):
      #print(f'keys:{("ids","user")} not found in {dct_resp}')
      return False
    #endif    
    if(dct_resp['user'] != self.username ):      
      return False
    #endif

    self.ids = dct_resp['ids']
    return True
  #endif

  def _verify_response_get_comicio_id(self,response):
    '''
    Metodo callback para verificar el response del tipo ``edit_user``

    Params
      response : objeto response
    
    '''
    ''' Response {
        "date": "Mon, 03 Feb 2025 21:48:37 GMT",
        "id": "1d746807e4a828c64eedb824423aa9b8",
        "request": {
          "escanios": 7,
          "listas": 10,
          "votos": [
            {
              "name": "Partido A",
              "votos": 340000
            },
            {
              "name": "Partido B",
              "votos": 280000
            },
            {
              "name": "Partido C",
              "votos": 160000
            },
            {
              "name": "Partido D",
              "votos": 60000
            },
            {
              "name": "Partido E",
              "votos": 15000
            }
          ]
        },
        "response": [
          {
            "escanios": 3,
            "lista": "Partido A"
          },
          {
            "escanios": 3,
            "lista": "Partido B"
          },
          {
            "escanios": 1,
            "lista": "Partido C"
          },
          {
            "escanios": 0,
            "lista": "Partido D"
          },
          {
            "escanios": 0,
            "lista": "Partido E"
          }
        ]
      }
    '''
    # 1° Verificamos que contenga todos los key
    dct_resp = response.json()
    if not all(key in dct_resp for key in ("date","id","request","response")):    
      print(f'keys <{("date","id","request","response")}> not found in resp: <{dct_resp}>')
      return False
    #endif
    dct_req = dct_resp['request']
    '''lista es opcional en el request'''
    #if not all(key in dct_req for key in ("escanios","listas","votos")):
    if not all(key in dct_req for key in ("escanios","votos")):
      print(f'keys <{("escanios","listas","votos")}> not found in response/request: <{dct_req}>')
      return False
    #endif

    dct_req = dct_resp['response']
    for r in dct_req:
      if not all(key in r for key in ("escanios","lista")):    
        return False
      #endif
    #endfor
    return True
  #endif
#endclass



''' verificamos si este script es el principal
    invocado desde la linea de comandos
'''
if (__name__ == "__main__"):
  import os  
  print(f'Import Module "import {os.path.basename(__file__)[:-3]}" and use me!')  
# end if
  
    