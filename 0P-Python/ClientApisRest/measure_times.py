''' Decorator functions con @functools.wraps del modulo functools 
      - Apliaction ex timing mesure in func
'''
import traceback
import functools
import timeit
import json

from RequestSequential import download_data as RequestSequential_download_data
from RequestThreadPool import download_data as RequestThreadPool_download_data
from RequestAnsync import download_data as RequestAnsync_download_data

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

    return wrapper_timer


def dump_file(path:str,mode:str='w',encoding:str='utf-8'):
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
                    with open(path,mode,encoding=encoding) as file2write:
                        file2write.write(value)

                case 'int':
                    with open(path,mode,encoding=encoding) as file2write:
                        file2write.write(value)

                case 'list':
                    with open(path,mode,encoding=encoding) as file2write:
                        file2write.write(json.dumps(value,indent=2))

                case 'dict':
                    with open(path,mode,encoding=encoding) as file2write:
                        file2write.write(json.dumps(value,indent=2))

            return value

        return wrapper_dump_file

    return dump_file_decorator


@dump_file('logs/RequestSequential.log')
@timer
def RequestSequential(urls:list) -> list:
    """ measure RequestSequential"""    
    return RequestSequential_download_data(urls)


@dump_file('logs/RequestThreadPool.log')
@timer
def RequestThreadPool(urls:list) -> list:
    """ measure RequestSequential"""
    return RequestThreadPool_download_data(urls)

@dump_file('logs/RequestAnsync.log')
@timer
def RequestAnsync(urls:list) -> list:
    """ measure RequestSequential"""
    return RequestAnsync_download_data(urls)



def main():
    """Implementacion"""
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

    except Exception as e:# pylint:disable=broad-exception-caught
        print(f'Exception Type {type(e).__name__}\nTRACEBACK:{traceback.format_exc()}')

    except KeyboardInterrupt:
        print('End request for current user')

    except:# pylint:disable=bare-except
        print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')


if __name__ == "__main__":
    main()
