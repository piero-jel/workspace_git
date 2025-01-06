# Contenido
  + [Observaciones](#observaciones)
  + [Armado del Contenedor](#armado-del-contenedor)
  + [Esquema de directorios de la Aplicación](#esquema-de-directorios-de-la-aplicacion)
  + [Instalaccion utilidades para el manejo sin docker](#instalaccion-utilidades-para-el-manejo-sin-docker)
    - [Instacion python3 linux](#instacion-python-linux)
    - [Instacion pip linux](#instacion-pip-linux)
    - [Instalaccion dependencias del proyecto](#instalaccion-dependencias-del-proyecto)
    - [Ejecucion del proyecto](#ejecucion-del-proyecto)

  + [Ejecucion del proyecto](#ejecucion-del-proyecto)
  + [Script de testing](#script-de-testing)
    - **Creación de Usuario** [curl_register.sh](#creacion-de-usuario)
    - **Login** [curl_login.sh](#login)
    - **Editar Usuario** [curl_edit_register.sh](#editar-usuario)
    - **Obtener todos los usuario** [curl_get_users.sh](#obtener-todos-los-usuario)
    - **Healt Check** [curl_health_check.sh](#healt-check)
    - **Obtener comicios por id** [curl_get_comicio_id.sh](#obtener-comicio-por-id)
    - **Obtener Todos los comicios para el usuario actual** [curl_get_comicios.sh](#obtener-todos-los-comicios-para-el-usuario-actual)
    
    - **Publicar comicios** [curl_comicio.sh](#publicar-comicio)
    
    - **Obtener detalles de todos los comicios registrados** [curl_get_comicios_details.sh](get-comicios-details)
    
  + [Documentación de las APIs](#documentacion-de-las-apis)
    - [Registrar un nuevo usuario](#registrar-un-nuevo-usuario)
    - [Modificar un nuevo usuario](#modificar-un-nuevo-usuario)
    - [Obtener todos los usuarios](#obtener-todos-los-usuarios)
    - [Login Obtener token](#login-obtener-token)
    - [Get Comicios por Id](#get-comicio-por-id)
    - [Get All Comicios](#get-all-comicios)
    - [Publicar un Comicios](#publicar-un-comicio)
    - [Healt Check](#healt-check)

  + [Eliminicacion y clean de directorios](#eliminicacion-y-clean-de-directorios)

  + [Docker Example](#docker-example)

  + [Autor](#autor)

# Observaciones
El armado del proyecto contempla que ya posee instalado docker (Sistemas anfitriones donde se realizaron los despliegues Linux debian, ubuntu). O en su defecto que se instalen python3 con su gestro de paquetes (**pip**), con el cual instalaremos los paquetes necesario para el armado y ejecucion del proyecto.

## Install Docker Compose V2
Search del instalador:

~~~ bash
apt search docker-compose-v2
Ordenando... Hecho
Buscar en todo el texto... Hecho
docker-compose-v2/jammy-updates 2.24.6+ds1-0ubuntu1~22.04.1 amd64
  tool for running multi-container applications on Docker
~~~

Obtenemso informacion para el packages:

~~~ bash
apt-cache search docker-compose-v2
docker-compose-v2 - tool for running multi-container applications on Docker
~~~

Instalaccion del packages:

~~~ bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker-compose-v2
~~~

# Armado del Contenedor
Para esto dentro del directorio **0D-Dockerfiles** contamos con la siguientes estructura:

~~~ bash
0D-Dockerfiles/
├── bashrc
│
├── pgsql
│   ├── Dockerfile
│   └── requerimientos.txt
│
└── sqlite
    ├── Dockerfile
    └── requerimientos.txt
~~~

  + **bashrc** : directorio con los archivos de configuracion para el usuario del sistema (setting de alias y path enviroment)
  
  + **pgsql** : Los archivos necesarios para la configuracion de la base de datos postgresql
    - Dockerfile : archivo con la configuracion para armar la imagen principal de la aplicaicon
    - requerimientos.txt : archivo con las dependencias de librerias para python (listados de package ```para python```, los cuales se instalaran mediante ```pip```)
    
  + **sqlite** : Los archivos necesarios para la configuracion de la base de datos (auto contenida) sqlite
    - Dockerfile : archivo con la configuracion para armar la imagen principal de la aplicaicon
    - requerimientos.txt : archivo con las dependencias de librerias para python (listados de package ```para python```, los cuales se instalaran mediante ```pip```)
    
Los archivos de construccion de la imagen estan separados en funcion del tipo de base de datos a utilizar. Para configurar esto contamos dentro del archivo [devops.sh](devops.sh) con la variable **CFG_COMPOSE_FILE** . La cual puede tener uno de los siguentes valores:

  + ```CFG_DBMS='sqlite'``` : para la seleccion de base de datos sqlite
  + ```CFG_DBMS='pgsql'``` : para la seleccion de PostgreSQL
  
  
Con los archivos correspondiente configurados (*los mismos están configurado para el proyecto*) podemos armar el contenedor mediante el uso del script **devops.sh** :

~~~ bash
devops.sh --build
devops.sh -b
~~~
Con este no solo se creara la imagen si no tambien el contendor y se ejecuta el mismo. Para validar el estado podemos ejecutar:

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

Para ver la evolucion en tiempo real de cada contenedor (uso de memoria y cpu por cada proceso dentro de cada uno), contamos con :

~~~ bash
devops.sh --top
devops.sh top
~~~


Como la mayoria de los script, este posee un help para acceder al mismo podemos realizarlo de la siguiente forma:

~~~ bash
devops.sh -h
Setting data base autocontenida sqlite
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
    devops.sh {--help | -h} --attach
    devops.sh {--help | -h} --rm-build-cache
    devops.sh {--help | -h} --inspect
    devops.sh {--help | -h} --logs
    devops.sh {--help | -h} --restart
    devops.sh {--help | -h} --rebuild
    devops.sh {--help | -h} --clean
    devops.sh {--help | -h} --top

~~~
Lo mismo vemos para la opcion '--help' (```devops.sh --help```).

Para obtener información detallada de lo que hace uno en particular, debemos usar la sintaxis (```devops.sh -h <LongOption>```):

~~~ bash
devops.sh -h --build
Setting data base autocontenida sqlite
--build 
     -b 
  build 
     
  Default values:    
    + Container FlaskApis

  Construye el proyecto con las imagenes y conetenedors establecidos en 'docker-compose-sqlite.yml'.

~~~

# Instalaccion utilidades para el manejo sin docker
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


## Ejecucion del proyecto
~~~ bash
  # sobre el directorio root del proyecto
  python3 main.py
~~~


# Esquema de directorios de la Aplicacion

  + [0D-Dockerfiles](0D-Dockerfiles/) Directorio con las configuraciones para docker.
  + [0T-TestScripts](0T-TestScripts/) : Directorio con los Script bash y archivos json para los test de la aplicacion
  + [ApiErrorHandler](ApiErrorHandler/) : Modulo con las Funciones para manejo en el armado de los response en caso de error.
  + [Config](Config/) : Modulo para la configuracion del proyecto
  + [Models](Models/) : Modulo para el modelo de los registros (de BBDD) de la aplicacion
  + [logs](logs/) : directorio donde se localiza el log de la aplicacion
  + [main.py](main.py) : script principal de la aplicacion
  + [cfg_wsgi.py](cfg_wsgi.py) : script con la configuracion wsgi para servicio **Gunicorn**
  + [readme.md](readme.md) : este documento

~~~
.
├── 0D-Dockerfiles
│   │
│   ├── bashrc
│   │
│   ├── pgsql
│   │   ├── Dockerfile
│   │   └── requerimientos.txt
│   │
│   └── sqlite
│       ├── Dockerfile
│       └── requerimientos.txt
│
├── 0T-TestScripts
│   ├── curl_comicio.sh
│   ├── curl_edit_register.sh
│   ├── curl_get_comicio_id.sh
│   ├── curl_get_comicios_details.sh
│   ├── curl_get_comicios.sh
│   ├── curl_get_users.sh
│   ├── curl_health_check.sh
│   ├── curl_login.sh
│   ├── curl_register.sh
│   ├── post_comicio_01.json
│   ├── post_comicio_02.json
│   ├── post_comicio_03.json
│   ├── post_comicio_04.json
│   ├── register_user.json
│   └── utilities.sh
│
├── ApiErrorHandler
│   ├── ApiErrorHandler.py
│   └── __init__.py
│
│
├── Config
│   ├── Config.py
│   └── __init__.py
│
├── Models
│   ├── __init__.py
│   └── Models.py
│
├── cfg_wsgi.py
├── main.py
│
├── devops.sh
├── docker-compose-pgsql.yml
├── docker-compose-sqlite.yml
├── logs
└── readme.md


~~~ 

# Ejecucion del proyecto
Para iniciar la aplicacion, dentro del entorno si docker, solo debemos ejecutar con **Python3** el script principal de la aplicacion

~~~ bash
  python3 main.py
~~~

En el caso de docker, luego del build podemos verificar si los contenedores estan correindo ejecutando:

~~~ bash
devops.sh --top
## Ctrl + C para finalizar
~~~

De lo contrario, solo debemos iniciar los contendores:

~~~ bash
devops.sh --start
~~~

# Script de testing
El listado de script para testing, dentro del directorio ```0T-TestScripts```:

  - **Creacion de Usuario** [curl_register](#creacion-de-usuario)
  - **Login** [curl_login](#login)
  - **Editar Usuario** [curl_edit_register](#editar-usuario)
  - **Obtener todos los usuario** [curl_get_users](#obtener-todos-los-usuario)
  - **Healt Check** [curl_health_check](#healt-check)
  - **Obtener comicio por id**[curl_get_comicio_id](#obtener-comicio-por-id)
  - **Obtener Todos los comicios para el usuario actual** [curl_get_comicios](#obtener-todos-los-comicios-para-el-usuario-actual)
  
  - **Publicar comicio** [curl_comicio](#publicar-comicio)
  
  - **Obtener detalles de todos los comicios registrados** [curl_get_comicios_details](get-comicios-details)
  
  - **Funciones utilitarias** [utilities](#funciones-utilitarias)

## Creacion de Usuario
~~~ bash
curl_register.sh '{"username":"jel","password":"pass12345"}'
request: http://127.0.0.1:5000/api/register

curl -sS http://127.0.0.1:5000/api/register -i -X POST -H Content-Type: application/json --data {"username":"jel","password":"pass12345"} -w '\n'
response: HTTP/1.1 201 CREATED
Server: Werkzeug/3.0.3 Python/3.10.12
Date: Sat, 18 May 2024 21:39:06 GMT
Content-Type: application/json
Content-Length: 24
Connection: close

{
  "username": "jel"
}
~~~

## Login
~~~ bash
curl_login.sh "jel:pass12345"
request: http://127.0.0.1:5000/api/login

{ "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZXhwIjoxNzE2MDcwNzUxLjc2NDY3ODd9.XGiCk9qoLLRqaQwiFhavNaqn4luCW9vpRVvfQCnH3cQ", "timeout": 1800 
}
~~~

## Editar Usuario
~~~ bash
curl_edit_register.sh '{"password":"12345"}'
request: http://127.0.0.1:5000/api/register

response: HTTP/1.1 200 OK
Server: Werkzeug/3.0.3 Python/3.10.12
Date: Sat, 18 May 2024 21:54:45 GMT
Content-Type: application/json
Content-Length: 190
Connection: close

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZXhwIjoxNzE2MDcxMDg1LjE3NjExODR9.zRZQu61aUHEXNoSv1LZnEvWCyT-w3g8HcSQK8BORLII",
  "timeout": 1800,
  "username": "jel"
}
~~~

## Obtener todos los usuario
~~~ bash
curl_get_users.sh 
request: http://127.0.0.1:5000/api/users

curl -sS -u eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZXhwIjoxNzE2MDcxNjU2LjYxOTE4NjJ9.ha2GXLFvFZtjoetY6P-KdapcTFyit6UZ1v_Bo2zHph8:notrelevant http://127.0.0.1:5000/api/users -X GET -H Content-Type: application/json -w '\n'
response: {
  "users": [
    "nombre_usuario",
    "user_01",
    "jel"
  ]
}
~~~


## Healt Check
~~~ bash
curl_health_check.sh 
request: http://127.0.0.1:5000/api/HealthCheck

{ 
  "version": "0.0.1" 
}
~~~

## Obtener comicio por id
~~~ 
curl_get_comicio_id.sh d8257e84b09053f6c3c8ba53d4269d85
request: http://127.0.0.1:5000/api/get_comicio/d8257e84b09053f6c3c8ba53d4269d85


response: HTTP/1.1 200 OK
Server: Werkzeug/3.0.3 Python/3.10.12
Date: Sat, 18 May 2024 22:14:47 GMT
Content-Type: application/json
Content-Length: 840
Connection: close

{
  "date": "Sat, 18 May 2024 19:14:31 GMT",
  "id": "d8257e84b09053f6c3c8ba53d4269d85",
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
~~~

## Obtener Todos los comicios para el usuario actual
~~~ bash
request: http://127.0.0.1:5000/api/get_comicios


response: HTTP/1.1 200 OK
Server: Werkzeug/3.0.3 Python/3.10.12
Date: Sat, 18 May 2024 22:12:47 GMT
Content-Type: application/json
Content-Length: 366
Connection: close

{
  "ids": [
    "f302ef7949b442eb88aee338217d0103",
    "77b54bfb8aee34590c23c6b36aa12c15",
    "c766f5f7520a86c6169fe4c322ed2f43",
    "ba9ea3928fcdd64ead224ed085289001",
    "26baa07ba90134e1d3aa41bc0152884e",
    "0b0f4697ef452d332973317c0137ab71",
    "5b19c3f8f207f95d20dd3a66619f0491",
    "6c3de225c80b0e985dc47dde428068d8"
  ],
  "user": "nombre_usuario"
}
~~~

## Get Comicios Details
Este script primero ejecuta la peticion para obtener todos los [id de comicios registrados por el usuario actual](#obtener-todos-los-comicios-para-el-usuario-actual) y luego para cada **id** realiza una [peticion detallada del comicio en cuestion](#obtener-comicio-por-id)

~~~ bash
  curl_get_comicios_details.sh
~~~

~~~ 
request: http://127.0.0.1:3000/api/get_comicio/18186ff6d81a597aa10b1c8d50ed89b6

{
  "date": "Thu, 06 Jun 2024 18:07:37 GMT",
  "id": "18186ff6d81a597aa10b1c8d50ed89b6",
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


request: http://127.0.0.1:3000/api/get_comicio/3f3c76d0fc16890b11bb1c4d3696576b

{
  "date": "Thu, 06 Jun 2024 18:44:07 GMT",
  "id": "3f3c76d0fc16890b11bb1c4d3696576b",
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


request: http://127.0.0.1:3000/api/get_comicio/1fc8a5618bfee1530bbd66224236320d

{
  "date": "Thu, 06 Jun 2024 18:44:08 GMT",
  "id": "1fc8a5618bfee1530bbd66224236320d",
  "request": {
    "escanios": 6,
    "votos": [
      {
        "name": "Partido A",
        "votos": 43000
      },
      {
        "name": "Partido B",
        "votos": 30000
      },
      {
        "name": "Partido C",
        "votos": 27000
      }
    ]
  },
  "response": [
    {
      "escanios": 3,
      "lista": "Partido A"
    },
    {
      "escanios": 2,
      "lista": "Partido B"
    },
    {
      "escanios": 1,
      "lista": "Partido C"
    }
  ]
}


request: http://127.0.0.1:3000/api/get_comicio/4e86fc4579aa8176f71a751f2a590935

{
  "date": "Thu, 06 Jun 2024 18:44:08 GMT",
  "id": "4e86fc4579aa8176f71a751f2a590935",
  "request": {
    "escanios": 21,
    "listas": 10,
    "votos": [
      {
        "name": "Partido A",
        "votos": 391000
      },
      {
        "name": "Partido B",
        "votos": 311000
      },
      {
        "name": "Partido C",
        "votos": 184000
      },
      {
        "name": "Partido D",
        "votos": 73000
      },
      {
        "name": "Partido E",
        "votos": 27000
      },
      {
        "name": "Partido F",
        "votos": 12000
      },
      {
        "name": "Partido G",
        "votos": 2000
      }
    ]
  },
  "response": [
    {
      "escanios": 9,
      "lista": "Partido A"
    },
    {
      "escanios": 7,
      "lista": "Partido B"
    },
    {
      "escanios": 4,
      "lista": "Partido C"
    },
    {
      "escanios": 1,
      "lista": "Partido D"
    },
    {
      "escanios": 0,
      "lista": "Partido E"
    },
    {
      "escanios": 0,
      "lista": "Partido F"
    },
    {
      "escanios": 0,
      "lista": "Partido G"
    }
  ]
}


request: http://127.0.0.1:3000/api/get_comicio/ac6aa154bab6fbf3029396ba7db744e0

{
  "date": "Thu, 06 Jun 2024 18:44:08 GMT",
  "id": "ac6aa154bab6fbf3029396ba7db744e0",
  "request": {
    "escanios": 6,
    "listas": 10,
    "votos": [
      {
        "name": "Nulos y Blancos",
        "votos": 30656
      },
      {
        "name": "Partido B",
        "votos": 6745
      },
      {
        "name": "Partido G",
        "votos": 63942
      },
      {
        "name": "Partido M",
        "votos": 2590
      },
      {
        "name": "Partido N",
        "votos": 41036
      },
      {
        "name": "Partido O",
        "votos": 24854
      },
      {
        "name": "Partido P",
        "votos": 237460
      }
    ]
  },
  "response": [
    {
      "escanios": 5,
      "lista": "Partido P"
    },
    {
      "escanios": 1,
      "lista": "Partido G"
    },
    {
      "escanios": 0,
      "lista": "Partido N"
    },
    {
      "escanios": 0,
      "lista": "Nulos y Blancos"
    },
    {
      "escanios": 0,
      "lista": "Partido O"
    },
    {
      "escanios": 0,
      "lista": "Partido B"
    },
    {
      "escanios": 0,
      "lista": "Partido M"
    }
  ]
}
~~~


## Publicar Comicio
~~~ 
curl_comicio.sh post_comicio_01.json 
request: http://127.0.0.1:5000/api/comicio
@post_comicio_01.json

response: HTTP/1.1 200 OK
Server: Werkzeug/3.0.3 Python/3.10.12
Date: Sat, 18 May 2024 22:14:31 GMT
Content-Type: application/json
Content-Length: 372
Connection: close

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
  "id": "d8257e84b09053f6c3c8ba53d4269d85"
}
~~~


<!-- 
Test: public all json files family ```post_comicio_*```:

~~~ bash
  for it in $(ls post_comicio_*.json); do curl_comicio.sh $it ;done
~~~
-->

## Funciones utilitarias
Este script no debería ser invocado como los demás, ya que solo contiene funciones utilitarias de uso común entre todos los demás script, como así también el setting de variables generales como:

  + **IP** : dirección ip para el armado de la url
  + **PORT**: numero de puerto para el armado de la url
  + **URL**: url armada con las anteriores con el postfix del tipo ```{http,https}```

Estas pueden ser redefinidas dentro de cada script especifico para un propósito particular.
  


# Documentacion de las APIs
  - [Registrar un nuevo usuario](#registrar-un-nuevo-usuario)
  - [Modificar un usuario](#modificar-un-usuario)
  - [Obtener todos los usuarios](#obtener-todos-los-usuarios)
  - [Login Obtener token](#login-obtener-token)
  - [Get Comicion por Id](#get-comicio-por-id)
  - [Get All Comicios](#get-all-comicios)
  - [Publicar un Comicio](#publicar-un-comicio)
  - [Healt Check](#healt-check)
  
## Registrar un nuevo usuario
```POST ${url}/api/register```

### request  
~~~ json
{
  "username":"nombre_usuario",
  "password":"pass12345"
}
~~~

+ **username** : nombre de usuario con el que se creara el nuevo registro, este no debe existir actualmente.
+ **password** : clave para el usuario.

***Nota: ninguno de los campos puede estar vacio.***

### response
~~~ json
{
  "username": "nombre_usuario"
}
~~~


## Modificar un usuario
```PATH ${url}/api/register/${username}```

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***
### request:
~~~ json
{  
  "password":"pass12345"
}
~~~
  + **password** : nuevo clave para el usuario, no puede ser un campo vacio.
  


### response 
~~~ json
{
  "access_token": "nuevo token",
  "timeout": 1800,
  "username": "nombre del usuario"
}
~~~

## Obtener todos los usuarios
```GET ${url}/api/users```

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica

### response
~~~ json
{
  "users": [
    "nombre_usuario",
    "user_01",
    "jel"
  ]
}
~~~
Lista de usuarios que actualmente están activos en el sistema



## Login Obtener token
```PATH ${url}/api/login```

Debemos usar el **username** y **password** con el cual se creo el Usuario a loguear, en las credenciales de la peticion. El token y su duración estaran asociados a estos datos

### request
  - No Aplica
  
### response
~~~ json
{  
  "timeout": 600,
  "access_token":"token ...."
}
~~~
  + **timeout** : tiempo de duración para el token generado.
  + **access_token** : token que se debe utilizar para la invocación futura de las demás APIs.
  


## Get Comicion por Id
```GET ${url}/api/comicio/${id}```

  - **id** : identificador hash del comicios, devuelto en la publicación de este.
  
***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica
  
### response
~~~ json
{
  "date": "Sat, 18 May 2024 19:14:31 GMT",
  "id": "6c3de225c80b0e985dc47dde428068d8",
  "request": {
    "escanios": 6,
    "votos": [
      {
        "name": "Partido A",
        "votos": 43000
      },
      {
        "name": "Partido B",
        "votos": 30000
      },
      {
        "name": "Partido C",
        "votos": 27000
      }
    ]
  },
  "response": [
    {
      "escanios": 3,
      "lista": "Partido A"
    },
    {
      "escanios": 2,
      "lista": "Partido B"
    },
    {
      "escanios": 1,
      "lista": "Partido C"
    }
  ]
}
~~~
  
## Get All Comicios
```GET ${url}/api/comicios```

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica
  
### response
Listado de los Hash Id de los comicios publicados por el usuario actual.

~~~ json
{
  "ids": [
    "f302ef7949b442eb88aee338217d0103",
    "77b54bfb8aee34590c23c6b36aa12c15",
    "c766f5f7520a86c6169fe4c322ed2f43",
    "ba9ea3928fcdd64ead224ed085289001",
    "26baa07ba90134e1d3aa41bc0152884e",
    "0b0f4697ef452d332973317c0137ab71",
    "5b19c3f8f207f95d20dd3a66619f0491",
    "6c3de225c80b0e985dc47dde428068d8"
  ],
  "user": "nombre_usuario"
}
~~~
  
## Publicar un Comicio
```POST ${url}/api/comicio```

Esta API realiza el calculo y registro de comicios en funcion de la cantidad de votos por listas y escaños, segun el metodo de [D'Hondt](https://es.wikipedia.org/wiki/Sistema_D%27Hondt).

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
~~~ json
{
  "listas": 10,
  "escanios" : 7,
  "votos" : [
        {"name":"Partido A","votos":340000}
      , {"name":"Partido B","votos":280000}
      , {"name":"Partido C","votos":160000}
      , {"name":"Partido D","votos":60000}
      , {"name":"Partido E","votos":15000}     
    ]
}
~~~

  + **listas** : numero de listas de la publicacion, opcional (de lo contrario se calcula en funcion del objeto **votos**)
  + **escanios** : excaños a disputar.
  + **votos** : lista de objetos con la dupla de **nombre de la lista** y **cantidad de votos** por cada una de estas.

### response
~~~ json
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
  "id": "d8257e84b09053f6c3c8ba53d4269d85"
}
~~~



## Healt Check
```GET ${url}/api/HealthCheck```

Esta peticion nos permite verificar el estado de la APIs como asi tambien el login.

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica

### response
~~~ json
{ 
  "version": "0.4.5" 
}
~~~
Versión actual de las APIs. 



# Eliminicacion y clean de directorios
Para la eliminacion del proyecto, en caso de despliegues con docker, contamos con las opciones de ejecucion del script:

~~~ bash
devops.sh --rm
~~~
Este detiene en contenedor/s, elimina estos y luego elimina la imagen creada.

En caso de necesitar eliminar los archivos auto generados por python y sqlite contamos con la opcion clean, la cual debe ejecutarse luego del anterior. Ya que de otra forma no podra recuperar el nombre autogenerado para la imagen.

~~~ bash
devops.sh --clean
~~~
***Esta opcion Nos pedira clave del usuario super/root.***


# Docker Example
## Creacion
~~~ bash
devops.sh -b
[+] Building 1.6s (13/13) FINISHED                                                                                                                        docker:default
 => [flask-apis internal] load build definition from Dockerfile                                                                                                     0.0s
 => => transferring dockerfile: 3.46kB                                                                                                                              0.0s
 => [flask-apis internal] load metadata for docker.io/library/python:3.12                                                                                           1.5s
 => [flask-apis internal] load .dockerignore                                                                                                                        0.0s
 => => transferring context: 2B                                                                                                                                     0.0s
 => [flask-apis 1/7] FROM docker.io/library/python:3.12@sha256:e3d5b6f95ce66923b5e48a06ee5755abb097de96a8617c3f2f7d431d48e63d35                                     0.0s
 => [flask-apis internal] load build context                                                                                                                        0.0s
 => => transferring context: 39B                                                                                                                                    0.0s
 => CACHED [flask-apis 2/7] WORKDIR /home/user                                                                                                                      0.0s
 => CACHED [flask-apis 3/7] COPY requerimientos.txt ./                                                                                                              0.0s
 => CACHED [flask-apis 4/7] RUN mkdir -p /home/user                                                                                                                 0.0s
 => CACHED [flask-apis 5/7] RUN apt-get update                                                                                                                      0.0s
 => CACHED [flask-apis 6/7] RUN apt-get install -y python3-pip                                                                                                      0.0s
 => CACHED [flask-apis 7/7] RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requerimientos.txt                                        0.0s
 => [flask-apis] exporting to image                                                                                                                                 0.0s
 => => exporting layers                                                                                                                                             0.0s
 => => writing image sha256:30305f7c1fbf96fa655cfa96f44e9d28ab891b69df2ce831a1fac0e44e4620f4                                                                        0.0s
 => => naming to docker.io/library/flask_apis-flask-apis                                                                                                            0.0s
 => [flask-apis] resolving provenance for metadata file                                                                                                             0.0s
[+] Running 2/2
 ✔ Network flask_apis_default  Created                                                                                                                              0.1s
 ✔ Container FlaskApis         Started
~~~

## Verificacion
~~~ bash
 devops.sh logs
FlaskApis  | [2024-08-25 13:06:28 -0300] [1] [INFO] Starting gunicorn 23.0.0
FlaskApis  | [2024-08-25 13:06:28 -0300] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
FlaskApis  | [2024-08-25 13:06:28 -0300] [1] [INFO] Using worker: gthread
FlaskApis  | [2024-08-25 13:06:28 -0300] [7] [INFO] Booting worker with pid: 7
FlaskApis  | [2024-08-25 13:06:28 -0300] [8] [INFO] Booting worker with pid: 8
FlaskApis  | [2024-08-25 13:06:28 -0300] [9] [INFO] Booting worker with pid: 9
FlaskApis  | [2024-08-25 13:06:28 -0300] [10] [INFO] Booting worker with pid: 10

devops.sh top
FlaskApis
UID    PID    PPID   C    STIME   TTY   TIME       CMD
root   8031   8011   3    12:46   ?     00:00:00   /usr/local/bin/python /usr/local/bin/gunicorn --config cfg_wsgi.py main:app
root   8063   8031   13   12:46   ?     00:00:00   /usr/local/bin/python /usr/local/bin/gunicorn --config cfg_wsgi.py main:app
root   8064   8031   13   12:46   ?     00:00:00   /usr/local/bin/python /usr/local/bin/gunicorn --config cfg_wsgi.py main:app
root   8065   8031   13   12:46   ?     00:00:00   /usr/local/bin/python /usr/local/bin/gunicorn --config cfg_wsgi.py main:app
root   8066   8031   13   12:46   ?     00:00:00   /usr/local/bin/python /usr/local/bin/gunicorn --config cfg_wsgi.py main:app
~~~

## remove and clean
~~~ bash
devops.sh --rm
[+] Stopping 1/1
 ✔ Container FlaskApis  Stopped                                                                                                                                     1.3s
[+] Running 2/2
 ✔ Container FlaskApis         Removed                                                                                                                              0.1s
 ✔ Network flask_apis_default  Removed                                                                                                                              0.3s
Untagged: flask_apis-flask-apis:latest
Deleted: sha256:30305f7c1fbf96fa655cfa96f44e9d28ab891b69df2ce831a1fac0e44e4620f4


devops.sh --clean
clean comodin files
clean array files

clean array folders with prefix
clean array folders
~~~


# Autor
  + [Luccioni Jesuse Emanuel](mailto:piero.jel@gmail.com)


