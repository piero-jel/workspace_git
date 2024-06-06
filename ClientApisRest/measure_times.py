#!/bin/python3
import traceback
''' Decorator functions con @functools.wraps del modulo functools 
      - Apliaction ex timing mesure in func
'''
import functools
import timeit
import json

RANGO_MAX:int = 25


def timer(func):
  ''' Decorator Function para calcular e imprimir el tiempo que tardo en 
      ejecutarse la funcion decorada
        - func funcion decoradora con @timer
  '''
  @functools.wraps(func)
  def wrapper_timer(*args, **kwargs):
    start_time = timeit.default_timer()
    value = func(*args, **kwargs)
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    print(f"Finished {func.__name__}() in {run_time:.4f} secs")
    return value
  # end def
  return wrapper_timer
# end def

def dump_file(path:str,mode:str='w'):
  ''' Decorator Function para volcar la respuesta del
      llamado a una funcion sobre un archivo.      
        - path: ruta del archivo donde se volara la info
          de la devoluccion de la funcion decoradora con @dump_file('path/file')
        
        El dato que devuelve la funcion decoradora para la aplicacion, debe ser:
          - str
          - list
          - dict
  '''
  def dump_file_decorator(func):
    @functools.wraps(func)
    def wrapper_dump_file(*args, **kwargs):      
      value = func(*args, **kwargs)
      match type(value).__name__:
        case 'str':
          with open(path,mode) as file2write:
            file2write.write(value)

        case 'int':
          with open(path,mode) as file2write:
            file2write.write(value)            

        case 'list':
          with open(path,mode) as file2write:
            file2write.write(json.dumps(value,indent=2))

        case 'dict':
          with open(path,mode) as file2write:
            file2write.write(json.dumps(value,indent=2))
      #end with
      return value
    # end def
    return wrapper_dump_file
  # end def
  return dump_file_decorator
# end def

@dump_file('logs/RequestSequential.log')
@timer
def RequestSequential(urls:list) -> list:
  from RequestSequential import download_data  
  return download_data(urls)
# end def

@dump_file('logs/RequestThreadPool.log')
@timer
def RequestThreadPool(urls:list) -> list:
  from RequestThreadPool import download_data
  return download_data(urls)  
# end def

@dump_file('logs/RequestAnsync.log')
@timer
def RequestAnsync(urls:list) -> list:
  from RequestAnsync import download_data  
  return download_data(urls)  
# end def

try:
  url_base:str = 'https://jsonplaceholder.typicode.com/posts/{}'
  urls:list = [url_base.format(post) for post in range(1, RANGO_MAX+1)]
  urls.append('https://not-found-url/1')
  urls.append('http://not-found-url/2')
  
  
  print('Test RequestSequential()')
  RequestSequential(urls)

  print('\n\nTest RequestThreadPool()')
  RequestThreadPool(urls)

  print('\n\nTest RequestAnsync()')
  RequestAnsync(urls)

  
except Exception as e:    
  print(f'Exception Type {type(e)}\nTRACEBACK:{traceback.format_exc()}')

except KeyboardInterrupt:
  print('End request for current user')

except: 
  ''' la clausula except sin arg debe quedar siempre al final '''
  print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')    
# end try
