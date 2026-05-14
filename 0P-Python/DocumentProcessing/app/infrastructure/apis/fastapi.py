'''
FIXME add copyrigth a todos los py que corresponda
'''
# build module
from typing import Optional

# third-party modules
from fastapi import FastAPI #,Depends
from pydantic import BaseModel

# project modules
from app.application.services import ProcessGateway
from app.infrastructure.adapters.tasks_celery import TaskProcessingGateway
from app.infrastructure.adapters.worker_redis import (
    #WorkerContextRedis, 
    WorkerIdRedis,
    WorkerRedis,
    WorkerStatus,
)

fastapi:FastAPI = FastAPI()





class PipelineProcessCreate(BaseModel):
    name: str
    topic: str
    content:str
    compression:Optional[str|list[str]] = None
    pipeline_config:Optional[str|list[str]] = None

class PipelineProcessPut(BaseModel):
    status: str


@fastapi.post("/pipeline_process/")
async def process_create(order:PipelineProcessCreate):
    ''' Metodo para Enviar documento a procesar
    [POST] url/pipeline_process/

        body example:
    ``` json
    {
        "name"        : "Nombre de archivo",
        "topic"       : "Topico/tema en el cual se publicara al finalizar",
        "compression" : "Opcional, compresion puede ser: gzip, snappy, lz4, zstd",
        "content"     : "string con el contenido del archivo",
        "pipeline_config" : "Opcional nombre de los stage del Provider"
    }
    ```

    Opcion por defecto:
    ```
    url='http://127.0.0.1:8000/pipeline_process/';\\
    body='{"name": "example1","topic": "string","content": "Esto es un Ejemplo" }';\\
    header=(-H 'accept: application/json' -H 'Content-Type: application/json');\\
    curl -X 'POST' ${url} "${header[@]}" -d "${body}" -w '\\n'
    ```

    Pasando pipeline_config como un string separado por comas:
    ```
    url='http://127.0.0.1:8000/pipeline_process/';\\
    body='{"name": "example1","topic": "string","content": "Esto es un Ejemplo 2","pipeline_config" : "Extraction,Analysis,Enrichment"}';\\
    header=(-H 'accept: application/json' -H 'Content-Type: application/json');\\
    curl -X 'POST' ${url} "${header[@]}" -d "${body}" -w '\\n'
    ```

    Pasando pipeline_config como un array de string:
    ```
    url='http://127.0.0.1:8000/pipeline_process/';\\
    body='{"name": "example1","topic": "string","content": "Esto es un Ejemplo 2","pipeline_config" : ["Extraction "," Analysis ", "Enrichment"]}';\\
    header=(-H 'accept: application/json' -H 'Content-Type: application/json');\\
    curl -X 'POST' ${url} "${header[@]}" -d "${body}" -w '\\n'
    ```
    '''
    if order.pipeline_config is None:
        order.pipeline_config = ['extraction']

    elif isinstance(order.pipeline_config,str):
        order.pipeline_config = [x.strip().lower() for x in order.pipeline_config.split(',')]

    elif isinstance(order.pipeline_config,list):
        order.pipeline_config = [x.strip().lower() for x in order.pipeline_config]

    pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
    job_id:str = pr_gateway.create(TaskProcessingGateway.launch(order.model_dump()))
    return {
        'job_id':job_id, **order.model_dump()
    }


@fastapi.get("/pipeline_process/{job_id}")
async def process_get(job_id:str):
    '''
    Consultar estado de un job, [GET]  pipeline_process/<job_id>

    Get, con info detallada
    ```
    job_id="$(uuidgen --time)" ;\\
    uri="http://127.0.0.1:8000/pipeline_process/${job_id}" ;\\
    curl -sS "${uri}" -i -X GET -w '\\n'
    ```

    Get con informacion resumida
    ```
    job_id="$(uuidgen --time)" ;\\
    uri="http://127.0.0.1:8000/pipeline_process/${job_id}" ;\\
    curl -sS "${uri}" -X GET -w '\\n'
    ```
    '''
    pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
    return pr_gateway.get(job_id)


@fastapi.put("/pipeline_process/{job_id}")
async def process_discard(job_id:str,option:PipelineProcessPut):
    '''
    Cancelar o Eliminar un job, [PUT]  pipeline_process/<job_id> {"status": "'cancel|delete'"}

    Cancel Job
    ```
    job_id="$(uuidgen --time)";\\
    url="http://127.0.0.1:8000/pipeline_process/${job_id}";\\
    header=(-H 'accept: application/json' -H 'Content-Type: application/json');\\
    body='{"status": "cancel"}';\\
    curl -X 'PUT' "${url}" "${header[@]}" -d "${body}" -w '\\n'
    ```

    Delete Job
    ```
    job_id="$(uuidgen --time)";\\
    url="http://127.0.0.1:8000/pipeline_process/${job_id}";\\
    header=(-H 'accept: application/json' -H 'Content-Type: application/json');\\
    body='{"status": "delete"}';\\
    curl -X 'PUT' "${url}" "${header[@]}" -d "${body}" -w '\\n'
    ```
    '''

    '''
    job_id="$(uuidgen --time)";\
    url="http://127.0.0.1:8000/pipeline_process/${job_id}";\
    header=(-H 'accept: application/json' -H 'Content-Type: application/json');\
    body='{"status": "cancel"}';\
    curl -X 'PUT' "${url}" "${header[@]}" -d "${body}" -w '\n'
    '''
    st:str = option.status.lower()
    pr:ProcessGateway = ProcessGateway(WorkerRedis())
    if st == 'cancel':
        return pr.cancel(job_id)

    if st == 'delete':
        return pr.delete(job_id)

    #return {'job_id':job_id,**option.model_dump()}
    return {
        "job_id": job_id,
        "message": f"Estado '{option.status}' no permitido, solo 'cancel' o 'delete'",
        **option.model_dump()
    }


@fastapi.get("/pipeline_process/list/")
@fastapi.get("/pipeline_process/list/{status}")
async def process_list(status:Optional[str] = None):
    '''
    Retorna el listado de Job que se encuentran en un estado en particualar.
    [GET]  pipeline_process/list/[<status>]
    Los estados posibles en los que puede estar el Proccess

    - `pending`
    - `processing`
    - `completed`
    - `failed`
    - `cancelled`

    Get, status=cancelled
    ```
    status="cancelled" ;\\
    url="http://127.0.0.1:8000/pipeline_process/list/${status}" ;\\
    curl -sS "${url}" -i -X GET -w '\\n'
    ```

    Get default, el listado de todos los estados
    ```
    url="http://127.0.0.1:8000/pipeline_process/list/";\\
    curl -sS "${url}" -i -X GET -w '\\n'
    ```
    '''
    pr_gateway:ProcessGateway = ProcessGateway(WorkerRedis())
    #job_list:dict = pr_gateway.get_list(status)
    #return {"status": status}
    return pr_gateway.get_list(status)


## Run 
# fastapi dev app/infrastructure/apis/fastapi.py
# bash activate.sh --run fastapi dev app/infrastructure/apis/fastapi.py

## Doc
# http://127.0.0.1:8000/docs
