#!/bin/bash
THIS_FILE="${0##*/}"
LOG_INFO='false'
LOG_DEBUG='false'

## listado de carpetas a buscar y borar
CLEAN_RECURSIVE_FOLDERS=(
  '__pycache__'
  '.venv'
  'htmlcov'
  '.mypy_cache'
)

CLEAN_RECURSIVE_FILES=(
  '.coverage'
  '*.d'       # c/c++
  '*.o'       # c/c++
)


## Delete Only the Contents of a Specific Folder (Keep the Folder)
CLEAN_CONTENT_RECURSIVE_FOLDERS=(
  'app'       # c/c++
  'logs'
)

DIR_EXC_CONTENT=(
    #'inp' 'out' 'logs'
)
## listados de carpetas a elimnar dentro del directorio actual y de los anidados


set -e

function log::_print(){
    echo $@
    echo -ne "\e[0m"
    return 0
}

function log::info(){
    [[ ${LOG_INFO} != 'true' ]] && return 0
    ## set text colour blue
    echo -ne "\e[1;34m"
    log::_prin $@
    return 0
}

function log::error(){
    [[ ${LOG_INFO} != 'true' ]] && return 0
    ## set text colour blue
    echo -ne "\e[1;30m"
    log::_prin $@
    return 0
}

function log::debug(){
    [[ ${LOG_DEBUG} != 'true' ]] && return 0
    ## set text colour green
    echo -ne "\e[1;32m"
    log::_prin $@
    return 0
}



function main::clean() {
    #find . -name __pycache__ -type d -exec rm -rf {} +
    ## BEGIN delete de folders recursivo
    for it in ${CLEAN_RECURSIVE_FOLDERS[@]}
    do
        echo "main::clean() <${it}>"
        find . -name "${it}" -type d -exec rm -rf {} +
    done
    ## END   delete de folders
    ##
    ## BEGIN delete de archivos recursivos
    for it in ${CLEAN_RECURSIVE_FILES[@]}
    do
        echo "main::clean() <${it}>"
        find . -name "${it}" -type f -exec rm -rf {} +
    done
    ## END   delete de archivos recursivos
    ##


    #
    for folder in ${CLEAN_CONTENT_RECURSIVE_FOLDERS[@]}
    do
        for it in $(find . -name ${folder} -type d)
        do
            # verificamos que el path no termine con el de git logs
            [[ "${it}" == *".git/logs" ]] && continue

            # verificamos que el directorio contenga archivos, not hidden
            [[ "$(ls "${it}" | wc -l)" -eq 0 ]] && continue

            echo "rm ${it}/*"
            rm ${it}/*
        done
    done

    for it in ${DIR_EXC_CONTENT[@]}
    do
        [[ ! -d ${it} ]] && continue
        echo "remove content in <${it}>"

        cd "${it}" > /dev/null
        rm -fR *
        #cont=$(ls)
        #[[ ! -z ${cont} ]] && echo "Contenmido : ${cont}"
        #[[ ! -z ${cont} ]] && rm -fR "${cont}"
        #find . -print0 | grep -v .gitignore -z | xargs -0 rm -fR
        #find . -print0 | grep -v .gitignore -z | xargs -0 echo
        cd - > /dev/null
    done
    return 0
}




## s1 nombre del comando
## $@ resto de parametros
function run_funtion(){
    local cmd
    cmd=${1}
    case "${cmd}" in
        '--clean'|'-c')
            main::clean
            return $?
        ;;

        '--help'|'-h')
            shift
            main::help '-h' '--all'
            return 0
        ;;
        *)
            echo "Error en el llamado a <${THIS_FILE}> con el parametro <${cmd}>"
            echo "Para obtener ayuda, intente ejecutar:"
            echo "  ${THIS_FILE} --help"
            return 0
        ;;
    esac
}


function main(){
    local cmd
    cmd=${1:-''}


    if [[ ${cmd} != '' ]]
    then
        shift
        run_funtion "${cmd}" $@
        return $?
    fi

    run_funtion '--clean' $@
    return $?
}

function main::help(){
  local app arg1
  app=${0##*/}
  if [ "$#" -eq "2" ];then
    arg1=$2
  else
    arg1="-h"
  fi

  arrHelp=( '--clean' '--codecoverage' )

  case "$arg1" in
  --clean|-t)
    cat << EOH >&2
${THIS_FILE} --clean

  Realiza el clean de los diretorios
EOH
  return 0
  ;;

#   --codecoverage)
#     cat << EOH >&2
# ${THIS_FILE} --codecoverage
#
#   Realiza el code covera en conjunto con los unittest del proyecto. Primero debemos habilitar el venv y luego ejecutar este.
# Example:
# ${THIS_FILE}
# ${THIS_FILE} --codecoverage
#
# EOH
#     return 0
#   ;;


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
    main::help "-h"
    echo
    for it in ${arrHelp[@]}
    do
      #echo "msg_help -h $it"
      main::help "-h" "$it"
      echo
    done
    return 0
  ;;
  *)
cat << EOH >&2
    -h                             : llamado a help con parametro <$arg1> incorrecto (no documentado).
EOH
    main::help "-h" "--all"
    return 0
  ;;
  esac
}

main "$@" && echo "Status $?" && exit 0
