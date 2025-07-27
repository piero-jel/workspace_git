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
THIS_SRC=${0##*/}

function main::help()
{
  if [ "$#" -eq "2" ];then
    arg1=$2
  else
    arg1="-h"
  fi

  arrHelp=( '--migrate'
            '--shell'
            '--load_data'
            '--run'
            '--unittest'
            '--coverage'
            '--clean'
          )

  case "$arg1" in

  --up)
    cat << EOH >&2
--up          Realiza todas las acciones necesarias para iniciar el servicio web del proyecto,
este remplaza la siguente secuencia de pasos:

    ${THIS_SRC} '--migrate'
    ${THIS_SRC} '--load_data'
    ${THIS_SRC} '--run'

EOH
  ;;

  --coverage)
    cat << EOH >&2
--coverage    Realiza el test y genera el reporte coverage del codigo.

EOH
  ;;

  --migrate)
    cat << EOH >&2
--migrate    Realiza la migracion de todos los modelos.

EOH
  ;;

  --shell)
    cat << EOH >&2
--shell      Open Shell iteractivo con los modelos ORM disponibles.

EOH
  ;;

  --load_data)
    cat << EOH >&2
--load_data  Carga dato a la base desde un archivo con items del tipo objetos json, uno por cada linea, del archivo.

EOH
  ;;

  --run)
    cat << EOH >&2
--run        Inicia el server, con la aplicacion.

EOH
  ;;

  --unittest)
    cat << EOH >&2
--unittest   Ejecuta el unittest/test.

EOH
  ;;

  --clean)
    cat << EOH >&2
--clean   Realiza el clean de proyecto, esto borra los siguentes archivos y directorios:

    + htmlcov/
    + .coverage
    + *.sqlite3

EOH
  ;;


  --help|-h)
  cat << EOH >&2
  $THIS_SRC {--help | -h }        Visualiza Help General
  $THIS_SRC {--help | -h } --all  Visualiza Help Especifico para todos los Targets

  Para Visualizar Help Especifico Intente con:
EOH
  for it in ${arrHelp[@]}
  do
  cat << EOH >&2
  $THIS_SRC {--help | -h} $it
EOH
  #echo
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
    done
    echo
    return 0
  ;;
  *)
cat << EOH >&2
    -h                             : llamado a help con parametro <$arg1> incorrecto (no documentado).
EOH
    main::help "-h" "--all"
    echo
    return 0
  ;;
  esac
  echo
}


function main()
{
  if [ "$#" -lt "1" ]
  then
    echo "Numero de Parametros incorrecto"
    main::help "-h"
    return 0
  fi

  if [[ ! -z ${2} ]] && [[ ${2} == '-h' || ${2} == '--help' ]]
  then
    main::help "-h" "${1}"
    return 0
  fi

  case "$1" in
    '-h'|'--help')
      main::help "$@"
      echo
      return 0
    ;;
    '--up')
      main '--migrate'
      main '--load_data'
      main '--run'
      return 0
    ;;
    '--coverage')
      coverage run manage.py test
      coverage report -m
      coverage html
      if command -v gio &> /dev/null;
      then
        gio open $PWD/htmlcov/index.html
      else
        echo "Report, open with browser: <$PWD/htmlcov/index.html>"
      fi
      return 0
    ;;
    '--migrate')
      python3 manage.py makemigrations
      python3 manage.py migrate
      return 0
    ;;
    '--shell')
      python3 manage.py shell
      return 0
    ;;
    '--load_data')
      python3 manage.py load_list_items --pathfile in/items.json
      return 0
    ;;

    '--run')
      python3 manage.py runserver 127.0.0.1:8080
      return 0
    ;;

    '--unittest')
      python3 manage.py test -v 2
      return 0
    ;;
    '--clean')
      #  + htmlcov/
      #  + .coverage
      #  + db.sqlite3 
      # folder_list='.venv htmlcov __pycache__'
      # file_list='db.sqlite3 .coverage'
      # find . -name ${folder_list} -type d -exec rm -rf {} +
      # find . -name ${file_list} -type f -exec rm -rf {} +

      find . -name __pycache__ -type d -exec rm -rf {} +
      find . -name .venv -type d -exec rm -rf {} +
      find . -name htmlcov -type d -exec rm -rf {} +
      find . -name .coverage -type f -exec rm -rf {} +
      find . -name db.sqlite3 -type f -exec rm -rf {} +
      return 0
    ;;

    *)
      echo "Error en el llamado \"$THIS_SRC $@\""
      return 1
    ;;
  esac

  return 1
}

main "$@" || main::help
exit 0
