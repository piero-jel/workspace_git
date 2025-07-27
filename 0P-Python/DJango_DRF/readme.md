# Contenido
<!--
Pendiente nginx deploy
https://medium.com/@akshatgadodia/deploying-a-django-application-with-docker-nginx-and-certbot-eaf576463f19
-->

* [Run Project With Enviroment](#enviroment)
  + [Creacion del virtual enviroment](#creacion-del-virtual-enviroment)
  + [Ejecucion del proyecto dentro del enviroment](#ejecucion-del-proyecto-dentro-del-enviroment)
  + [Resumen Pasos](#resumen-pasos)

* [Docker and Docker Compose](#docker-and-docker-compose)
  - [Coverage](#coverage)



# Enviroment
  + [Creacion del virtual enviroment](#creacion-del-virtual-enviroment)
  + [Ejecucion del proyecto dentro del enviroment](#ejecucion-del-proyecto-dentro-del-enviroment)
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

  + `bash Action.sh --migrate`    Realiza la migración de todos los modelos.
  + `bash Action.sh --shell`      Open Shell iterativo con los modelos ORM disponibles.
  + `bash Action.sh --load_data`  Carga dato a la base desde un archivo `dataset` con items del tipo objetos json, uno por cada linea, del archivo.
  + `bash Action.sh --run`        Inicia el server, con la aplicación, poner en marcha el proyecto.
  + `bash Action.sh --unittest`   Ejecuta el unittest/test.
  + `bash Action.sh --coverage`   Realiza el test y genera el reporte coverage del codigo.
  + `bash Action.sh --up`         Realiza todas las acciones necesarias para iniciar el servicio web del proyecto.

  + `bash Action.sh --clean`      Realiza el clena de los directorios y archivos autogenerados.
    - generados por `--coverage` `htmlcov/` y `.coverage`.
    - generados por `--migrate`


</details>




## Unit Test and Code Coverage
Para esto contamos con las siguentes acciones:

```bash
## si no migro o ejecuto --up demos crear y migrar los modelos
bash Action.sh --migrate


## ejecucion de los test unitarios
bash Action.sh --unittest

## ejecucion del coverage p/obtenre el informe
bash Action.sh --coverage
```
Si no

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
  - [Coverage](#coverage)
<!-- BEGIN -->
Para este script `devops.sh`, debemos considerar tener instalado en el sistema la versión v2 (`Docker version 26.1.3,`). La cuál posee el `Management Commands` compose. Dentro del script contamos con las opciones/parámetros:

1. `--build [-f <path-file> | --file <path-file>]` :  Construye los contenedores, podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
  devops.sh --build
  devops.sh --build -f docker-compose-prod.yml
  devops.sh --build --file docker-compose-prod.yml

```
</details>


2. `--up [-f <path-file> | --file <path-file>]` : Crea las imágenes, si estas no existen y luego crea e inicia los contenedores,  podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
  devops.sh --up
  devops.sh --up -f docker-compose-prod.yml
  devops.sh --up --file docker-compose-prod.yml

```
</details>


3. `--down [-f <path-file> | --file <path-file>]` : Borra los contenedores creados para el proyecto, podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
  devops.sh --down
  devops.sh --down -f docker-compose-prod.yml
  devops.sh --down --file docker-compose-prod.yml
```
</details>


4. `--start <target>`  :Inicia el servicio del contenedor, target:

  + **app** : inicia solo el **service** para el contenedor de la aplicación
  + **ddbb** : inicia solo el **service** para el contenedor de la base de datos, **para nuestro caso no aplica**.
  + **all** : Inicia todos los servicios

<details>
  <summary>Example:</summary>

```bash
  devops.sh --start app
  devops.sh --start ddbb
  devops.sh --start all

```
</details>

5. `--stop <target>` Detiene el servicio del contenedor, target:

  + **app** : detiene solo el **service** para el contenedor de la aplicación
  + **ddbb** : detiene solo el **service** para el contenedor de la base de datos, **para nuestro caso no aplica**.
  + **all** : detiene todos los servicios

<details>
  <summary>Example:</summary>

```bash
  devops.sh --stop app
  devops.sh --stop ddbb
  devops.sh --stop all

```
</details>


6. `--restart <target>` : Reinicia el servicio del contenedor, target:

  + app : Reinicia solo el service para el contenedor de la aplicación
  + ddbb : Reinicia solo el service para el contenedor de la base de datos, **para nuestro caso no aplica**.
  + all : Reinicia todos los servicios

<details>
  <summary>Example:</summary>

```bash
  devops.sh --restart app
  devops.sh --restart ddbb
  devops.sh --restart all

```
</details>

7. `--term <target>` Conexión a una terminal dentro del Contenedor deseado

  + app : Terminal al contenedor de la aplicación
  + ddbb : Terminal al contenedor de la base de datos, **para nuestro caso no aplica**.

<details>
  <summary>Example:</summary>

```bash
  devops.sh --term app
  devops.sh --term ddbb

```
</details>


8. `--top [-f <path-file> | --file <path-file>]` : Visualiza el monitoreo de los contenedores, podemos usar '`-f <path-file>`' o '`--file <path-file>`' para usar un archivo de configuración diferente.

<details>
  <summary>Example:</summary>

```bash
  devops.sh --top
  devops.sh --top -f docker-compose-prod.yml
  devops.sh --top --file docker-compose-dev.yml

```
</details>

9. `--logs` Target para ver los log en tiempo real de los servicios.

<details>
  <summary>Example:</summary>

```bash
  devops.sh --logs

```
</details>
<!-- END -->


## Coverage
Para esto podemos realizar los siguientes pasos:

1. Atachando una terminal al contenedor de la aplicacion.
```bash
cd DJango_DRF
devops.sh --term app
```
este paso nos dejara en el directorio del proyecto dentro del contenedor (`DJango_DRF/rd_wepapp`), para ejecutar el coverage solo debemos correr la siguiente linea:

```bash
bash Action.sh --coverage
```
Y para visualizar el informe debemos abrir el archivo html `DJango_DRF/rd_wepapp/htmlcov/index.html`, para cerrar la consola atachada al contenedor solo debemos presionar la combinación de teclas `ctrl + d` (o ingresar el comando `exit` ).

2. Ejecutando la acciones sobre un Contenedor que ya esta corriendo:
```bash
devops.sh --coverage
```
Este realiza los mismos pasos, pero sobre un contenedor aislado, genera el reporte e intenta abrir el mismo en browser. De lo contrario visualiza el path para que lo abramos.

