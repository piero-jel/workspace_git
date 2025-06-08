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
THIS_NAME=${0##*/}
TARGET=""




### BEGIN Function MAIN
function main()
{
  TARGET=${1:-'--up'}
  case "${TARGET}" in
    '--up')
        python3 manage.py migrate
        python3 manage.py load_list_items --pathfile in/items.json
        echo "Local URL: http://localhost:8080"
        python3 manage.py runserver 0.0.0.0:8080
        gunicorn --bind  0.0.0.0:8000 rd_wepapp.wsgi
        return 0
    ;;
    *)
      echo "param <${1}> no contemplado"
      return 1
    ;;
  esac
  return 0
}
### END   Function MAIN

### BEGIN ENTRY POINT TO RUN
main "$@" && exit 0
### END   ENTRY POINT TO RUN
