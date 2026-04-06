from django.apps import AppConfig


class ButtonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Buttons'



class BtnWithImage:
    def __init__(self,**kwargs):
        self.path:str  = kwargs.get('path',None)
        self.url:str   = kwargs.get('url',None)
        self.label:str = kwargs.get('label',None)
        self.msg:str   = kwargs.get('msg',self.label) 
  
    def __iter__(self):
        return self
      
    def __str__(self):    
        return f'path: {self.path} | url: {self.url} | label: {self.label} | msg: {self.msg} '


class BtnFormWithImage:
    def __init__(self,**kwargs):
        ## perfil css, opcional
        self.css:str = kwargs.get('css',None)
            
        ## si no lo pasamos colocamos su valor por defecto
        self.type:str = kwargs.get('type','submit')
                
        ## path de la imagen, no es mandatorio
        self.path:str = kwargs.get('path',None)
        
        ## campos mandatorios, deben venir si o si en caso de que no vengan debemso
        # lanzar una excepcion
        self.name:str = kwargs.get('name',None)
        if self.name is None:
           raise ValueError(f'{type(self).__name__} No se establecio el atributo "name"')
        
        self.label:str = kwargs.get('label',None)
        
        ## name, este es opcional en caso de no venir lo igualamos a 'value'
        self.value:str = kwargs.get('label',self.name)

        

    
class BtnForm:
    def __init__(self,**kwargs):
        ## perfil css, opcional
        self.css:str = kwargs.get('css',None)
            
        ## si no lo pasamos colocamos su valor por defecto
        self.type:str = kwargs.get('type','submit')
                
        ## campos mandatorios, deben venir si o si
        # en caso de que no vengan debemos lanzar una excepcion
        self.name:str = kwargs.get('name',None)
        if self.name is None:
           raise ValueError(f'{type(self).__name__} No se establecio el atributo "name"')
        
        self.label:str = kwargs.get('label',None)

        
        ## value, este es opcional en caso de no venir lo igualamos a 'value'
        self.value:str = kwargs.get('value',self.name )
        
