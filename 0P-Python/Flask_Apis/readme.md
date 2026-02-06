# Contenido
  + [Observaciones](#observaciones)
  + [Armado del Contenedor](#armado-del-contenedor)
  + [Esquema de directorios de la Aplicación](#esquema-de-directorios-de-la-aplicación)

  + [Ejecuccion con docker](#ejecución-con-docker)

  + [Ejecuccion sin docker](#ejecución-sin-docker)
    - [Instacion python3 linux](#instalación-python-linux)
    - [Instacion pip linux](#instalación-pip-linux)
    - [Instalaccion dependencias del proyecto](#instalación-dependencias-del-proyecto)
    - [Ejecucion del proyecto](#ejecución-del-proyecto)

  + [Ejecuccion con virtual enviroment sobre linux](#ejecución-con-virtual-enviroment-sobre-linux)

  + [Ejecucion del proyecto](#ejecución-del-proyecto)
  + [Bash Script de testing](#bash-script-de-testing)
    - **Creación de Usuario** [curl_register.sh](#creación-de-usuario)
    - **Login** [curl_login.sh](#login)
    - **Editar Usuario** [curl_edit_register.sh](#editar-usuario)
    - **Obtener todos los usuario** [curl_get_users.sh](#obtener-todos-los-usuario)
    - **Healt Check** [curl_health_check.sh](#healt-check)
    - **Obtener comicios por id** [curl_get_comicio_id.sh](#obtener-comicios-por-id)
    - **Obtener Todos los comicios para el usuario actual** [curl_get_comicios.sh](#obtener-todos-los-comicios-para-el-usuario-actual)

    - **Publicar comicios** [curl_comicio.sh](#publicar-comicio)

    - **Obtener detalles de todos los comicios registrados** [curl_get_comicios_details.sh](get-comicios-details)

  + [Documentación de las APIs](#documentación-de-las-apis)
    - [Registrar un nuevo usuario](#registrar-un-nuevo-usuario)
    - [Modificar un nuevo usuario](#modificar-un-nuevo-usuario)
    - [Obtener todos los usuarios](#obtener-todos-los-usuarios)
    - [Login Obtener token](#login-obtener-token)
    - [Get Comicios por Id](#get-comicios-por-id)
    - [Get All Comicios](#get-all-comicios)
    - [Publicar un Comicios](#publicar-un-comicios)
    - [Healt Check](#healt-check)

  + [Test mediante request](#test-mediante-request)
  + [Unit Test con request](#unit-test-con-request)


  + [static code analyzers with pylint](#static-code-analyzers-with-pylint)

  + [Autor](#autor)

# Observaciones
El armado del proyecto esta contemplado para ser desplegado usando docker. En el caso de que el sistema anfitrión sea linux (distribuciones **debian**, **ubuntu**) podemos seguir los pasos a continuación para instalar el mismo.

## Install Docker Compose V2
Search del instalador:

``` bash
apt search docker-compose-v2
Ordenando... Hecho
Buscar en todo el texto... Hecho
docker-compose-v2/jammy-updates 2.24.6+ds1-0ubuntu1~22.04.1 amd64
  tool for running multi-container applications on Docker
```

Obtenemos información para él packages:

``` bash
apt-cache search docker-compose-v2
docker-compose-v2 - tool for running multi-container applications on Docker
```

Instalación del packages:

``` bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker-compose-v2
```

# Armado del Contenedor
Para esto dentro del directorio **0D-Dockerfiles** contamos con la siguientes estructura:

``` bash
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
```

  + **bashrc** : directorio con los archivos de configuración para el usuario del sistema (setting de alias y path enviroment)

  + **pgsql** : Los archivos necesarios para la configuración de la base de datos postgresql
    - Dockerfile : archivo con la configuración para armar la imagen principal de la aplicación
    - `requerimientos.txt` : archivo con las dependencias de librerías para python (listados de package ```para python```, los cuales se instalaran mediante ```pip```)

  + **sqlite** : Los archivos necesarios para la configuración de la base de datos (auto contenida) sqlite
    - Dockerfile : archivo con la configuración para armar la imagen principal de la aplicación
    - `requerimientos.txt` : archivo con las dependencias de librerías para python (listados de package ```para python```, los cuales se instalaran mediante ```pip```)

Los archivos de construcción de la imagen estan separados en función del tipo de base de datos a utilizar. Para configurar esto contamos dentro del archivo [devops.sh](devops.sh) con la variable **CFG_COMPOSE_FILE** . La cual puede tener uno de los siguientes valores:

  + ```CFG_DBMS='sqlite'``` : para la selección de base de datos sqlite
  + ```CFG_DBMS='pgsql'``` : para la selección de PostgreSQL



Con los archivos correspondiente configurados (*los mismos están configurado para el proyecto*) podemos armar el contenedor mediante el uso del script **devops.sh** :

``` bash
devops.sh --build
devops.sh -b
```
En el caso de querer construir el proyecto sin la necesidad de modificar los script podemos ejecutar los comandos anteriores especificando **DataBase Management System** con la opción ```--dbms=``` .

``` bash
## para DBMS sqlite
devops.sh -b --dbms=sqlite
devops.sh --build --dbms=sqlite

## para DBMS PostgreSQL
devops.sh -b --dbms=pgsql
devops.sh --build --dbms=pgsql
```


Con este no solo se creara la imagen si no también el contenedor y se ejecuta el mismo. Para validar el estado podemos ejecutar:

``` bash
devops.sh --status
devops.sh status
```
Este nos traerá la información unicamente relacionada al contenedor configurado para este proyecto.

Si el **status** del contenedor no es **up**, podemos verificar que sucedió con la ayuda del siguiente comando:

``` bash
devops.sh --logs
devops.sh logs
```

Para ver la evolución en tiempo real de cada contenedor (uso de memoria y **cpu** por cada proceso dentro de cada uno), contamos con :

``` bash
devops.sh --top
devops.sh top
```


Como la mayoría de los script, este posee un help para acceder al mismo podemos realizarlo de la siguiente forma:

``` bash
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

```
Lo mismo vemos para la opción '--help' (```devops.sh --help```).

Para obtener información detallada de lo que hace uno en particular, debemos usar la sintaxis (```devops.sh -h <LongOption>```):

``` bash
devops.sh -h --build
Setting data base autocontenida sqlite
--build
     -b
  build

  Default values:
    + Container FlaskApis

  Construye el proyecto con las imagenes y conetenedors establecidos en 'docker-compose-sqlite.yml'.

```
# Ejecución con docker
1. Construimos las imágenes y levantamos los servicios
```bash
bash devops.sh --build
```

2. Atachamos una terminal a los logs
```bash
tail -f -n0 logs/Flask_Apis.log
```

3. Conectamos una terminal al contenedor para realizar el test
```bash
bash devops.sh --terminal
```

4. Ejecutamos el test
```bash
python3 0T-TestScripts/UnitTest_Comicios/test_ApisRestComicios.py
```

5. Stop y delete de contenedores, imagens y archivos generados de forma automatica:
```bash
bash devops.sh --rm
```


# Ejecución sin docker
Para la ejecución sin el uso de contenedor debemos tener instalada en el host los siguientes comandos:

  + **python3**
  + **pip3** (gestor de paquetes python)

## Instalación python linux
``` bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y python3
```

## Instalación pip linux
``` bash
  sudo apt-get install -y python3-pip
```


## Instalación dependencias del proyecto
``` bash
  # sobre el directorio root del proyecto
  pip3 install --no-cache-dir -r 0D-Dockerfiles/requerimientos.txt
```


## Ejecución del proyecto
``` bash
  # sobre el directorio root del proyecto
  python3 main.py
```


# Ejecución con virtual enviroment sobre linux
Para esto contamos con el script [activate.sh](activate.sh), el cual solo depende de la instalacion de [python en el sistema](#instacion-python-linux). Este script realiza dos o solo una tarea dependiendo del contexto:

  1. Si el directorio del entorno virtual no existe crea el mismo e instala las dependencias sobre este.
  2. Habilita el entorno virtual y nos deja la terminal lista para [lanzar el proyecto](ejecucion-del-proyecto).

Para ejecutar el mismo solo debemos ejecutar el script de la siguente forma:

```bash
bash activate.sh
```
> Note: en caso de necesitar reinstalar el entorno virtual solo debemos ejecutar el comando **`bash activate.sh --clean`**, este eliminara el contexto actual para que luego pueda rearmar el mismo ejecutando **`bash activate.sh`**

# Esquema de directorios de la Aplicacion

  + **0D-Dockerfiles** : directorio con los archivos auxiliares para la creación de las imágenes para docker.
  + **0T-TestScripts** : Directorio con los diferentes Script bash, python y archivos json para los test de la aplicación.
    - Bash Script para el test usando ```curl```.
    - Python Script (```test_With_request.py```) para el test mediante el uso de request
    - Python Script para el test unitario (```test_ApisRestComicios.py```0) mediante el uso de unittest y request (sin mock), este usa auxiliar mente el modelo de clase definido en ```Comicios.py```, con la finalidad de facilitar la implementación y posible modificación de la APIs.

  + **ApiErrorHandler** : Modulo con las Funciones para manejo en el armado de los response en caso de error.
  + **Config** : Modulo para la configuración del proyecto
  + **Models** : Modulo para el modelo de los registros (de BBDD) de la aplicación
  + **logs** : directorio donde se localiza el log de la aplicación
  + **main.py** : script principal de la aplicación
  + **cfg_wsgi.py** : script con la configuración wsgi para servicio **Gunicorn**
  + **readme.md** : este documento

```
  .
  ├── 0D-Dockerfiles
  │   ├── bashrc
  │   ├── docker_config
  │   ├── Dockerfile
  │   ├── pgsql
  │   │   ├── Dockerfile
  │   │   └── requerimientos.txt
  │   ├── requerimientos_old.txt
  │   └── sqlite
  │       ├── Dockerfile
  │       └── requerimientos.txt
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
  │   ├── token_dump.log
  │   ├── UnitTest_Comicios
  │   │   ├── Comicios.py
  │   │   ├── in
  │   │   │   ├── post_comicio_01.json
  │   │   │   ├── post_comicio_02.json
  │   │   │   ├── post_comicio_03.json
  │   │   │   ├── post_comicio_04.json
  │   │   │   └── register_user.json
  │   │   ├── __init__.py
  │   │   ├── ou
  │   │   │   ├── TestComicioApis.json
  │   │   │   └── token.json
  │   │   ├── test_ApisRestComicios.py
  │   │   ├── test_Comicios.py
  │   │   └── test_With_request.py
  │   │
  │   └── utilities.sh
  ├── ApiErrorHandler
  │   ├── ApiErrorHandler.py
  │   └── __init__.py
  ├── cfg_wsgi.py
  ├── Config
  │   ├── Config.py
  │   └── __init__.py
  │
  ├── devops.sh
  ├── docker-compose-pgsql.yml
  ├── docker-compose-sqlite.yml
  ├── logs
  ├── main.py
  ├── Models
  │   ├── __init__.py
  │   └── Models.py
  └── readme.md
```

# Ejecución del proyecto
Para iniciar la aplicación, dentro del entorno si docker, solo debemos ejecutar con **Python3** el script principal de la aplicación

``` bash
  python3 main.py
```

En el caso de docker, luego del build podemos verificar si los contenedores están corriendo ejecutando:

``` bash
devops.sh --top
## Ctrl + C para finalizar
```

De lo contrario, solo debemos iniciar los contenedores:

``` bash
devops.sh --start
```

# Bash Script de testing
El listado de script para testing, dentro del directorio ```0T-TestScripts```:

  - **Creacion de Usuario** [curl_register.sh](#creacion-de-usuario)
  - **Login** [curl_login.sh](#login)
  - **Editar Usuario** [curl_edit_register.sh](#editar-usuario)
  - **Obtener todos los usuario** [curl_get_users.sh](#obtener-todos-los-usuario)
  - **Healt Check** [curl_health_check.sh](#healt-check)
  - **Obtener comicio por id**[curl_get_comicio_id.sh](#obtener-comicio-por-id)
  - **Obtener Todos los comicios para el usuario actual** [curl_get_comicios.sh](#obtener-todos-los-comicios-para-el-usuario-actual)

  - **Publicar comicio** [curl_comicio.sh](#publicar-comicio)

  - **Obtener detalles de todos los comicios registrados** [curl_get_comicios_details.sh](get-comicios-details)

  - **Funciones utilitarias** [utilities.sh](#funciones-utilitarias)



## Creacion de Usuario
1. Creando un nuevo usuario
``` bash
curl_register.sh '{"username":"jel","password":"pass12345"}'
request: http://127.0.0.1:8080/api/register

response: HTTP/1.1 201 CREATED
Server: gunicorn
Date: Thu, 30 Jan 2025 11:53:39 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 19

{"username":"jel"}
```

2. Intentado crear un usuario ya existente
``` bash
request: http://127.0.0.1:8080/api/register

response: HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 30 Jan 2025 11:54:04 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 59

{"code":400,"message":"username <jel> ya esta registrado"}
```


## Login
``` bash
curl_login.sh "jel:pass12345"
request: http://127.0.0.1:8080/api/login

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNzM4MjM5ODc0LjMyMjMwNH0.NCAWOkUb6XWxwf6lsFTca1Jv6BTye6Q7SuOKk0YcxCc",
  "timeout": 1800,
  "username": "jel"
}
```

## Editar Usuario
``` bash
curl_edit_register.sh '{"password":"12345"}'

request: http://127.0.0.1:8080/api/register

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNzM4MjQwMTMxLjQ4MjkwODV9.BboA3tYk3i_YggA2A7b7NnEFIHZhtcidhE-JSAcOE2c",
  "timeout": 1800,
  "username": "jel"
}
```

## Healt Check
``` bash
curl_health_check.sh
request: http://127.0.0.1:8080/api/HealthCheck

{
  "version": "0.5.0"
}
```

## Obtener todos los usuario
``` bash
curl_get_users.sh
request: http://127.0.0.1:8080/api/users

{
  "users": [
    "nombre_usuario",
    "jel"
  ]
}
```

## Publicar Comicio
```
curl_comicio.sh post_comicio_01.json
request: http://127.0.0.1:8080/api/comicio
@post_comicio_01.json

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
  "id": "238b537b8ad7172220150d4f1d81cca1"
}
```



## Obtener comicio por id
```
curl_get_comicio_id.sh 238b537b8ad7172220150d4f1d81cca1
request: http://127.0.0.1:8080/api/get_comicio/238b537b8ad7172220150d4f1d81cca1

{
  "date": "Thu, 30 Jan 2025 09:00:54 GMT",
  "id": "238b537b8ad7172220150d4f1d81cca1",
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


## Obtener Todos los comicios para el usuario actual
``` bash
curl_get_comicios.sh
request: http://127.0.0.1:8080/api/get_comicios


{
  "ids": [
    "238b537b8ad7172220150d4f1d81cca1"
  ],
  "user": "jel"
}
```

## Get Comicios Details
Este script primero ejecuta la peticion para obtener todos los [id de comicios registrados por el usuario actual](#obtener-todos-los-comicios-para-el-usuario-actual) y luego para cada **id** realiza una [peticion detallada del comicio en cuestion](#obtener-comicio-por-id)

``` bash
  curl_get_comicios_details.sh
```

```
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
```





## Funciones utilitarias
Este script no debería ser invocado como los demás, ya que solo contiene funciones utilitarias de uso común entre todos los demás script, como así también el setting de variables generales como:

  + **IP** : dirección ip para el armado de la url
  + **PORT**: numero de puerto para el armado de la url
  + **URL**: url armada con las anteriores con el postfix del tipo ```{http,https}```

Estas pueden ser redefinidas dentro de cada script especifico para un propósito particular.



# Documentación de las APIs
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
``` json
{
  "username":"nombre_usuario",
  "password":"pass12345"
}
```

+ **username** : nombre de usuario con el que se creara el nuevo registro, este no debe existir actualmente.
+ **password** : clave para el usuario.

***Nota: ninguno de los campos puede estar vacio.***

### response
``` json
{
  "username": "nombre_usuario"
}
```


## Modificar un usuario
```PATCH ${url}/api/register/${username}```

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***
### request:
``` json
{
  "password":"pass12345"
}
```
  + **password** : nuevo clave para el usuario, no puede ser un campo vacio.



### response
``` json
{
  "access_token": "nuevo token",
  "timeout": 1800,
  "username": "nombre del usuario"
}
```

## Obtener todos los usuarios
```GET ${url}/api/users```

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica

### response
``` json
{
  "users": [
    "nombre_usuario",
    "user_01",
    "jel"
  ]
}
```
Lista de usuarios que actualmente están activos en el sistema



## Login Obtener token
```PATH ${url}/api/login```

Debemos usar el **username** y **password** con el cual se creo el Usuario a loguear, en las credenciales de la peticion. El token y su duración estaran asociados a estos datos

### request
  - No Aplica

### response
``` json
{
  "timeout": 600,
  "access_token":"token ...."
}
```
  + **timeout** : tiempo de duración para el token generado.
  + **access_token** : token que se debe utilizar para la invocación futura de las demás APIs.



## Get Comicion por Id
```GET ${url}/api/comicio/${id}```

  - **id** : identificador hash del comicios, devuelto en la publicación de este.

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica

### response
``` json
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
```

## Get All Comicios
```GET ${url}/api/get_comicios```

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica

### response
Listado de los Hash Id de los comicios publicados por el usuario actual.

``` json
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
```

## Publicar un Comicio
```POST ${url}/api/comicio```

Esta API realiza el calculo y registro de comicios en función de la cantidad de votos por listas y escaños, según el método de [D'Hondt](https://es.wikipedia.org/wiki/Sistema_D%27Hondt).

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
``` json
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
```

  + **listas** : numero de listas de la publicación, opcional (de lo contrario se calcula en función del objeto **votos**)
  + **escanios** : excanios a disputar.
  + **votos** : lista de objetos con la dupla de **nombre de la lista** y **cantidad de votos** por cada una de estas.

### response
``` json
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
```



## Healt Check
```GET ${url}/api/HealthCheck```

Esta petición nos permite verificar el estado de la APIs como así también el login.

***Debe estar logueado el usuario actual que usa la APIs (el token del mismo debe estar vigente).***

### request
  - No Aplica

### response
``` json
{
  "version": "0.4.5"
}
```
Versión actual de las APIs.



# Test mediante request
Para esto nos movemos al directorio `0T-TestScripts/UnitTest_Comicios`, donde tenemos el script `test_With_request.py` con los diferentes test.


## Visualización del help
```bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py help -s
```

Salida del comando anterior:

``` bash
  Funcion que lista todos los test disponibles en este modulo.

  Params
    opt Opcional (default None) opcion para especificar formato del help
      --short o -s impresion corta.

Listado de test para el modulo: "test_With_request.py"

test_With_request.py create_user [-q | --quiet]       : Creacion de un nuevo usuario.
test_With_request.py edit_user [-q | --quiet]         : Edit User, obtiene un nuevo token para el uaurio modificado.
test_With_request.py get_users [-q | --quiet]         : Obtener el listado actual de usuarios.
test_With_request.py login [-q | --quiet]             : Login, obtiene nuevo token para el usuario.
test_With_request.py health_check [-q | --quiet]      : Health Check, con la version actual de la api.
test_With_request.py post_comicio [-q | --quiet]      : Publicar comicio.
test_With_request.py get_comicios [-q | --quiet]      : Obtener todos los comicios registrado para el usuario.
test_With_request.py get_comicio_id [-q | --quiet]    : Obtener Comicio por id.
test_With_request.py help [-q | --quiet]              : Visualiza este mensaje de ayuda.
```
  - La opción '-s' o '--short' en el help indica que debe visualizar la descripciones breves de cada caso de test.
  - La opción '-q' o '--quiet' luego de la opción deshabilita la impresión extendida de información, sobre la utilidad.

***Los test individuales son validos solo si el servicio o los contenedores esta en ejecución, de lo contrario tendremos respuesta de error relacionados a la conexion.***

### Verificamos la isntalaccion de request
Paso previo, verificamos si esta disponible en el sistema o ambiente virtual el **package** `request`. En caso de estarlo, verificamos la versión instalada:

``` bash
python3 -m pip freeze | grep requests
requests==2.32.5
```

En caso de no estar disponible (respuesta vaciá, en la ejecución anterior) o tener una versión por debajo de '1' instalamos el **package**:

``` bash
python3 -m pip install requests==2.32
```


## Apertura de logs
Con la aplicacion corriendo, podemos atachar una terminal a los logs en el caul veremos la respuesta de cada peticion. Para esto en una consola ejecutamos :

```bash
tail -f 0T-TestScripts/UnitTest_Comicios/logs/test_$(date +%Y%m%d).log
```
> Note: el nombre del log esta atado a la fecha de ejecucion del test, no del servicio. Ya que es otro log por separado.



## Creamos un Usuario
``` bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py create_user -q jesus 1234
```
Salida por log:
```bash
2026-02-04 12:27:34.165 INFO    - Creando el usuario con el payload: {'username': 'jesus', 'password': '1234'}
2026-02-04 12:27:34.166 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 12:27:34.370 DEBUG   - http://127.0.0.1:8080 "POST /api/register HTTP/1.1" 201 26
2026-02-04 12:27:34.371 INFO    - Resp Code: 201
2026-02-04 12:27:34.371 INFO    - Resp JSON:
{
  "username": "jesus"
}
```


## Intentamos crear un usuario duplicado
``` bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py create_user -q jesus 1234
```

Salida por log:
```bash
2026-02-04 12:39:14.245 INFO    - Creando el usuario con el payload: {'username': 'jesus', 'password': '1234'}
2026-02-04 12:39:14.246 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 12:39:14.251 DEBUG   - http://127.0.0.1:8080 "POST /api/register HTTP/1.1" 400 55
2026-02-04 12:39:14.251 INFO    - Resp Code: 400
2026-02-04 12:39:14.252 INFO    - Resp JSON:
{
  "message": "username <jesus> ya esta registrado"
}
```


## Edit user
``` bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py edit_user -q jesus 1234 4321
```

Salida por log:
```bash
2026-02-04 13:06:46.014 INFO    - Editando el Usuario <jesus>, con el payload <{'password': '4321'}>
2026-02-04 13:06:46.015 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 13:06:46.819 DEBUG   - http://127.0.0.1:8080 "PATCH /api/register HTTP/1.1" 200 191
2026-02-04 13:06:46.820 INFO    - Resp Code: 200
2026-02-04 13:06:46.821 INFO    - Resp JSON:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzcwMjIzMDA2LjgxNzg3OH0._7XhX0D3q7S6bRqWAlmTcXA-ZOmIUkUpVhAsa9PjtnA",
  "timeout": 1800,
  "username": "jesus"
}
```

## Obtener listado de Usuarios
Para este paso y los siguientes necesitamos el token, por lo que si no editamos el usaurio debemos primero ejecutar el [login](#login) para obtener el mismo.

``` bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py get_users -q
```


Salida por log:
```bash
2026-02-04 13:08:22.585 INFO    - Get users, listado actual de usuarios, auth: ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzcwMjIzMDA2LjgxNzg3OH0._7XhX0D3q7S6bRqWAlmTcXA-ZOmIUkUpVhAsa9PjtnA', 'notrelevant')
2026-02-04 13:08:22.586 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 13:08:22.593 DEBUG   - http://127.0.0.1:8080 "GET /api/users HTTP/1.1" 200 33
2026-02-04 13:08:22.593 INFO    - Resp Code: 200
2026-02-04 13:08:22.593 INFO    - Resp JSON:
{
  "users": [
    "jesus"
  ]
}
```

## login
``` bash
## si ejecutamos el paso de modificación de usuario
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py login -q jesus 4321

## en caso de saltear la modificación de usuario usamos la clave original
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py login -q jesus 1234
```

Salida por log:
```bash
2026-02-04 13:09:46.674 INFO    - Login User jesus, auth:('jesus', '4321')
2026-02-04 13:09:46.674 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 13:09:46.754 DEBUG   - http://127.0.0.1:8080 "GET /api/login HTTP/1.1" 200 192
2026-02-04 13:09:46.754 INFO    - Resp Code: 200
2026-02-04 13:09:46.755 INFO    - Resp JSON:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzcwMjIzMTg2Ljc1MzM4MDN9.-YN4wl8OgFZ1u4ob_oKq5S88jZrRUKJxCVj2K9ynCIw",
  "timeout": 1800,
  "username": "jesus"
}
```

## health check
``` bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py health_check -q
```

Salida por log:
```bash
2026-02-04 13:10:48.321 INFO    - Health Check, username <jesus>
2026-02-04 13:10:48.321 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 13:10:48.324 DEBUG   - http://127.0.0.1:8080 "GET /api/HealthCheck HTTP/1.1" 200 25
2026-02-04 13:10:48.325 INFO    - Resp Code: 200
2026-02-04 13:10:48.325 INFO    - Resp JSON:
{
  "version": "0.5.0"
}
```

## Publicar un comicio
```bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py post_comicio -q
```

Salida por logs:
```
2026-02-04 13:11:43.052 INFO    - Publicar comicio, File: in/post_comicio_01.json | username <jesus> | Payload:
{
  "listas": 10,
  "escanios": 7,
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
}
2026-02-04 13:11:43.053 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 13:11:43.945 DEBUG   - http://127.0.0.1:8080 "POST /api/comicio HTTP/1.1" 200 372
2026-02-04 13:11:43.946 INFO    - Resp Code: 200
2026-02-04 13:11:43.946 INFO    - Resp JSON:
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
  "id": "dbb2bc603628e38c13a58ff3fea4cd77"
}
```


## Obtener todos los comicios registrado para el usuario

``` bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py get_comicios -q
```


Salida por log:
```bash
2026-02-04 13:14:36.022 INFO    - Los comicios registrado para el usuario <jesus>
2026-02-04 13:14:36.023 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 13:14:36.026 DEBUG   - http://127.0.0.1:8080 "GET /api/get_comicios HTTP/1.1" 200 77
2026-02-04 13:14:36.026 INFO    - Resp Code: 200
2026-02-04 13:14:36.026 INFO    - Resp JSON:
{
  "ids": [
    "dbb2bc603628e38c13a58ff3fea4cd77"
  ],
  "user": "jesus"
}
```

## Obtener Comicios por id
```bash
python3 0T-TestScripts/UnitTest_Comicios/test_With_request.py get_comicio_id -q "dbb2bc603628e38c13a58ff3fea4cd77"
```

Salida por log:
```
2026-02-04 13:19:49.696 DEBUG   - Comicios Registrado con el id:<dbb2bc603628e38c13a58ff3fea4cd77>, username <jesus>
2026-02-04 13:19:49.697 DEBUG   - Starting new HTTP connection (1): 127.0.0.1:8080
2026-02-04 13:19:49.707 DEBUG   - http://127.0.0.1:8080 "GET /api/get_comicio/dbb2bc603628e38c13a58ff3fea4cd77 HTTP/1.1" 200 840
2026-02-04 13:19:49.708 INFO    - Resp Code: 200
2026-02-04 13:19:49.708 INFO    - Resp JSON:
{
  "date": "Wed, 04 Feb 2026 13:11:43 GMT",
  "id": "dbb2bc603628e38c13a58ff3fea4cd77",
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

# Unit Test con request
Dentro del directorio `0T-TestScripts/UnitTest_Comicios`, nos encontramos con el script `test_ApisRestComicios.py` con los test unitarios y secuenciales.

1. Nos aseguramos que el servicio este corriendo, para cualqueira de los casos:
  + [Ejecuccion con docker](#ejecuccion-con-docker)
  + [Ejecuccion sin docker](#ejecuccion-sin-docker)
    - [Ejecucion del proyecto](#ejecución-del-proyecto)
  + [Ejecuccion con virtual enviroment sobre linux](#ejecuccion-con-virtual-enviroment-sobre-linux)

2. Nos atachamos al log
```bash
# Si es la primera ves el archivo no existira, lo podemos crear
touch 0T-TestScripts/UnitTest_Comicios/logs/test_$(date +%Y%m%d).log

# atachamos la terminal al log
tail -f -n0 0T-TestScripts/UnitTest_Comicios/logs/test_$(date +%Y%m%d).log
```
> Nota: el archivo de log lo genera automaticamente la ejecucion de los test, no es necesario crearlo. Pero si necesitamos la existencia del archivo si nos queremos atachar con una terminal a este.

3. Ejecutamos el test
```bash
python3 0T-TestScripts/UnitTest_Comicios/test_ApisRestComicios.py
```


Salida por consola:
``` bash
test_create_user (__main__.TestComicioApis.test_create_user)
01- test create user ... ok
test_edit_user (__main__.TestComicioApis.test_edit_user)
02- test edit user ... ok
test_get_users (__main__.TestComicioApis.test_get_users)
03- test get users ... ok
test_login (__main__.TestComicioApis.test_login)
04- test login ... ok
test_health_check (__main__.TestComicioApis.test_health_check)
05- test health check ... ok
test_post_comicio (__main__.TestComicioApis.test_post_comicio)
06- test post comicio ... ok
test_get_comicios (__main__.TestComicioApis.test_get_comicios)
07- test get comicios ... ok
test_get_comicio_id (__main__.TestComicioApis.test_get_comicio_id)
08- test get comicio id ... ok
test_get_comicio_id_list (__main__.TestComicioApis.test_get_comicio_id_list)
09- test get comicio id desde la lista de get comicios ... ok
test_post_comicio_list (__main__.TestComicioApis.test_post_comicio_list)
10- test post comicio, desde una lista de archivos ... ok

----------------------------------------------------------------------
Ran 10 tests in 5.156s

OK
```

> Note: ***Los test individuales son validos solo si el servicio o los contenedores esta en ejecución, de lo contrario tendremos respuesta de error relacionados a la conexión.***


# static code analyzers with pylint

## Instalaccion
```bash
python3 -m pip install pylint
```


## Ejecucion
```bash
## modo recursivo
pylint --recursive=y .
```

Por cada modulo:
```bash
## Packages Models
pylint ./Models/

## Packages Config
pylint ./Config/
```



# Autor
  + [Luccioni Jesuse Emanuel](mailto:piero.jel@gmail.com)


