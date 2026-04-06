# buil-in import
from __future__ import annotations
from config.utils import ModelAttr

# framework import
from django.db.models import (
    Model, CharField, DateTimeField, EmailField,ForeignKey, CASCADE, OneToOneField, DateField 
)
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Project Modules import
from Login.managers import CustomUserManager


class Empresa(Model,ModelAttr):
    """ Modelo de la tabla para Empresa
        * nombre          : Nombre de la empresa.
        * telefono1       : Telefono Principal.
        * telefono2       : Telefono secundario.
        * date_creacion   : Fecha/Hora de creacion del registro.
        * email           : Email General de la empresa, un contacto general.
    """
    nombre:CharField = CharField(max_length=50,blank=False,null=False)
    telefono1:CharField = CharField(max_length=50,blank=False,null=False)
    telefono2:CharField = CharField(max_length=50,blank=True,null=True)
    date_creacion:DateTimeField = DateTimeField(default=timezone.now,blank=True,null=True)
    email:EmailField = EmailField(blank=True,null=True)

    ATTR:tuple = (
       'id','nombre','telefono1','telefono2',
       'date_creacion', 'email'
    )
     
    def __str__(self):
        return self.nombre
          
    class Meta:
        ## para acceder a los miembros : 
        ordering = ['id']
        verbose_name = 'empresa'
        verbose_name_plural='empresas'


class User(AbstractUser,ModelAttr):
    """ Descripcion del modelo
    AbstractUser
      * id          : Identifcacion primary key
      * username    : Nombre de usuario (unique=True)
      * first_name  : Primer Nombre
      * last_name   : Segundo Nombre, Apellido

    this:
      * email       : Dirreccion de Correo
      * empresa     : Empresa 'Empresa'
      * telefono    : Numero de Telefono
    """
    ## establecemso el default para la tabla ya creada    
    empresa:ForeignKey = ForeignKey(Empresa, on_delete=CASCADE,blank=True,null=True)
    telefono:CharField = CharField(max_length=50,blank=True,null=True)
    objects:CustomUserManager = CustomUserManager()
    ## atributo de clase p/ModelAttr
    ATTR:tuple = ('id','username','first_name','last_name','email','empresa','telefono')

    def __str__(self)->str:
        """ Representacion de informal de un `User` """
        return self.username

    class Meta:
        ## para acceder a los miembros : 
        ordering = ['id']
        verbose_name = 'user'
        verbose_name_plural='users'
    

class Programador(Model,ModelAttr):
    """ Descripcion del modelo
      * programador   : quien esta atendiendo actualmente el ticket.
      * fecha_inicio  : fecha de inicio de actividad en la empresa.    
    """
    ## es un usuario
    programador:OneToOneField = OneToOneField(User, on_delete=CASCADE,blank=True,null=True)
    ## Numero de legajo, l reemplaza el id 
    ## legajo=models.CharField(max_length=50,blank=False,null=False)
    ## Debemos verificar si se puede consultar la existencia
    #  de Grupos y si existe el de programador asignarselo cuando 
    #  Se crea uno nuevo
    fecha_inicio:DateField =  DateField(default=timezone.now)

    ## atributo de clase p/ModelAttr
    ATTR:tuple = ('id','fecha_inicio')
        
    class Meta:
        ## para acceder a los miembros : 
        ordering = ['id']
        verbose_name = 'programador'
        verbose_name_plural='programadores'

    @classmethod
    def item_to_dict(cls,item:Programador=None)->dict:
        """class method for comvert item to dict representation in function cls.ATTR """
        
        if item is None:
            return dict({ key:None for key in cls.ATTR }, **User.item_to_dict() )
        
        return item.to_dict()
        #usr:User = User.objects.get(username=item.programador)
        #return dict({ key:getattr(item,key,None) for key in cls.ATTR }, **usr.to_dict())
            
    def to_str(self,sep:str=', ',sepk:str='=')->str:
        """
        - sep:str separador entre duplas clave valor
        - sepk:str separador entre clave y valor
        """
        cls = type(self)
        usr:User = User.objects.get(username=self.programador)
        return sep.join([f"{key}{sepk}{getattr(self,key,None)}" for key in cls.ATTR]) +\
            sep + usr.to_str(sep,sepk)
    
    def to_dict(self)->dict:
        """class method for comvert item to dict representation in function cls.ATTR """
        cls = type(self)
        usr:User = User.objects.get(username=self.programador)
        return dict({ key: getattr(self,key,None) for key in cls.ATTR },
                    **usr.to_dict() )
    
    def get(self, name):
        cls = type(self)
        if name in cls.ATTR:
            return getattr(self,name)
        
        usr:User = User.objects.get(username=self.programador)
        return usr.get(name)
  
    def __str__(self)->str:
        return f'{self.programador.username}'
    
