#!/bin/python3
import requests


def download_data(urls:list | tuple) -> list:
  ''' Funcion para obtener los response relacionada a la peticion GET para 
      cada url/endpoint contenido dentro de las lista de urls.
        - urls : lista o tupla de url 
      
      Return el listado de response json de cada request para el cual el 
      code status es 200 (respuesta ok)
  '''
  if(not isinstance(urls,list) and not isinstance(urls,tuple)):
    raise TypeError(f'urls type <{type(urls)} no soportado>')
  # end if
  data = []
  for url in urls:
    ''' en este caso podemos tomar la opcion de reportar el mensaje
        , para no cancelar todas las peticiones, o lanzar la excepcion
    '''
    if(not isinstance(url,str)):
      raise TypeError(f'url type <{type(url)} no soportado, debe ser string>')
    # end if
    try:
      response = requests.get(url,timeout=5)
      if(response.status_code == 200):
        data.append(response.json())
      else:
        print(f'Error: {response.status_code}')  
      # end if
    except requests.exceptions.RequestException as e:
      print(f'Exception: {e}')
    # end try    
  # end for
  return data
# end def

''' implementacion '''
if __name__ == '__main__':
  try:
    url_base:str = 'https://jsonplaceholder.typicode.com/posts/{}'
    urls:list = [url_base.format(post) for post in range(1, 100)]
    urls.append('https://not-found-url/1')
    urls.append('http://not-found-url/2')
    #urls.append(float(1))
    data = download_data(urls)
    print(data)
    print("\n\n")    
    for i,it in enumerate(data):
      print(f'[{i}]: {it}')
    # end for
  except Exception as e:
    print(f'Exception {type(e)}: {e}')
  # end try
# end fi
