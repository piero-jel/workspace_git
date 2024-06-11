from Records import Records

class RangesRegister(Records.Record):  
  ''' Defincion del objeto RangesRegister que modela los registros 
      del archivo de rangos 
      RANGE_LOW(8)~RANGE_HIGHT(8)~LEN(2BYTES)~ID(4BYTES)
  '''
  def __init__(self,v:str):
    self.low:str = ''
    self.high:str = ''
    self.len:str = ''
    self.id:str = ''

    mp:dict = {
        'low':slice(0,8)
      , 'high':slice(9,17)
      , 'len':slice(18,20)
      , 'id':slice(21,25)      
    }
    super().__init__(mp)
    super().set(v)
  #end def

  def __repr__(self):
    ''' representacion formal del objeto mediante un string'''
    return f"{type(self).__name__}(low={self.low:8},high={self.high:8},len={self.len:02},id={self.id:04})"
  #end if

  def __str__(self):
    ''' representacion informal del objeto mediante un string'''
    return f"{self.low:8} {self.high:8} {self.len:02} {self.id:04}"
  #end if

  @classmethod
  def Predicate(cls,v:str):
    return RangePredicate(v)
# end class

class RangePredicate:
  def __init__(self,v:str):
    ''' Inicializa el objeto para poder ser usado luego como
        predicado
    '''
    if(not isinstance(v,str)):
      raise TypeError(f'type {type(v)} no permitido')
    # endif
    self.cardnum = v[0:8]
  # end def

  def __call__(self, item:'RangesRegister')-> bool:
    ''' Method para el uso como predicado
    '''
    if( item.low <= self.cardnum <= item.high):
      return True
    return False
  #end def
#end class














  