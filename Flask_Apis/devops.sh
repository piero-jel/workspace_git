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
DOCK_FOLDER="$PWD/0D-Dockerfiles"

[ -z "$__docker_config__" ] && . ${DOCK_FOLDER}/docker_config  2>/dev/null

## BEGIN setting default, if config not load
### DOCKERFLAGS
if [[ ! -v DOCKERFLAGS ]]; then
  DOCKERFLAGS="-it -v $PWD/:/home/user:rw"
fi

### DOCKERDAEMON_FLG
if [[ ! -v DOCKERDAEMON_FLG ]]; then DOCKERDAEMON_FLG=0; fi

### DOCKERFOLDER
if [[ ! -v DOCKERFOLDER ]]; then DOCKERFOLDER='0D-Dockerfiles'; fi

### DOCKERFILE
if [[ ! -v DOCKERFILE ]]; then DOCKERFILE="Dockerfile"; fi

### DOCKERIMAGE
if [[ ! -v DOCKERIMAGE ]]; then DOCKERIMAGE="jeluccioni/test-img-name"; fi

### DOCKERCONTAINER
if [[ ! -v DOCKERCONTAINER ]]; then DOCKERCONTAINER="TestImgName"; fi

## END   setting default, if config not load



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
            '--rm-image'
            '--rm-all'
            '--attach'            
            '--check'
            '--del-build-cache'
            '--inspect'
            '--logs'
            '--test'
            '--clean'
          )

  case "$arg1" in
  --test)
    cat << EOH >&2
--test [CONTAINER-NAME]
  test [CONTAINER-NAME]

  [CONTAINER-NAME] opcional Nombre del Container, por defecto usa el configurad ${DOCKERCONTAINER}
  Inicia el contenedor en modo iterativo atachando el prompt al log del mismo ( stdout , stderr ).

EOH
  return 0
  ;;
  --logs)
    cat << EOH >&2
--logs [CONTAINER-NAME]
  logs [CONTAINER-NAME]

  [CONTAINER-NAME] opcional Nombre del Container, por defecto usa el configurad ${DOCKERCONTAINER}
  Nos muestra los log del contenedor, util para el caso de que el contenedor se detubo de forma inesperada.

EOH
  return 0
  ;;

  --status)
    cat << EOH >&2
--status [CONTAINER-NAME]
  status [CONTAINER-NAME]

  [CONTAINER-NAME] opcional Nombre del Container, por defecto usa el configurad ${DOCKERCONTAINER}
  Realiza la busqueda del Contenedor en el servico corriendo en el host y retorna el Status.
  
EOH
  return 0
  ;; 
  
  --inspect)
    cat << EOH >&2
--inspect [CONTAINER-NAME]
  inspect [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Return JSON with low-level information from Container objects
  
EOH
  return 0
  ;;  

  --terminal|-t)
    cat << EOH >&2
--terminal [CONTAINER-NAME]
  terminal [CONTAINER-NAME]
        -t [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Open new terminal session with bash tty, conect to container run.
  Podemos tener varias terminales conectadas de forma simultanea a un contenedor
  en ejecucion.  
  
EOH
  return 0
  ;;
  
  --del-build-cache)
    cat << EOH >&2
--del-build-cache
  del-build-cache

  Remove build cache
  
EOH
  return 0
  ;;
 
  --check)
    cat << EOH >&2
--check [IMAGE-NAME:TAG]
  check [IMAGE-NAME:TAG]

  [IMAGE-NAME:TAG] opcional Imagen Tag, por defecto usa el configurad ${DOCKERIMAGE}
  Realiza la busqueda de la imagen en el registro local.

EOH
  return 0
  ;;  

  --attach)
    cat << EOH >&2
--attach
  attach

  Docker container ${DOCKERCONTAINER} attach
  Attach local standard input, output, and error streams to a running container <${DOCKERCONTAINER}>.


EOH
    return 0
  ;;

  --start)
    cat << EOH >&2
--start [CONTAINER-NAME]
  start [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Inicia el Contenedor, previamente creado (de lo contrario notificara error)  

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
--kill [CONTAINER-NAME]
  kill [CONTAINER-NAME]

  [CONTAINER-NAME] : it is optional, defautl container is <$DOCKERCONTAINER>
  Envia la señal correspondiente al Servicio para detenerlo de manera forzada al
  Contenedor, previamente creado e iniciado (de lo contrario notificara error).

EOH
    return 0
  ;;  
  
  --rm)
    cat << EOH >&2
--rm

  Docker remove container ${DOCKERCONTAINER}
  Elimina el contenedor <${DOCKERCONTAINER}>, si este existe.

EOH
    return 0
  ;;

  --build|-b)
    cat << EOH >&2
--build [IMAGE-NAME [CONTAINER-NAME]]
     -b [IMAGE-NAME [CONTAINER-NAME]]
  build [IMAGE-NAME [CONTAINER-NAME]]
     
  Default values:
    + Image ${DOCKERIMAGE}
    + Container ${DOCKERCONTAINER}

  Construye la imagen <${DOCKERIMAGE}> para el contenedor <${DOCKERCONTAINER}> a partir de las configuraciones del dockerfile <${DOCKERFILE}>. Inicia el container en funcion de los flags <${DOCKERFLAGS}>.

EOH
    return 0
  ;;

  --rm-image)
    cat << EOH >&2
--rm-image

  Docker Image ${DOCKERIMAGE} Remove
  Remueve la imagen <${DOCKERIMAGE}>, si esta existe.

EOH
    return 0
  ;;

  --rm-all)
    cat << EOH >&2
--rm-all

  Docker, remove the container ${DOCKERCONTAINER} and then the image ${DOCKERIMAGE}
  Elimina el contenedor <${DOCKERCONTAINER}> y luego la imagen ${DOCKERIMAGE}, si existen.

EOH
    return 0
  ;;

  --clean)
    cat << EOH >&2
--clean  

  clean current folder <$PWD>, take file .gitignore for targets to cleans

EOH
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


function main()
{  
  local app target
  app=${0##*/}
  
  if [ ! -d ${DOCK_FOLDER} ];then
    echo "Folder <${DOCK_FOLDER}> not found, abort operations \"$app $@\""
    return 0
  fi
  
  if [ "$#" -eq '0' ]; then
    # por defecto tomamos el target terminal
    target="-t"
  else
    target=$1
  fi 
  
  case "$target" in
    inspect|--inspect)
      # Return low-level information on Container objects
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=$DOCKERCONTAINER
      fi
      docker inspect ${container_name}
      return 0
    ;;
    
    del-build-cache|--del-build-cache)
      docker builder prune -af
      return 0
    ;;   
    
    check|--check)
      local img_name
      if [ "$#" -gt "1" ]; then
        img_name=$2
      else
        img_name=$DOCKERIMAGE
      fi
      CheckImageInLocalRegistry "${img_name}"
      if [ "$?" -eq "0" ]; then
        echo "Localized Image <${img_name}> in Local Registry"        
        docker image ls ${img_name}        
      else
        echo "Image <${img_name}> not found in Local Registry"
      fi
      
      declare -F dck_cfg_dk_test &>/dev/null && dck_cfg_dk_test       
      return 0
    ;;
    
    build|--build|-b)
      local currfolder flags
      local container_name img_name      

      currfolder=$(pwd)      
      case $# in
        1)
          img_name=$DOCKERIMAGE
          container_name=$DOCKERCONTAINER          
        ;;
        2) 
          img_name=$2
          container_name=$DOCKERCONTAINER          
        ;;
        3)
          img_name=$2
          container_name=$3          
        ;;        
        *)
          echo "Error in call to \"$app $@\""
          msg_help "-h"          
          return 0
        ;;
      esac      
      #echo "container_name=$container_name"
      #echo "img_name=$img_name"
      #return 0

      if [[ $DOCKERDAEMON_FLG == 1 ]]; then
        flags="$DOCKERFLAGS -d"
      else
        flags="$DOCKERFLAGS -i"
      fi
      ## El container ya existe, descartamos la operacion
      CheckContainer "${container_name}"        
      if [ "$?" -eq "0" ]; then
        echo "The Container ${container_name} already exists try \"$app --start\""
        return 0
      fi
    
      ## Si la imagen ya existe no la creo
      CheckImageInLocalRegistry "$img_name"
      if [ "$?" -eq "1" ]; then
        cd ${DOCKERFOLDER}
        docker build -t=${img_name} -f ${DOCKERFILE} .
        #echo "docker build -t=${img_name} -f ${DOCKERFILE} ."
        cd ${currfolder}
      fi
              
      ## Si el Container no exite lo creo y lo ejecuto por primera ves
      CheckContainer "${container_name}"
      if [ "$?" -eq "1" ]; then
        ## Si existe la funcion la ejecuta (redirect for no print function in screen), si no sigue de largo
        declare -F dck_cfg_dk_build_ini &>/dev/null && dck_cfg_dk_build_ini 
        #echo "docker run --name ${container_name} ${flags} ${img_name} ${DOCKERCMD}"
        docker run --name ${container_name} ${flags} ${img_name} ${DOCKERCMD}
      fi
      return 0
    ;;
    
    start|--start)
      local flags container_name
      if [[ $DOCKERDAEMON_FLG == 0 ]]; then        
        flags='-i'
      fi      

      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=$DOCKERCONTAINER
      fi
      
      #echo "docker start ${container_name} $flags"
      docker start ${container_name} $flags
      status_print "$app" "--start" "$?"      
      return 0
    ;;
    
    status|--status)
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
      return 0      
    ;;
    
    logs|--logs)
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=$DOCKERCONTAINER
      fi

      CheckContainer "${container_name}"
      if [ "$?" -eq "0" ]; then
        echo "Localized Container <${container_name}> in Local host"
        docker logs -t ${container_name}
      else
        echo "Container <${container_name}> not found"
      fi
      return 0
    ;;

    test|--test)
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=$DOCKERCONTAINER
      fi

      CheckContainer "${container_name}"
      if [ "$?" -eq "0" ]; then
        echo "Localized Container <${container_name}> in Local host"
        docker start -i ${container_name}
      else
        echo "Container <${container_name}> not found"
      fi
      return 0
    ;;

    stop|--stop)
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=$DOCKERCONTAINER
      fi
      docker stop ${container_name}
      return 0
    ;;

    kill|--kill)
      local container_name
      if [ "$#" -gt "1" ]; then
        container_name=$2
      else
        container_name=$DOCKERCONTAINER
      fi
      docker kill ${container_name}
      return 0
    ;;    
    
    attach|--attach)
      docker attach ${DOCKERCONTAINER}
      status_print "$app" "--attach" "$?"
      return 0
    ;;

    --rm)
      docker rm ${DOCKERCONTAINER}
      status_print "$app" "--rm" "$?"
      return 0
    ;;
    
    --rm-image)
      docker rmi $(docker images -q ${DOCKERIMAGE})
      status_print "$app" "--rm-image" "$?"
      return 0
    ;;
    
    --rm-all)
      local flg
      docker rm ${DOCKERCONTAINER}
      flg=$?
      status_print "$app" "--rm-all delete container" "$flg"
      if [ "$flg" -ne "0" ]; then return 0 ;fi

      docker rmi $(docker images -q ${DOCKERIMAGE})
      status_print "$app" "--rm-all delete image" "$?"
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

      docker exec -it ${container_name} bash
      if [ "$?" -ne "0" ]; then        
        echo "Error open the terminal for <${container_name}>"
      fi
      return 0
    ;;

    --clean)
      local gfile
      gfile=.gitignore
      if [ ! -f "${gfile}" ]; then
        echo "file <${gfile}> not found"
        return 0      
      fi
      while IFS= read -r line
      do 
        # discard linea vacia
        if [[ ${#line} == '0' ]] ; then continue; fi
        
        # discard old files or directories
        if echo "$line" | grep -q "_old"
        then
          #echo "OLD target: <$line>"
          continue
        fi
        
        # discard files con prefix '!' (archivos ocultos que deben agregarse al seguimiento)
        if [[ ${line:0:1} == '!' ]] ; then continue; fi
        
        # discard comment
        if [[ ${line:0:1} == '#' ]] ; then continue; fi
        
        # rm folder
        if [[ ${line:0-1} == '/' ]]; then
          #echo "rm -fR ${line:0:-1}"
          rm -fR "${line:0:-1}"
          continue
        fi
        # remove, extension and file is same
        #echo "rm -f ${line}"
        rm -f "${line}"
        #echo "${line}"
      done < ${gfile}      
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
