#!/bin/bash
[ -z "$__utilities__" ] && . utilities.sh &> /dev/null

if [[ ! -v URL ]]; then URL='http://127.0.0.1:8080'; fi


ENDPOINT='/api/get_comicios'
METHOD='GET'
HEADER='Content-Type: application/json'
URI="${URL}${ENDPOINT}"
DEFAULT_USER="nombre_usuario:pass12345"


get_token ${DEFAULT_USER}
USER=$TOKEN


function msg_help()
{
  app=${0##*/}
    
  cat << EOH >&2
${app} : Este script ejecuta una peticion para obtener el listado de de comicios para el usuario logueado actualmente.


Usuario: El usuario con el que se realizara la peticion:
  1 Si contamos con el TOKEN <${TOKEN}> 
    el usuario es el relacionado a este.
    
  2 Si no contamos con Token, utiliza el usario por defecto es "${DEFAULT_USER}"  
         
EOH
}

if [ "$#" -eq "1" ] && ([ "$1" == "-h" ] || [ "$1" == "--help" ])
then 
  msg_help
  exit
fi


echo "request: ${URI}"
declare -F pretty_json &> /dev/null &&  pretty_json "$DATA" && echo "$PRETTY_JSON" || echo $DATA
echo
resp=$(curl -sS -u "${USER}" "${URI}" -i -X "${METHOD}" -H "${HEADER}" -w '\n')

# echo "response: ${resp}"
declare -F pretty_json &> /dev/null &&  pretty_json "$resp" && echo "$PRETTY_JSON" || echo $resp



