from __future__ import annotations


from django.db.models import (Model,CharField, ForeignKey, DateField,
                              FileField, BooleanField,DateTimeField,
                              TimeField,
                              CASCADE,DO_NOTHING)
from multi_email_field.fields import MultiEmailField
from django.utils import timezone
from django.db.models.query import QuerySet


from Ticket.constants import (DETAIL_MAX_LEN, MODULOS_NOMBRE_MAXLEN, MODULOS_DESC_MAXLEN)
from Login.models import User, Programador , Empresa
from Ticket.validators import FileSize


class Modulos(Model):
    """Descripcion del modelo 
      * nombre      : Nombre del Modulo.
      * descripcion : Descripcion del Modulo.
    """
    nombre:CharField = CharField(max_length=MODULOS_NOMBRE_MAXLEN,blank=False,null=True)
    descripcion:CharField = CharField(max_length=MODULOS_DESC_MAXLEN,blank=False,null=True)
  
    def __str__(self):
        return f'{self.nombre}'

  
class Tickets(Model):
    """ Descripcion del modelo
      * register  : quien registra el ticket, Modelo User
      * attend    : quien esta atendiendo actualmente el ticket, Modelo Programador
      * brief     : Nombre / etiqueta que representa el Issue.
      * detail    : Detalle issue incidente.
      * email     : Lista de meil a quien notificar ls trabajaos registrados sobre el issue
      * fecha_creacion : Fecha en la cual se creo el issue.
      * fecha_update  : Fecha de ultima actualizacion (fecha en la cual se registro un nuevo
                         trabajo tabla TicketsHistory)
      * fecha_cierre  : Fecha de cierre del issue (None, valor por defecto)
      * file1     : Archivo uno para acompañar el detalle del insidente
      * file2     : Archivo dos para acompañar el detalle del insidente
      * estado    : Estado Actual del issue
      * edit_register 
      * register_estado
    """
    ATTR:tuple = (
       'id', 'empresa' ,'register', 'attend','brief','detail','email',
       'fecha_creacion','fecha_cierre','file1','file2','estado',
       'fecha_update','edit_register','register_estado'
    )

    register:ForeignKey = ForeignKey(User, on_delete=CASCADE,blank=True,null=True)    
    attend:ForeignKey   = ForeignKey(Programador,on_delete=DO_NOTHING,blank=True,null=True)    
    brief:ForeignKey    = ForeignKey(Modulos, on_delete=DO_NOTHING,blank=True,null=True)
    detail:CharField    = CharField(max_length=DETAIL_MAX_LEN,blank=False)    
    email:MultiEmailField = MultiEmailField(blank=True,null=True)    
    fecha_creacion:DateField = DateField(default=timezone.now)
    ## Debemos agragar Fecha update
    fecha_update:DateField =  DateField(null=True,blank=True)
    
    ## habilitamos que coloque NULL y pueda dejarse en blanco  
    fecha_cierre:DateField = DateField(null=True,blank=True)
    file1:FileField = FileField(null=True,blank=True, upload_to='files/tickets/%Y%m%d/'
                                ,validators=[FileSize])
    file2:FileField = FileField(null=True,blank=True, upload_to='files/tickets/%Y%m%d/',
                                validators=[FileSize])
    file3:FileField = FileField(null=True,blank=True, upload_to='files/tickets/%Y%m%d/',
                                validators=[FileSize])
  
    ## agregamos el estado del ticket    
    estado:BooleanField = BooleanField(default=True)    
    register_estado:BooleanField = BooleanField(default=True)
    edit_register:BooleanField = BooleanField(default=False)

    class Meta:
        ## para acceder a los miembros : 
        ordering = ['id']
        verbose_name = 'ticket'
        verbose_name_plural='tickets'
        
        ## Definimos los permisos sobre esta tabla
        permissions = [
          ##(codename   , descripcion ) 
            ('admin'    , 'Puede Administrar los ticket (ver historial, dar de baja)'),
            ('attend'   , 'Puede Atender un ticket'),
            ('register' , 'Puede Registrar un nuevo ticket'),
        ] 
    
    @classmethod
    def item_to_dict(cls,**kwargs)->dict:
        '''
        Definimos le metodo para obtener un mapa desde un objeto, una instancia del modelo 
        proveniente de una query.
        @return 
          retornamos un mapa con todo los campos que pueden ser requeridos, campos que son anidados.
        '''
        Object:Tickets = kwargs.get('item',None)

        if Object and isinstance(Object,QuerySet):
            # Es tipico pasar un Set Query completo, por eso debemos chequear
            #  y tomar el primer elemento
            Object = Object[0]            
    
        ## Creamos el mapa por defecto
        if Object is None:
            ## si no tenemso id, no se lleno la BBDD
            return { key : None for key in cls.ATTR }

        return Object.to_dict()

    def to_dict(self)->dict:

        ret:dict = { 
            'id'    : self.id,
            'brief' : self.brief,
            'detail': self.detail,
            'email' : self.email,
            'fecha_creacion': self.fecha_creacion,
            'fecha_cierre'  : self.fecha_cierre,
            'file1':  self.file1,
            'file2':  self.file2,
            'estado': self.estado, 
            'fecha_update' :  self.fecha_update,
            'edit_register':  self.edit_register,
            'register' : User.item_to_dict(item = self.register),
            'attend'   : Programador.item_to_dict(item = self.attend)
        }
        tmp:dict = User.item_to_dict(item = self.register)
        if tmp is not None:
            ret['register'] = tmp['username']
            ret['empresa']  = tmp['empresa']

        tmp:dict = Programador.item_to_dict(item = self.attend)
        if tmp is not None:
            ret['attend'] = tmp['username']

        if len(ret['email']) > 0:
            ret['email'] = ', '.join(ret['email'])
        else:
            ret['email'] = None

        #ret['register'] = User.item_to_dict(item = self.register)
        #ret['register']['register'] = ret['register']['username']
        #ret['empresa']  = ret['register']['empresa']
        #ret['attend']   = Programador.item_to_dict(item = self.attend)
        #ret['attend']['attend'] = ret['attend']['username']

        ret['register_estado'] = 'Cerrado'
        if self.estado and self.register_estado:
            ret['register_estado'] = 'Activo'

        elif self.estado and not self.register_estado:
            ret['register_estado'] = 'Cierre Pend'
                
        return { key : ret.get(key,None) for key in type(self).ATTR }
        #return ret

    def __str__(self):
        return f'{self.id} | {self.register} | {self.attend} |{self.brief} | {self.fecha_creacion}'
    

class RegisterWork(Model):
    """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un ticket.
      * ticket          : Ticket sobre el cual se registrara el trabajo, Modelo Tickets
      * register_work   : quien registra el trabajo sobre el ticket en cuestion, Modelo 
                          User en caso de reg  Programador 'luser.programador'
      * date_creacion   : Fecha en la cual se creo el registro del nuevo trabajo.
      * modulo          : Modulo sobre el cual se realizo el trabajo.
      * msg             : Detalle del trabajo realizado o mensage descriptivo.    
      * file1           : Archivo para acompañar el detalle del trabajo realizado.
      * file2           : Archivo para acompañar el detalle del trabajo realizado.    
      * tiempo          : Tiempo consumido para realizar el trabajo.    
      * date_update     : Hora y Fecha de actualizacion del registro.
      * programmer      : True | False , especifica si es programador quien registra
    """
    ticket:ForeignKey = ForeignKey(Tickets, on_delete=CASCADE,blank=False,null=True)    
    register_work:ForeignKey = ForeignKey(User,on_delete=DO_NOTHING,blank=True,null=True)
    date_creacion:DateTimeField = DateTimeField(null=True,blank=True)
    msg:CharField = CharField(max_length=DETAIL_MAX_LEN,blank=False)
    file1:FileField = FileField(null=True,blank=True, upload_to = 'files/ticket_history/%Y%m%d/',
                                validators=[FileSize])
    file2:FileField = FileField(null=True,blank=True, upload_to = 'files/ticket_history/%Y%m%d/',
                                validators=[FileSize])  
    
    ## para almacenar el tiempo y la hora    
    tiempo:TimeField = TimeField(blank=True,null=True)
    date_update:DateTimeField = DateTimeField(auto_now=True,null=True,blank=True)  
    programmer:BooleanField = BooleanField(default=False)
    
    def __str__(self):
        attrs:tuple = ('id', 'date_creacion',
            'date_update', 'file1',
            'file1', 'tiempo', 'programmer'
        )
        return " ,".join([ f'{key}={getattr(self,key,None)}' for key in attrs]) 
  
    @classmethod
    def item_to_dict(cls,**kwargs):
        """ """
        item:RegisterWork = kwargs.get('item',None)        
        if item is None:
            return None
                 
        ## Mapeamos el campo externo
        mapTickets = Tickets.item_to_dict(item = item.ticket)
        ## definimos cual es el representativo del modelo Ticket, depende de la info representativa
        mapTickets['ticket'] = mapTickets['id']
    
        return {
            'id':item.id, 'ticket':mapTickets, 'register_work':item.register_work,
            'date_creacion': item.date_creacion, 'msg' : item.msg, 'file1': item.file1,
            'file2': item.file2, 'date_update': item.date_update ,
            'programmer': item.programmer 
        }
    

class Desarrollo(Model):
    """ Descripcion del modelo
      * registro    : quien registra el pedido de un nuevo desarrollo 
      * empresa     : Para que empresa, peude ser interno (opcionale)
      * asistente   : quien esta trabajando actualmente en el desarrollo, Modelo Programador    
      * modulo      : Modulo si es que este esta definido, se puede asignar luego.
      * descripcion : Descripcion del desarrollo a realizar.
      * email       : Lista de meil a quien notificar los trabajos registrados sobre el desarrollo
      * fecha_creacion : Fecha en la cual se creo el issue.
      * fecha_actualizacion  : Fecha de la ultima actualizacion (en la cual se registro un nuevo trabajo )
      * fecha_cierre  : Fecha de cierre del Desarrollo (None, valor por defecto)
      * file1     : Archivo uno para acompañar el detalle del Desarrollo
      * file2     : Archivo dos para acompañar el detalle del Desarrollo
      * file3     : Archivo dos para acompañar el detalle del Desarrollo
      * estado    : Estado Actual del issue
    """
    ## use -> administrador 
    registro:ForeignKey   = ForeignKey(User, on_delete=CASCADE,blank=False,null=True)
    empresa:ForeignKey    = ForeignKey(Empresa,on_delete=DO_NOTHING,blank=True,null=True)
    asistente:ForeignKey  = ForeignKey(Programador,on_delete=DO_NOTHING,blank=True,null=True)
    modulo:ForeignKey     = ForeignKey(Modulos, on_delete=DO_NOTHING,blank=True,null=True)
    descripcion:CharField = CharField(max_length=DETAIL_MAX_LEN,blank=False)  
    email:MultiEmailField = MultiEmailField(blank=True,null=True)    
    fecha_creacion:DateField = DateField(default=timezone.now)
    fecha_actualizacion:DateField = DateField(null=True,blank=True)  
    fecha_cierre:DateField = DateField(null=True,blank=True)      
    file1:FileField = FileField(null=True,blank=True, upload_to='files/desarrollos/%Y%m%d/',
                                validators=[FileSize])
    file2:FileField = FileField(null=True,blank=True, upload_to='files/desarrollos/%Y%m%d/',
                                validators=[FileSize])
    file3:FileField = FileField(null=True,blank=True, upload_to='files/desarrollos/%Y%m%d/',
                                validators=[FileSize])
    
    estado:BooleanField = BooleanField(default=True)
  
    @classmethod    
    def item_to_dict(cls,**kwargs)->dict:
        '''
          Definimos le metodo para obtener un mapa desde un objeto, una instancia del modelo 
          proveniente de una query.
          @return 
            retornamos un mapa con todo los campos que pueden ser requeridos, campos que son anidados.
        '''
        attrs:tuple = (
           'id', 'empresa' ,'register', 'attend', 'brief',
            'detail', 'email', 'fecha_creacion', 'fecha_cierre',
            'file1', 'file2' ,'estado' ,'fecha_update' ,
            'edit_register' ,'register_estado'
        )
        item:Desarrollo = kwargs.get('item',None)

        if item is None:        
            ## si no tenemso id, no se lleno la BBDD
            # print(f'Object: {Object}')
            return { key : None for key in attrs }
          
        if isinstance(item,QuerySet):
            item = item[0]
    
        mapRegsiter = User.item_to_dict(item = item.register)
        ## definimos cual es el representativo del modelo regsiter
        mapRegsiter['register'] = mapRegsiter['username']
        mapAttend = Programador.item_to_dict(item_query = item.attend)
        
        ## definimos cual es el representativo del modelo regsiter
        mapAttend['attend'] = mapAttend['username']
        
        tckRegisterEstado = 'Cerrado'
        if item.estado and item.register_estado:
            tckRegisterEstado = 'Activo'

        elif item.estado and not item.register_estado: 
          tckRegisterEstado = 'Cierre Pend'
    
        return { 
            'id': item.id, 'empresa': mapRegsiter['empresa'],'register':mapRegsiter,
            'attend':mapAttend ,'brief': item.brief, 'detail': item.detail,
            'email' : item.email,'fecha_creacion': item.fecha_creacion,
            'fecha_cierre': item.fecha_cierre, 'file1': item.file1,
            'file2': item.file2, 'estado': item.estado, 'fecha_update': item.fecha_update,
            'edit_register': item.edit_register , 'register_estado': tckRegisterEstado 
        }
            
    def __str__(self):
        '''
          * registro    : quien registra el pedido de un nuevo desarrollo 
          * empresa     : Para que empresa, peude ser interno (opcionale)
          * asistente   : quien esta trabajando actualmente en el desarrollo, Modelo Programador    
          * descripcion : Descripcion del desarrollo a realizar.
          * email       : Lista de meil a quien notificar los trabajos registrados sobre el desarrollo
          * fecha_creacion : Fecha en la cual se creo el issue.
          * fecha_actualizacion  : Fecha de la ultima actualizacion (en la cual se registro un nuevo trabajo )
          * fecha_cierre  : Fecha de cierre del Desarrollo (None, valor por defecto)
          * file1     : Archivo uno para acompañar el detalle del Desarrollo
          * file2     : Archivo dos para acompañar el detalle del Desarrollo
          * file3     : Archivo dos para acompañar el detalle del Desarrollo
          * estado    : Estado Actual del issue
        '''
        attrs:tuple = (
            'id', 'registro', 'empresa', 
            'asistente', 'descripcion', 'fecha_creacion',
            'fecha_actualizacion', 'fecha_cierre'
        )
        return ', '.join( f'{key}={getattr(self,key,None)}' for key in attrs )


class RegistroTrabajo(Model):
    """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un ticket.
      * desarrollo      : Ticket sobre el cual se registrara el trabajo, Modelo Tickets
      * register_work   : quien registra el trabajo sobre el ticket en cuestion, Modelo Programador    
      * fecha_creacion  : Fecha en la cual se creo el registro del nuevo trabajo.    
      * msg             : Detalle del trabajo realizado o mensage descriptivo.    
      * file1           : Archivo para acompañar el detalle del trabajo realizado.
      * file2           : Archivo para acompañar el detalle del trabajo realizado.    
      * tiempo          : Tiempo consumido para realizar el trabajo.    
      * date_update     : Hora y Fecha de actualizacion del registro.
      * programmer      : True | False , especifica si es programador quien registra
    """
    desarrollo:ForeignKey = ForeignKey(Desarrollo, on_delete=CASCADE,blank=False,null=True)      
    register_work:ForeignKey = ForeignKey(User,on_delete=DO_NOTHING,blank=True,null=True)  
    fecha_creacion:DateTimeField = DateTimeField(default=timezone.now,null=True,blank=True)
    msg:CharField=CharField(max_length=DETAIL_MAX_LEN,blank=False)
    file1:FileField = FileField(null=True,blank=True, 
                                upload_to = 'files/registros_de_trabajos/%Y%m%d/',
                                validators=[FileSize])
    file2:FileField = FileField(null=True,blank=True, 
                                upload_to = 'files/registros_de_trabajos/%Y%m%d/',
                                validators=[FileSize])  
    tiempo:TimeField = TimeField(blank=True,null=True)
    date_update:DateTimeField = DateTimeField(auto_now=True,null=True,blank=True)  
    programmer:BooleanField = BooleanField(default=False)
   
    def __str__(self):
        attrs:tuple = (
            'id', 'fecha_creacion', 'date_update', 'file1', 'file2',
            'tiempo', 'programmer'
        )
        return ', '.join( f"{key}={getattr(self,key,None)}" for key in attrs )
  
    
    @classmethod    
    def item_to_dict(cls,**kwargs)->dict:
        item:RegistroTrabajo = kwargs.get('item',None)

        if item is None:
            return None
                 
        ## Mapeamos el campo externo
        mapTickets = Tickets.item_to_dict(item = item.ticket)
        ## definimos cual es el representativo del modelo Ticket, depende de la info representativa
        mapTickets['ticket'] = mapTickets['id']
    
        return { 
            'id': item.id, 'ticket': mapTickets, 'register_work': item.register_work,
            'date_creacion': item.date_creacion , 'msg' : item.msg,
            'file1': item.file1 ,'file2': item.file2, 'date_update': item.date_update,
            'programmer': item.programmer 
        } 