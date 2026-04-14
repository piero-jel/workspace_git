<!--  
Shift + Ctrl + v : vscode views
-->
# WebSocket Gauge
Servidor WebSocket para ser consumido por clientes que dispongan de indicadores del tipo Gauges (FrontEnd).

Estructura del proyecto:

```bash
├── http_server_gauge
│   ├── constants.js
│   ├── gauge.css
│   ├── index.html
│   ├── main.js
│   ├── settings.js
│   └── WebSocket.css
├── gauge.py
├── activate.sh
├── requirements
│   └── requirements.txt
├── readme
│   └── img
│       ├── consola_servers_close_01.png
│       ├── consola_servers_ups_01.png
│       └── gauge_01.png
└── readme.md
```
1. Directorio `http_server_gauge`, representa el FronEnd en JavaScript.
2. `gauge.py` es el backend en python todo en un solo script.
3. `activate.sh` shell script con las secuencias de comando para facilitar el despliegue del proyecto usando virtual Environment.
4. `requirements` directorio con los archivos relacionado a las dependencias del proyecto.
5. `readme` directorio con los complementos (imágenes) para este readme `readme.md`.


+ [**Preparación del entorno en linux**](#preparación-del-entorno-en-linux)
+ [**Virtual Environment**](#virtual-environment)
+ [**Ejecución del proyecto**](#ejecución-del-proyecto)
+ [**Verificación del servicio**](#verificación-del-servicio)
+ [**Resumen**](#resumen)

# Preparación del entorno en linux
Para la ejecución sin el uso de virtual environment debemos tener instalada en el host los siguientes binarios:

  + **python3**
  + **pip3** (gestor de paquetes python)

Instalación de los utilitarios en dos pasos, primero updates para la verificación e instalación de nuevas versiones de los packages instalados y luego instalación de los utilitarios.


## Distribuciones Debian y derivadas
``` bash
# con apt
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip

# o con apt-get
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip
```


## Distribuciones Fedora Red-Hat
``` bash
# distros fedora red-hat
sudo dnf update -y
sudo dnf install -y python3 python3-pip
```


# Virtual Environment
Para esto contamos con el archivo `requirements/requirements.txt` con las librerías de python que son necesarios para el proyecto. Para simplificar la creación del entorno virtual contamos con el script `activate.sh` el cual se encarga de crear el entorno virtual, si no existe aun, instalar las dependencias y habilita el entorno virtual.

```bash
## crea, instala y habilita el venv
bash activate.sh

## Solo crea e instala 
bash activate.sh --create
```
Para eliminar el venv en caso de no necesitarlo mas contamos con la opción:

```bash
bash activate.sh --delete
```

Y para realizar una limpieza de archivos generados de forma automática:
```bash
bash activate.sh --clean
```




# Ejecución del proyecto
## Con virtual Environment
Para esto contamos con el target `--run`, el cual nos permite ejecutar script python con o sin en entorno virtual habilitado. Este verifica y toma el ejecutable dependiendo del estado del venv.

```bash
bash activate.sh --run gauge.py 
```
Este paso creara el servicio para el frontend que correrá en `http://localhost:8000` y el WebSocket Server que auspicia de Backend, el cual correrá en `ws://127.0.0.1:8080`. Luego podemos ir a la [Verificacion del servicio](#verificacion-del-servicio) para constatar que todo funciona ok.

## Sin Virtual Environment
Para esto debemos contar con los [utilirios instalados](#preparacion-del-entorno-en-linux). Preparado el host instalamos las dependencias:

``` bash
python3 -m pip install -r requirements/requirements.txt
```

Para verificar que las mismas estén instalada solo debemos ejecutar:

```bash
websockets --version
```
Esto nos dará la versión de la librería de `websocket` instalada, con este paso ok solo debemos lanzar el proyecto de la siguiente manera:

```bash
python3 gauge.py 
```
Luego podemos saltar al paso de [Verificación del servicio](#verificación-del-servicio) para corroborar.




# Verificación del servicio
Si abrimos la pagina `http://localhost:8000` en el navegador veremos algo similar a lo siguiente:

![gauge](readme/img/gauge_01.png)

De forma automática si todo esta ok veremos la evoluciona de los gauges, el botón `start` en verde y sobre la consola que lanzamos el proceso la generación de los valores aleatorios.

![prompt](readme/img/consola_servers_ups_01.png)

Para bajar el proceso de forma ordenada:

1. Primero debemos presionar en la pagina (`http://localhost:8000` ) el botón `stop`. Esta acción detendrá y cerrara la conexión al backend para el cliente en cuestión. Podemos re conectar presionando el botón `start`. Ambos Botones (`start` y `stop`) maneja conexión y desconexión (o cierre) del socket cliente.

2. Cerrada la conexión del WebSocket podemos ahora cerrar o detener el servicio del frontend y de WebSockets, desde la consola solo presionamos la combinación `Ctrl+c`.

![close servers](readme/img/consola_servers_close_01.png)

> Nota: En caso de no ser ordenados nos quedara tomados los puertos (sobre todo el usado por el frontend  para la presentación `HTTP Server`) y esto no nos permitirá relanzar el proyecto. Al menos que cerremos la terminales y las volvamos a abrir o ejecutar la secuencia de comandos para verificar y forzar el cierre de los puertos (`8000` para el HTTP Server y el `8080` para el Server WebSocket)

## logs
Para revisar cada uno de los logs podemos recurrir a cada uno de los siguientes comandos, cada uno en una terminal o prompt diferente:

```bash
# Log general del Project
tail -f -n0 logs/servers_gauge.log 

# log del HTTP Server
tail -f -n0 logs/HttpServer.log 

# log del WebSocket Server
tail -f -n0 logs/ServerWebSocket.log 
```
Para todos los casos el `n0` indica iniciar desde la ultima linea insertada, a la hora de iniciar el monitoreo. Si deseamos ver lineas anteriores o las que están por defecto para el prompt podemos omitir la opción para cada terminal dedicada:


```bash
# Log general del Project
tail -f logs/servers_gauge.log 

# log del HTTP Server
tail -f logs/HttpServer.log 

# log del WebSocket Server
tail -f logs/ServerWebSocket.log 
```





# Resumen
## Con virtual Environment
```bash
# creamos el venv
bash activate.sh --create

# ejecutamos el project
bash activate.sh --run gauge.py
```

## Sin virtual Environment
```bash
# instalamso dependencias
python3 -m pip install -r requirements/requirements.txt

# ejecutamos el project
python3 gauge.py
```


