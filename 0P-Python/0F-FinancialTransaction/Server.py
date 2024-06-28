#!/bin/python3
import traceback
from PSocket import Stream
from sys import argv


def main():  
  try:    
    argc = len(argv)
    ip  = '0.0.0.0'
    port = 8080
    
    if(argc == 2):
      port = int(argv[1])
    # end if
    
    if(argc == 3):
      ip,port = argv[1],int(argv[2])
    # end if
    
    if(argc > 3):
      print(f'Error in call aplication try: {argv[0]} [ip] [port]')
      return
    #endif
    
    with Stream.Server(ip=ip,port=port,fmt_len=4) as st:
      if(not st.Connect()):
        print(f'Error connect <{repr(st)}>: {st.last_error}')
        return
      # end if
      print(f'Connect Success to {repr(st)}')
      adr = st.Accept()
      print(f'Connect Address Client {adr}')
      
      while True:
        msg = st.Receive()
        if(msg == ''):
          print('End, request from client')
          break
        # end if
        print(f'Message receive: {msg}')
        code = input("Insert CODE (Ctrl+c to end) :")
        if(code == ''):
          print('End, request from user')
          ## enviamos al client para que cierre
          st.Send("")
          continue
        # end if
        response = f'0210{int(code):02}'
        print(f'response :{response }')
        st.Send(response)        
      # end while      
    # end with
    
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


  
  except: 
    ''' la clausula except sin arg debe quedar siempre al final '''
    print(f'Exception Desconocida\nTRACEBACK:{traceback.format_exc()}')    
  # end try  
# end def
  




''' verificamos si este script es el principal
    invocado desde la linea de comandos
'''
if (__name__ == "__main__"):
  main()  
# end if
  
