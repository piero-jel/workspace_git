# Document Processing
Aplicacion de Microservicio y Arquitectura Hexagonal para procesamiento de documentos.

Contenido

# Document Processing Gateway
- job : Abreviatrua para representar el trabajo que realizar el 'Document Processing'

## Contexto
Microservicio para la orquestacion del procesamiento de documentos a través de un pipeline de proveedores externos. Se recibe JSON con la informacion (como la metadata del archivo) y string del documentos (`"content"` como un string), dicha informacion es procesada por distintos stages de procesamiento (extracción, análisis y enriquecimiento), y al finalizar la misma es publicada en un servicios Event Streaming para que sea luego consumida por servicio de downstream de eventos.


## Arquitectura General

```
      [API Rest]                     [Celery/Redis]             [Providers]
                                 +------------------+
 Peticion de procesamiento -->   |                  |
                                 |    Document      | <----> Proveedor de Extracción (mock)
 Status de un Job          -->   |    Processing    | 
 Cancel/Delete Job         -->   |    Gateway       | <----> Proveedor de Análisis (mock)
                                 |                  | 
 Listado de Jobs           -->   |                  | <----> Proveedor de Enriquecimiento (mock)
                                 +--------+---------+
                                          |
                                          |
                                         \ /
                                          .
                                  Event Streaming               [Apache Kafka]
                               (eventos del pipeline)                    
                                          |
                                          |
                                         \ /
                                          .
                                   Consumer(s)
                                (servicios downstream)
```

Desde el punto de vista de las APIs (Entrada) tenemos :

  - Enviar documento a procesar `[POST] url/pipeline_process/`
  - Consultar estado de un job  `[GET]  url/pipeline_process/<job_id>`
  - Cancelar o ELiminar un job  `[PUT]  url/pipeline_process/<job_id> {"status": "'cancel|delete'"}`
  - Listar jobs                 `[GET]  url/pipeline_process/list/[<status>]`


## Peticion de procesamiento
Para la peticion (`[POST] pipeline_process/`) de la creacion de un job tenemos el siguente Body:

``` json
{
    "name"        : "Nombre de archivo",
    "topic"       : "Topico/tema en el cual se publicara al finalizar",
    "compression" : "Opcional, compresion puede ser: gzip, snappy, lz4, zstd",
    "content"     : "string con el contenido del archivo",
    "pipeline_config" : "Opcional nombre de los stage del Provider"
}
```
Y el response debera tener la siguente Forma:

``` json
{
    "job_id"      : "ID del JOB creado",
    "name"        : " ... ",
    "topic"       : " ... ",
    "compression" : " ... ",
    "content"     : " ... ",
    "pipeline_config" : ""
}
```
  > En caso de error tendremos los tabulados para API Rest relacionados al servicio. 
  > Debemos onsiderar que los errores relacionados a la sintaxis de un campo en particular no se capturan, ya que es un sistema asincronico y estos son validados para cada etapa y capa en particular. Los mismos se reflejaran en los llamados posteriores para obtener el estado en funcion del ID generado.

Ejemplos para el lanzamiento de un nuevo Job:

1. Opcion por defecto:

``` bash
url='http://127.0.0.1:8000/pipeline_process/';\
body='{"name": "example1","topic": "string","content": "Esto es un Ejemplo" }';\
header=(-H 'accept: application/json' -H 'Content-Type: application/json');\
curl -X 'POST' ${url} "${header[@]}" -d "${body}" -w '\n'
```

2. Pasando `pipeline_config` como un string separado por comas:

```bash
url='http://127.0.0.1:8000/pipeline_process/';\
body='{"name": "example1","topic": "string","content": "Esto es un Ejemplo 2","pipeline_config" : "Extraction,Analysis,Enrichment"}';\
header=(-H 'accept: application/json' -H 'Content-Type: application/json');\
curl -X 'POST' ${url} "${header[@]}" -d "${body}" -w '\n'
```

3. Pasando `pipeline_config` como un array de string:

```bash
url='http://127.0.0.1:8000/pipeline_process/';\
body='{"name": "example1","topic": "string","content": "Esto es un Ejemplo 2","pipeline_config" : ["Extraction "," Analysis ", "Enrichment"]}';\
header=(-H 'accept: application/json' -H 'Content-Type: application/json');\
curl -X 'POST' ${url} "${header[@]}" -d "${body}" -w '\n'
```



## Status de un Job
Consultar estado de un job mediante su ID, `[GET]  pipeline_process/<job_id>`

1. Get de estado, con info detallada del servicio 
```bash
job_id="XXXXXXXX";\
uri="http://127.0.0.1:8000/pipeline_process/${job_id}" ;\
curl -sS "${uri}" -i -X GET -w '\n'
```

2. Get corriente, solo informacion del job
```bash
job_id="XXXXXXXX";\
uri="http://127.0.0.1:8000/pipeline_process/${job_id}" ;\
curl -sS "${uri}" -X GET -w '\n'
```

3. Response
``` json
{
  "code": 0,
  "job_id": "061656bc-9ed2-4636-a21f-6b1364a8b95f",
  "name": "Nombre de archivo",
  "topic": "dato-comprimidos-v1",
  "compression": "gzip",
  "stages": "completed",
  "pipeline": "extraction, analysis, enrichment",
  "job_status": "completed",
  "ready": true,
  "status": "completed",
  "result": {
    "name": "Nombre de archivo",
    "topic": "dato-comprimidos-v1",
    "compression": "gzip",
    "stages": "completed",
    "pipeline": "extraction, analysis, enrichment",
    "job_status": "completed"
  }
}
```
## Cancel Eliminar un Job
Cancelar o Eliminar un job, `[PUT]  pipeline_process/<job_id> {"status": "'cancel|delete'"}`. Podemos eliminar el mismo en cualquier ciclo de vida. Debemso considerar que la eliminacion se realiza en dos etapas, primero se cancela el job (si el mismo esta siendo ejecutado) y luego se elimina del sistema persistente. 

> Nota el sistema persistente solo mantiene la minima informacion posible sobre un job. Esta no preserva informacion relacionada al archivo, solo los estados y demas data relacionada al procesamiento (pipeline, stage, status). Dichos datos son encapsualdos en un mecanismo de contexto el cual tiene una vida limitada en cuanto a persitencia (hasta 7 dias, segun configuracion).


1. Cancelacion de Job

```bash
job_id="XXXXXXXX";\
url="http://127.0.0.1:8000/pipeline_process/${job_id}";\
header=(-H 'accept: application/json' -H 'Content-Type: application/json');\
body='{"status": "cancel"}';\
curl -X 'PUT' "${url}" "${header[@]}" -d "${body}" -w '\n'
```

2. Delete Job

```bash 
job_id="XXXXXXXX";\
url="http://127.0.0.1:8000/pipeline_process/${job_id}";\
header=(-H 'accept: application/json' -H 'Content-Type: application/json');\
body='{"status": "delete"}';\
curl -X 'PUT' "${url}" "${header[@]}" -d "${body}" -w '\n'
```

3. Response de un Job Completado
``` json
{
  "code": 0,
  "job_status": "completed",
  "message": "No se puede cancelar el worker id '061656bc-9ed2-4636-a21f-6b1364a8b95f', fue completado",
  "job_id": "061656bc-9ed2-4636-a21f-6b1364a8b95f"
}
```
## Listado de Jobs
Retorna el listado de Job que se encuentran en un estado en particualar. `[GET]  pipeline_process/list/[<status>]`. En caso de no aportar el `<status>` retornara el listado para cada uno de los estados.

Los estados posibles en los que puede estar el Proccess

- `pending`
- `processing`
- `completed`
- `failed`
- `cancelled`

1. Get, `status=cancelled`

```bash
status="cancelled" ;\
url="http://127.0.0.1:8000/pipeline_process/list/${status}" ;\
curl -sS "${url}" -i -X GET -w '\n'
```

2. Get default, el listado de todos los estados

```bash
url="http://127.0.0.1:8000/pipeline_process/list/";\
curl -sS "${url}" -i -X GET -w '\n'
```

3. Response para el Status processing:
``` json
{
  "processing": [
    "98a18e95-3c2b-4c7a-b22e-65061f468214"
  ]
}
```

4. Response sin status
``` json
{
  "pending": [],
  "processing": [
    "98a18e95-3c2b-4c7a-b22e-65061f468214"
  ],
  "completed": [
    "061656bc-9ed2-4636-a21f-6b1364a8b95f"
  ],
  "failed": [],
  "cancelled": []
}
```


# Preparacion del entorno
## Dependencias
La principal dependencia es la instalaccion de docker en la version V2, la cual incluye el subcomando `compose`. Instalada esta podemos ejecutar los comandos para el despliegue independientemente del sistema operativo.

Para el caso de usar distribuciones de linux como Fedora o RedHat debemos habilitar los permisos de acceso al directorio principal del proyecto. Ya que este se montara como un volumen a los diferentes contenedores. 

```bash
curr=${PWD};cd .. && chcon -R -t svirt_sandbox_file_t "${curr}/" && cd -
```

<!--  
Resumen de Pasos para el Despliegue 

1. build and up
```bash
docker compose up -d
```

2. Verificamos que todos los services este Creados y Up
```bash
docker compose ps
```
> Debemos considerar que el Service tests o Contenedor Tests no debe quedar en estado Up, ya que el mismo solo se preparo para realizar los test unitarios e incluye todas las librerias necesarias (combinacion de todos los servicios)

3. Verificamos los logs
```bash
docker compose logs -f
```

Podemos reccorrer uno por uno para verificar que no existen errores de despliegue

```bash
docker compose logs -f celery
docker compose logs -f fastapi
docker compose logs -f kafka
docker compose logs -f redis
```



4. Ingreso a la pagina FastAPI Swagger UI `http://0.0.0.0:8000/docs`

5. Ejecucion de los unittest
```bash
services='tests'; \
flags="--rm -u $(id -u $USER):20 -e TZ=America/Argentina/Buenos_Aires"; \
docker compose run ${flags} ${services} bash -c "python3 -m unittest -v"
```
FIXME Revisar los unittest, 
 - no se estan pasando en topic en los create jobs
 - algunos quedaron con el print() en lugar del log.info()
-->


## Creacion de los .env Kafka
Debemos crear el archivo `deploy/kafka/environment/.env` con la siguente configuracion:

```bash
KAFKA_NODE_ID=1
KAFKA_PROCESS_ROLES='broker,controller'
KAFKA_LISTENERS='PLAINTEXT://:9092,CONTROLLER://:9093'
KAFKA_CONTROLLER_LISTENER_NAMES='CONTROLLER'
KAFKA_CONTROLLER_QUORUM_VOTERS='1@kafka:9093'
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1
KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0
KAFKA_NUM_PARTITIONS=3
KAFKA_ADVERTISED_LISTENERS='PLAINTEXT://kafka:9092'
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP='PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT'
KAFKA_INTER_BROKER_LISTENER_NAME='PLAINTEXT'
CLUSTER_ID='MkU3OEVBNTcwNTJENDM2Qk'
```
  > Para este caso `CLUSTER_ID` es opcional, se utiliza en caso que escalemos. En tal caso se deberan generar varios `CLUSTER_ID` uno por cada services (al igual que las Variables). Para generar el valor de esta solo debemos ejecutar en una terminal `uuidgen --time | tr -d '-' | base64 | cut -b 1-22`.


## Creacion de los .env del proyecto
Para este caso debemos generar el archivo `.env` (dentro del root del proyecto) con la siguente secuencia:

```bash
# enviroment con las claves
REDISCLI_AUTH='ContraseniaSegura'
REDIS_URL='redis'
REDIS_PORT=6379
REDIS_DB=0
MOCKING_PROVIDER=true
KAFKA_URL='kafka'
KAFKA_PORT=9092
```
  
# Despliegue con docker compose
## Verificacion
Paso previo debemos verificar la configuracion del archivo `docker-compose.yml`, esto nos servira para verificar si los `.env` fueron creados de forma sastifactoria.

```bash
docker compose config
```

<details>
  <summary> Configuracion Docker-Compose </summary>

```bash
name: documentprocessing
services:
  celery:
    build:
      context: /path-repo/0P-Python/DocumentProcessing/deploy
      dockerfile: ./celery/Dockerfile
    command:
      - celery
      - -A
      - app.infrastructure.adapters.tasks_celery
      - worker
      - --loglevel=info
      - --concurrency=4
    container_name: Celery
    depends_on:
      redis:
        condition: service_healthy
        required: true
    environment:
      TZ: America/Argentina/Buenos_Aires
    healthcheck:
      test:
        - CMD-SHELL
        - celery -A app.infrastructure.adapters.tasks_celery inspect ping --destination celery@$$HOSTNAME
      timeout: 10s
      interval: 30s
      retries: 3
      start_period: 5s
    networks:
      default: null
    volumes:
      - type: bind
        source: /path-repo/0P-Python/DocumentProcessing
        target: /application
        bind: {}
  fastapi:
    build:
      context: /path-repo/0P-Python/DocumentProcessing/deploy
      dockerfile: ./fastapi/Dockerfile
    command:
      - uvicorn
      - app.infrastructure.apis.fastapi:fastapi
      - --host
      - 0.0.0.0
      - --port
      - "8000"
    container_name: FastApi
    depends_on:
      celery:
        condition: service_healthy
        required: true
      redis:
        condition: service_healthy
        required: true
    environment:
      TZ: America/Argentina/Buenos_Aires
    networks:
      default: null
    ports:
      - mode: ingress
        target: 8000
        published: "8000"
        protocol: tcp
    volumes:
      - type: bind
        source: /path-repo/0P-Python/DocumentProcessing
        target: /application
        bind: {}
  kafka:
    container_name: Kafka
    environment:
      CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: "0"
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_NODE_ID: "1"
      KAFKA_NUM_PARTITIONS: "3"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: "1"
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: "1"
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: "1"
      TZ: America/Argentina/Buenos_Aires
    image: apache/kafka:latest
    networks:
      default: null
    ports:
      - mode: ingress
        target: 9092
        published: "9092"
        protocol: tcp
      - mode: ingress
        target: 9093
        published: "9093"
        protocol: tcp
    volumes:
      - type: volume
        source: kafka-data
        target: /var/lib/kafka/data
        volume: {}
  redis:
    command:
      - redis-server
      - --requirepass
      - ContraseniaSegura
      - --appendonly
      - "yes"
    container_name: Redis
    environment:
      TZ: America/Argentina/Buenos_Aires
    healthcheck:
      test:
        - CMD
        - redis-cli
        - ping
      timeout: 5s
      interval: 10s
      retries: 5
    image: redis:8-alpine
    networks:
      default: null
    ports:
      - mode: ingress
        target: 6379
        published: "6379"
        protocol: tcp
    restart: unless-stopped
    volumes:
      - type: volume
        source: redis-data
        target: /data
        volume: {}
  tests:
    build:
      context: /path-repo/0P-Python/DocumentProcessing/deploy
      dockerfile: ./tests/Dockerfile
    container_name: Tests
    environment:
      TZ: America/Argentina/Buenos_Aires
    networks:
      default: null
    volumes:
      - type: bind
        source: /path-repo/0P-Python/DocumentProcessing
        target: /application
        bind: {}
networks:
  default:
    name: documentprocessing_default
volumes:
  kafka-data:
    name: documentprocessing_kafka-data
  redis-data:
    name: documentprocessing_redis-data

```
    
</details>

## Creacion
```bash
# build and start containers
docker compose up --build -d 


# Create and start containers
## -d: Detached mode: Run containers in the background
docker compose up -d

# --build            Build images before starting containers
# --remove-orphans   Remove containers for services not defined in the Compose file
```

## Stop/Start/restart
```bash
# Stop services
docker compose stop

# Start services
docker compose start

# Restart service containers
docker compose restart
```

## status
```bash
# List containers
docker compose ps

# Display the running processes
docker compose top

# Display a live stream of container(s) resource usage statistics
docker compose stats

# List running compose projects
docker compose ls
```

## Delete
```bash
# Stop and remove containers, networks
## -v Remove named volumes declared in the "volumes" section and anonymous volumes attached to containers
docker compose down -v
```

## logs
```bash
# View output from containers
docker compose logs -f
docker compose logs -tf
```
Para una mejor comoodidad podemos atacharnos a un log en particular:

```bash
docker compose logs -f kafka 
docker compose logs -f redis 
docker compose logs -f celery 
docker compose logs -f tests 
```

## Attach terminal a un contenedor
```bash
docker exec -it Kafka '/bin/bash'
docker exec -it Redis '/bin/bash'
docker exec -it Celery '/bin/bash'
docker exec -it Tests '/bin/bash'
```

# Swager Docs 
Aprovechando la ventaja de la generacion de documentacion automatica de `FastAPIs` con los servicios iniciados podemos acceder a ella, para visualizar y ejecutar peticiones desde la web. Sin necesidad de ejecutar comandos que involucren `curl` o ejecutar script con finalidades similares.

Dentro de nuestro ambiente en el cual desplegamos debemos acceder a la pagina ` http://127.0.0.1:8000/docs`:





# unittest
<!--  
docker compose -f docker-compose-dev.yml run --rm -e TZ=America/Argentina/Buenos_Aires rd_django bash -c "bash Action.sh --coverage"
-->
## Para el test completo 
```bash
services='tests'; \
flags="--rm -u $(id -u $USER):20 -e TZ=America/Argentina/Buenos_Aires"; \
docker compose run ${flags} ${services} bash -c "python3 -m unittest -v"
```


## Test Especifico
```bash
services='tests'; \
flags="--rm -u $(id -u $USER):20 -e TZ=America/Argentina/Buenos_Aires"; \
module="tests.test_process_gateway.Test_ProcessGatewayV1.test_create"; \
docker compose run ${flags} ${services} bash -c "python3 -m unittest -v ${module}" 
```


