#!/bin/bash
#=====================================================================================================
### BEGIN Copyright
# Copyright 2025, Jesus Emanuel Luccioni
# All rights reserved.
#
# This file is part of devops for Open Container (in this case docker )
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##
### END   Copyright
#
#=====================================================================================================
#
#=====================================================================================================
THIS_NAME=${0##*/}

#. $PWD/.env
source "${PWD}/config.ini"


#=====================================================================================================
## [BEGIN locals functions]
#=====================================================================================================

## Verifica si el contenedor existe
## $1: container name
## return
##   0 : found
##   1 : not found
function __check_container()
{
  if [[ $# -lt 1 ]]; then return 1 ; fi
  local container_name resp
  container_name=$1
  resp=$(docker ps -af "name=${container_name}")

  if [[ ! ${resp[@]} =~ ${container_name} ]]
  then
    return 1
  fi
  return 0
  #   for it in ${resp[@]}
  #   do
  #     if [[ ${it} == ${container_name} ]]; then
  #       return 0
  #     fi
  #   done
  return 1
}


## Obtiene el id de un contenedor
## $1: container name
## return
##   0 : found, update CONTAINER_ID
##   1 : not found
CONTAINER_ID=""
function __get_container_id(){
  local container_id
  container_id=$(docker ps -qa -f name="${1}")
  if [[ -z ${container_id} ]]
  then
    return 1
  fi
  CONTAINER_ID=${container_id}
  return 0
}


## Obtiene el path file
## $1: target --file or -f
## $2: path file
## return
##   0 : found, update PARAM_FILE
##   1 : not found, error
PARAM_FILE=""
function __get_param_file(){
  local compose_file

  if [[ $# -lt 2 ]]
  then
    PARAM_FILE=${COMPOSE_FILE}
    return 0
  fi
  if [[ $1 != '-f' ]] && [[ $1 != '--file' ]]
  then
    echo "Error options <${1}> not valid"
    return 1
  fi
  compose_file=${2:-${COMPOSE_FILE}}

  if [[ ! -z ${compose_file} ]] && [[ ! -f ${compose_file} ]]
  then
    echo "File <${compose_file}> not found"
    return 1
  fi
  PARAM_FILE=${compose_file}
  return 0
}
#=====================================================================================================
## [END   locals functions]
#=====================================================================================================

## $1 Parametro Opcional file docker compose
function container::build(){

  __get_param_file "$@"
  [[ $? -ne 0 ]] && return 1

  if [[ ${BASH_DEBUG} == "true" ]]
  then
    echo "docker compose --file \"${PARAM_FILE}\" build"
  else
    docker compose --file "${PARAM_FILE}" build
  fi
  return $?
}

## $1 Parametro Opcional file docker compose
function container::up(){
  __get_param_file "$@"
  [[ $? -ne 0 ]] && return 1

  if [[ ${BASH_DEBUG} == "true" ]]
  then
    echo "docker compose --file \"${PARAM_FILE}\" up -d --remove-orphans"
  else
    docker compose --file "${PARAM_FILE}" up -d --remove-orphans
  fi
  return $?
}

## $1 Parametro Opcional file docker compose
function container::down(){
  __get_param_file "$@"
  [[ $? -ne 0 ]] && return 1

  if [[ ${BASH_DEBUG} == "true" ]];then
    echo "docker compose --file \"${PARAM_FILE}\" down"
  else
    docker compose --file "${PARAM_FILE}" down
  fi
  return $?
}


function container::service(){
  local trj_srv srv tarjet
  trj_srv=( start stop restart status )
  if [[ ! ${trj_srv[@]} =~ ${1} ]]
  then
    echo "action <${1}> no permitida"
    return 1
  fi
  trj=${1}
  tarjet=${2:-'all'}

  case "${tarjet}" in
    'ddbb')
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker compose --file ${COMPOSE_FILE} ${trj} ${SERVICE_DDBB}"
      else
        docker compose --file ${COMPOSE_FILE} ${trj} ${SERVICE_DDBB}
      fi
    ;;
    'app')
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker compose --file ${COMPOSE_FILE} ${trj} ${SERVICE_APP}"
      else
        docker compose --file ${COMPOSE_FILE} ${trj} ${SERVICE_APP}
      fi
    ;;
    'nginx')
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker compose --file ${COMPOSE_FILE} ${trj} ${SERVICE_NGINX}"
      else
        docker compose --file ${COMPOSE_FILE} ${trj} ${SERVICE_NGINX}
      fi
    ;;
    'all')
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker compose --file ${COMPOSE_FILE} ${trj}"
      else
        docker compose --file ${COMPOSE_FILE} ${trj}
      fi
    ;;
    *)
      echo "opcion <${tarjet}> incorrecta"
      return 1
    ;;
  esac
  return $?
}

## $1 {ddbb,app,all}
function container::start(){
  container::service "start" ${1}
  return $?
}

## $1 {ddbb,app,all}
function container::stop(){
  container::service "stop" ${1}
  return $?
}

## $1 {ddbb,app,all}
function container::restart(){
  container::service "restart" ${1}
  return $?
}

## $1 {ddbb,app,all}
function container::status(){
  container::service "status" ${1}
  return $?
}

## $1 {ddbb,app}
function container::term(){
  local id_container
  case "$1" in
    'ddbb')
      __get_container_id "${CONTAINER_DDBB}"
      if [[ $? -ne 0 ]]
      then
        echo "Contenedor <${CONTAINER_DDBB}> not found"
        return 1
      fi
      id_container=${CONTAINER_ID}
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker exec -it \"${id_container}\" \"${ENTRYPOINT_DDBB}\""
      else
        docker exec -it "${id_container}" "${ENTRYPOINT_DDBB}"
      fi
    ;;
    'app')
      __get_container_id "${CONTAINER_APP}"
      if [[ $? -ne 0 ]]
      then
        echo "Contenedor <${CONTAINER_APP}> not found"
        return 1
      fi
      id_container=${CONTAINER_ID}
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker exec -it \"${id_container}\" \"${ENTRYPOINT_APP}\""
      else
        docker exec -it "${id_container}" "${ENTRYPOINT_APP}"
      fi
    ;;
    'nginx')
      __get_container_id "${CONTAINER_NGINX}"
      if [[ $? -ne 0 ]]
      then
        echo "Contenedor <${CONTAINER_NGINX}> not found"
        return 1
      fi
      id_container=${CONTAINER_ID}
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker exec -it \"${id_container}\" \"${CONTAINER_NGINX}\""
      else
        docker exec -it "${id_container}" "${CONTAINER_NGINX}"
      fi
    ;;
    *)
      echo "opcion <$1> para --term  incorrecta"
      return 1
    ;;
  esac
  return $?
}


## $1 {ddbb,app}
## $2 command to run in container
function container::run(){
  local id_container entry_point flags

  flags="--rm -u $(id -u $USER):20 -e TZ=America/Argentina/Buenos_Aires"
  case "$1" in
    'ddbb')
      # __get_container_id "${CONTAINER_DDBB}"
      # if [[ $? -ne 0 ]]
      # then
      #   echo "Contenedor <${CONTAINER_DDBB}> not found"
      #   return 1
      # fi
      entry_point=${2:-${}}
      #id_container=${CONTAINER_ID}|
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker compose --file ${COMPOSE_FILE} run ${flags} ${SERVICE_DDBB} ${ENTRYPOINT_DDBB} ${entry_point}"
      else
        #docker exec "${id_container}" "${entry_point}"
        docker compose --file ${COMPOSE_FILE} run ${flags} ${SERVICE_DDBB} ${ENTRYPOINT_DDBB} ${entry_point}
      fi
    ;;
    'app')      
      entry_point=${2:-${ENTRYPOINT_APP}}      
      if [[ ${BASH_DEBUG} == "true" ]];then
        echo "docker compose --file ${COMPOSE_FILE} run ${flags} ${SERVICE_APP} ${ENTRYPOINT_DDBB} ${entry_point}"
      else
        # docker compose -f docker-compose-dev.yml run --rm -e TZ=America/Argentina/Buenos_Aires rd_django bash -c "bash Action.sh --coverage"
        docker compose --file ${COMPOSE_FILE} run ${flags} ${SERVICE_APP} ${ENTRYPOINT_DDBB} ${entry_point}
      fi
      return 0
    ;;
    *)
      echo "opcion <$1> para --term  incorrecta"
      return 1
    ;;
  esac
  return $?
}


## Sin params
function container::top(){
  __get_param_file "$@"
  [[ $? -ne 0 ]] && return 1

  if [[ ${BASH_DEBUG} == "true" ]];then
    echo "docker compose --file \"${PARAM_FILE}\" stats"
  else
    docker compose --file "${PARAM_FILE}" stats
  fi
  return $?
}


## Sin params
function container::logs(){
  if [[ ${BASH_DEBUG} == "true" ]];then
    echo "docker compose --file \"${COMPOSE_FILE}\" logs -tf"
  else
    docker compose --file "${COMPOSE_FILE}" logs -tf
  fi
  return $?
}



function container::info(){
  echo "COMPOSE_FILE     : ${COMPOSE_FILE}"
  echo "CONTAINER_APP    : ${CONTAINER_APP}"
  echo "CONTAINER_DDBB   : ${CONTAINER_DDBB}"
  echo "ENTRYPOINT_APP   : ${ENTRYPOINT_APP}"
  echo "ENTRYPOINT_DDBB  : ${ENTRYPOINT_DDBB}"
  echo "DEFAULT_TARGET   : ${DEFAULT_TARGET}"
}

function container::coverage(){
  container::run "app" "Action.sh --coverage"
  [[ $? -ne 0 ]] && return 0  
  ou_file='rd_wepapp/htmlcov/index.html'
  if command -v gio &> /dev/null;
  then
    gio open "$PWD/${ou_file}"
  else
    echo "Report, open with browser: <$PWD/${ou_file}>"
  fi
  return 0
}



## $1 Parametro Opcional file docker compose
function container::clean(){  
  local images  
  # obtenemos el nombre del archivo p/docker compose
  __get_param_file "$@"
  [[ $? -ne 0 ]] && return 1

  images=$(docker compose --file "${PARAM_FILE}" images -q)
  docker compose --file "${PARAM_FILE}" stop
  docker compose --file "${PARAM_FILE}" down
  docker compose --file "${PARAM_FILE}" rm -fsv

  if [[ ! -z ${images} ]];then
    echo "images<${images}>"
    docker rmi ${images}
  fi

  # clean builder chaceh
  #docker image prune -af
  docker builder prune -af
  ## delete dir  
  sudo find . -name __pycache__ -type d -exec rm -rf {} +  
  sudo find . -name htmlcov -type d -exec rm -rf {} +
  sudo find . -name .coverage -type f -exec rm -rf {} +
  sudo find . -name db.sqlite3 -type f -exec rm -rf {} +
  return 0
}




function container::help {
  local target app_name
  arrHelp=( '--build' '--up'
            '--down'
            '--start'
            '--stop'
            '--restart'
            '--term'
            '--top'
            '--logs'
            '--coverage'
            '--clean'
          )

  app_name=${1}
  if [[ -z ${2} ]] || [[ ! ${arrHelp[@]} =~ ${2} ]]
  then
    [[ ${2} != '--help' ]] && echo "Opcion <${2}> incorrecta intente con:"
    target='--help'
  else
    target=${2}
  fi

  case "$target" in
  '--build')
    cat << EOH >&2
--build [-f <path-file> | --file <path-file>]
  Construye los contenedores, podemos usar '-f <path-file>' o '--file <path-file>' para usar un archivo de 
  configuracion diferente.

Example:
  ${app_name} --build
  ${app_name} --build --file docker-compose-dev.yml

EOH
  return 0
  ;;
  '--up')
    cat << EOH >&2
--up [-f <path-file> | --file <path-file>]
  Inicia los contenedores,  podemos usar '-f <path-file>' o '--file <path-file>' para usar un archivo de configuracion diferente.

Example:
  ${app_name} --up
  ${app_name} --up --file docker-compose-dev.yml

EOH
  return 0
  ;;
  '--down')
    cat << EOH >&2
--down [-f <path-file> | --file <path-file>]
  Borra los contenedores, podemos usar '-f <path-file>' o '--file <path-file>' para usar un archivo de configuracion diferente.

Example:
  ${app_name} --down
  ${app_name} --down --file docker-compose-dev.yml

EOH
  return 0
  ;;

  '--start')
    cat << EOH >&2
--start <target>
  Inicia el servicio del contenedor, target:
    + app : inicia solo el service para el contenedor de la aplicacion
    + ddbb : inicia solo el service para el contenedor de la base de datos
    + all : Inicia todos los servicios

Example:
  ${app_name} --start app
  ${app_name} --start ddbb
  ${app_name} --start all

EOH
  return 0
  ;;

  '--stop')
    cat << EOH >&2
--stop <target>
  Detiene el servicio del contenedor, target:
    + app : detiene solo el service para el contenedor de la aplicacion
    + ddbb : detiene solo el service para el contenedor de la base de datos
    + all : detiene todos los servicios

Example:
  ${app_name} --stop app
  ${app_name} --stop ddbb
  ${app_name} --stop all

EOH
  return 0
  ;;

  '--restart')
    cat << EOH >&2
--restart <target>
  Reinicia el servicio del contenedor, target:
    + app : Reinicia solo el service para el contenedor de la aplicacion
    + ddbb : Reinicia solo el service para el contenedor de la base de datos
    + all : Reinicia todos los servicios

Example:
  ${app_name} --restart app
  ${app_name} --restart ddbb
  ${app_name} --restart all

EOH
  return 0
  ;;

  '--logs')
    cat << EOH >&2
--logs
  Target para ver los log en tiempo real de los servicios.

Example:
  ${app_name} --logs

EOH
  return 0
  ;;

  '--clean')
    cat << EOH >&2
--clean
  Realiza el clean de los directorios creados de forma automatica.

Example:
  ${app_name} --clean

EOH
  return 0
  ;;

  '--top')
    cat << EOH >&2
--top [-f <path-file> | --file <path-file>]
  Visulaiza el monitores de los contenedores, podemos usar '-f <path-file>' o '--file <path-file>'
  para usar un archivo de configuracion diferente.

Example:
  ${app_name} --top  
  ${app_name} --top --file docker-compose-dev.yml

EOH
  return 0
  ;;

  '--term')
    cat << EOH >&2
--term <target>
  Conexion a una terminal dentro del Contendor deseado:
    + app : Terminal al contenedor de la aplicacion
    + ddbb : Terminal al contenedor de la base de datos

Example:
  ${app_name} --term app
  ${app_name} --term ddbb

EOH
  return 0
  ;;
  '--coverage')
    cat << EOH >&2
--coverage 
  Realiza el test y genera el reporte 'code coverage' del codigo.
    
Example:
  ${app_name} --coverage

EOH
  return 0
  ;;


  '--help'|'-h')
  cat << EOH >&2
  ${app_name} {--help | -h }        Visualiza Help General
  ${app_name} {--help | -h } <target> para un help Especifico

EOH
    for it in ${arrHelp[@]}
    do
      container::help "${app_name}" "${it}"
    done
  return 0
  ;;

  *)
cat << EOH >&2
  ${app_name} {--help | -h }        Llamado a help con parametro <${target}> incorrecto (no documentado).

EOH
    return 0
  ;;
  esac
}


