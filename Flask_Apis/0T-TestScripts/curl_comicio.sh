#!/bin/bash
[ -z "$__utilities__" ] && . utilities.sh &> /dev/null

if [[ ! -v URL ]]; then URL='http://127.0.0.1:8080'; fi

ENDPOINT='/api/comicio'
METHOD='POST'
HEADER='Content-Type: application/json'
DEFAULT_USER="nombre_usuario:pass12345"


URI="${URL}${ENDPOINT}"
## si pasamos un valor lo consideramos como file json
## con los datos del usuario
DATA='{
  "listas": 10,
  "escanios" : 7,
  "votos" : [
        {"name":"Partido A","votos":340000}
      , {"name":"Partido B","votos":280000}
      , {"name":"Partido C","votos":160000}
      , {"name":"Partido D","votos":60000}
      , {"name":"Partido E","votos":15000}
    ]
}'

get_token ${DEFAULT_USER}
USER=$TOKEN

function msg_help()
{
  app=${0##*/}    
  cat << EOH >&2
${app} [DATA] : Este script ejecuta un request para publicar un comicio, en funcion del DATO. 
                Por defecto el DATO es:                
$DATA

          - DATA : Como string completo que representa el request JSON.            
          - DATA : Un archivo JSON con el request.
          
Usuario: El usuario con el que se creara el registro
  1 Si contamos con el TOKEN <${TOKEN}> 
    el usuario es el relacionado a este.
    
  2 Si no contamos con Token, utiliza el usario por defecto es "${DEFAULT_USER}"

JSON DATA FORMAT:
$DATA

EOH
}


if [ "$#" -eq "1" ] && ([ "$1" == "-h" ] || [ "$1" == "--help" ])
then 
  msg_help
  exit
fi

if [ "$#" -ge "1" ]
then
  if [ -f $1 ]
  then
    DATA="@$1"
  else
    DATA="$1"
  fi
fi



echo "request: ${URI}"
declare -F pretty_json &> /dev/null &&  pretty_json "$DATA" && echo "$PRETTY_JSON" || echo $DATA
echo
resp=$(curl -sS -u "${USER}" "${URI}" -i -X "${METHOD}" -H "${HEADER}" --data "${DATA}" -w '\n')

# echo "response: ${resp}"
declare -F pretty_json &> /dev/null &&  pretty_json "$resp" && echo "$PRETTY_JSON" || echo $resp

