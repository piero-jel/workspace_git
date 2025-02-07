#!/usr/bin/env python3
''' Brief
  Modulo python para relaizar test (no atumotizados) de las Apis, usando la libreria ``requests``
  

  Este script se puede invocar de forma opcional con un arguemento 
  numerico que representa el test_XXXX() a ejecutar.
  En caso de no aportar el mismo se ejecutara el default tabulado
  en la cariable global '__VERSION__'. 
'''
import traceback


__VERSION__ : int = 0

## def constantes Globales
IP:str    = '127.0.0.1'
PORT:str  = '8080'
TOKEN:str = None


def dict_to_jsonfile(data:dict,filename:str,tab:int=2) -> None:
  ''' Dictionary dump to file JSON.

  Params
    - data    : dict, data to dump in file
    - filename: str, path/file del archivo
    - tab     : identation for dump
  '''
  import json

  with open(filename, 'w') as file2write:
    json.dump(data, file2write,indent=tab) 
# end def

def jsonfile_to_dict(path:str) -> dict|list:
  ''' Load json file in dict

  Params
    - path: str, path/file del archivo

  Returns
    Dict con el json, si el archivo no existe retornara None
  '''  
  from pathlib import Path
  import json
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

''' BEGIN TEST FUNCTIONs '''
def test_get_comicio_id(id='fac0179bf7a42e755e17bab20e51f2cd'):
  ''' 
  Test Obtener Comicio publicado, por id.

  Params
    id : Opcional (id = 'fac0179bf7a42e755e17bab20e51f2cd') id del comicio a localizar
  
  '''
  import requests # import para manejo de APIs Rest
  import json
  
  url=f'http://{IP}:{PORT}/api/get_comicio/'
    
  if(TOKEN == None or not 'access_token' in TOKEN):
    return 0
  #endif
  '''
    "fac0179bf7a42e755e17bab20e51f2cd",
    "05df7faa91a18f39b46b3d821d66e88f",
    "03a60fcdb024e0230b081e3c311ca99c"
  '''
  id:str = id
  
  auth_tkn = (TOKEN['access_token'],'notrelevant')
  print(f'Comicios Registrado con el id:<{id}>, username <{TOKEN["username"]}>\n')
  response = requests.get( url+id
                         , auth=auth_tkn                         
                         )  
  print(f'Resp Code: {response.status_code}')
  
  if( not 200 <= response.status_code <= 210 ):
    return 0
  
  response = response.json()  
  print(f'Resp JSON:\n{ json.dumps(response,indent=2) }')    
  return 0
# end def test_07()

def test_get_comicios():
  '''
  Test Obtener todos los comicios registrado para el usuario actual.

  '''
  import requests # import para manejo de APIs Rest
  import json
  
  url=f'http://{IP}:{PORT}/api/get_comicios'
    
  if(TOKEN == None or not 'access_token' in TOKEN):
    return 0
  #endif
   
  auth_tkn = (TOKEN['access_token'],'notrelevant')
  print(f'Los comicios registrado para el usuario <{TOKEN["username"]}>\n')

  response = requests.get( url           
                         , auth=auth_tkn                         
                         )  
  print(f'Resp Code: {response.status_code}')
  
  if( not 200 <= response.status_code <= 210 ):
    return 0
  
  response = response.json()  
  print(f'Resp JSON:\n{ json.dumps(response,indent=2) }')    
  return 0
# end def test_06()

def test_post_comicio(path='in/post_comicio_01.json'):
  ''' 
  Test Publicar comicio

  Params
    - path : Opcional (default 'in/post_comicio_01.json'),ruta al archivo con el request json para publicar un comicio.

  '''
  import requests # import para manejo de APIs Rest
  import json
  
  url=f'http://{IP}:{PORT}/api/comicio'
  jsonfile = 'in/post_comicio_01.json'
  
  if(TOKEN == None or not 'access_token' in TOKEN):
    print(f'No contamos con Token para realizar la peticion')
    return 0
  #endif
  payload:dict = jsonfile_to_dict(jsonfile)
  if(payload is None):
    raise ValueError(f'Archivo <{jsonfile}> not found')
  #endif

  print(f'Publicar comicio, File: {jsonfile} | username <{TOKEN["username"]}> | Payload:\n{json.dumps(payload,indent=2)}\n')
  auth_tkn = (TOKEN['access_token'],'notrelevant')
  response = requests.post( url
                          , json=payload
                          , auth=auth_tkn              
                         )  
  print(f'Resp Code: {response.status_code}')
  
  if( not 200 <= response.status_code <= 210 ):
    return 0
  
  response = response.json()  
  print(f'Resp JSON:\n{ json.dumps(response,indent=2) }')
  return 0
# end def test_05()

def test_health_check():
  '''
  Test Health Check, esta funcion utiliza el token obtenido
  en el login o al editar el usuario.

  '''
  import requests # import para manejo de APIs Rest
  import json
  
  url=f'http://{IP}:{PORT}/api/HealthCheck'

  if(TOKEN == None or not 'access_token' in TOKEN):
    print(f'No contamos con Token para realizar la peticion')
    return 0
  #endif   
  
  auth_tkn = (TOKEN['access_token'],'notrelevant')
  print(f'Health Check, username <{TOKEN["username"]}>\n')
  response = requests.get( url           
                         , auth=auth_tkn
                         )  
  print(f'Resp Code: {response.status_code}')
  
  if( not 200 <= response.status_code <= 210 ):
    return 0
  
  resp = response.json()  
  print(f'Resp JSON:\n{ json.dumps(resp,indent=2) }')  
  return 0
# end def test_04()
  
def test_login(user='jel',key='789ABC123'):
  '''
  Test Login, para que nos permite obtener el token para el usuairo
  
  Params
    - user    : Opcional (default 'jel'), Nombre de usuario, 
    - key     : Opcional (default '123ABC789'), keypass actual

  '''
  import requests # import para manejo de APIs Rest
  import json
  
  url=f'http://{IP}:{PORT}/api/login'
  username:str = user
  password:str = key
  
  auth_user = (username,password)
  print(f'Login User {username}, auth:\n{auth_user}\n')

  response = requests.get( url                         
                         , auth=auth_user
                         )  
  print(f'Resp Code: {response.status_code}')
  
  if( not 200 <= response.status_code <= 210 ):
    return 0
  #endif
  # Si el estado es difetenete al rango, no tenemos body de respuesta
  resp = response.json()  
  print(f'Resp JSON:\n{ json.dumps(resp,indent=2) }')    
  if('access_token' in resp):
    '''Almacenamos el token'''    
    global TOKEN
    TOKEN=resp
  #endif
  return 0
# end def test_03()

def test_get_users():
  '''
  Test Obtener el listado actual de usuarios, este usa el archivo de token
  previamente creado al realizar el login o editar el usuario.

  '''
  import requests # import para manejo de APIs Rest
  import json
  
  url=f'http://{IP}:{PORT}/api/users'
  if(TOKEN == None or not 'access_token' in TOKEN):
    return 0
  #endif
  
  auth_tkn = (TOKEN['access_token'],'notrelevant')
  print(f'Get users, listado actual de usuarios, auth:\n{auth_tkn}\n')
  response = requests.get( url                         
                         , auth=auth_tkn
                         )  
        
  print(f'Resp Code: {response.status_code}')
  
  if( not 200 <= response.status_code <= 210 ):
    return 0
  # si el estado es difetenete al rango, no tenemos body de respuesta
  resp = response.json()  
  print(f'Resp JSON:\n{ json.dumps(resp,indent=2) }')
  return 0
# end def test_02()

def test_edit_user(user='jel',key='123ABC789',new_key='789ABC123'):
  '''
  Test Edit User, obtiene un nuevo token para el uaurio modificado

  Params
    - user    : Opcional (default 'jel'), Nombre de usuario, 
    - key     : Opcional (default '123ABC789'), keypass actual
    - new_key : Opcional (default '789ABC123'), nuevo keypass

  '''  
  import requests # import para manejo de APIs Rest
  import json
  
  
  url=f'http://{IP}:{PORT}/api/register'

  # valor actual de password p/el usuario
  username:str = user
  password:str = key

  payload = { "password": new_key}
  
  print(f'Editando el Usaurio <{username}>, con el payload\n{payload}')

  response = requests.patch ( url
                            , json=payload
                            , auth=(username,password)
                            )
  print(f'Resp Code: {response.status_code}')
  
  if( not 200 <= response.status_code <= 210 ):
    return 0
  
  resp = response.json()
  if('access_token' in resp):
    '''Almacenamos el token'''
    print(f'Resp JSON:\n{ json.dumps(resp,indent=2) }')
    global TOKEN
    TOKEN=resp
  #endif
  return 0
# end def test_01()

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
  import requests # import para manejo de APIs Rest
  import json
  
  url=f'http://{IP}:{PORT}/api/register'

  payload = { "username": user
            , "password": key
            }
  print(f'Creando el usuario con el payload:\n {payload}')
  response = requests.post( url
                          , json=payload
                          )
  print(f'Resp Code: {response.status_code}')
  print(f'Resp JSON:\n{ json.dumps(response.json(),indent=2) }')
  return 0
# end def test_00()

def test_help(opt=None):
  '''
  Funcion que lista todos los test disponibles en este modulo.

  Params
    opt Opcional (default None) opcion para especificar formato del help
      --short o -s impresion corta.
  '''
  import os,inspect,sys
  from collections import namedtuple

  
  app_path:str = os.path.basename(__file__)
  Target = namedtuple('Target', ('type','msg'))

  ## en caso de que los comentarios docstring de cada funcion se elimines dejamos estos.
  lst_test_case:list = [
      Target('create_user'   , 'Creacion de un nuevo usuario.')
    , Target('edit_user'     , 'Edit User, obtiene un nuevo token para el uaurio modificado.')
    , Target('get_users'     , 'Obtener el listado actual de usuarios.')
    , Target('login'         , 'Login, obtiene nuevo token para el usuario.')
    , Target('health_check'  , 'Health Check, con la version actual de la api.')
    , Target('post_comicio'  , 'Publicar comicio.')
    , Target('get_comicios'  , 'Obtener todos los comicios registrado para el usuario.')
    , Target('get_comicio_id', 'Obtener Comicio por id.')
    , Target('help'          , 'Visualiza este mensaje de ayuda.')
  ]
  print(f'Listado de test para el modulo: "{app_path}"\n')

  if(opt is not None and opt == '--short' or opt == '-s'):
    for it in lst_test_case:
      tmp = it.type + ' [-q | --quiet]'
      print(f'{app_path} {tmp:32s} : {it.msg}')
    #endfor
    print('')
    return 
  #endif
  for it in lst_test_case:
    name_func = f'test_{it.type}'
    def predicado(obj):  
      if(not inspect.isfunction(obj)):
        return False    
      return True if obj.__name__ == name_func else False
    #endif  
    func = inspect.getmembers(sys.modules[__name__],predicado)[0][1]
    print(f'{app_path} {it.type} [-q | --quiet]',end='')
    if(func is not None and hasattr(func, '__doc__') and  func.__doc__ is not None and func.__doc__.strip()):
      print(func.__doc__)
    else:
      print(f': {it.msg}')
    #endif    
  #endfor
  print('\n')  
#enddef
''' END   TEST FUNCTIONs '''

class ExceptionRun(Exception):
  '''Tipo de exepcion para ser capturada y controladas en el llamado a las funcion de 
  test. Y evitar orientar al usuario sobre lo sucedido, sin la necesidad de mostrar
  el traceback con informacion inecesaria. Ya que el error debe ser del tipo de parametros
  aportados a la hora de invocar el script.
  '''
  pass
#enclass

def main():
  '''Funcion principal del modulo tiny_template.py'''
  import sys
  import inspect
  import requests # import para manejo de APIs Rest
  def get_orden(val:int)-> tuple:
    if(isinstance(val,str)):
      return (val,len(val))
    if(val <= 1):
      return (1,1)
    #endif
    ret = 1
    ndig = 1
    while(val > 1):
      val = val / 10          
      ret *= 10
      ndig += 1
      if(val < 10):
        break
    #endwhile
    return (ret,ndig)
  #enddef

  try:
    ver:int = __VERSION__
    argv:list = None
    argc:int  = len(sys.argv)
    quiet:bool = False
    
    if(argc > 1):
      v = sys.argv[1]
      if(v.isdigit()):
        ver = int(v)
      else:
        ver = v
      #endif      
    #endif
    if(argc > 2):
      if(sys.argv[2] == '-q' or sys.argv[2] == '--quiet'):
        quiet=True
        argv = None if not argc > 3 else sys.argv[3:]
      else:
        argv = sys.argv[2:]
      #endif      
    #endif

    nord,ndig = get_orden(ver)
    #print(f'nord: {nord} | ndig: {ndig}')
    if(nord == 1 and ndig == 1):      
      ndig +=1
    #endif
    if(isinstance(ver,int)):
      name_func = f'test_{ver:0{ndig}}'
    else:
      name_func = 'test_'+ ver
    #endif

    def predicado(obj):  
      if(not inspect.isfunction(obj)):
        return False    
      return True if obj.__name__ == name_func else False
    #endif
    def print_doc(o_fn):
      '''Funcion para imprimir el doc string de una tupla (name,function), en caso
      de no poseer doc string imprime el name con un leyenda.

      Params
        o_fn : tupla del tipo (name,function)

      '''
      if(quiet):
        return
      if(not isinstance(o_fn,tuple)):        
        return ''
      #endif
      if(hasattr(o_fn[1], '__doc__') and o_fn[1].__doc__ is not None and o_fn[1].__doc__.strip()):
        print(o_fn[1].__doc__)
      else:
        print(f'function locate {o_fn[0]}(), run:\n')
      #endif
    #enddef

    ''' obj_func
      obj_func[0] : nombre de la funcion 
      obj_func[1] : objeto function
    '''
    lst_obj_func = inspect.getmembers(sys.modules[__name__],predicado)
    if(lst_obj_func is None or len(lst_obj_func) < 1):
      print(f'function <{name_func}()> Not Found')
      return 0
    #endif
    #     
    '''Verificamos si la funcion a llamar recibe parametros o no'''
    in_args = inspect.getfullargspec(lst_obj_func[0][1])
    #print(f'in_args: {in_args}')
    in_argc = len(in_args.args)
    len_defaults = len(in_args.defaults) if in_args.defaults else 0
    if( in_argc > 0 or in_args.varargs is not None or in_args.varkw is not None):
      '''En caso que admita un solo parametro debemos llamarla con el index 0'''
      if( in_argc == 1):
        if(argv is not None and len(argv) > 1):
          raise ExceptionRun(f'La funcion {lst_obj_func[0][0]}(), admite un solo parametro <{in_args.args[0]}>, y se esta intentando pasar el siguente conjunto: {argv}')
        #endif
        if(argv is None and len_defaults != 1):
          raise ExceptionRun(f'La funcion {lst_obj_func[0][0]}(), espera un solo parametro <{in_args.args[0]}>, y no se esta pasando el mismo.')
        #endif
        print_doc(lst_obj_func[0])
        if(argv is None):
          return lst_obj_func[0][1]()  
        #endif
        return lst_obj_func[0][1](argv[0])
      #endif
      if(argv is None and len_defaults != in_argc ):
        '''No tenemos argumentos pasados y la funcion admite almenos un parametro que no default'''
        raise ExceptionRun(f'La funcion {lst_obj_func[0][0]}(), espera los parametro <{in_args.args}>, y no se esta pasando los mismos.')
      #endif
      ##
      if(in_argc > 0 and (argv is None or in_argc != len(argv)) and (len_defaults-in_argc) < 0):
        raise ExceptionRun(f'Error con los Argumentos al intentar llamar a la funcion <{lst_obj_func[0][0]}()>, que admite los paramtros <{in_args.args}> y se intenta pasar <{argv}>')
      #endif
      if(argv is None):
        print_doc(lst_obj_func[0])
        return lst_obj_func[0][1]()
      #endif
      print_doc(lst_obj_func[0])
      return lst_obj_func[0][1](*argv)          
    #endif
    print_doc(lst_obj_func[0])
    return lst_obj_func[0][1]()
  except AttributeError as err:
    print(f'AttributeError : {err}\nTRACEBACK:{traceback.format_exc()}')
    
  except TypeError as err:
    print(f'TypeError : {err}\nTRACEBACK:{traceback.format_exc()}')
    
  except NameError as err:      
    print(f'NameError : {err}\nTRACEBACK:{traceback.format_exc()}')
    
  except SyntaxError as err:
    print(f'SyntaxError : {err}\nTRACEBACK:{traceback.format_exc()}')
  
  except ExceptionRun as e:
    print(f'ExceptionRun al intentar ejecutar la funcion:\n\n{e}\n')

  except requests.exceptions.ConnectionError as e:
    print(f'Error de conexion: {e}')    
  except Exception as e:    
    print(f'Exception Type {type(e)}\nTRACEBACK:{traceback.format_exc()}')

  except KeyboardInterrupt:
    print('KeyboardInterrupt, end program')

  except: 
    ''' la clausula except sin arg debe quedar siempre al final '''
    print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')    
  # end try
#enddef
  
''' verificamos si este script es el principal
    invocado desde la linea de comandos
'''
if (__name__ == "__main__"):
  if(TOKEN == None):
    TOKEN = jsonfile_to_dict('ou/token.json')
  #endif
  main()
  if(TOKEN is not None):
    #print(f'save TOKEN: {TOKEN}')
    dict_to_jsonfile(TOKEN,'ou/token.json')
  #endif
# end if
  
