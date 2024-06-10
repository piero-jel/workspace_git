#!/bin/python3
import traceback
from Records.Ranges import RangesRegister
from Records.Cards import CardsRegister
from PSocket import Stream
from sys import argv

def GetAmount(msg:str,maxlen:int=12)->int:     
  am_str:str = input(msg)
  am_str = am_str.lstrip()
  if(am_str[0] == '-'):
    raise ValueError(f'Negative Amount <{am_str}> not allowed"')
  #end if
  am_str = am_str.lstrip('+')
  if(len(am_str) > maxlen):
    raise ValueError(f'Negative Amount <{am_str}> not allowed"')
  return int(float(am_str)*100)    
  if(not am_str.isdecimal()):
    raise ValueError(f'Amount <{am_str}> It is not composed only of digits')
  #end if    
#end def

def GetCardNumber(msg:str,minlen:int=13,maxlen:int=99)->str:
  am_str:str = input(msg)
  am_str = am_str.lstrip()    
  if(not minlen <= len(am_str) <= maxlen):
    raise ValueError(f'Card Number <{am_str:15}> length<{len(am_str)}> incorrect')
  #end if    
  if(not am_str.isdigit()):
    raise ValueError(f'Card Number <{am_str}> It is not composed only of digits')
  #end if
  return am_str
#end def

def GetCardCode(msg:str,maxlen:int=3)->str:
  am_str:str = input(msg)
  am_str = am_str.lstrip()    
  if( len(am_str) != maxlen):
    raise ValueError(f'Card Code <{am_str}> length<{len(am_str)}> incorrect')
  #end if    
  if(not am_str.isdigit()):
    raise ValueError(f'Card Number <{am_str}> It is not composed only of digits')
  #end if
  return am_str
#end def
  
def main():
  """ Opcional argumentos
    
      - ip : ip server IPv8
      - port : port 
  """
  try:
    argc = len(argv)
    ip  = '0.0.0.0'
    port = 8080
    
    if(argc>2):
      ip = argv[2]
    # end if
    
    if(argc>3):
      ip,port = argv[2],int(argv[3])
    # end if

    frange = 'files/local/ranges.dat'
    fcards = 'files/local/cards.dat'
    crange = RangesRegister.Parsing(frange)
    ccards = CardsRegister.Parsing(fcards)

    amount = GetAmount("Ingrese el monto (hasta 2 decimales Implicitos): ")
    #print(f'amount: {amount}')    
    num_card = GetCardNumber('Ingrese el numero de Tarjeta: ')
    ## find card number
    #rng_reg:RangesRegister = RangesRegister.Find(num_card,crange)
    rng_reg = RangesRegister.Find(num_card,crange)
    
    if(not rng_reg):    
      print(f'TARJETA <{num_card}> NO SOPORTADA')
      return 
    #endif
    #card_reg:CardsRegister = CardsRegister.Find(rng_reg,ccards)
    card_reg = CardsRegister.Find(rng_reg,ccards)
    if(not card_reg):
      print(f'TARJETA <{num_card}> NO SOPORTADA, ID {card_reg.id} no localizado')
      return 
    #endif
    print(f'LABEL CARD: {card_reg.label}')
    card_code = GetCardCode('Ingrese el Codigo de Seguridad (hasta 3 digitos): ')

    request = f'0200{len(num_card):02}{num_card}{amount:012}{card_code}'
    response = None
    with Stream.Client(ip=ip,port=port,fmt_len=4) as st:
      if(not st.Connect()):
        print(f'ERROR DE COMUNICACION <Error connect {st}: {st.last_error}>')
        return
      # end if
      print(f'Connect Success to {repr(st)}')
      st.Send(request)
      response = st.Receive(5.0)
      ## para notificar que cierre al server
      st.Send("")
    #end with
    print(f'response: {response}')
    if(response == ''):
      print(f'ERROR DE COMUNICACION, SERVER CLOSE COMUNICATION')
      return 
    #end if

    if(response[0:4] != '0210'):
      print(f'MTID <{response[0:4]}> Incorrecto')
      return 
    #end if
    
    if(response[4:6] == '00'):
      print('APROBADA')
    else:
      print(f'RECHAZADA, code <{response}>')
    #end if
  except TimeoutError as e:
    print(f'ERROR DE COMUNICACION TIME-OUT')

  except Exception as e:    
    print(f'Exception Type {type(e)}\nTRACEBACK:{traceback.format_exc()}')

  except KeyboardInterrupt:
    print('End request for current user')
  
  except: 
    ''' la clausula except sin arg debe quedar siempre al final '''
    print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')    
  # end try
# end def

if (__name__ == "__main__"):
  main()  
# end if
  
