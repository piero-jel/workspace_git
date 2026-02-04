'''
Docstring for 0T-TestScripts.UnitTest_Comicios.utils
'''
import json
from pathlib import Path
from datetime import datetime
from logging import ( Logger,
                        getLogger,basicConfig,
                        #INFO,
                        DEBUG
                    )

DIR_LOGS = f'{Path(__file__).resolve().parent}/logs'
CONFIG_LOGGING:dict = {
    'level'    : DEBUG,
    #'level'    : INFO,
    'filemode' : "a",
    #'format'   : "%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(funcName)s() - %(message)s",
    'format'   : "%(asctime)s.%(msecs)03d %(levelname)-8.8s- %(message)s",
    'datefmt'  : "%Y-%m-%d %H:%M:%S",
    'filename' : f"{DIR_LOGS}/test_{datetime.now().strftime('%Y%m%d')}.log"
}


def get_log(appname:str,config:dict=None)->Logger:
    '''
    funcion para obtener el objeto logger para una aplicacion
    
    :param appname: Nombre de la aplicacion
    :type appname: str

    :param config: Opcional, configuracion para el logger
    :type config: dict

    :return: objeto logger
    :rtype: Logger
    '''
    if config is None:
        config = CONFIG_LOGGING

    ret = getLogger(appname)
    basicConfig(**config)
    return ret


def strjson_to_dict(data:str)->dict:
    '''Funcion para convertir un json string a un dict
    Params
        data string con el json

    Return 
        dict : con la representacion del json
    '''
    return json.loads(data)


def dict_to_strjson(data:dict,tabs=None)->str:
    '''Funcion para convertir un dict a un json string
    Params
        data dict con los datos

    Return 
        str : string con la representacion json del dict
    '''
    if tabs:
        return json.dumps(data,indent=tabs)
    return json.dumps(data)


def dict_to_jsonfile(data:dict,filename:str,tab:int=2) -> None:
    ''' Dictionary dump to file JSON.

    Params
        - data    : dict, data to dump in file
        - filename: str, path/file del archivo
        - tab     : identation for dump
    '''
    with open(filename, 'w',encoding='utf-8') as file2write:
        json.dump(data, file2write,indent=tab)


def jsonfile_to_dict(path:str) -> dict|list:
    ''' Load json file in dict

    Params
        - path: str, path/file del archivo
    '''
    if not Path(path).exists():
        return None

    content:str = ''
    ## concatenamos el contenido sin espacios
    with open(path,"r",encoding='utf-8') as file2read:
        for it in file2read:
            tmp = it.rstrip()
            content += tmp.lstrip()

    return json.loads(content)
