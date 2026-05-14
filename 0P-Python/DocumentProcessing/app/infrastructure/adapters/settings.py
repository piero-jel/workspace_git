

# third-party modules
from dotenv import dotenv_values
from celery import Celery
from redis import Redis



ENV_VARS:dict = dotenv_values()
if ENV_VARS is None:
    raise ValueError('Error, enviroment file not found')


REDISCLI_AUTH:str = ENV_VARS.get('REDISCLI_AUTH',None)
REDIS_URL:str     = ENV_VARS.get('REDIS_URL','localhost')
REDIS_PORT:int    = ENV_VARS.get('REDIS_PORT',6379)
REDIS_DB:int      = ENV_VARS.get('REDIS_DB',0)

KAFKA_URL:str     = ENV_VARS.get('KAFKA_URL','localhost')
KAFKA_PORT:int    = ENV_VARS.get('KAFKA_PORT',9092)

redis:Redis = Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    password=REDISCLI_AUTH,
    db=REDIS_DB
)

# app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')   
celery:Celery = Celery(
    'tasks',
    broker  = f'redis://:{REDISCLI_AUTH}@{REDIS_URL}:{REDIS_PORT}/0',
    backend = f'redis://:{REDISCLI_AUTH}@{REDIS_URL}:{REDIS_PORT}/0',
    result_extended=True
)


celery.conf.update(    
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)



# si hacemso esto : celery -A app worker --loglevel=info
#celery.autodiscover_tasks(['app.infrastructure.adaptersls'])

'''
app.autodiscover_tasks(['proj.tasks'])   

celery -A proj worker --loglevel=info
celery -A proj worker --loglevel=debug   
'''