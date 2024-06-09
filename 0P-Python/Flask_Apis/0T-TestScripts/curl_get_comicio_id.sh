#!/bin/bash
[ -z "$__utilities__" ] && . utilities.sh &> /dev/null

if [[ ! -v URL ]]; then URL='http://127.0.0.1:8080'; fi

ENDPOINT='/api/get_comicio/'
METHOD='GET'
HEADER='Content-Type: application/json'
DEFAULT_USER="nombre_usuario:pass12345"
## si pasamos un valor lo consideramos como file json
## con los datos del usuario
ID='6c3de225c80b0e985dc47dde428068d8'

get_token ${DEFAULT_USER}
USER=$TOKEN

function msg_help()
{
  app=${0##*/}    
  cat << EOH >&2
${app} [id]  : Este script ejecuta un request para obtener los datos correspondiente a un id
               relacionado a una publicacion de comicios previamente realizada
               Id por defecto <$ID>.
                
          
Usuario con el que se realiza la peticion
  1 Si contamos con el TOKEN <${TOKEN}> 
    el usuario es el relacionado a este.
    
  2 Si no contamos con Token, utiliza el usario por defecto "${DEFAULT_USER}"          


ID FORMAT:
<$ID>

EOH
}

if [ "$#" -eq "1" ] && ([ "$1" == "-h" ] || [ "$1" == "--help" ])
then 
  msg_help
  exit
fi



if [ "$#" -ge "1" ]
then   
  ID="$1"
fi
URI="${URL}${ENDPOINT}${ID}"


echo "request: ${URI}"
declare -F pretty_json &> /dev/null &&  pretty_json "$DATA" && echo "$PRETTY_JSON" || echo $DATA
# echo
resp=$(curl -sS -u "${USER}" "${URI}" -i -X "${METHOD}" -H "${HEADER}")

#echo "response: ${resp}"
declare -F pretty_json &> /dev/null &&  pretty_json "$resp" && echo "$PRETTY_JSON" || echo $resp

