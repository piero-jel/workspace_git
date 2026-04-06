# buil-in import
from re import match as re_match
from logging import getLogger,Logger

# framework import
#from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.forms import (
    Form, CharField, TextInput, EmailField,PasswordInput, ModelChoiceField,
    ChoiceField, ModelChoiceField
)

# Project Modules import
from Ticket.models import Tickets,Modulos
from Login.models import Empresa,Programador,User
from Login.constants import GROUPS
from Login.contexto import EmailThread
from config.settings import (FORM_TITLE, FORM_PLACEHOLDER,PHONE_NUMBER_PATTERN)


log:Logger = getLogger('administrator')


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','telefono','email','empresa']
        widgets = {
            'username':   TextInput(attrs={ 'autofocus': False ,
                                           'placeholder': FORM_PLACEHOLDER.username,
                                           'title':FORM_TITLE.username}),
    
            'first_name': TextInput(attrs={ 'autofocus': False ,
                                           'placeholder': FORM_PLACEHOLDER.username,
                                           'title':FORM_TITLE.firstname}),
    
            'last_name':  TextInput(attrs={ 'autofocus': False ,
                                           'placeholder': FORM_PLACEHOLDER.lastname,
                                           'title':FORM_TITLE.lastname}),
    
            'telefono':   TextInput(attrs={ 'autofocus': False ,
                                           'placeholder': FORM_PLACEHOLDER.telephone,
                                           'title':FORM_TITLE.telephone}),
    
            'email':      TextInput(attrs={ 'autofocus': False ,
                                           'placeholder': FORM_PLACEHOLDER.email,
                                           'title':FORM_TITLE.email})        
        }
    
    def is_valid(self)->bool:
        # validamos la base, duplicidad de username `model = User`
        if not super().is_valid():
            return False
        
        empresa = self.data.get('empresa',None)
        log.debug(f'{type(self).__name__}::is_valid() empresa: {empresa}')
        if empresa and len(empresa)==0:
            self.add_error('empresa', f"Seleccione Una Empresa de la lista")
            return False

        telefono:str = self.data.get('telefono',None)
        if telefono and not re_match(PHONE_NUMBER_PATTERN,telefono):
            self.add_error('telefono', f"Numero de telefono invalido.")
            return False
        

        return True
    

class FormularioCheckUser(Form):
    """ Formulario para check de contraseña """
    password:CharField = CharField(label='Contraseña',min_length=5, max_length=30,
                                   widget=PasswordInput(render_value=False))
    
    def check_pass(self,user=None)->bool:
        """Metodo que se encarga de verificar el pass del user, pado previo 
        verifica si el form es valido
        """
        if not self.is_valid():
            log.info('Formulario no valid')  
            return False
        
        if user is None:
            log.info('No se paso un user valido')  
            return False
            
        return check_password(password=self.data["password"],encoded=user.password)


class FormEditUser(Form):
    username:CharField = CharField(required=True,label='Nombre Usuario', max_length=150,
                                   widget=TextInput(attrs={
                                      'autofocus': True,
                                      'placeholder':FORM_PLACEHOLDER.username,
                                      'title':FORM_TITLE.username} ))
  
    first_name:CharField = CharField(required = False,label='Nombre', max_length=30,
                                    widget=TextInput(attrs={
                                       'autofocus': True,
                                       'placeholder':FORM_PLACEHOLDER.firstname,
                                       'title':FORM_TITLE.firstname} ))
  
    last_name:CharField = CharField(required = False,label='Apellido', max_length=150,
                                    widget=TextInput(attrs={
                                       'autofocus':True,
                                       'placeholder': FORM_PLACEHOLDER.lastname,
                                       'title':FORM_TITLE.lastname} ))
  
    telefono:CharField = CharField(required = False,label='Numero Telefono', max_length=50,
                                   widget= TextInput(attrs={
                                      'autofocus': True ,
                                      'placeholder':FORM_PLACEHOLDER.telephone,
                                      'title':FORM_TITLE.telephone} ))
  
    email:EmailField = EmailField(required = False,label='Direccion de Correo',
                                  widget=TextInput(attrs={
                                     'autofocus': True ,
                                     'placeholder':FORM_PLACEHOLDER.email,
                                     'title':FORM_TITLE.email} ))

    #empresa:ModelChoiceField = ModelChoiceField(empty_label="----",
    #                                label = 'Empresa',
    #                                queryset=Empresa.objects.all(),
    #                                required=False,
    #                                #help_text='Seleccione el Nombre de la Empresa'
    #                            )    
  
    def save(self,**kwargs):
        # log.debug(f'self.data {self.data}')
        instance:User = kwargs.get('instance',None)
        if instance is None:
            log.debug(f'Falta la instance donde almacenar el form')
            return 
        instance.username = self.data['username']
        instance.first_name = self.data['first_name']
        instance.last_name = self.data['last_name']
        instance.telefono = self.data['telefono']
        instance.email = self.data['email']
        instance.save()
        ## add emvio de email cunaod se edite un usuario
        EmailThread(registro=instance,msg=f'update user {instance}',
                    header=f'User "{instance}" Actualizado').start()
  
    def is_valid(self,**kwargs)->bool:
        # data = self.data
        instance = kwargs.get('instance',None)        
        if not super().is_valid():
            return False
        
        telefono:str = self.data.get('telefono',None)
        if telefono and not re_match(PHONE_NUMBER_PATTERN,telefono):
            self.add_error('telefono', f"Numero de telefono invalido.")
            return False      
        
        if instance is None or self.data['username'] == instance.username:
            return True
    
        luser = None
        try:
            luser = User.objects.filter(username=self.data['username'])
        except:
            luser = None
            log.debug(f'Fallo la query: User.objects.filter(username={self.data["username"]})')
    
        if luser is None:
            self.add_error('username',
                           f"Fallo la verificacion para Nombre de usuario:{self.data['username']}.")
            
            log.error(f"Fallo la quey para verificar el Nombre de usuario: {self.data['username']}.")
            return False
        
        if len(luser) == 0:
            return True
        
        self.add_error('username',
                        f"Ya tenemos registrado un Nombre de Usuario <{self.data['username']}>.")
        return False


class FormEditClient(Form):  
    first_name:CharField = CharField(required = False,label='Nombre', max_length=30,
                                    widget=TextInput(attrs={
                                       'autofocus': True,
                                       'placeholder':FORM_TITLE.firstname,
                                       'title':FORM_TITLE.firstname} ))
  
    last_name:CharField = CharField(required = False,label='Apellido', max_length=150,
                                    widget=TextInput(attrs={
                                       'autofocus':True,
                                       'placeholder': FORM_PLACEHOLDER.lastname,
                                       'title':FORM_TITLE.lastname} ))
  
    telefono:CharField = CharField(required = False,label='Numero Telefono', max_length=50,
                                   widget= TextInput(attrs={
                                      'autofocus': True ,
                                      'placeholder':FORM_PLACEHOLDER.telephone,
                                      'title':FORM_TITLE.telephone} ))
  
    email:EmailField = EmailField(required = False,label='Direccion de Correo',
                                  widget=TextInput(attrs={
                                     'autofocus': True ,
                                     'placeholder':FORM_PLACEHOLDER.email,
                                     'title':FORM_TITLE.email} ))

  
    def save(self,**kwargs)->User:
        # log.debug(f'self.data {self.data}')
        instance:User = kwargs.get('instance',None)
        if instance is None:
            return None
        
        instance.first_name = self.data['first_name']
        instance.last_name = self.data['last_name']
        instance.telefono = self.data['telefono']
        instance.email = self.data['email']
        instance.save()

        ## add emvio de email cunaod se edite un usuario
        EmailThread(registro=instance,msg=f'update user {instance}',
                    header=f'User "{instance}" Actualizado').start()
  
    def is_valid(self)->bool:
        """ realiza verificaciones sobre los campos cargados"""
        if not super().is_valid():
            return False
        
        telefono:str = self.data.get('telefono',None)
        if telefono is not None and not re_match(PHONE_NUMBER_PATTERN,telefono):
            self.add_error('telefono', f"Numero de telefono invalido.")
            return False      
        
        return True    


TICKET_STATUS_CHOICE:list[tuple] = [
    ('all'     , 'Todos'),
    ('open'    , 'Abiertos'),
    ('pending' , 'Pendientes'),
    ('close'   , 'Cerrados')
]

class FormSearchTicket(Form):
    """
      * ticketStatus
      * ticketAsignacion
      * ticketModulo
    """ 
    status:ChoiceField = ChoiceField(
        label = 'Estado Ticket',
        choices=TICKET_STATUS_CHOICE,
        required = False 
    )
  
    module:ModelChoiceField = ModelChoiceField(
        empty_label="Todos",label = 'Modulo',
        queryset=Modulos.objects.all(),
        required=False
    )  
    
    company:ModelChoiceField = ModelChoiceField(
        empty_label="Todos",
        label = 'Empresa',
        queryset=Empresa.objects.all(),
        required=False
    ) 
    
    # 'to_app_name', 'to_model_name', 'foreign_key_app_name', 'foreign_key_model_name', and 'foreign_key_field_name'
    # 'to_app_name' and 'to_model_name'
    #cliente:ChainedModelChoiceField = ChainedModelChoiceField(        
    #    to_app_name='Login',             # El nombre de tu app donde esta el Modelo User
    #    to_model_name='User',            # Nombre del modelo que se va a listar
    #    foreign_key_app_name='Login',     # Nombre de la app donde está el modelo 'User'
    #    #model_name='User',               # El nombre del modelo destino
    #    foreign_key_model_name='User',    # Nombre del modelo que quieres listar
    #    foreign_key_field_name='empresa', # El nombre de la FK en el modelo 'User' que apunta a 'empresa'
    #
    #    chained_field='company',         # El nombre del campo anterior en ESTE formulario
    #    chained_model_field='Empresa',   # El nombre de la FK en el modelo 'User'
    #    show_all=False,
    #    auto_choose=True,
    #    sort=True
    #)
    cliente:ModelChoiceField = ModelChoiceField(
        empty_label="Todos",
        label = 'Cliente',
        queryset=User.objects.filter(is_staff=False),
        ## XXX fail in `python3 manage.py makemigrations`
        #queryset=User.objects.filter(groups=Group.objects.get(name=GROUPS.client)),
        required=False
    )
    
    programador:ModelChoiceField = ModelChoiceField(
        empty_label="Todos",label='Asistente Actual',
        queryset=Programador.objects.all(),
        required=False
    )
    
    #def ticket_for_company(self,company_id:str|int)->tuple[QuerySet[User],QuerySet[Tickets]]:
    def ticket_for_company(self,company_id:str|int,
                           cliente_id:str|int = None,query_set:dict=None,
                           update_fields:bool=False)->QuerySet[Tickets]:
        """ """
        if isinstance(company_id,str):
            company_id = int(company_id)

        employees:QuerySet[User] = None
        company:Empresa = None
        try:
            company = Empresa.objects.get(id=company_id)
        except Exception as e:
            log.error('Exception<%s>, Try get Empresa id <>. Detail: %s.',
                      type(e).__name__,company_id,e)
            return []

        if cliente_id is None:
            ret:list[Tickets] = []
            try:
                employees = User.objects.filter(empresa=company)
                for emp in employees:
                    ret.extend(Tickets.objects.filter(register=emp))
            except Exception as e:
                log.error('Exception<%s>, try get User Employees list. Detail: %s.',
                          type(e).__name__,e)
                return []
            
            if update_fields:
                self.update_fields('cliente','Cliente',employees)

            return ret
        
        try:
            if update_fields:
                employees = User.objects.filter(empresa=company)

            query_set['register'] = User.objects.get(id = int(cliente_id),empresa=company)
        except Exception as e:
            log.error('Exception<%s>, Cliente<%s> no pertenece a la Empresa<%s> detail: %s',
                        type(e).__name__,cliente_id,company_id,e)
            return self.ticket_for_company(company_id,update_fields=update_fields)

        if update_fields:
            self.update_fields('cliente','Cliente',employees)            
        return Tickets.objects.filter(**query_set)
    
    def update_fields(self,field_name:str,label:str,queryset:QuerySet,initial:bool=True)->None:
        """ upadete fields in form
        - field_name:str      nombre del campo, con el cual se definio
        - label:str           etiqueta que acompaña al campo sobre le form
        - queryset:QuerySet   listado de item, resultado de una query
        """
        if field_name not in self.fields or len(queryset)<1:
            log.debug('%s::update_fields() Query set %s | %s in fields %s',
                      type(self).__name__,queryset,field_name,field_name in self.fields)
            return
        
        if initial:
            self.fields[field_name] = ModelChoiceField(
                empty_label="Todos",
                label = label,
                queryset=queryset,
                #required=False,
                initial=queryset[0].id
            )
        else:
            self.fields[field_name] = ModelChoiceField(
                empty_label="Todos",
                label = label,
                queryset=queryset,
                required=False
            )
        
    
    #def update_form(self,**kwargs)->FormSearchTicket:
    def update_form(self,**kwargs)->Form:
        """ Metodo para actualizar el formulario en funcion de un post lanzado por una seleccion
        en un despliegue list
        kwargs:
            - company : string con el id de la compania seleccionada
        """
        company_id:str = kwargs.get('company',None)
        initial:bool = True
        if company_id:            
            try:
                company_id = int(company_id)
                company = Empresa.objects.get(id=company_id)
                employees = User.objects.filter(empresa=company)
                if len(employees) == 0:
                    employees = User.objects.filter(groups=Group.objects.get(name=GROUPS.client))
                    initial = False
                    log.debug('%s::update_form() la empresa selaccionada "%s", no posee Empleados.',
                              type(self).__name__,company)

                    self.add_error('company',
                                   f"La empresa selaccionada '{company}', no posee Empleados aun.")
                    #messages.error(f"La empresa selaccionada '{company}', no posee Empleados aun.")

                self.update_fields('cliente','Cliente',employees,initial=initial)
            except Exception as e:
                log.error('Exception<%s>, try get User Employees list. Detail: %s.',
                          type(e).__name__,e)
            
            return self
        
        
        return self

    def get_queryset(self,tickets:QuerySet[Tickets])->QuerySet[Tickets]:
        """ """
        status:str = self.data.get('status',None)
        module_id:int = self.data.get('module',None)
        company_id:int = self.data.get('company',None)
        cliente_id:int = self.data.get('cliente',None)
        programador_id:int = self.data.get('programador',None)

        #log.debug(f"{type(self).__name__}::get_queryset() data:{self.data}")
        #log.debug(f"{type(self).__name__}::get_queryset() status:{status}")
        #log.debug(f"{type(self).__name__}::get_queryset() module_id:{module_id}")
        #log.debug(f"{type(self).__name__}::get_queryset() company_id:{company_id}")
        #log.debug(f"{type(self).__name__}::get_queryset() cliente_id:{cliente_id}")
        #log.debug(f"{type(self).__name__}::get_queryset() programador_id:{programador_id}")

        query_set:dict = {}
        if status != 'all':
            if status == 'open':
                query_set['estado'] = True
                query_set['register_estado'] = True

            elif status == 'pending':
                query_set['estado'] = True
                query_set['register_estado'] = False
            elif status == 'close' :
                query_set['estado'] = False
                query_set['register_estado'] = False

        if module_id:
            try:
                query_set['brief'] = Modulos.objects.get(id = int(module_id))                
            except Exception as e:
                log.error(f'Exception<{type(e).__name__}>, detail: {e}')
        
        if programador_id:
            try:
                query_set['attend'] = Programador.objects.get(id = int(programador_id))
            except Exception as e:
                log.error(f'Exception<{type(e).__name__}>, detail: {e}')

        if cliente_id:
            if not company_id:
                try:
                    query_set['register'] = User.objects.get(id = int(cliente_id))
                except Exception as e:
                    log.error(f'Exception<{type(e).__name__}>, detail: {e}')
            else:
                return self.ticket_for_company(company_id,cliente_id,query_set,update_fields=True)                

        elif company_id:
            return self.ticket_for_company(company_id,update_fields=True)

        ret:QuerySet[Tickets] = None
        try:
            ret = Tickets.objects.filter(**query_set)

        except Exception as e:
            log.error(f'Exception<{type(e).__name__}>, detail: {e}')
            return tickets
        
        log.debug(f"{type(self).__name__}::get_queryset() query_set:{query_set}")
        return ret
    