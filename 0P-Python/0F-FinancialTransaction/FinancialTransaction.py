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

\b file FinancialTransaction.py
\b brief main script for project `FinancialTransaction`
\b author Jesus Emanuel Luccioni - piero.jel@gmail.com.
\b date Lunes 05 de Mayo de 2022.
\b version 0.0.1.
  
\b Change History:

Author         Date                 Version     Brief
JEL            2022.05.05           0.0.1       Version Inicial

"""
import traceback
from sys import argv
from Records import RangesRegister,CardsRegister
from PSocket import Client

def GetAmount(msg:str,maxlen:int=12)->int:
    """
    Funcion para obtener el monto desde input 

    :param msg: mensaje para la peticion del monto
    :type msg: str

    :param maxlen: longitud maxima esperada para el monto
    :type maxlen: int

    :return: return monto ingresado
    :rtype: int
       
    """
    am_str:str = input(msg)
    am_str = am_str.lstrip()
    if am_str[0] == '-':
        raise ValueError(f'Negative Amount <{am_str}> not allowed"')

    am_str = am_str.lstrip('+')
    if len(am_str) > maxlen:
        raise ValueError(f'Amount length <{len(am_str)}> too long"')

    return int(float(am_str)*100)

def GetCardNumber(msg:str,minlen:int=13,maxlen:int=99)->str:
    """
    Funcion para obtener el Numero de la Tarjeta desde input 

    :param msg: mensaje para la peticion del Nro de Tarjeta
    :type msg: str

    :param minlen: longitud minima esperada para el Nro de Tarjeta
    :type minlen: int

    :param maxlen: longitud maxima esperada para el Nro de Tarjeta
    :type maxlen: int

    :return: return Numero de Tarjeta
    :rtype: str
       
    """
    am_str:str = input(msg)
    am_str = am_str.lstrip()

    if not minlen <= len(am_str) <= maxlen:
        raise ValueError(f'Card Number <{am_str:15}> length<{len(am_str)}> incorrect')

    if not am_str.isdigit():
        raise ValueError(f'Card Number <{am_str}> It is not composed only of digits')

    return am_str

def GetCardCode(msg:str,maxlen:int=3)->str:
    """
    Funcion para obtener el Codigo de la Tarjeta

    :param msg: mensaje para la peticion del Codigo de la Tarjeta
    :type msg: str

    :param maxlen: longitud maxima esperada para el Codigo de la Tarjeta
    :type maxlen: int

    :return: return Codigo de la Tarjeta
    :rtype: int
       
    """
    am_str:str = input(msg)
    am_str = am_str.lstrip()
    if len(am_str) != maxlen:
        raise ValueError(f'Card Code <{am_str}> length<{len(am_str)}> incorrect')

    if not am_str.isdigit():
        raise ValueError(f'Card Number <{am_str}> It is not composed only of digits')

    return am_str

def main(): # pylint: disable=too-many-locals, disable=too-many-statements
    """ Funcion Principal 

        - ip : ip server IPv8
        - port : port 
    """
    try:
        argc:int = len(argv)
        ip:str  = '0.0.0.0'
        port:int = 8080

        if argc>2:
            ip = argv[2]

        if argc>3:
            ip,port = argv[2],int(argv[3])


        frange = 'files/local/ranges.dat'
        fcards = 'files/local/cards.dat'
        crange = RangesRegister.Parsing(frange)
        ccards = CardsRegister.Parsing(fcards)

        amount = GetAmount("Ingrese el monto (hasta 2 decimales Implicitos): ")
        num_card = GetCardNumber('Ingrese el numero de Tarjeta: ')

        ## find card number
        rng_reg = RangesRegister.Find(num_card,crange)

        if not rng_reg:
            print(f'TARJETA <{num_card}> NO SOPORTADA')
            return

        card_reg = CardsRegister.Find(rng_reg,ccards)
        if not card_reg:
            print(f'TARJETA <{num_card}> NO SOPORTADA, ID {card_reg.id} no localizado')
            return

        print(f'LABEL CARD: {card_reg.label}')
        card_code = GetCardCode('Ingrese el Codigo de Seguridad (hasta 3 digitos): ')

        request = f'0200{len(num_card):02}{num_card}{amount:012}{card_code}'
        response = None
        with Client(ip=ip,port=port,fmt_len=4) as st:
            if not st.Connect():
                print(f'ERROR DE COMUNICACION <Error connect {st}: {st.last_error}>')
                return

            print(f'Connect Success to {repr(st)}')
            st.Send(request)
            response = st.Receive(5.0)
            ## para notificar que cierre al server
            st.Send("")

        print(f'response: {response}')

        if response == '':
            print('ERROR DE COMUNICACION, SERVER CLOSE COMUNICATION')
            return

        if len(response) < 6:
            print('ERROR RESPONSE <{response}> Too short')
            return

        if response[0:4] != '0210':
            print(f'MTID <{response[0:4]}> Incorrecto')
            return

        if response[4:6] == '00':
            print('APROBADA')
        else:
            print(f'RECHAZADA, code <{response[4:6]}>')

    except TimeoutError as e:
        print(f'ERROR DE COMUNICACION TIME-OUT <{e}>')

    except ValueError as e:
        print(f'ERROR EN EL INGRESO DE DATOS <{e}>')

    except Exception as e: # pylint: disable=broad-exception-caught
        print(f'Exception Type {type(e)}\nTRACEBACK:{traceback.format_exc()}')

    except KeyboardInterrupt:
        print('End request for current user')

    except: # pylint: disable=bare-except
        print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')


if __name__ == "__main__":
    main()
