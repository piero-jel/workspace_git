# buil-in import
import os
import sys
from logging import getLogger,Logger
from datetime import timedelta

# framework import
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.forms.fields import DateField
from django.forms import (
    ModelForm, Form, Textarea, CharField, TextInput, TimeField, ModelChoiceField,
    BooleanField, ValidationError 
)
from django.utils import timezone
from django.utils.translation import gettext as _

# Project Modules import
from Ticket.models import (Desarrollo, RegistroTrabajo, Tickets , RegisterWork ,Modulos)
from Ticket.constants import (DETAIL_MAX_LEN,MODULOS_NOMBRE_MAXLEN)
from config.apps import deltatime2time
from Login.models import User,Programador,Empresa
from Login.contexto import EmailThread
from Login.constants import GROUPS
from Ticket.validators import SizeValidator


log:Logger = getLogger('Ticket')

class FormularioTicket(ModelForm):
    class Meta:
        model = Tickets
        fields:list[str] = ['brief','detail','email','file1','file2', 'file3' ]    
        labels:dict = {
            'brief': 'Modulo',
            'detail': 'Descripcion del Incidente',
            'email': 'Lista de Direcciones de correo',
            'file1': 'Adjuntar Archivo 1',
            'file2': 'Adjuntar Archivo 2',
            'file3': 'Adjuntar Archivo 3' 
        }    
        widgets:dict = {
            'detail': Textarea(attrs={
                        'cols': 50,
                        'rows': 10,
                        'title': f'Ingrese un mensaje de hasta {DETAIL_MAX_LEN} caracteres',
                        'placeholder': 'Mensaje o Descripcion del Incidente' 
                    })
        }
    
    def is_valid(self)->bool:
        """ metho for validation of form """
        if not super().is_valid():
            return False
        
        log.debug(f'self.data: {self.data}')
        ## check modulos seleccionado
        if self.data['brief'] in ('',None):
            self.add_error('brief', f"Selecciones Un Modulos de la Lista.")
            return False
    
        mod:Modulos = None
        try:
            mod = Modulos.objects.get(id=self.data['brief'])
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}> detail: {e}')
            self.add_error('brief',
                           "Fallo la query para verificar el Nombre de Modulo:"\
                          f" {self.data['brief']}.")
            return False
    
        return False if mod is None else True
            
    def save(self,**kwargs)->Tickets:
        """ metho for save instance
            - instance
            - register
            - ticket_id
        """
        mod:Modulos = None
        try:
            mod = Modulos.objects.get(id=self.data['brief'])
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}> detail: {e}')
            self.add_error('username', 
                           "Fallo la quey para verificar el Nombre de usuario: "\
                            f"{self.data['username']}.")
            return None

        #log.debug(f'{type(self).__name__}::save() instance: {self.instance}')
        t1:Tickets = kwargs.get('instance',None)
        #if t1 is None:
        #    t1 = self.instance
        ticket_id:int = kwargs.get('ticket_id',None)
        if t1 is None and ticket_id is not None:
            try:
                t1 = Tickets.objects.get(id=ticket_id)
            except:
                log.error(f"Fallo la quey para obtener el ticket con id {ticket_id}")
                return None

        okInstance:bool = False
        if t1 is not None:          
            t1.brief  = mod
            t1.detail = self.data['detail']
            t1.email  = self.data['email']
            okInstance = True
        else:
            t1 = Tickets(register=kwargs.get('register'),
                       brief=mod, detail=self.data['detail'],
                       email=self.data['email'])
                
        if okInstance:
            if 'file1-clear' in self.data:              
                if os.path.isfile(t1.file1.path):
                    os.remove(t1.file1.path)
                t1.file1 = None
            
            if 'file2-clear' in self.data:              
                if os.path.isfile(t1.file2.path):
                    os.remove(t1.file2.path)
                t1.file2 = None
            
            if 'file3-clear' in self.data:              
                if os.path.isfile(t1.file3.path):
                    os.remove(t1.file3.path)
                t1.file3 = None
    
        if 'file1' in self.files.keys():
            t1.file1 = self.files['file1']
            log.debug(f'self.files: {self.files["file1"]}')
    
        if 'file2' in self.files.keys():
            t1.file2 = self.files['file2']
        
        if 'file3' in self.files.keys():
            t1.file3 = self.files['file3']
            
        t1.save()    
        
        # Enviamos el Mail        
        if okInstance:
            emailMsg = f'update ticket {t1.id}'
            headerEmail = f'Ticket "{t1.id}" Actualizado'          
        else:          
            emailMsg = f'created ticket {t1.id}'
            headerEmail = f'Ticket "{t1.id}" Creado'
    
        EmailThread(registro=t1,msg=emailMsg,header=headerEmail).start()
        EmailThread(attend=True,registro=t1,msg=emailMsg,header=headerEmail).start()
        return t1


class FormEditTicket(ModelForm):
    class Meta:
        model = Tickets    
    
        fields = [
            'register', 'attend', 'estado', 'register_estado', 
            'brief','detail','email','file1','file2', 'file3'
        ]
        labels = {
            'register'        : 'Quien Registro el Issue',
            'attend'          : 'Quien Atiende el Ticket',      
            'brief'           : 'Modulo',
            'estado'          : 'Estado del Ticket',
            'register_estado' : 'Estado Pendiente',
            'detail'          : 'Descripcion del Incidente',
            'email'           : 'Lista de Direcciones de correo',
            'file1'           : 'Archivo 1',
            'file2'           : 'Archivo 2',
            'file3'           : 'Archivo 3' 
        }
        widgets = {
            'detail': Textarea(attrs={
                                    'autofocus': '',
                                    'cols': 40,
                                    'rows': 5,
                                    'title': f'Ingrese un mensaje de hasta {DETAIL_MAX_LEN} '\
                                      'caracteres',
                                    'placeholder': 'Mensaje o Descripcion del Incidente' 
                                })   
        }
    
  
    def is_valid(self,**kwargs):
        """Verifica si los datos cargados para editar el ticket son validos"""
        if not super().is_valid():
            return False

        try:      
            User.objects.get(id=self.data['register'],
                             groups=Group.objects.get(name= GROUPS.client))      
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}> detail: {e}')
            #log.debug(f'No se localizo en la tabla Clientes {self.data["register"]}')  
            self.add_error('register',"El usuario seleccionado no tiene los atributos de Cliente.")    
            return False

        try:      
            Modulos.objects.get(id=self.data['brief'])
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}> detail: {e}')            
            self.add_error('brief', "Seleccione un Modulo de la lista.")
            return False

        modulo:str = self.data.get('detail',None)
        if modulo and not len(modulo):
            self.add_error('detail', "Coloque una descripcion sobre el incidente.")    
            return False
        
        #     'file1'           : 'Archivo 1',
        #     'file2'           : 'Archivo 2',
        #     'file3'           : 'Archivo 3'         
        log.debug(f"Data from Form: => {self.data} | Files: {self.files}") 
        file = self.files.get('file1',None)
        if file and SizeValidator.check_file_size(file):
            self.add_error('file1',
                           f"Archivo supera el maximo soportado {SizeValidator.FILE_SIZE_LBL}.")    
            log.error(f"Archivo {file} supera el maximo soportado {SizeValidator.FILE_SIZE_LBL}.")  
            return False
            
        log.debug(f"Archivo {file} guardado de forma sastifactoria") 
        return True
  
    def save(self,**kwarg)->Tickets:
        """ Metodo que se encarga de actualizar la informacion del ticket sobre BBDD"""        
        try:
            mod = Modulos.objects.get(id=self.data['brief'])
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}> detail: {e}')
            raise ValidationError(f"No tenemos un modulo con el nombre {self.data['brief']}.")
    
        t1:Tickets = kwarg.get('instance',None)
        if t1 is None:
            log.debug(f'No se paso la instancia "instance="')
            return None
    
        asignacion = None
        if t1.attend is None:
            asignacion = 'No'
        else:
            asignacion = f'{t1.attend.programador.username}'
            
        try:
            t1.register = User.objects.get(id=self.data['register'],
                                           groups=Group.objects.get(name=GROUPS.client))      
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}> detail: {e}')
            #log.debug(f'No se localizo en la tabla Clientes {self.data["register"]}')  
            self.add_error('register',"El usuario seleccionado no tiene los atributos necesearios.")    
            return None
    
        try:
            t1.attend = Programador.objects.get(id=self.data['attend'])
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}> detail: {e}')
            t1.attend = None
    
        t1.brief=mod
        t1.detail = self.data['detail']
        t1.email=self.data['email']
        if 'estado' in self.data.keys():
            t1.estado=True
        else:
            t1.estado=False
    
        if 'register_estado' in self.data.keys():
            t1.register_estado=True
        else:
            t1.register_estado=False
            
        if 'file1-clear' in self.data:
            if os.path.isfile(t1.file1.path):
                os.remove(t1.file1.path)
            t1.file1 = None

        if 'file2-clear' in self.data:          
            if os.path.isfile(t1.file2.path):
                os.remove(t1.file2.path)
            t1.file2 = None

        if 'file3-clear' in self.data:          
            if os.path.isfile(t1.file3.path):
                os.remove(t1.file3.path)
            t1.file3 = None
    
        if 'file1' in self.files.keys():
            t1.file1 = self.files['file1']
            log.debug(f'self.files: {self.files["file1"]}')
    
        if 'file2' in self.files.keys():
            t1.file2 = self.files['file2']
        
        if 'file3' in self.files.keys():
            t1.file3 = self.files['file3']

        t1.save()
    
        if t1.attend is not None and asignacion != t1.attend.programador.username \
            and t1.attend.programador.email is not None:
            EmailThread(attend=True,registro=t1,msg=f'Ticket "{t1.id}" Asignado',
                        header=f'Ticket "{t1.id}" Asignado').start()

        EmailThread(registro=t1,msg=f'update ticket {t1.id}',
                    header=f'Ticket "{t1.id}" Actualizado').start()
        return t1


class FormularioRegisterWork(ModelForm):
    tiempo:CharField = CharField(required=False,
                       widget=TextInput(attrs={
                            'autofocus': False,
                            'placeholder': 'HH:MM:SS',
                            'title':'Ingrese el Tiempo que Consumio el trabajo, por defecto '\
                                    'cargara el que tarde en llenar este formulario.'
                          }
                        )
                    )
    class Meta:
        """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un ticket.
        - ticket         Ticket sobre el cual se registrara el trabajo, Modelo Tickets
        - register_work  quien registra el trabajo sobre el ticket en cuestion, Modelo Programador
        - date_creacion  Fecha en la cual se creo el registro del nuevo trabajo.
        - modulo         Modulo sobre el cual se realizo el trabajo.
        - msg            Detalle del trabajo realizado o mensage descriptivo.    
        - file1          Archivo para acompañar el detalle del trabajo realizado.
        - file2          Archivo para acompañar el detalle del trabajo realizado.    
        - tiempo         Tiempo consumido para realizar el trabajo.    
        - date_update    Hora y Fecha de actualizacion del registro.  
        """
        model = RegisterWork
        fields:list[str] = [ 'msg','file1','file2','tiempo']    
        labels:dict = {
            'msg': 'Mensaje, Detalle del trabajo realizado',
            'file1':'Adjuntar Archivo 1',
            'file2':'Adjuntar Archivo 2',
            'tiempo':'Tiempo consumido para realizar el trabajo.'
        }              
        widgets:dict = {
            'msg': Textarea(attrs={
                'autofocus': '',
                'cols': 70,
                'rows':7 ,
                'title': f'Ingrese un mensaje de hasta {DETAIL_MAX_LEN} caracteres',
                'placeholder': 'Mensaje o Descripcion del Incidente' 
            }),
        }
  
    def save(self,**kwargs)->RegisterWork:
        """ Metodo para guardar un registro del tipo RegisterWork mediante un 
        FormularioRegisterWork().

        kwargs
          - ticket
          - register_work        
          - deltatime
          - localtime
          - programmer
          - instance : todos los anteriores menso "deltatime" se descartan      
        """
        lticket:Tickets = kwargs.get('ticket',None)
        registerWork = kwargs.get('register_work',None)    
        # deltatime = arg.get('deltatime',None)
        localtime = kwargs.get('localtime',None)    
        currentAttend = None
        if isinstance(registerWork,Programador):
            currentAttend = registerWork.programador
        else:
            currentAttend = registerWork
    
        t1:RegisterWork = kwargs.get('instance',None)
        programmer:bool = kwargs.get('programmer',False)
        okInstance:bool = False
        if t1 is not None:
            okInstance = True            
            t1.msg = self.data['msg']
            t1.date_update=timezone.now()   
            lticket = t1.ticket
            programmer = t1.programmer
            log.debug(f'Editando Registro {t1}')
        else:
            if lticket is None or currentAttend is None:
                log.debug('Faltan los Parametros => lticket: %s, currentAttend: %s',
                          lticket,currentAttend)
                return None
            
            t1 = RegisterWork(ticket=lticket,date_creacion=timezone.now(),
                              msg = self.data['msg'], date_update=timezone.now(),
                              register_work = currentAttend,
                              programmer = programmer)

        if programmer and len(self.data['tiempo']) != 0:
            t1.tiempo = self.data['tiempo']
        elif localtime is not None:
            deltatime = timezone.now() - localtime
            t1.tiempo = deltatime2time(deltatime)
        else:
            log.debug('No se paso un "localtime" valido y no tenemos el dato Cargado en '\
                      'el Form, no se almacena el registro')
            return None
    
        if okInstance:
            if 'file1-clear' in self.data:
                if os.path.isfile(t1.file1.path):
                    os.remove(t1.file1.path)
                t1.file1 = None
            
            if 'file2-clear' in self.data:
                if os.path.isfile(t1.file2.path):
                    os.remove(t1.file2.path)
                t1.file2 = None
    
        if 'file1' in self.files.keys():
            t1.file1 = self.files['file1']
    
        if 'file2' in self.files.keys():
            t1.file2 = self.files['file2']
        
        lticket.fecha_update = timezone.now()
        lticket.save()
    
        ## Salvamos el objeto
        t1.save()
        EmailThread(registro=t1,msg=f'update ticket {lticket.id}',
                    header=f'Ticket "{lticket.id}" actualizado').start()
    
        ## Consultamos si debemos enviar meil al programador
        if not programmer:
            EmailThread(attend=True,registro=t1,msg=f'update ticket {lticket.id}',
                        header=f'Ticket "{lticket.id}" actualizado').start()
        
        return t1


class FormularioModulos(ModelForm):
    nombre:CharField = CharField(max_length=MODULOS_NOMBRE_MAXLEN,
                                 widget=TextInput(attrs={
                                    'autofocus': True,
                                    'placeholder': 'Modulo',
                                    'title':'Ingrese el Nombre del Modulo'
                                    }
                                ))
    
    class Meta:
        """ Descripcion del modelo 
          * nombre      : Nombre del Modulo.
          * descripcion : Descripcion del Modulo.
        """
        model = Modulos
        fields:list[str] = ['nombre','descripcion']    
        labels:dict = {
            'nombre': 'Nombre del Modulo',
            'descripcion': 'Descripcion del Modulo'
        }        
        widgets:dict = {
            'descripcion': Textarea(attrs={
                'cols': 50,
                'rows':2,
                'placeholder': 'Descripcion',
                'title':'Ingrese la Descripcion del Modulo'
                }), 
        }
  
    def save(self,**kwargs)->Modulos:
        instance:Modulos = kwargs.get('instance',None)
    
        if instance is not None:
            instance.nombre=self.data['nombre']
            instance.descripcion=self.data['descripcion']
            instance.save()  
            return instance
          
        rval = Modulos(nombre=self.data['nombre'], descripcion=self.data['descripcion'])
        rval.save()
        return rval
      
    def is_valid(self,**kwargs)->bool:
        """ method for validation in form """        
        edit:bool = kwargs.get("edit",False)
        valid:bool = super().is_valid()    
        mod:QuerySet[Modulos] = None
        try:
            mod = Modulos.objects.filter(nombre=self.data['nombre'])
        except Exception as e:
            log.error('Exception %s in query for Modulos nombre=%s',
                      type(e).__name__,self.data["nombre"])
    
        if not edit and mod is not None and len(mod) > 0:
            self.add_error('nombre', 
                           f"Ya Tenemos un Modulo con este Nombre: {self.data['nombre']}.")
            return False

        elif not edit and not valid:
            return False
                
        return True


class FormularioDesarrollo(ModelForm):
    class Meta:
        '''
          registro : quien registra el pedido de un nuevo desarrollo
          empresa : Para que empresa, peude ser interno (opcionale)
          asistente : quien esta trabajando actualmente en el desarrollo, Modelo Programador
          descripcion : Descripcion del desarrollo a realizar.
          modulo : Modulo si es que este esta definido, se puede asignar luego.
          email : Lista de meil a quien notificar los trabajos registrados sobre el desarrollo
          fecha_creacion : Fecha en la cual se creo el issue.
          fecha_actualizacion : Fecha de la ultima actualizacion (en la cual se registro un nuevo trabajo )
          fecha_cierre : Fecha de cierre del Desarrollo (None, valor por defecto)
          file1 : Archivo uno para acompañar el detalle del Desarrollo
          file2 : Archivo dos para acompañar el detalle del Desarrollo
          file3 : Archivo dos para acompañar el detalle del Desarrollo
          estado : Estado Actual del issue    
        '''
        model = Desarrollo

        fields:list[str] = [
            'empresa','asistente','modulo',
            'descripcion','email','file1',
            'file2', 'file3' 
        ]
    
        labels:dict = {
            'empresa': 'Para que Empresa',
            'asistente': 'Asistente ( que participará en el desarrollo) ',
            'modulo' : ' Modulo (si es que este esta definido)',
            'email': 'Lista de Direcciones de correo',
            'file1': 'Adjuntar Archivo 1',
            'file2': 'Adjuntar Archivo 2',
            'file3': 'Adjuntar Archivo 3' 
        }
    
        help_texts:dict = {
            'empresa': 'Opcional, puede ser desarrollo interno',
            'asistente': 'Opcional, puede establecerlo luego',
            'modulo' : 'Opcional'
        }
        
        widgets:dict = {            
            'descripcion': Textarea(attrs={
                    'autofocus': '',
                    'cols': 50,
                    'rows': 10,
                    'title': f'Ingrese una descripcion de hasta {DETAIL_MAX_LEN} caracteres',
                    'placeholder': 'Descripción del Desarrollo a realizar' 
            })
        }
  
    def save(self,**kwargs)->Desarrollo:
        """ save instance  Desarrollo
            - instance instancia del objeto Desarrollo
            - register quien registro
        """    
        reg:User = kwargs.get('register',None)
        if reg is None:
            log.debug("Estamos intentado guardar un registro sin el campo 'register'.")
            return None

        t1:Desarrollo = Desarrollo(registro = reg, descripcion = self.data['descripcion'],
                                   email=self.data['email'])

        if 'empresa' in self.data.keys():
            try:
                t1.empresa = Empresa.objects.get(id=self.data['empresa'])
            except:
                t1.empresa = None
    
        if 'asistente' in self.data.keys():
            try:
                t1.asistente = Programador.objects.get(id=self.data['asistente'])
            except:
                t1.asistente = None
        
        if 'modulo' in self.data.keys():
            try:
                t1.modulo = Modulos.objects.get(id=self.data['modulo'])
            except:
                t1.modulo = None

        if 'file1' in self.files.keys():
            t1.file1 = self.files['file1']
              
        if 'file2' in self.files.keys():
            t1.file2 = self.files['file2']
        
        if 'file3' in self.files.keys():
            t1.file3 = self.files['file3']
            
        t1.save()
        
        # Enviamos el Meil        
        emailMsg = f'created pedido de Desarrollo {t1.id}'
        headerEmail = f'Pedido de Desarrollo "{t1.id}" Creado'
        EmailThread(registro=t1,msg=emailMsg,header=headerEmail).start()
        ## Envio de email a attend
        if t1.asistente is not None:
            emailMsg = f'Se Asigno el Desarrollo {t1.id}'
            headerEmail = f'Desarrollo "{t1.id}" Asignado'   
            EmailThread(attend=True,registro=t1,msg=emailMsg,header=headerEmail).start()
        
        return t1


class FormularioEditDesarrollo(ModelForm):
    '''
    registro : quien registra el pedido de un nuevo desarrollo
    empresa : Para que empresa, peude ser interno (opcionale)
    asistente : quien esta trabajando actualmente en el desarrollo, Modelo Programador
    modulo      : Modulo si es que este esta definido, se puede asignar luego.
    descripcion : Descripcion del desarrollo a realizar.
    email : Lista de meil a quien notificar los trabajos registrados sobre el desarrollo
    fecha_creacion : Fecha en la cual se creo el issue.
    <> fecha_actualizacion : Fecha de la ultima actualizacion (en la cual se registro un 
                             nuevo trabajo )
    <> fecha_cierre : Fecha de cierre del Desarrollo (None, valor por defecto)
    file1 : Archivo uno para acompañar el detalle del Desarrollo
    file2 : Archivo dos para acompañar el detalle del Desarrollo
    file3 : Archivo dos para acompañar el detalle del Desarrollo
    estado : Estado Actual del issue    
    '''
    registro:ModelChoiceField = ModelChoiceField(
        empty_label="Todos",
        label = 'Quien Registra el Pedido',
        queryset = User.objects.filter(is_staff=True),        
        ## XXX fail in `python3 manage.py makemigrations`
        #queryset = User.objects.filter(groups=Group.objects.get(name=GROUPS.admin)) | \
        #    User.objects.filter(is_superuser=True),
        required=False
    )

    class Meta:
        model = Desarrollo
        fields:list[str] = [
            #'registro',
            'empresa','asistente','modulo','descripcion',
            'email','fecha_creacion','estado','file1','file2', 'file3' 
        ]
    
        labels:dict = {
            #'registro' : 'Quien Registra el Pedido',
            'empresa': 'Para que Empresa',
            'fecha_creacion' : 'Fecha de Creacion',
            'estado' : 'Estado Actual',
            'asistente': 'Asistente Actual',
            'modulo' : ' Modulo si es que este esta definido',
            'email': 'Lista de Direcciones de correo',
            'file1': 'Adjuntar Archivo 1',
            'file2': 'Adjuntar Archivo 2',
            'file3': 'Adjuntar Archivo 3' 
        }

        widgets:dict = {
            'descripcion': Textarea(attrs={
                'autofocus': '',
                'cols': 50,
                'rows': 10,
                'title':f'Ingrese una descripcion de hasta {DETAIL_MAX_LEN} caracteres',
                'placeholder': 'Descripcion del Desarrollo' 
            })
        }
  
    # def is_valid(self)->bool:
    #     """ method to validation form """      
    #     if not super().is_valid():
    #         return False
    # 
    #     return True
  
    def save(self,**kwargs)->Desarrollo:
        """ kwargs
            - instance instancia del objeto Desarrollo
            - register quien registro
        """    
        t1:Desarrollo = kwargs.get('instance',None)
        reg:User = kwargs.get('register',None)
        okInstance:bool = False        
        lempresa:Empresa = None
        lasistente:Programador = None
        lestado:bool = False
        lmodulo:Modulos = None
        asignacion:bool = False
        
        if 'estado' in self.data.keys() and self.data['estado'] == 'on':
            lestado = True
    
        if 'empresa' in self.data.keys():
            try:
                lempresa = Empresa.objects.get(id=self.data['empresa'])
            except:
                lempresa = None
    
        if 'asistente' in self.data.keys():
            try:
                lasistente = Programador.objects.get(id=self.data['asistente'])
            except:
                lasistente = None
        
        if 'modulo' in self.data.keys():
            try:
                lmodulo = Modulos.objects.get(id=self.data['modulo'])
            except:
                lmodulo = None
        
        
        if t1 is not None:          
            t1.empresa = lempresa
            if t1.asistente != lasistente:
                asignacion = True

            t1.asistente = lasistente
            t1.estado = lestado
            t1.modulo = lmodulo

            if 'descripcion' in self.data.keys():
                t1.descripcion = self.data['descripcion']

            if 'email' in self.data.keys():
                t1.email=self.data['email']

            okInstance = True
        else:
            ## creamos el registro con los datos obligatorios
            if reg is None:
                log.debug("Estamos intentado guardar un registro sin el campo 'register'.")
                return None

            t1 = Desarrollo(registro=reg, descripcion=self.data['descripcion'],
                            email=self.data['email'])                
            asignacion = True
            t1.empresa = lempresa
            t1.asistente = lasistente
            t1.modulo = lmodulo
       
        if okInstance:
            if 'file1-clear' in self.data:              
                if os.path.isfile(t1.file1.path):
                    os.remove(t1.file1.path)
                t1.file1 = None

            if 'file2-clear' in self.data:
                if os.path.isfile(t1.file2.path):
                    os.remove(t1.file2.path)
                t1.file2 = None

            if 'file3-clear' in self.data:              
                if os.path.isfile(t1.file3.path):
                    os.remove(t1.file3.path)
                t1.file3 = None

        if 'file1' in self.files.keys():
            t1.file1 = self.files['file1']
    
        if 'file2' in self.files.keys():
            t1.file2 = self.files['file2']

        if 'file3' in self.files.keys():
            t1.file3 = self.files['file3']

        ## Salvamos el objeto
        t1.save()

        # Enviamos el Meil        
        if okInstance:
            emailMsg = f'update Desarrollo {t1.id}'
            headerEmail = f'Desarrollo "{t1.id}" Actualizado'
        else:
            emailMsg = f'created pedido de Desarrollo {t1.id}'
            headerEmail = f'Pedido de Desarrollo "{t1.id}" Creado'    
            
        EmailThread(registro=t1,msg=emailMsg,header=headerEmail).start()
        if lasistente is not None and asignacion:
            emailMsg = f'Se Asigno el Desarrollo {t1.id}'
            headerEmail = f'Desarrollo "{t1.id}" Asignado'   
            EmailThread(attend=True,registro=t1,msg=emailMsg,header=headerEmail).start()

        return t1


class FormularioSetDesarrollo(ModelForm):
    '''      
    empresa : Para que empresa, peude ser interno (opcionale)
    asistente : quien esta trabajando actualmente en el desarrollo, Modelo Programador      
    modulo : Modulo si es que este esta definido, se puede asignar luego.
    '''
    class Meta:
        model = Desarrollo
        fields:list[str] = ['empresa','asistente','modulo']    
        labels:dict = {
            'empresa': 'Para que Empresa',
            'modulo' : ' Modulo si es que este esta definido',
            'asistente': 'Asistente Actual'
        }
    
  
    #def is_valid(self)->bool:
    #    """ mathod to validity """      
    #    if not super().is_valid():
    #        return False
    #    return True
  
    def save(self,**kwargs)->Desarrollo:
        """ kwargs
        - instance instancia del objeto Desarrollo
        """    
        instancia:Desarrollo = kwargs.get('instance',None)
        if instancia is None:
            log.debug("No se paso 'instance' para editar.")
            return None

        lempresa:Empresa = None
        lasistente:Programador = None
        lmodulo:Modulos = None

        if 'empresa' in self.data.keys():
            try:
                lempresa = Empresa.objects.get(id=self.data['empresa'])
            except Exception as e:
                log.error(f'Exception<{type(e).__name__}> detail: {e}')
                lempresa = None
    
        if 'asistente' in self.data.keys():
            try:
                lasistente = Programador.objects.get(id=self.data['asistente'])
            except Exception as e:
                log.error(f'Exception<{type(e).__name__}> detail: {e}')
                lasistente = None
    
        if 'modulo' in self.data.keys():
            try:
                lmodulo= Modulos.objects.get(id=self.data['modulo'])
            except Exception as e:
                log.error(f'Exception<{type(e).__name__}> detail: {e}')
                lmodulo = None 
        
        instancia.empresa = lempresa
        asignacion:bool = instancia.asistente != lasistente        
        instancia.asistente = lasistente
        instancia.modulo = lmodulo
        instancia.save()    
        
        #  Enviamos el Meil
        emailMsg = f'Nuevo Mensaje para Desarrollo {instancia.id}'
        headerEmail = f'Desarrollo "{instancia.id}" Actualizado'    
        EmailThread(registro=instancia,msg=emailMsg,header=headerEmail).start()

        if lasistente is not None and asignacion:
            emailMsg = f'Se Asigno el Desarrollo {instancia.id}'
            headerEmail = f'Desarrollo "{instancia.id}" Asignado'   
            EmailThread(attend=True,registro=instancia,msg=emailMsg,header=headerEmail).start()
        
        return instancia


class FormularioRegistroTrabajo(ModelForm):    
    tiempo:TimeField = TimeField(required=False,
                                widget=TextInput(attrs={
                                    'autofocus': False,
                                    'placeholder': 'HH:MM:SS',
                                    'title':'Ingrese el Tiempo que Consumio el trabajo, '\
                                            'por defecto cargara el que tarde en llenar '\
                                                'este formulario.'
                                }))
    class Meta:
        """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un ticket.
          <> desarrollo      : 
          <> fecha_creacion  : Fecha en la cual se creo el registro del nuevo trabajo.    
          <> date_update     : Hora y Fecha de actualizacion del registro.
          <> programmer      : True | False , especifica si es programador quien registra
          <> register_work   : quien registra el trabajo sobre el ticket en cuestion, Modelo Programador          
          * msg             : Detalle del trabajo realizado o mensage descriptivo.    
          * file1           : Archivo para acompañar el detalle del trabajo realizado.
          * file2           : Archivo para acompañar el detalle del trabajo realizado.    
          * tiempo          : Tiempo consumido para realizar el trabajo.       
        """
        model = RegistroTrabajo
        fields:list[str] = ['msg','file1','file2','tiempo']    
        labels:dict = {
            'msg': 'Mensaje, Detalle del trabajo realizado',
            'file1':'Adjuntar Archivo 1',
            'file2':'Adjuntar Archivo 2',
            'tiempo':'Tiempo consumido para realizar el trabajo.'
        }        
        widgets:dict = {
            'msg': Textarea(attrs={
                    'autofocus': '',
                    'cols': 70,
                    'rows':7,
                    'title': f'Ingrese un mensaje de hasta {DETAIL_MAX_LEN} caracteres',
                    'placeholder': 'Mensaje o detalle del trabajo realizado' 
                }), 
        }
    
    def save(self,**kwargs)->RegistroTrabajo:
        """ Metodo para guardar un registro del tipo RegisterWork mediante un FormularioRegisterWork()
        kwargs
        - desarrollo
        - register_work        
        - deltatime
        - localtime
        - programmer
        - instance : todos los anteriores menso "deltatime" se descartan      
        """
        develop:Desarrollo = kwargs.get('desarrollo',None)
        registerWork = kwargs.get('register_work',None)    
        localtime = kwargs.get('localtime',None)    
        currentAttend = None
        
        if isinstance(registerWork,Programador):
            currentAttend = registerWork.programador
        else:
            currentAttend = registerWork

        programmer:bool = kwargs.get('programmer',False)
        okInstance:bool = False

        if develop is None or currentAttend is None:
            log.debug('Faltan los Parametros => lticket: %s, currentAttend: %s',
                      develop,currentAttend)
            return None
        
        t1 = RegistroTrabajo(desarrollo=develop,fecha_creacion=timezone.now(),
                            msg = self.data['msg'], date_update=timezone.now(),
                            register_work = currentAttend, programmer = programmer)    

        if programmer and len(self.data['tiempo']) > 0:
            t1.tiempo = self.data['tiempo']
            log.debug(f'self.data["tiempo"] {self.data["tiempo"]}')

        elif localtime is not None:
            deltatime = timezone.now() - localtime
            t1.tiempo = deltatime2time(deltatime)           
            log.debug('timezone.now(): %s localtime: %s deltatime : %s',
                      timezone.now(),localtime,deltatime)

        else:
            log.debug('No se paso un "localtime" valido y ademas no tenemos el dato Cargado '\
                      'en el Form, no se almacena el registro')
            return None
        
        log.debug(f't1.tiempo {t1.tiempo}')    
        if okInstance:
            if 'file1-clear' in self.data:              
                if os.path.isfile(t1.file1.path):
                    os.remove(t1.file1.path)
                t1.file1 = None

            if 'file2-clear' in self.data:                
                if os.path.isfile(t1.file2.path):
                    os.remove(t1.file2.path)
                t1.file2 = None
    
        if 'file1' in self.files.keys():
            t1.file1 = self.files['file1']
    
        if 'file2' in self.files.keys():
            t1.file2 = self.files['file2']

        ## actualizamos la el registro develop
        develop.fecha_actualizacion = timezone.now()
        develop.save()    
        t1.save()

        EmailThread(registro=t1,msg=f'update development order {develop.id}',
                    header=f'Orden de Desarrollo "{develop.id}" Actualizado').start()

        if not programmer:
            EmailThread(attend=True,registro=t1,msg=f'development order {develop.id}',
                        header=f'Orden de Desarrollo "{develop.id}" actualizado').start()

        return t1


class FormularioEditRegistroTrabajo(ModelForm):
    tiempo:TimeField = TimeField(required=False,
                                widget=TextInput(attrs={
                                    'autofocus': False,
                                    'placeholder': 'HH:MM:SS',
                                    'title':'Ingrese el Tiempo que Consumio el trabajo, por '\
                                            'defecto cargara el que tarde en llenar este '\
                                            'formulario.'
                                    }
                                ))
    class Meta:
        """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un ticket.
          <> desarrollo      : 
          <> fecha_creacion  : Fecha en la cual se creo el registro del nuevo trabajo.    
          <> date_update     : Hora y Fecha de actualizacion del registro.
          <> programmer      : True | False , especifica si es programador quien registra
          <> register_work   : quien registra el trabajo sobre el ticket en cuestion, Modelo Programador          
          * msg             : Detalle del trabajo realizado o mensage descriptivo.    
          * file1           : Archivo para acompañar el detalle del trabajo realizado.
          * file2           : Archivo para acompañar el detalle del trabajo realizado.    
          * tiempo          : Tiempo consumido para realizar el trabajo.       
        """
        model = RegistroTrabajo
        fields:list[str] = ['msg','file1','file2','tiempo']
        labels:dict = {
            'msg': 'Mensaje, Detalle del trabajo realizado',
            'file1':'Adjuntar Archivo 1',
            'file2':'Adjuntar Archivo 2',
            'tiempo':'Tiempo consumido para realizar el trabajo.'
        }        
        widgets:dict = {
            'msg': Textarea(attrs={
                    'autofocus':'',
                    'cols': 70,
                    'rows':7 ,
                    'title':f'Ingrese un mensaje de hasta {DETAIL_MAX_LEN} caracteres',
                    'placeholder': 'Mensaje o detalle del trabajo realizado'
                 }),
        }
    
    def save(self,**kwargs)->RegistroTrabajo:
        """ Metodo para guardar un registro del tipo RegisterWork mediante un 
        FormularioRegisterWork()

        kwargs
        - instance
        - deltatime
        - localtime        
        """
        instancia:RegistroTrabajo = kwargs.get('instance',None)
        if instancia is None:
            log.debug(f'Faltan el Parametro "instance"')
            return None    
        
        localtime = kwargs.get('localtime',None)
        instancia.msg = self.data['msg']
        instancia.date_update=timezone.now()    
        log.debug(f'Editando Registro {instancia}') 

        if instancia.programmer and len(self.data['tiempo']) > 0:
            instancia.tiempo = self.data['tiempo']

        elif localtime is not None:
            deltatime = timezone.now() - localtime
            instancia.tiempo = deltatime2time(deltatime) 

        elif localtime is None and not instancia.programmer:
            instancia.tiempo = deltatime2time(timezone.now() - instancia.date_update)

        else:
            log.debug('No se paso un "localtime" valido y ademas no tenemos el dato Cargado en el '\
                      'Form, no se almacena el registro')
            return  None         
    
        if 'file1-clear' in self.data:          
            if os.path.isfile(instancia.file1.path):
                os.remove(instancia.file1.path)
            instancia.file1 = None

        if 'file2-clear' in self.data:          
            if os.path.isfile(instancia.file2.path):
                os.remove(instancia.file2.path)
            instancia.file2 = None
        
        if 'file1' in self.files.keys():
            instancia.file1 = self.files['file1']
    
        if 'file2' in self.files.keys():
            instancia.file2 = self.files['file2']

        instancia.desarrollo.fecha_actualizacion = timezone.now()
        instancia.desarrollo.save()        
        instancia.save()
        
        ## enviamsos los meil    
        EmailThread(registro=instancia,msg=f'update development order {instancia.desarrollo.id}',
                    header=f'Orden de Desarrollo "{instancia.desarrollo.id}" Actualizado').start()
    
        
        if not instancia.programmer:
            EmailThread(attend=True,registro=instancia,
                        msg=f'development order {instancia.desarrollo.id}',
                        header=f'Orden de Desarrollo "{instancia.desarrollo.id}" actualizado'
                        ).start()
