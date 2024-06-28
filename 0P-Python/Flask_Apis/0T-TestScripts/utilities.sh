#!/bin/bash
__utilities__=1

### BEGIN Global Vars
IP='127.0.0.1'
PORT='8000'
# PORT='3000'
URL="http://${IP}:${PORT}"
### END   Global Vars



### BEGIN utility json pretty
PRETTY_JSON=''
## $1 json body
## PRETTY_JSON var donde coloca la respuesta
function pretty_json()
{
  if command -v python3 &> /dev/null ; then
PYCMD=$(cat <<EOF
import json
from sys import argv

def pretty_json(data:str)->str:
  idx:int = data.find('{')
  if(idx == -1):
    return data
  return json.dumps(json.loads(data[idx:]),indent=2)
# end if
print(pretty_json(argv[1]))
EOF
)
    PRETTY_JSON=$(python3 -c "$PYCMD" "$1")
    return 0
  fi

  if [ "$#" -eq "0" ]; then return 1 ; fi
  ## tab offset 2
  PRETTY_JSON=$(echo "$1" | grep -Eo '"[^"]*" *(: *([0-9]*|"[^"]*")[^{}\["]*|,)?|[^"\]\[\}\{]*|\{|\},?|\[|\],?|[0-9 ]*,?' | awk '{if ($0 ~ /^[}\]]/ ) offset-=2; printf "%*c%s\n", offset, " ", $0; if ($0 ~ /^[{\[]/) offset+=2}')
}
### END   utility json pretty

### BEGIN utility get_token() and store_token()
TOKEN_FILE="${PWD}/token_dump.log"
TOKEN=''
## $1 opcional DEFAULT_USER
function get_token()
{
  local get_token
  if [ -f ${TOKEN_FILE} ]
  then
    get_token=$(cat ${TOKEN_FILE})
    TOKEN="${get_token}:notrelevant"
  else
    TOKEN=$1
  fi
}

## $1 json message
function store_token()
{
  local get_token var
  if command -v python3 &> /dev/null ; then
PYCMD=$(cat <<EOF
import json
from sys import argv

def get_token(data:str,name:str='access_token') -> str:
  idx:int = data.find('{')  
  if(idx == -1):
    return ''
  dct_data = json.loads(data[idx:])
  if(name in dct_data.keys()):
    return json.dumps(dct_data[name])
  return ""
#end if
print(get_token(argv[1]).strip('"'))
EOF
)
    #python3 -c "$PYCMD" "${DATA_JSON}"
    get_token=$(python3 -c "$PYCMD" "$1")
    #echo "get_token <$get_token>";return 0
    if [[ ${#get_token} == 0 ]]; then return ; fi
    echo ${get_token} > ${TOKEN_FILE}
    return 0
  fi

  # get token
  var=$(awk -F'\"access_token\":\"|\",' '{print $2}' <<< "$1")
  get_token=$(echo "$var" | tr -d '\n')
  if [[ ${#get_token} == 0 ]]; then return ; fi
  echo ${get_token} > ${TOKEN_FILE}
}
### END   utility get_token() and store_token()

### BEGIN utility get_target()
RESPONSE=''
## $1 string json
## $2 target to found in root object or array JSON
function get_target()
{
  RESPONSE=''
  if ! command -v python3 &> /dev/null ; then return 1 ; fi

PYCMD=$(cat <<EOF
import json
from sys import argv

def get_target(data:str,target:str) -> str:
  idx:int = data.find('{')
  if(idx == -1):
    return ''
  dct_data = json.loads(data[idx:])
  if(not target in dct_data.keys()):
    return

  ret=''
  for it in dct_data[target]:
    ret += f'{it} '
  #end for
  return ret
#end if
print(get_target(argv[1],argv[2]).strip('"'))
EOF
)
  #python3 -c "$PYCMD" "${DATA_JSON}"
  RESPONSE=$(python3 -c "$PYCMD" "$1" "$2")
  #echo "RESPONSE <${RESPONSE}>"
  return 0
}
### END   utility get_target()
