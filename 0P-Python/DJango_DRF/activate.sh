#!/bin/bash

REQ_FILE="$PWD/requirements/requirements.txt"
VENV_FOLDER="$PWD/.venv"
#FLAGS='--system-site-packages'
set -e

function check_virtualenv() 
{
    if command -v virtualenv &> /dev/null;
    then
      return 0
    fi
  echo "virtualenv is not installed. Installing..."
  python3 -m pip install --user virtualenv
  echo "virtualenv installation complete."
  return 0  
}


## Funcion encargadda de crear el virtual enviroment
## $1 Opcional, folder name for enviroment, este sera el nuevo valor para VENV_FOLDER
function venv_create(){    
  ## si existe el directorio ya tenemos el venv
  [[ -d ${VENV_FOLDER} ]] && return 0 
   
  echo "Creando el Virtual Enviroment <${VENV_FOLDER}>"
  ## no existe el directorio creamos el virtual envelopment
  python3 -m venv ${FLAGS} ${VENV_FOLDER}
  if [[ $? -ne 0 ]]
  then
    echo "Failed to try created Virtual Enviroment <${VENV_FOLDER}>"
    return 1    
  fi 
  ## en este punto se creo el archivo bash '${VENV_FOLDER}/bin/activate'
  ## en este concatenamos todos los alias y setting actuales
  echo "unset PS1" >> ${VENV_FOLDER}/bin/activate
  echo "PS1='(.venv):\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;34m\]\W\[\033[00m\]]\$ '" >> ${VENV_FOLDER}/bin/activate  
  return 0
}

## Funcion que se encarga de instalar los requerimientos para pip
## \param[in] $1 Opcional, path file requerimientos 
## \return 
##   + 0 localizado e instalado
##   + 1 no se localizo el archivo
function venv_install_pipreq(){
  local ret_val  

  if [[ ! -f ${REQ_FILE} ]]
  then
    echo "pip file requeriment <${REQ_FILE}> not found"
    return 1
  fi
  if [[ ! -e  ${VENV_FOLDER}/bin/activate ]] || [[ ! -f  ${VENV_FOLDER}/bin/activate ]]
  then
    echo "file <${VENV_FOLDER}/bin/activate> not found"
    return 1
  fi
  ## Activamos el envelopment
  source ${VENV_FOLDER}/bin/activate
  ## prompt dentro del venv
  ## install packages  
  python -m pip install -r ${REQ_FILE}
  ## almacenamos el estado de la instalaccion
  ret_val=$?
  deactivate
  ## 
  return $ret_val
}

## Funcion que se encarga de habilitar el virtual enviroment
function venv_enable(){  
  bash --rcfile ${VENV_FOLDER}/bin/activate -i
}



function main()
{
  if [[ ! -z ${1} ]] && [[ ${1} == '--clean' ]]
  then
    if [[ ! -d ${VENV_FOLDER} ]]
    then
      echo "Folder <${VENV_FOLDER}> not found"
      return 0
    fi
    rm -fR ${VENV_FOLDER}
    return $?
  fi
  if [[ ! -d ${VENV_FOLDER} ]]
  then # si ya tenemos el enviroment solo debemos habilitarlo 
    # 1° Consultamos si tenemos el comando instalado, y de no lo instalamos
    check_virtualenv
    [[ $? -ne 0 ]] && return 1

    # 2° Creamos el venv, si este ya existe no hace nada
    venv_create
    [[ $? -ne 0 ]] && return 1

    # 3° Instalamos los requeriments
    venv_install_pipreq
    [[ $? -ne 0 ]] && return 1  
  fi
  venv_enable
  return 0
}


main "$@" && exit 0
