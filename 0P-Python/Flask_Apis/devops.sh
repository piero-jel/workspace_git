#!/bin/bash
#=====================================================================================================
### BEGIN Copyright
# Copyright 2024, Jesus Emanuel Luccioni
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
CONTAINER_NAME='FlaskApis'
IMGAGE_NAME='flask-apis'

## BEGIN setting default, if config not load
### DOCKERCONTAINER
if [[ ! -v DOCKERCONTAINER ]]; then DOCKERCONTAINER=${CONTAINER_NAME}; fi

if [[ ! -v DOCKERCONTAINER ]]; then DOCKERIMAGE="jeluccioni/${IMGAGE_NAME}"; fi
## END   setting default, if config not load

## para distro debian y deribados
ENTRYPOINT='bash'


CLEAN_ARR_FILES=( )

CLEAN_ARR_COMODIN_FILES=( 
  "logs/*.log" 
)

CLEAN_ARR_FOLDERS=(
  
)

CLEAN_ARR_DIR=( 
  "instance/"
  "__pycache__/"
  "ApiErrorHandler/__pycache__"
  "Config/__pycache__"
  "Models/__pycache__/"
)

##
## $1 single target valor por defecto -h/--help
## $2 <$1> target
function msg_help()
{
  local app arg1 
  app=${0##*/}
  if [ "$#" -eq "2" ];then
    arg1=$2
  else
    arg1="-h"
  fi

  arrHelp=( '--start'
            '--stop'
            '--kill'
            '--status'
            '--build'
            '--terminal'
            '--rm'            
            '--attach'
            '--rm-build-cache'
            '--inspect'
            '--logs'                        
            '--restart'
            '--rebuild'
            '--clean'
            '--top'
          )

  case "$arg1" in
  --top)
    cat << EOH >&2
--top
  top     
  
  View List process running actualemtne para la configuraciones restablecidas.

EOH
  return 0
  ;;  
  --rebuild)
    cat << EOH >&2
--rebuild 
  rebuild 
  
  Reconstruye la imagen y el contenedor, util cuando se realizan cambios sobre los archivos de configuracion.

EOH
  return 0
  ;;
  
  --restart)
    cat << EOH >&2
--restart [CONTAINER-NAME]
  restart [CONTAINER-NAME]

  Detiene y luego inicia el contenedor nuevamente.
  [CONTAINER-NAME] opcional Nombre del Container, por defecto usa el configurado <${DOCKERCONTAINER}>,
  Si no pasamos este reinia todos los configurados en el docker-compose.yml.

EOH
  return 0
  ;;
  
  --logs)
    cat << EOH >&2
--logs [CONTAINER-NAME]
 -l [CONTAINER-NAME]
  logs [CONTAINER-NAME]

  [CONTAINER-NAME] opcional Nombre del Container, por defecto usa el configurado <${DOCKERCONTAINER}>
  Nos muestra los log del contenedor, util para el caso de que el contenedor se detubo de forma inesperada.
  Si no pasamos este visualiza el log general.
EOH
  return 0
  ;;

  --status)
    cat << EOH >&2
--status [CONTAINER-NAME]
  status [CONTAINER-NAME]

  [CONTAINER-NAME] opcional Nombre del Container, por defecto usa el configurado <${DOCKERCONTAINER}>
  Realiza la busqueda del Contenedor en el servico corriendo en el host y retorna el Status.
  Si no pasamos este visualiza el status general.
  
EOH
  return 0
  ;; 
  
  --inspect)
    cat << EOH >&2
--inspect [CONTAINER-NAME]
  inspect [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Return JSON with low-level information from Container objects
  Si no pasamos este visualiza el inspect general.
  
EOH
  return 0
  ;;  

  --terminal|-t)
    cat << EOH >&2
--terminal [CONTAINER-NAME]
  terminal [CONTAINER-NAME]
        -t [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Open new terminal session with ${ENTRYPOINT} tty, conect to container run.
  Podemos tener varias terminales conectadas de forma simultanea a un contenedor
  en ejecucion.  
  
EOH
  return 0
  ;;
  
  --rm-build-cache)
    cat << EOH >&2
--rm-build-cache
  del-build-cache

  Remove build cache
  
EOH
  return 0
  ;;
 
  --attach)
    cat << EOH >&2
--attach [CONTAINER-NAME]
  attach [CONTAINER-NAME]

  Docker container <${DOCKERCONTAINER}> attach
  Attach local standard input, output, and error streams to a running container, default  <${DOCKERCONTAINER}>.


EOH
    return 0
  ;;

  --start)
    cat << EOH >&2
 -s [CONTAINER-NAME]    
--start [CONTAINER-NAME]
  start [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Inicia el Contenedor, previamente creado (de lo contrario notificara error).

EOH
    return 0
  ;;

  --stop)
    cat << EOH >&2
--stop [CONTAINER-NAME]
  stop [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Detiene el Contenedor, previamente creado e iniciado (de lo contrario notificara error).  

EOH
    return 0
  ;;
  
  --kill)
    cat << EOH >&2
 -k [CONTAINER-NAME]
--kill [CONTAINER-NAME]
  kill [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Envia la señal correspondiente al Servicio para detenerlo de manera forzada al
  Contenedor, previamente creado e iniciado (de lo contrario notificara error).

EOH
    return 0
  ;;  
  
  --build)
    cat << EOH >&2
--build 
     -b 
  build 
     
  Default values:    
    + Container ${DOCKERCONTAINER}

  Construye el proyecto con las imagenes y conetenedors establecidos en 'docker-compose.yml'.

EOH
    return 0
  ;;

  --rm)
    cat << EOH >&2
--rm

  Remove todos los contenedores establecidos en 'docker-compose.yml'.  

EOH
    return 0
  ;;
  
  --clean)
    cat << EOH >&2
--clean
  Clean folder de trabajos, files and folder autogenerated for build aplications, para las configuraciones actuales elimina los siguentes archivos y directorios
  
EOH
  CleanFilesAndFolders "0"
  return 0
  ;;  

  --help|-h)
  cat << EOH >&2
  $app {--help | -h }        Visualiza Help General
  $app {--help | -h } --all  Visualiza Help Especifico para todos los Targets

  Para Visualizar Help Especifico Intente con:
EOH
  for it in ${arrHelp[@]}
  do
    cat << EOH >&2
    $app {--help | -h} $it
EOH
  done

  return 0
  ;;

  --all)
    msg_help "-h"
    echo
    for it in ${arrHelp[@]}
    do
      #echo "msg_help -h $it"
      msg_help "-h" "$it"
      echo
    done
    return 0
  ;;
  *)
cat << EOH >&2
    -h                             : llamado a help con parametro <$arg1> incorrecto (no documentado).
EOH
    msg_help "-h" "--all"
    return 0
  ;;  
  esac
}

## $1 appname
## $2 target
function status_print()
{
  local app command flg
  if [ "$#" -ne "3" ];then return 1;fi

  flg=$3
  app=$1
  command=$2

  if [ "$flg" -eq "0" ];then
    echo "\"$app $command\" success"
  else
    echo "\"$app $command\" failure"
  fi
}

## $1: <image-name>:<tag>”
function CheckImageInLocalRegistry()
{
  if [ "$#" -lt "1" ]; then return 1 ; fi
  local img_name resp
  img_name=$1
  
  resp=$(docker images -f reference="${img_name}")
  for it in ${resp[@]}
  do    
    if [ "$it" == "${img_name}" ]; then
      return 0
    fi
  done  
  return 1
}

## $1: <image-name>:<tag>”
function CheckContainer()
{
  if [ "$#" -lt "1" ]; then return 1 ; fi
  local container_name resp
  container_name=$1     
  resp=$(docker ps -af "name=${container_name}")
  for it in ${resp[@]}
  do    
    if [ "$it" == "${container_name}" ]; then
      return 0
    fi
  done  
  return 1
}


## $1: type {0: print only | 1: clean }
function CleanFilesAndFolders()
{
  locale type
  if [ "$#" -ne "1" ]; then type=0; else type=$1;fi
  
  #echo "type $type"
  if [ $type == "1" ];then echo "clean comodin files" ;else echo "Clean list Files";fi
  for it in "${CLEAN_ARR_COMODIN_FILES[@]}"
  do
    for it2 in $(ls $it 2>/dev/null )
    do
      if [ -f "$it2" ]
      then
        if [ $type == "1" ];then sudo rm -f $it2;else echo "  $it2";fi
        #sudo rm -f $it2
      else
        echo "File <$it2> not found."
      fi        
    done        
  done
    
  if [ $type == "1" ];then echo "clean array files" ;fi
  for it in "${CLEAN_ARR_FILES[@]}"
  do
    if [ -f "$it" ]
    then
      if [ $type == "1" ];then sudo rm -f $it; else echo "  $it";fi
      #echo "rm -f $it"
      #sudo rm -f $it
    else
      echo "File <$it> not found."
    fi
  done
  
  echo 
  if [ $type == "1" ];then echo "clean array folders with prefix" ;else echo "Clean list Folders";fi  
  for it in "${CLEAN_ARR_FOLDERS[@]}"
  do
    for it2 in $(ls $it 2>/dev/null)
    do      
      if [ -d "$it$it2" ]
      then
        if [ $type == "1" ];then sudo rm -fR "$it$it2"; else echo "  $it$it2";fi
        #sudo rm -fR "$it$it2"
      else
        echo "Folder <$it$it2> not found."
      fi        
    done        
  done
  
  
  if [ $type == "1" ];then echo "clean array folders" ;fi
  for it in "${CLEAN_ARR_DIR[@]}"
  do
    if [ -d "$it" ]
    then
      if [ $type == "1" ];then sudo rm -fR "$it"; else echo "  $it";fi
      #sudo rm -fR "$it"
    else
      echo "Folder <$it> not found."
    fi
  done
  return 0
    

}

function main()
{  
  local app target
  app=${0##*/}  
  if [ "$#" -eq '0' ]; then
    # por defecto tomamos el target terminal
    target="-s"
  else
    target=$1
  fi 
  
  case "$target" in    
    --top|top)
      docker compose top
      return 0
    ;;
    --rebuild|rebuild)
      docker compose down
      docker compose up -d      
      return 0      
    ;;
    
    restart|--restart)      
      if [ "$#" -gt "1" ]
      then
        doceker restart "$2"
        docker compose exec "$2" ${ENTRYPOINT}
        return 0
      fi
      doceker compose restart      
      return 0
    ;;
    
    inspect|--inspect)
      # Return low-level information on Container objects
      for it in $(docker compose images -q)
      do 
        echo "inspect ${it}" 
        docker inspect "${it}"
      done      
      return 0
    ;;
    
    del-build-cache|--rm-build-cache)
      docker builder prune -af
      return 0
    ;;   
            
    build|--build|-b)
      # build and start in daemon
      docker compose up -d      
      return 0
    ;;
    
    -s|start|--start)
      if [ "$#" -gt "1" ]; then
        echo "docker start $2"
        docker compose start        
        return 0      
      fi      
      echo "docker compose start"
      docker compose start      
      return 0
    ;;
    
    status|--status)
      # listamso las imagenes
      docker compose images
      # los proceso corriendo
      docker compose top
      
      # si pasamos una contenedor name, print status de este
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        return 0        
      fi
      
      CheckContainer "${container_name}"
      if [ "$?" -eq "0" ]; then
        echo "Localized Container <${container_name}> in Local host"        
        docker ps -s -af "name=${container_name}"        
      else
        echo "Container <${container_name}> not found"
      fi      
      return 0      
    ;;
    
    -l|logs|--logs)
      local container_name
      if [ "$#" -gt "1" ]; then
        docker logs -t "$2"
        return 0
      fi
      docker compose logs      
      return 0
    ;;

    stop|--stop)
      if [ "$#" -gt "1" ]; then
        docker stop $2
        return 0      
      fi      
      docker compose stop
      return 0
    ;;

    -k|kill|--kill)      
      if [ "$#" -gt "1" ]; then
        docker kill $2
        return 0      
      fi
      docker compose kill
      return 0
    ;;    
    
    attach|--attach)
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=${DOCKERCONTAINER}        
      fi
      docker attach ${container_name}      
      return 0
    ;;

    --rm)
      # capturamos las imagenes usadas
      images=$(docker compose images -q)
      # detenemos servicios
      docker compose stop
      # removemos las images del enviroment
      docker compose down
      # removemos las imagenes desde host
      docker rmi ${DOCKERIMAGE}
      return 0
    ;;
    
    terminal|--terminal|-t)
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=$DOCKERCONTAINER
      fi
      CheckContainer "${container_name}"
      if [ "$?" -eq "0" ]; then
        echo "Localized Container <${container_name}> in Local host" 
        docker ps -s -af "name=${container_name}"
      else
        echo "Container <${container_name}> not found"
      fi

      docker exec -it ${container_name} ${ENTRYPOINT}
      if [ "$?" -ne "0" ]; then        
        echo "Error open the terminal for <${container_name}>"
      fi
      return 0
    ;;

    --clean)
      docker compose stop
      CleanFilesAndFolders "1"
      return 0
    ;;    

    -h|--help)
      msg_help $@
      return 0
    ;;    
    
    *)
      echo "Error en el llamado \"$app $@\""
      msg_help "-h"
      return 0
    ;;
  esac
  return 0
}

main "$@" && exit 0
