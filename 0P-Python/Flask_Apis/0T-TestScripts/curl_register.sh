#!/bin/bash
[ -z "$__utilities__" ] && . utilities.sh &> /dev/null

if [[ ! -v URL ]]; then URL='http://127.0.0.1:8080'; fi



ENDPOINT='/api/register'
METHOD='POST'
HEADER='Content-Type: application/json'

URI="${URL}${ENDPOINT}"
## si pasamos un valor lo consideramos como file json o reques string
## con los datos del usuario
DATA='{"username":"nombre_usuario","password":"pass12345"}'

function msg_help()
{
  app=${0##*/}    
  cat << EOH >&2
${app} [DATA] : Este script ejecuta un request para crear un nuevo usuario, este
                puede ser pasado como un String JSON o como un path a un 
                archivo JSON. Por defecto el usuario a intentar crear es
                
JSON DATA FORMAT:
<$DATA>
          
EOH
}

if [ "$#" -eq "1" ] && ([ "$1" == "-h" ] || [ "$1" == "--help" ])
then 
  msg_help
  exit
fi

if [ "$#" -ge "1" ]
then
  if [ -f "$1" ]
  then
    DATA="@$1"
  else
    DATA="$1"
  fi
fi

echo "request: ${URI}"
#declare -F pretty_json &> /dev/null &&  pretty_json "$DATA" && echo "$PRETTY_JSON" || echo $DATA
echo
#echo "curl -sS "${URI}" -i -X "${METHOD}" -H "${HEADER}" --data "${DATA}" -w '\n'"
resp=$(curl -sS "${URI}" -i -X "${METHOD}" -H "${HEADER}" --data "${DATA}" -w '\n')


echo "response: ${resp}"
#declare -F pretty_json &> /dev/null &&  pretty_json "$resp" && echo "$PRETTY_JSON" || echo $resp

