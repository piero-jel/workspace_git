#!/bin/bash
[ -z "$__utilities__" ] && . utilities.sh &> /dev/null

if [[ ! -v URL ]]; then URL='http://127.0.0.1:8080'; fi


METHOD='GET'
HEADER='Content-Type: application/json'
ENDPOINT="/api/users"
DEFAULT_USER="nombre_usuario:pass12345"
URI="${URL}${ENDPOINT}"

get_token ${DEFAULT_USER}
USER=$TOKEN

function msg_help()
{
  app=${0##*/}    
  cat << EOH >&2
${app} [user:password] : Este script ejecuta un request para obtener el listado actual de usuarios que 
                         actualmente estan registrado.
                
          
Usuario con el que se realiza la peticion
  1 Si se paso la dupla [user:password], usa este.
  2 Si contamos con el TOKEN <${TOKEN}> 
    el usuario es el relacionado a este.
    
  3 Si no contamos con Token, utiliza el usario por defecto "${DEFAULT_USER}"          
          
EOH
}

if [ "$#" -eq "1" ] && ([ "$1" == "-h" ] || [ "$1" == "--help" ])
then 
  msg_help
  exit
fi


## si pasamos un valor lo consideramos como la dupla key:user
if [ "$#" -ge "1" ]
then   
  USER=$1
fi

echo "request: ${URI}"
echo 
resp=$(curl -sS -u "${USER}" "${URI}" -X "${METHOD}" -H "${HEADER}" -w '\n')

# echo "response: ${resp}"
declare -F pretty_json &> /dev/null &&  pretty_json "$resp" && echo "$PRETTY_JSON" || echo $resp
