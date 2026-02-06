#!/usr/bin/env python3
''' Brief
  Modulo python para relaizar test (no atumotizados) de las Apis, usando la libreria ``requests``
  

  Este script se puede invocar de forma opcional con un arguemento 
  numerico que representa el test_XXXX() a ejecutar.
  En caso de no aportar el mismo se ejecutara el default tabulado
  en la cariable global '__VERSION__'. 
'''
import os
import inspect
import sys
from collections import namedtuple
import traceback
import json
import requests # import para manejo de APIs Rest



from utils import ( # pylint: disable=import-error
    dict_to_jsonfile,jsonfile_to_dict,
    Logger,get_log,CURR_DIR
)

__VERSION__ : int = 0

## def constantes Globales
IP:str    = '127.0.0.1'
PORT:str  = '8080'
TOKEN:str = None
TIMEOUT:int = 20

TOKEN_FILE_PATH:str = CURR_DIR + '/ou/token.json'


class ExceptionRun(Exception):
    '''Tipo de exepcion para ser capturada y controladas en el llamado a las funcion de 
    test. Y evitar orientar al usuario sobre lo sucedido, sin la necesidad de mostrar
    el traceback con informacion inecesaria. Ya que el error debe ser del tipo de parametros
    aportados a la hora de invocar el script.
    '''
    #pass

## BEGIN TEST FUNCTIONs
def test_get_comicio_id(id_hash:str='fac0179bf7a42e755e17bab20e51f2cd'):
    ''' 
    Test Obtener Comicio publicado, por id.

    Params
        id : Opcional (id = 'fac0179bf7a42e755e17bab20e51f2cd') id del comicio a localizar
    
    '''
    url=f'http://{IP}:{PORT}/api/get_comicio/'
    if TOKEN is None or not 'access_token' in TOKEN:
        return 0

    auth_tkn = (TOKEN['access_token'],'notrelevant')
    log:Logger = get_log('test_get_comicio_id')
    log.debug(f'Comicios Registrado con el id:<{id_hash}>, username <{TOKEN["username"]}>')
    response:requests.Response = None
    try:
        response = requests.get( url+id_hash, auth=auth_tkn,timeout=TIMEOUT)
    except Exception as e: # pylint: disable=broad-exception-caught
        log.error('Error en el request, detalle %s',e)
        return 0

    log.info('Resp Code: %s',response.status_code)

    if not 200 <= response.status_code <= 210:
        log.warning('Resp Code fuera del rango OK, response: %s',response)
        return 0

    response = response.json()
    log.info('Resp JSON:\n%s',json.dumps(response,indent=2))
    return 0


def test_get_comicios():
    '''
    Test Obtener todos los comicios registrado para el usuario actual.

    '''
    url = f'http://{IP}:{PORT}/api/get_comicios'

    if TOKEN is None or not 'access_token' in TOKEN:
        return 0

    log:Logger = get_log('test_get_comicios')
    auth_tkn = (TOKEN['access_token'],'notrelevant')
    log.info('Los comicios registrado para el usuario <%s>',TOKEN["username"])

    response:requests.Response = None
    try:
        response = requests.get( url, auth=auth_tkn,timeout=TIMEOUT)
    except Exception as e: # pylint: disable=broad-exception-caught
        log.error('Error en la petion, detalle %s',e)
        return 0

    log.info('Resp Code: %s',response.status_code)

    if not 200 <= response.status_code <= 210 :
        log.warning('Resp Code fuera del rango OK, response: %s',response)
        return 0

    log.info('Resp JSON:\n%s',json.dumps(response.json(),indent=2))
    return 0


def test_post_comicio(path:str=None):
    ''' 
    Test Publicar comicio

    Params
        - path : Opcional (default 'in/post_comicio_01.json'),ruta al archivo con el
        request json para publicar un comicio.

    '''
    url=f'http://{IP}:{PORT}/api/comicio'
    log:Logger = get_log('test_post_comicio')
    if path is None:
        path = CURR_DIR + '/in/post_comicio_01.json'

    if TOKEN is None or not 'access_token' in TOKEN:
        log.warning('No contamos con Token para realizar la peticion')
        return 0

    payload:dict = jsonfile_to_dict(path)
    if payload is None:
        raise ValueError(f'Archivo <{path}> not found')


    log.info('Publicar comicio, File: %s | username <%s> | Payload:\n%s',
             path,TOKEN["username"],json.dumps(payload,indent=2))

    auth_tkn = (TOKEN['access_token'],'notrelevant')
    response:requests.Response = None
    try:
        response = requests.post( url,json=payload,auth=auth_tkn,timeout=TIMEOUT)
    except Exception as e: # pylint: disable=broad-exception-caught
        log.error('Error en la peticion, detalle %s',e)
        return 0
    log.info('Resp Code: %s',response.status_code)

    if not 200 <= response.status_code <= 210:
        log.warning('Resp Code fuera del rango OK, response: %s',response)
        return 0

    response = response.json()
    log.info('Resp JSON:\n%s',json.dumps(response,indent=2))
    return 0


def test_health_check():
    '''
    Test Health Check, esta funcion utiliza el token obtenido
    en el login o al editar el usuario.

    '''
    url=f'http://{IP}:{PORT}/api/HealthCheck'
    log:Logger = get_log('test_health_check')

    if TOKEN is None or not 'access_token' in TOKEN:
        log.warning('No contamos con Token para realizar la peticion')
        return 0

    auth_tkn = (TOKEN['access_token'],'notrelevant')
    log.info('Health Check, username <%s>',TOKEN["username"])
    response:requests.Response = None
    try:
        response = requests.get( url,auth=auth_tkn,timeout=TIMEOUT)
    except Exception as e:# pylint: disable=broad-exception-caught
        log.error('Error en la peticion, detalle %s',e)
        return 0

    log.info('Resp Code: %s',response.status_code)

    if not 200 <= response.status_code <= 210 :
        log.warning('Resp Code fuera del rango OK, response: %s',response)
        return 0

    resp = response.json()
    log.info('Resp JSON:\n%s',json.dumps(resp,indent=2))
    return 0


def test_login(user='jel',key='789ABC123'):
    '''
    Test Login, para que nos permite obtener el token para el usuairo
    
    Params
        - user    : Opcional (default 'jel'), Nombre de usuario, 
        - key     : Opcional (default '123ABC789'), keypass actual

    '''
    url=f'http://{IP}:{PORT}/api/login'
    log:Logger = get_log('test_login')
    auth_user = (user,key)
    log.info('Login User %s, auth:%s',user,auth_user)
    response:requests.Response = None
    try:
        response = requests.get( url,auth=auth_user,timeout=TIMEOUT)
    except Exception as e:# pylint: disable=broad-exception-caught
        log.error('Error en la peticion, detalle: %s',e)
        return 0

    log.info('Resp Code: %s',response.status_code)

    if not 200 <= response.status_code <= 210 :
        log.warning('Resp Code fuera del rango OK, response %s',response)
        return 0

    # Si el estado es difetenete al rango, no tenemos body de respuesta
    resp = response.json()
    log.info('Resp JSON:\n%s',json.dumps(resp,indent=2))

    if  'access_token' in resp:
        # Almacenamos el token
        global TOKEN # pylint: disable=global-statement
        TOKEN=resp

    return 0


def test_get_users():
    '''
    Test Obtener el listado actual de usuarios, este usa el archivo de token
    previamente creado al realizar el login o editar el usuario.

    '''
    url=f'http://{IP}:{PORT}/api/users'
    if  TOKEN is None or not 'access_token' in TOKEN:
        return 0

    log:Logger = get_log('test_get_users')
    auth_tkn = (TOKEN['access_token'],'notrelevant')
    log.info('Get users, listado actual de usuarios, auth: %s',auth_tkn)
    response:requests.Response = None
    try:
        response = requests.get( url,auth=auth_tkn,timeout=TIMEOUT)
    except Exception as e:# pylint: disable=broad-exception-caught
        log.error('Error en la peticion, detalle: %s',e)
        return 0

    log.info('Resp Code: %s',response.status_code)

    if not 200 <= response.status_code <= 210:
        log.warning('Resp Code fuera del rango OK')
        return 0

    # si el estado es difetenete al rango, no tenemos body de respuesta
    resp = response.json()
    log.info('Resp JSON:\n%s',json.dumps(resp,indent=2))
    return 0


def test_edit_user(user='jel',key='123ABC789',new_key='789ABC123'):
    '''
    Test Edit User, obtiene un nuevo token para el uaurio modificado

    Params
        - user    : Opcional (default 'jel'), Nombre de usuario, 
        - key     : Opcional (default '123ABC789'), keypass actual
        - new_key : Opcional (default '789ABC123'), nuevo keypass

    '''
    url=f'http://{IP}:{PORT}/api/register'

    # valor actual de password p/el usuario
    payload = { "password": new_key}
    log:Logger = get_log('test_edit_user')

    log.info('Editando el Usuario <%s>, con el payload <%s>',user,payload)

    response:requests.Response = None
    try:
        response = requests.patch(url,json=payload, auth=(user,key),timeout=TIMEOUT)
    except Exception as e:# pylint: disable=broad-exception-caught
        log.error('Error en la peticion, detalle: %s',e)
        return 0


    if not 200 <= response.status_code <= 210:
        log.warning('Resp Code %s Fuera del rango, detalle:\n%s',
                    response.status_code,response)
        return 0

    log.info('Resp Code: %s',response.status_code)
    resp = response.json()
    if 'access_token' in resp:
        # Almacenamos el token
        log.info('Resp JSON:\n%s',json.dumps(resp,indent=2))
        global TOKEN # pylint: disable=global-statement
        TOKEN=resp

    return 0


def test_create_user(user='jel',key='123ABC789'):
    ''' 
    Test Create User

    Params:
        - user : Opcional, por defecto 'jel', Nombre de usario
        - key  : Opcional, por defecto '123ABC789', clave para el usuario

    Example:
        ```
        # -q modo silencioso
        test_With_request.py create_user -q jesus 4321
        ```
    '''
    url=f'http://{IP}:{PORT}/api/register'
    payload = { "username": user, "password": key}
    log:Logger = get_log('test_create_user')
    log.info('Creando el usuario con el payload: %s',payload)

    response:requests.Response = None
    try:
        response = requests.post( url,json=payload,timeout=TIMEOUT)
    except Exception as e:# pylint: disable=broad-exception-caught
        log.error('Error en la peticion, detalle: %s',e)
        return 0

    log.info('Resp Code: %s',response.status_code)
    log.info('Resp JSON:\n%s',json.dumps(response.json(),indent=2))
    return 0


def test_help(opt=None)->int:
    '''
    Funcion que lista todos los test disponibles en este modulo.
  
    Params
      opt Opcional (default None) opcion para especificar formato del help
        --short o -s impresion corta.
    '''
    app_path:str = os.path.basename(__file__)
    Target = namedtuple('Target', ('type','msg'))

    ## en caso de que los comentarios docstring de cada funcion se elimines dejamos estos.
    lst_test_case:list = [
        Target('create_user'   , 'Creacion de un nuevo usuario.'),
        Target('edit_user'     , 'Edit User, obtiene un nuevo token para el uaurio modificado.'),
        Target('get_users'     , 'Obtener el listado actual de usuarios.'),
        Target('login'         , 'Login, obtiene nuevo token para el usuario.'),
        Target('health_check'  , 'Health Check, con la version actual de la api.'),
        Target('post_comicio'  , 'Publicar comicio.'),
        Target('get_comicios'  , 'Obtener todos los comicios registrado para el usuario.'),
        Target('get_comicio_id', 'Obtener Comicio por id.'),
        Target('help'          , 'Visualiza este mensaje de ayuda.')
    ]
    print(f'Listado de test para el modulo: "{app_path}"\n')

    if(opt is not None and opt == '--short' or opt == '-s'):
        for it in lst_test_case:
            tmp = it.type + ' [-q | --quiet]'
            print(f'{app_path} {tmp:32s} : {it.msg}')

        print('')
        return 0

    for it in lst_test_case:
        name_func = f'test_{it.type}'
        def predicado(obj,nf=name_func)->bool:
            if not inspect.isfunction(obj):
                return False
            return obj.__name__ == nf

        func = inspect.getmembers(sys.modules[__name__],predicado)[0][1]
        print(f'{app_path} {it.type} [-q | --quiet]',end='')
        if func is not None and hasattr(func, '__doc__') and \
                func.__doc__ is not None and func.__doc__.strip():
            print(func.__doc__)
        else:
            print(f': {it.msg}')


    print('\n')
## END   TEST FUNCTIONS





def main()->int:
    '''Funcion principal del modulo tiny_template.py'''
    try:
        name_func:str = 'test_'
        argv:list = None
        argc:int  = len(sys.argv)
        quiet:bool = False

        if argc > 1:
            name_func += sys.argv[1]

        if argc > 2:
            if sys.argv[2] == '-q' or sys.argv[2] == '--quiet':
                quiet=True
                argv = None if not argc > 3 else sys.argv[3:]
            else:
                argv = sys.argv[2:]


        def predicado(obj):
            if not inspect.isfunction(obj):
                return False

            return obj.__name__ == name_func


        lst_obj_func = inspect.getmembers(sys.modules[__name__],predicado)
        if lst_obj_func is None or len(lst_obj_func) < 1:
            print(f'function <{name_func}()> Not Found')
            return 0

        # Verificamos si la funcion a llamar recibe parametros o no
        in_args = inspect.getfullargspec(lst_obj_func[0][1])
        #print(f'in_args: {in_args}')
        in_argc = len(in_args.args)
        len_defaults = len(in_args.defaults) if in_args.defaults else 0
        #if in_argc > 0 or in_args.varargs is not None or in_args.varkw is not None:
        if (in_argc == 0 and in_args.varargs is None and in_args.varkw is None) or argv is None:
            print_doc(lst_obj_func[0],quiet)
            return lst_obj_func[0][1]()

        # En caso que admita un solo parametro debemos llamarla con el index 0
        if in_argc == 1:
            if argv is not None and ( len(argv) > 1 or len_defaults != 1):
                msg:str = f'La funcion {lst_obj_func[0][0]}(), admite un solo parametro' \
                            f' <{in_args.args[0]}>,'
                if len_defaults != 1:
                    msg += 'y no se esta pasando el mismo.'
                else:
                    msg += f'y se esta intentando pasar el siguente conjunto: {argv}'

                raise ExceptionRun(msg)


            print_doc(lst_obj_func[0],quiet)
            if argv is None:
                return lst_obj_func[0][1]()

            return lst_obj_func[0][1](argv[0])

        if argv is None and len_defaults != in_argc:
            # No tenemos argumentos pasados y la funcion admite almenos un parametro que no default
            raise ExceptionRun(f'La funcion {lst_obj_func[0][0]}(), espera los parametro ' \
                               f'<{in_args.args}>, y no se esta pasando los mismos.')

        if out_of_range(in_argc,argv,len_defaults):
            raise ExceptionRun('Error con los Argumentos al intentar llamar a la funcion ' \
                               f'<{lst_obj_func[0][0]}()>, que admite los paramtros ' \
                               f'<{in_args.args}> y se intenta pasar <{argv}>')

        print_doc(lst_obj_func[0],quiet)
        return lst_obj_func[0][1](*argv)

    except Exception as e: # pylint: disable=broad-exception-caught
        print(f'Exception Type {type(e).__name__}\nTRACEBACK:{traceback.format_exc()}')

    except: # pylint: disable=bare-except
        # la clausula except sin arg debe quedar siempre al final
        print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')

    return 1



def print_doc(o_fn,quiet:bool=False)->None:
    '''Funcion para imprimir el doc string de una tupla (name,function), en caso
    de no poseer doc string imprime el name con un leyenda.

    Params
        o_fn : tupla del tipo (name,function)

    '''
    if quiet or not isinstance(o_fn,tuple):
        return

    if hasattr(o_fn[1], '__doc__') and o_fn[1].__doc__ is not None and \
            o_fn[1].__doc__.strip():
        print(o_fn[1].__doc__)
    else:
        print(f'function locate {o_fn[0]}(), run:\n')


def out_of_range(in_argc:int,argv:list,len_defaults:int)->bool:
    '''
    funcion que verifica si los parametros apportados estan fuera de rango 
    
    :param in_argc: Description
    :type in_argc: int
    :param argv: Description
    :type argv: list
    :param len_defaults: Description
    :type len_defaults: int
    :return: Description
    :rtype: bool
    '''
    if in_argc <= 0 :
        return False

    if argv is not None and in_argc == len(argv):
        return False

    if len_defaults-in_argc >= 0:
        return False

    return True



# verificamos si este script es el principal invocado desde la linea de comandos
if __name__ == "__main__":
    if TOKEN is None:
        TOKEN = jsonfile_to_dict(TOKEN_FILE_PATH)

    st:int = main()

    if st == 0 and TOKEN is not None:
        dict_to_jsonfile(TOKEN,TOKEN_FILE_PATH)
