#!/bin/bash
THIS_FILE="${0##*/}"
LOG_INFO='true'
LOG_DEBUG='true'
CLEAN_FOLDERS=(
  '__pycache__'
  #'olds'
  'htmlcov'
)
CLEAN_FILES=(
  '.coverage'
  
)

DIR_EXC_CONTENT=(
    'inp' 'out' 'logs'
)
## listados de carpetas a elimnar dentro del directorio actual y de los anidados

#REQ_FILE="$PWD/requirements/requirements.txt"
REQ_FILE="$PWD/0D-Dockerfiles/requerimientos.txt"

VENV_FOLDER="$PWD/.venv"
#FLAGS='--system-site-packages'
PIP_FLAGS='--break-system-packages'
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
    log::_print $@
    return 0
}

function log::error(){
    [[ ${LOG_INFO} != 'true' ]] && return 0
    ## set text colour blue
    echo -ne "\e[1;31m"
    log::_print $@
    return 0
}

function log::debug(){
    [[ ${LOG_DEBUG} != 'true' ]] && return 0
    ## set text colour green
    echo -ne "\e[1;32m"
    log::_print $@
    return 0
}

function venv::check(){
    ## check pip install
    if ! command -v pip &> /dev/null; then
        log::info "pip no localizado"
        sudo apt install -y python3-pip python3-venv
    else
        log::info "pip instalado y disponible en el sistema";
    fi


    ## check virtualenv install
    if command -v virtualenv &> /dev/null;
    then
        log::info "virtualenv instalado y disponible en el sistema";
        return 0
    fi
    log::info "virtualenv is not installed. Installing..."
    python3 -m pip install --user virtualenv ${PIP_FLAGS}
    log::info "virtualenv installation complete."
    return 0
}

## Funcion encargadda de crear el virtual enviroment
## $1 Opcional, folder name for enviroment, este sera el nuevo valor para VENV_FOLDER
function venv::create(){
    ## si existe el directorio ya tenemos el venv
    [[ -d ${VENV_FOLDER} ]] && return 0 
    
    log::info "Creando el Virtual Enviroment <${VENV_FOLDER}>"
    ## no existe el directorio creamos el virtual envelopment
    python3 -m venv ${FLAGS} ${VENV_FOLDER}
    if [[ $? -ne 0 ]]
    then
        log::error "Failed to try created Virtual Enviroment <${VENV_FOLDER}>"
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
function venv::install_pipreq(){
    local ret_val  

    if [[ ! -f ${REQ_FILE} ]]
    then
        log::error "pip file requeriment <${REQ_FILE}> not found"
        return 1
    fi

    if [[ ! -e  ${VENV_FOLDER}/bin/activate ]] || [[ ! -f  ${VENV_FOLDER}/bin/activate ]]
    then
        log::error "file <${VENV_FOLDER}/bin/activate> not found"
        return 1
    fi
    ## Activamos el envelopment
    log::info "Activando el entorno Virtual"
    source ${VENV_FOLDER}/bin/activate
    ## prompt dentro del venv
    ## install packages  
    log::info "Instalando Package PIP"
    python -m pip install -r ${REQ_FILE} ${PIP_FLAGS}
    ## almacenamos el estado de la instalaccion
    ret_val=$?
    deactivate
    ## 
    log::info "Operacion Finalizad Status ${ret_val}"
    return ${ret_val}
}

## Funcion que se encarga de habilitar el virtual enviroment
function venv::enable() {
    bash --rcfile ${VENV_FOLDER}/bin/activate -i
}

function main::clean(){
    #echo "main::clean()"
    #find . -name __pycache__ -type d -exec rm -rf {} +
    for it in ${CLEAN_FOLDERS[@]}
    do
        echo "main::clean() <${it}>"
        find . -name "${it}" -type d -exec rm -rf {} +
    done
    for it in ${CLEAN_FILES[@]}
    do
        echo "main::clean() <${it}>"
        [[ -f ${it} ]] && rm -f "${it}"
    done

    for it in ${DIR_EXC_CONTENT[@]}
    do
        echo "remove content in <${it}>"
        [[ ! -d ${it} ]] && continue
        
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

function main::delete(){
    if [[ -d ${VENV_FOLDER} ]];then
        #echo "rm -fR \"${VENV_FOLDER}\""
        rm -fR "${VENV_FOLDER}"
    else
        echo "folder <${VENV_FOLDER}> not found, for delete"
    fi
    return 0
}

function main::codecoverage(){
    #bash --rcfile ${VENV_FOLDER}/bin/activate -i
    coverage run -m unittest discover
    coverage html
    gio open htmlcov/index.html
    #deactivate
    #venv::disable
    return 0
}

function main::activate(){

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



## s1 nombre del comando
## $@ resto de parametros
function run_funtion(){
    local cmd
    cmd=${1}
    case "${cmd}" in    
        '--clean'|'-c')
            main::clean
            #[[ ${clean} == "--cleanolds" ]] && main::cleanolds
            return $?
        ;;
        '--codecoverage')
            main::codecoverage
            return $?
        ;;
        '--activate')
            main::activate
            return $?
        ;;
        '--delete')
            main::delete
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

    run_funtion '--activate' $@
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

  --codecoverage)
    cat << EOH >&2
${THIS_FILE} --codecoverage

  Realiza el code covera en conjunto con los unittest del proyecto. Primero debemos habilitar el venv y luego ejecutar este.
Example: 
${THIS_FILE}
${THIS_FILE} --codecoverage

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
