# Contenido
<!--
Pendiente nginx deploy
https://medium.com/@akshatgadodia/deploying-a-django-application-with-docker-nginx-and-certbot-eaf576463f19
-->

* [Run Project With Enviroment](#enviroment)
  + [Creación del virtual enviroment](#creacion-del-virtual-enviroment)
  + [Ejecución del proyecto dentro del enviroment](#ejecucion-del-proyecto-dentro-del-enviroment)
  + [Unit Test and Code Coverage](#unit-test-and-code-coverage)
  + [Resumen Pasos](#resumen-pasos)

* [Docker and Docker Compose](#docker-and-docker-compose)
  - [Instalación de docker en linux](#instalacion-de-docker-en-linux)
  - [Ejecución del proyecto dentro de docker](#ejecucion-del-proyecto-dentro-de-docker)
  - [Unit Test and Code coverage](#unit-test-and-code-coverage)
  - [Resumen de Comandos](#resumen-de-comandos)



# Enviroment
  + [Creación del virtual enviroment](#creacion-del-virtual-enviroment)
  + [Ejecución del proyecto dentro del enviroment](#ejecucion-del-proyecto-dentro-del-enviroment)
  + [Resumen Pasos](#resumen-pasos)


## Creacion del virtual enviroment
Para ésto contamos con él script `activate.sh`

Creación de un pequeño entorno para Django el cual se encarga:

  - Si es la primera ves en ser ejecutado, instala y crea el entorno necesario. Para luego habilitar el mismo.
  - Si ya se ejecuto con anterioridad, solo habilita el entorno virtual para poder iniciar a trabajar sobre el mismo.

Ejecución, para esto abrimos una consola y ejecutamos los siguientes comandos:

```bash
# path: ruta al directorio del proyecto
cd ${path}/DJango_DRF
bash activate.sh
```
Esto nos dejara dentro del **virtual enviroment**, en caso de necesitar salir del mismo, debemos presionar la combinación de teclas `Ctrl + d`

Para continuar con el proyecto debemos movernos al directorio del mismo `rd_wepapp`:

```bash
cd rd_wepapp/
```

## Ejecucion del proyecto dentro del enviroment
Dentro del directorio del paso anterior, tenemos el scrip `Action.sh` el cual simplifica diferentes acciones como:

<details>
  <summary>Action.sh Options:</summary>

  + `bash Action.sh --up`         ***Realiza todas las acciones necesarias para iniciar el servicio web del proyecto***.
  + `bash Action.sh --migrate`    Realiza la migración de todos los modelos.
  + `bash Action.sh --shell`      Open Shell iterativo con los modelos ORM disponibles.
  + `bash Action.sh --load_data`  Carga dato a la base desde un archivo `dataset` con items del tipo objetos **json**, uno por cada linea, del archivo.
  + `bash Action.sh --run`        Inicia el server, con la aplicación, poner en marcha el proyecto.
  + `bash Action.sh --unittest`   Ejecuta él unittest/test.
  + `bash Action.sh --coverage`   Realiza él test y genera el reporte **coverage** del código.

  + `bash Action.sh --clean`      Realiza el clean (limpieza) de los directorios y archivos auto generados.
    - generados por `--coverage` `htmlcov/` y `.coverage`.
    - generados por `--migrate`


</details>




## Unit Test and Code Coverage
Para esto contamos con las siguientes acciones:

```bash
## ejecucion de los test unitarios
bash Action.sh --unittest

## ejecucion del coverage p/obtenre el informe
bash Action.sh --coverage
```


## Resumen Pasos
Resumen de los pasos para poner en marcha el proyecto:

<details>
  <summary>Start Project</summary>

```bash
## creamos el venv
cd ${path}/DJango_DRF
bash activate.sh

## ponemos en marcha el proyecto
cd rd_wepapp
Action.sh --up
## open browser http://127.0.0.1:8080/
```
</details>



# Docker and Docker Compose
  - [Instalación de docker en linux](#instalacion-de-docker-en-linux)
  - [Ejecución del proyecto dentro de docker](#ejecucion-del-proyecto-dentro-de-docker)
  - [Unit Test and Code coverage](#unit-test-and-code-coverage)
  - [Resumen de Comandos](#resumen-de-comandos)

## Instalacion de docker en linux
Los pasos para la instalacion de docker en linux (distro debian, ubuntu) son los siguentes:

1. Agregamos las claves/key de **docker oficial** al repositorios de claves GPG:
```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

2. Agregamos el repositorio al gestor apt y actualizamos el mismo:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
```

3. Instalamos Docker, en la ultima version oficial disponible
```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

4. Creamos el grupo y agregamos nuestro usuario al mismo, para evitar usar `sudo` (ejecución con permisos de usuario root):
```bash
# 1. Create the docker group.
sudo groupadd docker

# 2. Add your user to the docker group.
sudo usermod -aG docker $USER

# 3. You can also run the following command to activate the changes to groups:
newgrp docker
```

5. Verificamos el correcto funcionamiento:
```bash
# 4. Verify that you can run docker commands without sudo.
docker run hello-world
```



## Ejecucion del proyecto dentro de docker
Para la ejecución del proyecto dentro del docker contamos con el siguiente comando, el cual se encarga de realizar todos los pasos:
  1. Creación de las imágenes y contenedores
  2. Crear y exportar los modelos para las tablas de base de datos
  3. Cargar los datos iniciales
  4. Inicia los servicios para la disponibilidad de los endpoint y la aplicación wep.

```bash
bash devops.sh --up
```

Luego verificamos ingresando mediante el browser a la dirección `http://127.0.0.1:8080/`.

En caso de ya no necesitar mas el mismo solo debemos ejecutar el siguiente comando, el cual detiene todos los contenedores:

```bash
bash devops.sh --down
```

## Unit Test and Code coverage
Estos pasos queda resumidos en el la opción `--coverage`, la cual ejecuta el **code coverage** del proyecto usando una contenedor (el mismo es dinámico; se crea, genera el reporte, ejecutando los casos de test y luego se elimina):

```bash
bash devops.sh --coverage
```
No es necesario paso previos, solo tener instalado docker (en la ultima versión disponible) en el sistema


En caso de poseer los contenedores en ejecución, luego de ejecutar `bash devops.sh --up`, podemos atachar una terminal al contenedor de la aplicación y ejecutar los siguientes comandos:

```bash
bash devops.sh --term app
```
este paso nos dejara en el directorio del proyecto dentro del contenedor (`DJango_DRF/rd_wepapp`), para ejecutar el **coverage** solo debemos correr la siguiente linea:

```bash
bash Action.sh --coverage
```
Y para visualizar el informe debemos abrir el archivo **html** `DJango_DRF/rd_wepapp/htmlcov/index.html`, para cerrar la consola atachada al contenedor solo debemos presionar la combinación de teclas `ctrl + d` (o ingresar el comando `exit` ).



## Resumen de Comandos
<!-- BEGIN -->
Para este script `devops.sh`, debemos considerar tener instalado en el sistema la ultima versión (`Docker version 26.1.3,`). La cuál posee el `Management Commands compose`. Dentro del script contamos con las opciones/parámetros:

1. `--build [-f <path-file> | --file <path-file>]` :  Construye los contenedores, podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --build
bash devops.sh --build -f docker-compose-dev.yml
bash devops.sh --build --file docker-compose-dev.yml

```
</details>


2. `--up [-f <path-file> | --file <path-file>]` : Crea las imágenes, si estas no existen y luego crea e inicia los contenedores,  podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --up
bash devops.sh --up -f docker-compose-dev.yml
bash devops.sh --up --file docker-compose-dev.yml

```
</details>


3. `--down [-f <path-file> | --file <path-file>]` : Borra los contenedores creados para el proyecto, podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --down
bash devops.sh --down -f docker-compose-dev.yml
bash devops.sh --down --file docker-compose-dev.yml
```
</details>


4. `--start <target>`  :Inicia el servicio del contenedor, target:

  + **app** : inicia solo el **service** para el contenedor de la aplicación
  + **ddbb** : inicia solo el **service** para el contenedor de la base de datos, **para nuestro caso no aplica**.
  + **all** : Inicia todos los servicios

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --start app
bash devops.sh --start ddbb
bash devops.sh --start all

```
</details>

5. `--stop <target>` Detiene el servicio del contenedor, target:
  + **app** : detiene solo el **service** para el contenedor de la aplicación
  + **ddbb** : detiene solo el **service** para el contenedor de la base de datos, **para nuestro caso no aplica**.
  + **all** : detiene todos los servicios

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --stop app
bash devops.sh --stop ddbb
bash devops.sh --stop all

```
</details>


6. `--restart <target>` : Reinicia el servicio del contenedor, target:
  + app : Reinicia solo el **service** para el contenedor de la aplicación
  + ddbb : Reinicia solo el **service** para el contenedor de la base de datos, **para nuestro caso no aplica**.
  + all : Reinicia todos los servicios

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --restart app
bash devops.sh --restart ddbb
bash devops.sh --restart all

```
</details>

7. `--term <target>` Conexión a una terminal dentro del Contenedor deseado:
  + app : Terminal al contenedor de la aplicación
  + ddbb : Terminal al contenedor de la base de datos, **para nuestro caso no aplica**.

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --term app
bash devops.sh --term ddbb

```
</details>

8. `--top [-f <path-file> | --file <path-file>]` : Visualiza el monitorio de los contenedores, podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
bash devops.sh --top
bash devops.sh --top -f docker-compose-dev.yml
bash devops.sh --top --file docker-compose-dev.yml

```
</details>

9. `--logs` Target para ver los log en tiempo real de los servicios.

<details>
  <summary>Example:</summary>
```bash
bash devops.sh --logs
```
</details>

10. `--coverage` Ejecuta todos los test unitarios y genera el reporte **Code Coverage** del proyecto.

<details>
  <summary>Example:</summary>
```bash
bash devops.sh --coverage
```
</details>

11. `--clean`, Detiene los contenedores y realiza el clean (limpieza, borrado) de archivos, contenedores e imágenes generadas. Este también ejecuta la purga de las imágenes de docker (elimina las imágenes y contenedores intermediarios).

<details>
  <summary>Example:</summary>
```bash
bash devops.sh --clean
```
</details>
<!-- END -->


