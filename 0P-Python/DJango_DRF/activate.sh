#!/bin/bash
source "${PWD}/activate.ini"

#FLAGS='--system-site-packages'
set -e

## funcion para el log de mensajes por stdout
## $@ lista de parametros a imprimir
function venv::log(){
  [[ ${VENV_LOGGER} == 'true' ]] && echo $@
  return 0
}

## funcion que se encarga de verificar si existe el virtual enviroment
## si el mismo no existe verifica los binarios necesarios y crea el venv
## 
function venv::check(){
  ## check pip install
  if ! command -v pip &> /dev/null; then
    venv::log "pip not fund" 
    sudo apt install -y python3-pip python3-venv
  else 
    venv::log "pip installed";
  fi

  if [[ ${VENV_SERVICE_ENABLE} == "true" ]];then         
    if ! command -v nginx &> /dev/null; then
      venv::log "nginx not fund" 
      sudo apt install -y nginx
    else 
      venv::log "nginx installed";
    fi
  fi
  
  ## check virtualenv instll
  if command -v virtualenv &> /dev/null;
  then
    return 0
  fi
  venv::log "virtualenv is not installed. Installing..."
  python3 -m pip install --user virtualenv
  venv::log "virtualenv installation complete."
  return 0  
}


## Funcion encargada de crear el virtual enviroment
## $1 Opcional, folder name for enviroment, este sera el nuevo valor para VENV_FOLDER
function venv::create(){    
  ## si existe el directorio ya tenemos el venv
  [[ -d ${VENV_FOLDER} ]] && return 0 
   
  venv::log "Creando el Virtual Enviroment <${VENV_FOLDER}>"
  ## no existe el directorio creamos el virtual envelopment
  python3 -m venv ${VENV_FLAGS} ${VENV_FOLDER}
  if [[ $? -ne 0 ]]
  then
    venv::log "Failed to try created Virtual Enviroment <${VENV_FOLDER}>"
    return 1    
  fi 
  ## en este punto se creo el archivo bash '${VENV_FOLDER}/bin/activate'
  ## en este concatenamos todos los alias y setting actuales
  venv::log "unset PS1" >> ${VENV_FOLDER}/bin/activate
  venv::log "PS1='(.venv):\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;34m\]\W\[\033[00m\]]\$ '" >> ${VENV_FOLDER}/bin/activate  
  return 0
}

## Funcion que se encarga de instalar los requerimientos para pip
## \param[in] $1 Opcional, path file requerimientos 
## \return 
##   + 0 localizado e instalado
##   + 1 no se localizo el archivo
function venv::install_pipreq(){
  local ret_val  

  if [[ ! -f ${VENV_REQ_FILE} ]]
  then
    venv::log "pip file requeriment <${VENV_REQ_FILE}> not found"
    return 1
  fi
  if [[ ! -e  ${VENV_FOLDER}/bin/activate ]] || [[ ! -f  ${VENV_FOLDER}/bin/activate ]]
  then
    venv::log "file <${VENV_FOLDER}/bin/activate> not found"
    return 1
  fi
  ## Activamos el envelopment
  source ${VENV_FOLDER}/bin/activate
  ## prompt dentro del venv
  ## install packages  
  python -m pip install -r ${VENV_REQ_FILE}
  ## almacenamos el estado de la instalaccion
  ret_val=$?
  deactivate
  ## 
  return $ret_val
}

## Funcion que se encarga de habilitar el virtual enviroment
function venv::enable(){
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
    venv::check
    [[ $? -ne 0 ]] && return 1

    # 2° Creamos el venv, si este ya existe no hace nada
    venv::create
    [[ $? -ne 0 ]] && return 1

    # 3° Instalamos los requeriments
    venv::install_pipreq
    [[ $? -ne 0 ]] && return 1  
  fi
  venv::enable
  return 0
}


main "$@" && exit 0
