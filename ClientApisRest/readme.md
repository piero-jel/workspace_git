<!-- 
url testing
urls for testion
https://jsonplaceholder.typicode.com/posts/{1~100}
https://httpbin.org/anything Returns most of the below.
https://httpbin.org/ip Returns Origin IP.
https://httpbin.org/user-agent Returns user-agent.
https://httpbin.org/headers Returns header dict.
https://httpbin.org/get Returns GET data.
https://httpbin.org/post Returns POST data.
https://httpbin.org/put Returns PUT data.
https://httpbin.org/delete Returns DELETE data
https://httpbin.org/gzip Returns gzip-encoded data.
https://httpbin.org/status/:code Returns given HTTP Status code.
https://httpbin.org/response-headers?key=val Returns given response headers.
https://httpbin.org/redirect/:n 302 Redirects n times.
https://httpbin.org/relative-redirect/:n 302 Relative redirects n times.
https://httpbin.org/cookies Returns cookie data.
https://httpbin.org/cookies/set/:name/:value Sets a simple cookie.
https://httpbin.org/basic-auth/:user/:passwd Challenges HTTPBasic Auth.
https://httpbin.org/hidden-basic-auth/:user/:passwd 404'd BasicAuth.
https://httpbin.org/digest-auth/:qop/:user/:passwd Challenges HTTP Digest Auth.
https://httpbin.org/stream/:n Streams n–100 lines.
https://httpbin.org/delay/:n Delays responding for n–10 seconds.
-->
# Contenido
  + [Observaciones](#observaciones)
  + [Armado del Contenedor](#armado-del-contenedor)
  + [Ejecuccion sin docker](#ejecuccion-sin-docker)
    - [Instacion python linux](#instacion-python-linux)
    - [Instacion pip linux](#instacion-pip-linux)
    - [Instalaccion dependencias del proyecto](#instalaccion-dependencias-del-proyecto)
  
  + [Esquema de directorios de la Aplicación](#esquema-de-directorios-de-la-aplicacion)
  
  + [Ejecución de cada script de python](#ejecucion-de-cada-script-de-python)
    - [Ejecuccion desde el contenedor](#ejecuccion-desde-el-contenedor)
    - [Ejecuccion desde el host](#ejecuccion-desde-el-host)
    - [Analisis de sintaxis](#analisis-de-sintaxis)

  + [Measure Times](#measure-times)
    - [Ejecuccion desde el contenedor](#run-from-container)
    - [Ejecuccion desde el host](#run-from-host)
    - [Analisis de sintaxis](#check-sintaxis)
  
  + [Autor](#autor)

# Observaciones
El armado del proyecto esta contemplado que ya posee instalado docker y que el sistema anfitrión es linux (distribuciones debian, ubuntu, en las cuales se desplegaron).

# Armado del Contenedor
Para esto dentro del directorio **0D-Dockerfiles** contamos con los siguientes script:

  - **docker_config** : script bash con la configuraciones especifica para el armado del contenedor (Nombre de imagen, contenedor, flags de creación y demás).
  
  - **Dockerfile** : Docker file script con la configuración base del contenedor (Sistema base para construir la imagen, los aplicativos base a instalar, etc).
  
  - **bashrc.sh** : Para el caso de necesitar cargar alias o exportar variables de entorno.
  
  - **requerimientos.txt** : listados de package ```para python```, los cuales se instalaran mediante ```pip```
  
Con los archivos correspondiente configurados (*los mismos están configurado para el proyecto*) podemos armar el contenedor mediante el uso del script **devops.sh** :

~~~ bash
devops.sh --build
devops.sh -b
~~~
Con este no solo se creara la imagen si no tambien el contendor y se ejecuta el mismo, colocando el prompt dentro del directorio ```/home/user``` del contenedor en ejecucion. Para validar, desde otra session/terminal podemos ejecutar:

~~~ bash
devops.sh --status
devops.sh status
~~~
Este nos traera la info unicamente relacionada al contenedor configurado para este proyecto.

Si el **status** del contendor no es **up**, podemos verificar que sucedio con la ayuda del siguente comando:

~~~ bash
devops.sh --logs
devops.sh logs
~~~



Como la mayoria de los script, este posee un help para acceder al mismo podemos realizarlo de la siguiente forma:

~~~ bash
  $ devops.sh -h
  devops.sh {--help | -h }        Visualiza Help General
  devops.sh {--help | -h } --all  Visualiza Help Especifico para todos los Targets

  Para Visualizar Help Especifico Intente con:
    devops.sh {--help | -h} --start
    devops.sh {--help | -h} --stop
    devops.sh {--help | -h} --kill
    devops.sh {--help | -h} --status
    devops.sh {--help | -h} --build
    devops.sh {--help | -h} --terminal
    devops.sh {--help | -h} --rm
    devops.sh {--help | -h} --rm-image
    devops.sh {--help | -h} --rm-all
    devops.sh {--help | -h} --attach
    devops.sh {--help | -h} --check
    devops.sh {--help | -h} --del-build-cache
    devops.sh {--help | -h} --inspect
    devops.sh {--help | -h} --logs
    devops.sh {--help | -h} --test
~~~
Lo mismo vemos para la opcion '--h' (```devops.sh --help```).

Para obtener información detallada de lo que hace uno en particular, debemos usar la sintaxis (```devops.sh -h <Option>```):

~~~ bash
$ devops.sh -h -b
--build [IMAGE-NAME [CONTAINER-NAME]]
     -b [IMAGE-NAME [CONTAINER-NAME]]
  build [IMAGE-NAME [CONTAINER-NAME]]
     
  Default values:
    + Image jeluccioni/client-apis-rest
    + Container ClientApisRest

  Construye la imagen <jeluccioni/client-apis-rest> para el contenedor <ClientApisRest> a partir de las configuraciones del dockerfile <Dockerfile>. Inicia el container en funcion de los flags <-it -v ~/ClientApisRest/:/home/user:rw --network=host -P>.
          
~~~

# Ejecuccion sin docker
Para la ejecucion sin el uso de contenedor debemos tener instalada en el host los siguentes comandos:

  + **python3**
  + **pip3** (gestor de paquetes python)

## Instacion python linux
~~~ bash  
  sudo apt update && sudo apt upgrade -y  
  sudo apt install -y python3  
~~~

## Instacion pip linux
~~~ bash  
  sudo apt-get install -y python3-pip
~~~


## Instalaccion dependencias del proyecto
~~~ bash
  # sobre el directorio root del proyecto
  pip3 install --no-cache-dir -r 0D-Dockerfiles/requerimientos.txt
~~~


# Esquema de directorios de la Aplicacion

  + **0D-Dockerfiles** : Directorio donde se localiza los archivos de configuración para **Docker**
  + **RequestSequential.py** : Script con ejecucion secuencial de peticiones REST.
  + **RequestThreadPool.py** : Idem al anterior pero con el uso de **threading**
  + **RequestAnsync.py** : Idem a **RequestSequential.py** pero con el uso de **async**.
  + **devops.sh** : Script bash para la creación del contenedor 
  + **readme.md** : este documento 
  + **measure_times.py** : Script Python para medir el tiempo recurrido por cada alternativa y generar los log con las respuestas a las peticiones solicitadas. Este ejecuta secuencialmente los script (Mientras en el prompt visualiza el tiempo y en caso de errores en las respuesta visualiza el mismo.):
  
    - ```RequestSequential.py```
    - ```RequestThreadPool.py```
    - ```RequestAnsync.py```
    
  
  
~~~
.
├── 0D-Dockerfiles
│   ├── bashrc.sh
│   ├── docker_config
│   ├── Dockerfile
│   └── requerimientos.txt
│
├── devops.sh
│
├── logs
│
├── readme.md
├── measure_times.py
├── RequestAnsync.py
├── RequestSequential.py
└── RequestThreadPool.py
~~~
    

# Ejecucion de cada script de python
Por defecto el contenedor inicia dentro del directorio donde se localiza los fuentes, en el caso de no usar el mismo debemos considar estar dentro del root del proyecto. 



## Ejecuccion desde el contenedor
Para ejectuar cada uno tenemos dos opciones:

~~~ bash
  py RequestSequential.py
  py RequestThreadPool.py
  py RequestAnsync.py  
~~~
Para esto contamos con el alias ```py=python3```, otra opciones es la siguiente:

~~~ bash
  python RequestSequential.py
  python RequestThreadPool.py
  python RequestAnsync.py  
~~~
Para esto contamos con el alias ```python=python3```.

## Ejecuccion desde el host
Para ejectuar cada uno hacemos uso del camando ```python3```:

~~~ bash
  python3 RequestSequential.py
  python3 RequestThreadPool.py
  python3 RequestAnsync.py  
~~~


## Analisis de sintaxis
Para el análisis estático y podemos usar el comando ```mypy``` el cual con ayuda de la sintaxis estática de tipos (para variables y signature de funciones/métodos) nos permite localizar algunas fallas de codificación.

<!--  
~~~ bash
  mypy RequestSequential.py
  mypy RequestThreadPool.py
  mypy RequestAnsync.py 
  mypy measure_times.py
  # analisis simultaneo
  for it in $(ls *.py); do mypy $it; done
  
  # o podemos pasarle el listado de archivos usando comodines
  mypy *.py
~~~
-->
~~~ bash
  mypy RequestSequential.py
  mypy RequestThreadPool.py
  mypy RequestAnsync.py   
~~~


# Measure Times
Este script nos permite lanzar una medición de tiempo, relacionado con cada alternativa, el volcado de la respuesta para cada ejecución se realiza a un archivo. Solo visualiza en el prompt las excepciones y/o errores en los response. Para ejecutarlo solo debemos ingresar una de las siguientes opciones:

## run from container
~~~ bash
  py measure_times.py
  
  python measure_times.py
~~~


## run from host
~~~ bash
python3 measure_times.py  
~~~

## check sintaxis
~~~ bash
  mypy measure_times.py  
~~~

# Autor
  + [Luccioni Jesuse Emanuel](mailto:piero.jel@gmail.com)
