from __future__ import annotations


class ModelAttr:
    """ clase para modelar los metodos basicos para las clases
    que tengan definido su ATTR atributo Clase con el listado de 
    atributo del objeto que puede obtener por nombre y demas metodos
    """
    ATTR:tuple = tuple()
    def get(self,name:str)->str|int:
        """ 
        Metodo para implementar el modelo dentro de un 'forms.Form' para la inicializacion
        mediante:
            contexto['user_form'] = FormEditUser(data=luser)

        - name:str : nombre del atributo a obtener
        """
        cls = type(self)
        if name not in cls.ATTR:
            return None
        
        return getattr(self,name)

    def attr(self)->tuple:
        '''metodo para obtener el Listado de atributos'''
        return type(self).ATTR
    
    def to_str(self,sep:str=', ',sepk:str='=')->str:
        """
        - sep:str separador entre duplas clave valor
        - sepk:str separador entre clave y valor
        """
        cls = type(self)
        return sep.join([f"{key}{sepk}{getattr(self,key,None)}" for key in cls.ATTR])
    
    def to_dict(self)->dict:
        """class method for comvert item to dict representation in function cls.ATTR """
        cls = type(self)        
        return { key: getattr(self,key,None) for key in cls.ATTR }
    
    # FIXME deprecada
    @classmethod
    def item_to_dict(cls,item:ModelAttr=None)->dict:
        """class method for comvert item to dict representation in function cls.ATTR """
        
        if item is None:
            return { key:None for key in cls.ATTR }
        
        return item.to_dict()
        #return { key:getattr(item,key,None) for key in cls.ATTR }