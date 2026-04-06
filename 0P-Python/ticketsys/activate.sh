#!/bin/bash
THIS_FILE="${0##*/}"
#DEBUG='true' # deshabilita acciones de borrador
DEBUG='false'

LOG_INFO='true'
LOG_DEBUG='true'

APP_IP='0.0.0.0'
APP_PORT='8080'
APP_DDBB='db.sqlite3'
APP_LOGS='logs/ticketsys.log'

## list dirs/folder to find and delete from pattern or full name
CLEAN_PATTERN_FOLDERS=(
  '__pycache__'
  #'olds'
  #'htmlcov'
)

## list file to find and delete from pattern or full name
CLEAN_PATTERN_FILES=(
    '*_initial.py' # ojo si tenemos .venv tambien elimina lo de django
)

CLEAN_FILES=(
  '.coverage'
)

## listados de carpetas bajo el root, de las cuales debe eliminar si contenido
## preserbando sus hidden files
DIR_EXC_CONTENT=(
    #'inp' 'out' 'logs'
)


#REQ_FILE="$PWD/0D-Dockerfiles/requerimientos.txt"
#REQ_FILE="$PWD/requirements/requirements.txt"
REQ_FILE="${PWD}/deploy/requirements/requirements.txt"

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
    if [[ ! -f ${REQ_FILE} ]]; then
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
    local iter
    iter=${1:-1}
    if (( iter == 1 ));then
        bash --rcfile ${VENV_FOLDER}/bin/activate -i
    else
        bash ${VENV_FOLDER}/bin/activate
    fi
    return 0
}

## find and delete file from patter or fullname
function main::rmpatternfile(){
    for it in ${CLEAN_PATTERN_FILES[@]}
    do
        log::info "main::patternfile() <${it}>"
        #find . -name "${it}" -type f -exec rm -rf {} +
        files=$(find . -name "${it}" -type f -not -path "*./$(basename ${VENV_FOLDER})/*")
        log::debug "delete files <${files[@]}>"
        [[ ${DEBUG} == 'false' ]] && find . -name "${it}" -type f -not -path "*./$(basename ${VENV_FOLDER})/*" -exec rm -rf {} +
    done
    return 0
}

## find and delete dirs/folder from patter or fullname
function main::rmpatterndirs(){
    for it in ${CLEAN_PATTERN_FOLDERS[@]}
    do
        log::info "main::patterndirs() <${it}>"
        # -path ./.venv -prune : excluimos el venv $(basename ${VENV_FOLDER})
        #find . -name "${it}" -type d -exec rm -rf {} +
        folder=$(find . -name "${it}" -type d -not -path "*./$(basename ${VENV_FOLDER})/*")
        log::debug "delete folders <${folder[@]}>"
        [[ ${DEBUG} == 'false' ]] && find . -name "${it}" -type d -not -path "*./$(basename ${VENV_FOLDER})/*" -exec rm -rf {} +
    done
    return 0
}

function main::clean(){
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
        cd - > /dev/null
    done
    return 0
}

## fucion que se encarga de eliminar el entorno virtual
function main::delete(){
    local base_dir
    base_dir=$(basename ${VENV_FOLDER})
    while true; do
        log::info "Reconstruir el venv<${base_dir}> tomara un tiempo considerable"
        printf "\e[1;31mEsta seguro que desea eliminar el venv? (y/n): \e[0m"
        read yn
        case $yn in
            [Yy]* )
                log::info "Eliminando el venv<${base_dir}> ..."
                break
            ;;
            [Nn]* )
                log::info "Peticion cancelada."
                return 0
            ;;
            * )
                log::error "Opcion <${yn}> Invalida, intentelo nuevamente."
            ;;
        esac
    done
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

# $1 : opcional, si no debe habilitar el venv luego de crearlo e instalar los packages
function main::activate(){
    local create
    create=${1:-1}

    if [[ ! -d ${VENV_FOLDER} ]]; then
        # 1° Consultamos si tenemos los bin instalado, y de lo contrario lo instala
        venv::check
        [[ $? -ne 0 ]] && return 1

        # 2° Creamos el venv, si este ya existe no hace nada
        venv::create
        [[ $? -ne 0 ]] && return 1

        # 3° Instalamos los requeriments
        venv::install_pipreq
        [[ $? -ne 0 ]] && return 1
    fi
    [[ "${create}" -eq '1' ]] && venv::enable
    return 0
}

## $1 Acction
## - 1: por defecto, crea la bbdd si no existe
## - 0: no crea la bbdd, solo verifica
function ddbb::check(){
    local crate
    [[ -f "${APP_DDBB}" ]] && return 0
    ## No tenemos base de datos, la creamos
    crate=${1:-1}
    log::info "No tenemos Base de datos <${APP_DDBB}>"
    [[ ${crate} -eq "0" ]] && return 0
    if [[ ! -f "${PWD}/manage.py" ]]; then
        log::error "No se localizo el archivo <manage.py>, principal."
        return 1
    fi
    if [[ -z "$VIRTUAL_ENV" ]]; then
        # Creamos la vase de datos con venv
        ${VENV_FOLDER}/bin/python3 manage.py makemigrations
        ${VENV_FOLDER}/bin/python3 python3 manage.py migrate
        return 0
    fi
    python3 manage.py makemigrations
    python3 manage.py migrate
    return 0
}

# funcion privada para ejecutar secuencia de comando con python dentro del vevn
function main::__exec_venv(){
    if [[ ! -d ${VENV_FOLDER} ]];then
        log::error "No tenemos venv creado"
        return 0
    fi

    if [[ -z "$VIRTUAL_ENV" ]]; then
        log::debug "No Python virtual environment is currently enabled."
        log::debug "Run from venv/bin/python3."
        ${VENV_FOLDER}/bin/python3 $@
        return $?
    else
        log::debug "Python virtual environment is enabled in: $VIRTUAL_ENV"
    fi
    python3 $@
    return $?
}

## Funcion que se encarga de ejecutar unit test
## $1 modulo name to run
function main::unittest(){
    if [[ ! -d ${VENV_FOLDER} ]];then
        log::error "No tenemos venv creado"
        return 0
    fi

    local appname
    appname=${1:-''}
    if [[ -z ${appname} ]];then
        main::__exec_venv manage.py test
    else
        main::__exec_venv manage.py test ${appname}
    fi
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
            main::rmpatternfile
            main::rmpatterndirs
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
        '--create')
            main::activate 0
            return $?
        ;;
        '--delete')
            main::delete
            return $?
        ;;
        '--run')
            ## En este queda la verificacion del venv, ddbb (si no existe la crea)
            ## y luego ejecuta el runserver
            #main::run
            shift
            local port
            port=${1:-${APP_PORT}}
            clear
            main::__exec_venv manage.py runserver ${APP_IP}:${port} --insecure
            return $?
        ;;
        '--logs')
            clear
            [[ -f ${APP_LOGS} ]] && tail -f -n0 ${APP_LOGS} || log::error "log file<${APP_LOGS}> not found"
            return 0
        ;;
        '--migrate')
            ## target que realiza la migracion {1° - makemigrations, 2° - migrate}
            main::__exec_venv manage.py makemigrations
            main::__exec_venv manage.py migrate
            return 0
        ;;
        '--staticfiles')
            main::__exec_venv manage.py collectstatic
            return $?
        ;;
        '--unittest')
            shift
            if [[ $# -gt '0' ]];then
                for app in $@; do
                    log::info "runnung unittest ${app}"
                    main::unittest "${app}"
                done
            else
                log::info "runnung unittest"
                main::unittest
            fi
            return $?
        ;;
        '--create-superuser')
            main::__exec_venv manage.py createsuperuser
            return $?
        ;;
        '--help'|'-h')
            shift
            #main::help '-h' '--all'
            main::help $@
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
    if [[ ${cmd} != '' ]];then
        shift
        run_funtion "${cmd}" $@
        return $?
    fi
    run_funtion '--activate' $@
    return $?
}

function main::help(){
  local arg1
  #echo "<$@>"

  if [ "$#" -eq "1" ];then
    arg1=$1
  else
    arg1="-h"
  fi

  arrHelp=( '--clean'   '--activate'  '--unittest'
            '--run'     '--migrate'   '--staticfiles'
            '--delete'  '--create'    '--create-superuser'
            #'--codecoverage'
  )

  case "$arg1" in
  --clean|-t)
    cat << EOH >&2
${THIS_FILE} --clean

  Realiza el clean de los diretorios


    CLEAN_PATTERN_FOLDERS   list dirs/folder to find and delete from pattern or full name <${CLEAN_PATTERN_FOLDERS[@]}>
    CLEAN_PATTERN_FILES     list file to find and delete from pattern or full name <${CLEAN_PATTERN_FILES[@]}>
    CLEAN_FOLDERS           lista de directorio que buscara y eliminara <${CLEAN_FOLDERS[@]}>
    DIR_EXC_CONTENT         Listados de Directorios debajo de root excluidos de segumiento, de los cuales eliminara
                            su contenido manteniendo los hiden files/folder <${DIR_EXC_CONTENT[@]}>
EOH
  return 0
  ;;
  --create-superuser)
    cat << EOH >&2
${THIS_FILE} --create-superuser

  Crea un nuevo usuario como "super user" en modo iterativo.
EOH
  return 0
  ;;

  --create)
    cat << EOH >&2
${THIS_FILE} --create

  Si no existe venv lo crea, luego instala los packages necesarios para el proyecto. Este no
  habilita el entorno virtual (venv).
EOH
  return 0
  ;;

  --activate)
    cat << EOH >&2
${THIS_FILE} --activate

  Realiza la tarea principal, activar el venv. Si este no existe lo crea, instala
  los packages y por ultimo lo habilita.
EOH
  return 0
  ;;

  --delete)
    cat << EOH >&2
${THIS_FILE} --delete

  Si existe el directorio del venv lo elimina.
EOH
  return 0
  ;;

  --run)
    cat << EOH >&2
${THIS_FILE} --run

  Ejecuta el server 'python3 manage.py runserver ${APP_IP}:${APP_PORT} --insecure'
EOH
  return 0
  ;;

  --migrate)
    cat << EOH >&2
${THIS_FILE} --migrate

  Target que realiza la migracion {1° - makemigrations, 2° - migrate}
EOH
  return 0
  ;;

  --staticfiles)
    cat << EOH >&2
${THIS_FILE} --staticfiles

  Target que se encarga de generar los static file de la aplicacion
EOH
  return 0
  ;;

  --unittest)
    cat << EOH >&2
${THIS_FILE} --unittest [appname , ...]

  Target que se encarga de ejecutar el unit test de todas las aplicaciones (si
  no se pasan parametros) o solo de las pasadas el la linea de comandos.

${THIS_FILE} --unittest                     Ejecuta todos los unittest
${THIS_FILE} --unittest app1 app2           Solo ejecuta el de las app1 y app2

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
      main::help "$it"
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

#main "$@" && echo "Status $?" && exit 0
main "$@" && ([[ "${DEBUG}" == 'true' ]] && echo "Status $?") && exit 0
