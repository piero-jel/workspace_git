"""@package docstring
Copyright 2022, Jesus Emanuel Luccioni
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

 3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

\b file Server.py
\b brief main script for test server Stream
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Lunes 05 de Mayo de 2022.
\b version 0.0.1.
  
\b Change History:

Author         Date                 Version     Brief
JEL            2022.05.05           0.0.1       Version Inicial

"""
import traceback
from sys import argv
from PSocket import Server


def main():
    '''Funcion principal'''
    try:
        argc = len(argv)
        ip  = '0.0.0.0'
        port = 8080

        if argc == 2:
            port = int(argv[1])

        if argc == 3:
            ip,port = argv[1],int(argv[2])

        if argc > 3:
            print(f'Error in call aplication try: {argv[0]} [ip] [port]')
            return

        with Server(ip=ip,port=port,fmt_len=4) as st:
            if not st.Connect():
                print(f'Error connect <{repr(st)}>: {st.last_error}')
                return

            print(f'Connect Success to {repr(st)}')
            adr = st.Accept()
            print(f'Connect Address Client {adr}')

            while True:
                msg = st.Receive()
                if msg == '':
                    print('End, request from client')
                    break

                print(f'Message receive: {msg}')
                code = input("Insert CODE (Ctrl+c to end) :")
                if code == '':
                    print('End, request from user')
                    ## enviamos al client para que cierre conexion
                    st.Send("")
                    continue

                response = f'0210{int(code):02}'
                print(f'response :{response }')
                st.Send(response)


    except ValueError as e :
        print(f'ValueError {e}')

    except KeyboardInterrupt:
        print('End request for current user')

    except AttributeError as err:
        print(f'AttributeError : {err} ')

    except TypeError as err:
        print(f'TypeError : {err} ')

    except NameError as err:
        print(f'{err} ')

    except SyntaxError as err:
        print(f'{err} ')

    except: # pylint: disable=bare-except
        print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')


# verificamos si este script es el principal invocado desde la linea de comandos
if __name__ == "__main__":
    main()
