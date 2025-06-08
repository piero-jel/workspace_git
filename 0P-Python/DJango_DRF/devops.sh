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
TARGET=""

## BEGIN Include settings
source "${PWD}/container.sh"
## END   Include settings

### BEGIN Functions definitions
##
## $1 single target valor por defecto -h/--help
## $2 <$1> target
function main::help()
{
  container::help ${THIS_NAME} ${TARGET}
  return $?
}





## $1: type {0: print only | 1: clean }
function CleanFilesAndFolders()
{
  local type
  if [[ $# -ne 1 ]]; then type=0; else type=$1;fi
  
  #echo "type $type"
  [[ ${type} == 1 ]] && echo "clean comodin files" || echo "Clean list Files"
  for it in "${CLEAN_ARR_COMODIN_FILES[@]}"
  do
    for it2 in $(ls ${it} 2>/dev/null )
    do
      if [[ -f ${it2} ]]
      then
        [[ ${type} == 1 ]] && sudo rm -f ${it2} || echo "  ${it2}"
        #sudo rm -f $it2
      else
        echo "File <${it2}> not found."
      fi        
    done        
  done
    
  [[ ${type} == 1 ]] && echo "clean array files"
  for it in "${CLEAN_ARR_FILES[@]}"
  do
    if [[ -f ${it} ]]
    then
      [[ ${type} == 1 ]] && sudo rm -f $it || echo "  ${it}"
      #echo "rm -f $it"
      #sudo rm -f $it
    else
      echo "File <${it}> not found."
    fi
  done
  
  echo 
  [[ ${type} == 1 ]] && echo "clean array folders with prefix" || echo "Clean list Folders"
  for it in "${CLEAN_ARR_FOLDERS[@]}"
  do
    for it2 in $(ls $it 2>/dev/null)
    do      
      if [ -d "$it$it2" ]
      then
        [[ ${type} == "1" ]] && sudo rm -fR "${it}${it2}" || echo "  ${it}${it2}"
        #sudo rm -fR "$it$it2"
      else
        echo "Folder <${it}${it2}> not found."
      fi        
    done        
  done
  
  
  [[ ${type} == 1 ]] && echo "clean array folders"
  for it in "${CLEAN_ARR_DIR[@]}"
  do
    if [[ -d ${it} ]]
    then
      [[ ${type} == 1 ]] && sudo rm -fR "${it}" || echo "  ${it}"
      #sudo rm -fR "$it"
    else
      echo "Folder <${it}> not found."
    fi
  done
  return 0
    

}
### END   Functions definitions






### BEGIN Function MAIN
function main()
{
  if [[ $# -lt 1 ]]
  then
    echo "No se pasaron parametros"
    TARGET='--help'
    return 1
  fi
  TARGET=${1}
  if [[ ! -z ${2} ]] && [[ ${2} == '-h' || ${2} == '--help' ]]
  then 
    container::help ${THIS_NAME} ${TARGET}
    return 0
  fi
  case "${TARGET}" in
    '--build')
        shift
        ## Opciones con argumentos opcinales
        container::build "$@"
        return $?
    ;;

    '--up')
        shift
        ## Opciones con argumentos opcinales
        echo "Local URL: http://localhost:8080"
        container::up "$@"
        return 0
    ;;
    '--down')
        shift
        ## Opciones con argumentos opcinales
        container::down "$@"
        return $?
    ;;
    '--start')
        ## Opciones con un argumento mandatorio        
        if [[ -z ${2} ]]
        then        
          echo "Opcion <${1}> sin parametros"
          return 1
        fi
        container::start $2
        return $?

    ;;
    '--stop')
        ## Opciones con un argumento mandatorio
        if [[ -z ${2} ]]
        then        
          echo "Opcion <${1}> sin parametros"
          return 1
        fi
        container::stop $2
        return $?
    ;;
    '--restart')
        ## Opciones con un argumento mandatorio
        if [[ -z ${2} ]]
        then        
          echo "Opcion <${1}> sin parametros"
          return 1
        fi
        container::restart $2
        return $?
    ;;
    '--term')
        ## Opciones con un argumento mandatorio
                ## Opciones con un argumento mandatorio
        if [[ -z ${2} ]]
        then        
          echo "Opcion <${1}> sin parametros"
          return 1
        fi
        container::term $2
        return $?
    ;;
    '--top')
        ## Opciones con argumento por defecto
        shift
        container::top "$@"
        return 0 # forzamos el 0 p/no mostrar el help
    ;;
    '--logs')
        container::logs
        return 0 # forzamos el 0 p/no mostrar el help
    ;;
    '--ddbb')
        ## Opciones con un argumento mandatorio
        echo "Option --term ${2}"

    ;;
    '--info')
      container::info
      return $?
    ;;
    --coverage)
      container::run "app" "Action.sh --coverage"
      ou_file='rd_wepapp/htmlcov/index.html'
      if command -v gio &> /dev/null;
      then
        gio open "$PWD/${ou_file}"
      else
        echo "Report, open with browser: <$PWD/${ou_file}>"
      fi
      return 0
    ;;
    '--help'|'-h')
      if [[ ! -z ${2} ]]
      then 
        TARGET=${2}
      fi      
      main::help
      return $?
    ;;
    *)
      #echo "param <${1}> no contemplado"
      ## call main::help
      #main::help
      return 1
    ;;
  esac
  return 0
}
### END   Function MAIN

### BEGIN ENTRY POINT TO RUN
#main "$@" && exit 0
main "$@" || main::help
exit 0
### END   ENTRY POINT TO RUN
