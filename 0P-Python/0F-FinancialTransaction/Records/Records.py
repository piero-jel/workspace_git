from abc import ABC, abstractmethod

class Record(ABC):
  ''' Clase Base Abstracta para Registros

      - mapkey es el dict que contiene el diccionario
        con el nombre de los atributos en funcion de los slice
        para verificar el contenido (si es solo digitos). 
        Si el nombre inicia cono '!' solo usa el slice para
        tomar el string.
  '''
  def __init__(self,mapkey=None):
    #self.mp:dict = mapkey
    self.mp = mapkey
  #end def

  @abstractmethod
  def __str__(self):
    '''Para un metodo abstracto forzamos a crear __str__'''
    pass
  # end def

  """ esta es util solo para degug, debemos cumplir
    SOLID 
      - SRP: Simple
      - OCP: Open And Close
      - LSP: Principio de Sustitucion
      - IS: Segregacion de Interfaces
      - DI: Inversion de Dependencias
      
  @abstractmethod
  def __repr__(self):
    '''Para un metodo abstracto forzamos a crear __repr__'''
    pass
  # end def
  """
  def set(self,v:str):
    ''' setting object from string 
        - v : string value, line in the file
    '''
    if(not self.mp):
      return 
    #end if

    if(not isinstance(v,str)):
      raise TypeError(f'type {type(v)} no permitido')
    # endif    

    for k,s in self.mp.items():      
      tmp = v[s]
      if( k[0] == '!'):        
        self.__dict__[k[1:]] = tmp
        continue
      #endif      
      if(not tmp.isdigit()):
        raise ValueError(f'Part {k} in card register <{tmp}> is not digits')
      #endif
      self.__dict__[k] = tmp      
    #endfor
    return 
  #end def

  @classmethod
  def Parsing(cls,pathfile:str, comment='#') -> list:
    ''' Class method for parsing file
        - pathfile path/file
        - comment optional, comment caracter in file
    '''
    if(not isinstance(pathfile,str)):
      raise TypeError(f'type {type(pathfile)} no permitido')
    # endif
    ret:list = []
    with open(pathfile,'r') as f2r:
      for it in f2r:
        if( it.startswith((comment,'\n','\r'))):
          continue
        # end if        
        ret.append(cls(it))
      #endif
    #end with
    return ret
  # end def

 
  @classmethod
  def Predicate(cls,v:str):
    pass
  #end def

  @classmethod
  def Find(cls,value,cont:list|tuple):
    pred = cls.Predicate(value)
    for it in cont:
      if( pred(it) ):
        return it
      #end if
    #end for
    return None
  #
#end class