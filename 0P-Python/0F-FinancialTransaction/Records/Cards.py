from Records import Records

class CardsRegister(Records.Record):  
  ''' Defincion del objeto CardsRegister que modela 
      los registros del archivo de tarjetas
      LABEL(12)~ID(4BYTES)
  '''
  def __init__(self,v:str):
    self.label:str = ''    
    self.id:str = ''
    mp:dict = {      
        '!label': slice(0,12)
      , 'id':slice(13,17)
    }
    super().__init__(mp)
    super().set(v)
  #end def

  def __repr__(self):
    ''' representacion formal del objeto mediante un string'''
    return f"{type(self).__name__}(label={self.label:12},id={self.id:04})"
  #end if

  def __str__(self):
    ''' representacion informal del objeto mediante un string'''
    return f"{self.label:8} {self.id:04}"
  #end if

  @classmethod
  def Predicate(cls,v):
    def wrapper(item):
      #print(f'v {v} == item.id {item.id}')
      return v.id == item.id
    #end def
    return wrapper
  #end def
# end class















  