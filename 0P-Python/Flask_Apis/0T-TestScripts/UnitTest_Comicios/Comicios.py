

import os
import requests              # type: ignore

from utils import (   # pylint: disable=import-error
    #strjson_to_dict,
    #dict_to_strjson,
    #dict_to_jsonfile,
    jsonfile_to_dict,
    Logger,get_log
)

log:Logger = get_log('')

class BaseApis:
    '''
    Interfaces Base para la verificacion de APIs
    '''

    def get_endpoint(self,tipo:str,*args,**kwargs) -> str:
        ''' Metodo para obtener los diferentes end point disponible 
        para un comicio.

        Params
        type : tipo de endpoint
            - create_user : para crear nuevos usuarios
            + 

        '''
        name_method = f'_get_endpoint_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}> para obtener end point no disponible')

        method = getattr(self,name_method)
        return method(*args,**kwargs)

    def get_auth(self,tipo:str,*args,**kwargs) -> tuple:
        ''' Metodo para obtener la tupla p/auth

        Params
            tipo : tipo de endpoint
        '''
        name_method = f'_get_auth_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}> para obtener Auth no disponible')

        method = getattr(self,name_method)
        return method(*args,**kwargs)

    def get_payload(self,tipo:str,*args,**kwargs)-> dict :
        ''' Metodo para obtener el payload para los diferentes end point
        disponible.

        Params
        tipo : tipo de endpoint
        '''
        name_method = f'_get_payload_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}> para obtener un payload no existe')

        method = getattr(self,name_method)
        return method(*args,**kwargs)

    def get_method(self,tipo:str,*args,**kwargs)-> str:
        ''' Metodo para obtener el metodo de la APIS para los diferentes type
        disponible.

        Params
        type : tipo de accion
        '''
        name_method = f'_get_method_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}> para obtener un Metodo no existe')

        method = getattr(self,name_method)
        return method(*args,**kwargs)

    def request_method(self,tipo:str,*args,**kwargs):
        ''' Metodo para obtener el Request Method (funcion encargada de realizar la peticion a
         la API) para los diferentes type disponible.

        Params
            tipo : tipo de accion
        '''
        name_method = f'_request_method_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}> para obtener un Request Metodo no existe')

        method = getattr(self,name_method)
        return method(*args,**kwargs)

    def get_headers(self,tipo:str,*args,**kwargs)-> str :
        ''' Metodo para obtener el Header de la APIS para los diferentes type
        disponible.

        Params
            tipo : tipo de accion
        '''
        name_method = f'_get_headers_{tipo}'
        if not hasattr(self,name_method) :
            raise ValueError(f'Type<{tipo}> para obtener un Metodo no existe')

        method = getattr(self,name_method)
        return method(*args,**kwargs)

    def get_response(self,tipo:str,*args,**kwargs)-> dict :
        ''' Metodo para obtener los response fijos, que solo depende de un template 
        mas los datos de la clase deribada, de la APIs. En contraparte contamos con 
        los metodo para el check de cada response el cual es especifico de cada objeto
        derivado y que puede variar en funcion del tipo de respuesta.

        Params
            tipo : tipo de accion
        '''
        name_method = f'_get_response_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}> para obtener un Response no existe')

        method = getattr(self,name_method)
        return method(*args,**kwargs)

    def verify_response(self,tipo:str,response:dict|str,*args,**kwargs) -> bool:
        '''Metodo para realizar la verificacion de una response, esta es customizable 
        para cada objeto derivado y a diferencia de los get, que nos permiten obtener
        un dict y comparar este directamente del lado del test. Este recibe el objeto 
        respnse y retorna un bool.

        Params
            tipo : tipo de verificacion
            response : respuesta a verificar 

        Returns 
        - True : verificacion succes
        - False : verificacion failure
        '''
        name_method = f'_verify_response_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}>, para la verificacion de response no Existe')

        if tipo != 'create_user' and (not 200 <= response.status_code <= 210):
            return False

        method = getattr(self,name_method)
        return method(response,*args,**kwargs)

    def verify_headers(self,tipo:str,response:dict|str,*args,**kwargs) -> bool:
        '''Metodo para realizar la verificacion de tipo de header de la respuesta, este
        sigue la misma logica que ``verify_response()`` es altamente customizable del 
        lado de clase deribada.

        Params
            tipo : tipo de verificacion
            response : respuesta a verificar 

        Returns 
        - True : verificacion succes
        - False : verificacion failure
        '''
        name_method = f'_verify_headers_{tipo}'
        if not hasattr(self,name_method):
            raise ValueError(f'Type<{tipo}>, para la verificacion ' \
                             'de Header de la response no Existe')

        method = getattr(self,name_method)
        return method(response,*args,**kwargs)


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
        '''
        Inicializacion de los objetos del tipo `Comicio`
        
        
        kwargs Parametros Opcionales
        
            - `username` : Nombre de usuario
            - `password` : password
            - `logger` : objeto Logger
        '''
        # self.username:str = kwargs.get('username','jel')
        # self.password:str = kwargs.get('password','pass12345')
        # self.data :dict = jsonfile_to_dict(kwargs.get('jsonfile','../post_comicio_01.json'))
        # ## new_password is reverse de la original
        # self.new_password:str = kwargs.get('new_password',self.password[::-1])
        # self.tkn = kwargs.get('tkn',None)
        # self.timeout = kwargs.get('timeout',0)
        # self.ids:list = kwargs.get('ids',[])


        password:str = kwargs.get('password','pass12345')
        self._contex:dict = {
            'username' : kwargs.get('username','jeluccioni'),
            'password' : password,
            'data'     : jsonfile_to_dict(kwargs.get('jsonfile','../post_comicio_01.json')),
            ## new_password is reverse de la original
            'new_password' : kwargs.get('new_password',password[::-1]),
            'token'    : kwargs.get('tkn',None),
            'timeout'  : kwargs.get('timeout',0),
            'ids'      : kwargs.get('ids',[])
        }

        self.log:Logger = kwargs.get('logger',get_log('ComicioApis'))
        #super().__init__(header_uniq=True)

    def to_json(self)->dict:
        '''Metodo que transforma el contenido del objeto en un json/dict'''
        return {
            'username'     : self._contex['username'],
            'password'     : self._contex['password'],
            'data'         : self._contex['data'],
            'new_password' : self._contex['new_password'],
            'tkn'          : self._contex['token'],
            'timeout'      : self._contex['timeout'],
            'ids'          : self._contex['ids']
        }

    def get_method(self,tipo:str,*args,**kwargs)-> str:
        ''' OVER WRITE Metodo para obtener el metodo de la APIS para los diferentes type
        disponible.

        Params
            tipo : tipo de funcionalidad
        '''
        match tipo:
            case 'create_user'|'comicio':
                return 'POST'

            case 'edit_user':
                return 'PATCH'

            case 'login'|'health_check'|'get_users'|'get_comicio'|'get_comicios':
                return 'GET'

            case _ :
                raise ValueError(f'Type<{tipo}> para obtener el Metodo no existe')

    def request_method(self,tipo:str,*args,**kwargs):
        ''' OVER WRITE Metodo para obtener la funcion que se encarga de realizar 
        el request.

        Params
        type : tipo de funcionalidad
        '''

        match tipo:
            case 'create_user'|'comicio':
                return requests.post

            case 'edit_user':
                return requests.patch

            case 'login'|'health_check'|'get_users'|'get_comicio_id'|'get_comicios':
                return requests.get

            case _ :
                raise ValueError(f'Type<{tipo}> para obtener el Request Metodo no existe')

    def get_auth(self,tipo:str,*args,**kwargs) -> tuple:
        ''' OVER WRITE Metodo para obtener el auth de la APIS para los diferentes type
        disponible.

        Params
            tipo : tipo de funcionalidad
        '''
        match tipo:
            case 'create_user':
                return None

            case 'edit_user'|'login':
                return (self._contex['username'],self._contex['password'])

            case 'get_users'|'health_check'|'comicio'|'get_comicios'|'get_comicio_id':
                return (self._contex['token'],'notrelevant')

            case _ :
                raise ValueError(f'Type<{tipo}> para obtener el Auth no existe')

    def get_endpoint(self, tipo:str, *args, **kwargs)->str:
        ret:str = None
        match tipo:
            case 'create_user' | 'edit_user':
                ret = '/api/register'

            case 'get_users':
                ret = '/api/users'

            case 'login':
                ret = '/api/login'

            case 'health_check':
                ret = '/api/HealthCheck'

            case 'comicio':
                ret = '/api/comicio'

            case 'get_comicio':
                ret = '/api/get_comicio'

            case 'get_comicios':
                ret = '/api/get_comicios'

            case 'get_comicio_id':
                ret = '/api/get_comicio/' + kwargs.get('id','fac0179bf7a42e755e17bab20e51f2cd')

            case _:
                raise ValueError(f'Type<{tipo}> para obtener el End Point no existe')

        return Comicio.URL + ret

    def _get_payload_create_user(self)-> dict:
        ''' Metodo para obtener el payload relacionado a la creacion de un usuario.
        '''
        return {"username":self._contex['username'],"password":self._contex['password']}

    def _get_payload_edit_user(self)-> dict:
        ''' Metodo para obtener el payload relacionado a la edicion de un usuario.
        '''
        # hacemos el swap de claves
        return {"password":self._contex['new_password']}

    def _get_payload_comicio(self,path=None)-> dict:
        ''' Metodo para obtener el payload relacionado a la creacion de un comicio.
        '''
        if path is None :
            return self._contex['data']

        return jsonfile_to_dict(path)

    def get_headers(self,tipo:str,*args,**kwargs) -> str:
        '''Metodo para obtener el header de la respuestas
        Params
            tipo : tipo de verificacion, para todos los metodos usamos el mismo
            response : respuesta a verificar 

        Returns 
        - True : verificacion succes
        - False : verificacion failure
        '''
        return 'application/json'

    def _get_response_create_user(self)-> dict :
        ''' Metodo para obtener el response relacionado a la creacion de un user.
        '''
        return {'username':self._contex['username']}

    def _get_response_edit_user(self)-> dict :
        ''' Metodo para obtener el response relacionado a la edicion de un user.
        No interviene el access_token, este cambia al editar el user
        '''
        return { 'timeout': self._contex['timeout'], 'username':self._contex['username'] }

    def _get_response_get_user(self)-> dict :
        ''' Metodo para obtener el response relacionado a obtener la lista de user.
        No interviene el access_token, este cambia al editar el user
        '''
        return { "users": [self._contex['username']] }

    def _get_response_login(self)-> dict :
        ''' Metodo para obtener el response relacionado al Login.
        No interviene el access_token, este obtiene le nuevo Token
        '''
        return { 'timeout': self._contex['timeout'] }

    def _get_response_health_check(self)-> dict :
        ''' Metodo para obtener el response relacionado a la health_check.
        No interviene el access_token, este obtiene le nuevo Token
        '''
        return { "version": Comicio.APIsVERSION }

    def verify_headers(self,tipo:str,response:dict|str,*args,**kwargs) -> bool:
        '''OVER WRITE Metodo para realizar la verificacion de tipo de header 
        de la respuesta. Ya que para todos los response el header debe ser el mismo.

        Params
            tipo : tipo de verificacion, para todos los metodos usamos el mismo
            response : respuesta a verificar 

        Returns 
        - True : verificacion succes
        - False : verificacion failure
        '''
        return response.headers["Content-Type"] == 'application/json'

    def _verify_response_create_user(self,response,repeat=False):
        '''Metodo callback para verificar el response del typo ``create_user``

        Params
        response : objeto response
        
        Response Type: 
        1. Case Success: ```{ "username": "${username}" }```
        2. Usuario Ya Creado: ```{
            "code": 400,
            "message": "username <jesus> ya esta registrado"
        }```
        '''
        data = response.json()
        if not repeat:
            if 'username' in data:
                return data['username'] == self._contex['username']

            return False

        if 'username' in data :
            return data['username'] == self._contex['username']

        if not 'code' in data or data['code'] != 11:
            return False

        ## usuario ya creado
        if 'code' in data and data['code'] == 11:
            return True

        return True

    def _verify_response_edit_user(self,response):
        '''Metodo callback para verificar el response del tipo ``edit_user``

        Params
        response : objeto response, Response Type:
        ```
        {
            "access_token": "...",
            "timeout": 1800,
            "username": "jesus"
        }
        ```
        '''
        # 1° Verificamos que contenga todos los key
        dct_resp = response.json()
        if not all(key in dct_resp for key in ("access_token","timeout","username")):
            return False

        if len(dct_resp['access_token'])<10:
            return False

        if dct_resp['timeout'] != 1800:
            return False

        if dct_resp['username'] != self._contex['username']:
            return False

        self._contex['password'] = self._contex['new_password']
        self._contex['token'] = dct_resp['access_token']
        return True

    def _verify_response_get_users(self,response):
        '''Metodo callback para verificar el response del tipo ``edit_user``

        Params
        response : objeto response, Response Type:
        ```
        {
            "users": [
                "jesus"
            ]
        }
        ```
        '''
        # 1° Verificamos que contenga todos los key
        dct_resp = response.json()
        if not 'users' in dct_resp:
            self.log.debug('key users, not found in %s',dct_resp)
            return False

        ## recorremos la lista para buscar nuestro usuario
        if not self._contex['username'] in dct_resp['users']:
            self.log.debug('users<%s>, not found in %s',self._contex['username'],dct_resp)
            return False

        return True

    def _verify_response_login(self,response):
        '''Metodo callback para verificar el response del tipo ``edit_user``

        Params
        response : objeto response, Response Type:
        ```
        {
            "access_token": "...",
            "timeout": 1800,
            "username": "jesus"
        }
        ```
        '''
        # 1° Verificamos que contenga todos los key
        dct_resp = response.json()
        if not all(key in dct_resp for key in ("access_token","timeout","username")):
            return False

        if len(dct_resp['access_token']) < 10:
            return False

        # Almacenamos el token, para la session de test
        self._contex['token'] = dct_resp['access_token']
        if dct_resp['timeout'] != 1800:
            return False

        if dct_resp['username'] != self._contex['username']:
            return False

        return True

    def _verify_response_health_check(self,response):
        '''Metodo callback para verificar el response del tipo ``edit_user``

        Params
        response : objeto response, Response Type:
        ```
        {
            "version": "0.5.0"
        }
        ```
        '''
        # 1° Verificamos que contenga todos los key
        dct_resp = response.json()
        if not 'version' in dct_resp:
            self.log.debug('key version, not found in %s',dct_resp)
            return False

        if dct_resp['version'] != Comicio.APIsVERSION:
            return False

        return True

    def _verify_response_comicio(self,response):
        '''Metodo callback para verificar el response del tipo ``edit_user``

        Params
        response : objeto response, Response Type:
        ```
        {
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
        ```
        '''
        # 1° Verificamos que contenga todos los key
        dct_resp = response.json()
        if not all(key in dct_resp for key in ("comicios","id")):
            self.log.debug('keys:("comicios","id") not found in %s',dct_resp)
            return False

        if len(dct_resp['comicios']) < 1:
            self.log.debug('comicios len menor a uno, en %s',dct_resp)
            return False

        if len(dct_resp['id']) < 10:
            self.log.debug('ID de Comicio len menor a 10, en %s',dct_resp)
            return False

        dct_resp = dct_resp['comicios'][0]
        if not all(key in dct_resp for key in ("escanios","lista")):
            return False

        return True

    def _verify_response_get_comicios(self,response):
        '''
        Metodo callback para verificar el response del tipo ```edit_user```

        Params
        response : objeto response, Response    
        
        ```{
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
        ```
        '''
        # 1° Verificamos que contenga todos los key
        dct_resp = response.json()
        if not all(key in dct_resp for key in ("ids","user")):
            self.log.warning('keys:("ids","user") not found in %s',dct_resp)
            return False

        if dct_resp['user'] != self._contex['username']:
            return False

        self._contex['ids'] = dct_resp['ids']
        return True

    def _verify_response_get_comicio_id(self,response):
        '''
        Metodo callback para verificar el response del tipo ``edit_user``

        Params
        response : objeto response
        
         Response 
        ```{
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
        ```
        '''
        # 1° Verificamos que contenga todos los key
        dct_resp = response.json()
        if not all(key in dct_resp for key in ("date","id","request","response")):
            self.log.debug('keys <{("date","id","request","response")}> not found in resp: <%s>',
                           dct_resp)
            return False

        dct_req = dct_resp['request']
        # lista es opcional en el request
        #if not all(key in dct_req for key in ("escanios","listas","votos")):
        if not all(key in dct_req for key in ("escanios","votos")):
            self.log.debug('keys <"escanios","listas","votos"> not found in response/request: <%s>',
                           dct_req)
            return False

        dct_req = dct_resp['response']
        for r in dct_req:
            if not all(key in r for key in ("escanios","lista")):
                return False

        return True

    @property
    def contex(self)->dict:
        '''getter attribute contex'''
        return self._contex

# verificamos si este script es el principal invocado desde la linea de comandos
if __name__ == "__main__":
    print(f'Import Module "import {os.path.basename(__file__)[:-3]}" and use me!')
