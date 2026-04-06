# buil-in import
from re import match as re_match
from logging import getLogger,Logger

# framework import
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,UsernameField,AuthenticationForm
)
from django.forms import (Form, CharField, TextInput, EmailField,Textarea, ModelForm, PasswordInput)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Project Modules import
from Login.models import User, Empresa
#from Login.contexto import EmailThread
from config.settings import (FORM_TITLE, FORM_PLACEHOLDER,PHONE_NUMBER_PATTERN)


log:Logger = getLogger('Login')


LABELS_PERM_PROGRAMADOR:str = 'Ticket.attend'
LABELS_PERM_CLIENTE:str     = 'Ticket.register'
LABELS_PERM_ADMIN:str       = 'Ticket.admin'

class FormUserLogin(AuthenticationForm):
    """ Custom form para authetication in login """
    username = UsernameField(
        label=_(" "),
        widget=TextInput(attrs={
                "autofocus": True,
                'placeholder': 'Nombre de Usuario'
            })
    )
       
    password = CharField(
        label=_(" "),        
        strip=False,
        widget=PasswordInput(attrs={
           "autocomplete": "current-password",
           'placeholder': "Clave de Usuario"
           }),
    )


class CustomUserCreationForm(UserCreationForm):
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
        if not super().is_valid():
            return False
        
        empresa = self.data.get('empresa',None)
        log.debug(f'{type(self).__name__}::is_valid() empresa: {empresa}')
        if empresa and len(empresa) < 1:
            self.add_error('empresa', f"Seleccione Una Empresa de la lista")
            return False
        
        telefono:str = self.data.get('telefono',None)
        if telefono and not re_match(PHONE_NUMBER_PATTERN,telefono):
            self.add_error('telefono', f"Numero de telefono invalido.")
            return False  

        return True
  

class CustomUserChangeForm(UserChangeForm):
    """ Formulario para el pedido de cambio de contraseña """
    class Meta:
        model = User
        fields = ('username',)


class FormularioContacto(Form):
    """
      * nombre : Nombre de Usuario
      * email  : Direcion de email donde notificara
      * contenido : Mensaje
    """
    nombre:CharField = CharField(label='Nombre Usuario',required =True,
                                widget=TextInput(attrs={
                                    'autofocus': True ,
                                    'placeholder':'user name',
                                    'title':'Ingrese su nombre de usuario'}))
    
    # email opcional, ya que el usuario puede tener ya uno cargado previamente
    email:EmailField = EmailField(label='Direccion de Correo Electronico',required = False,
                                  widget=TextInput(attrs={
                                    'autofocus': False ,
                                    'placeholder':'email address',
                                    'title':'Ingrese su direccion de correo electronico'}))
  
    contenido:CharField = CharField(label='Observaciones',required=False,max_length=100,
                                    widget = Textarea(attrs={
                                        'autofocus': False ,
                                        'placeholder':'observation of to 100 characters',
                                        'title':'Ingrese una observacion o comentario.'}))
    
    
    def is_valid(self)->bool:
        """ Metodo que se encarga de la Validacion de los datos en el formulario"""

        if not super().is_valid():
            return False

        user:User = None
        try:
            user = User.objects.get(username = self.data['nombre'] )
        except Exception as e:
            log.error(f'Exception<{type(self).__name__}>, detail: {e}')
            self.add_error('nombre', f"El Usuario '{self.data['nombre']}' No Existe.")
            return False      
        
        if (user.email is None or user.email == '') and (self.data['email'] == ''):
            self.add_error('nombre', 
                            f"El usuario '{self.data['nombre']}' no tiene una direccion de "\
                            "correo electronico cargada, contacte al administrador.")
            return False
        
        ## No se debe permitir a un superuser cambiar la clave de esta forma
        try:
            if user.is_superuser or user.has_perm(LABELS_PERM_ADMIN) \
                or user.has_perm(LABELS_PERM_PROGRAMADOR) or \
                not user.has_perm(LABELS_PERM_CLIENTE):

                self.add_error('nombre', 
                               f"La clave para el Usuario '{self.data['nombre']}' "\
                                "no puede ser blanqueada de esta forma.")
                return False        
        except:
            pass 
        
        if user is not None:
            log.debug(f'user: {user}')
            return True
        
        self.add_error('nombre', f"El Usuario '{self.data['nombre']}' No Existe.")
        return False
      

class FormSendComment(Form):
    """
      * firstname : Primer nombre 
      * lastname  : Apellido
      * email     : Direccion de Correro electronico
      * comment   : Comentario
    """  
    firstname:CharField = CharField(label='Nombre Usuario',required =True,
                                    widget=TextInput(attrs={
                                        'autofocus': True,
                                        'placeholder':FORM_PLACEHOLDER.firstname,
                                        'title':FORM_TITLE.firstname} ))
  
    lastname:CharField = CharField(label='Apellido',required =True,
                                   widget= TextInput(attrs={
                                        'autofocus': False,
                                        'placeholder': FORM_PLACEHOLDER.lastname,
                                        'title':FORM_TITLE.lastname}))
  
    email:EmailField = EmailField(label='Dirreccion de Correo Electronico',required =True,
                                  widget=TextInput(attrs={
                                    'autofocus': False ,
                                    'placeholder': FORM_PLACEHOLDER.email,
                                    'title':FORM_TITLE.email} ))
  
    comment:CharField = CharField(label='Comentario',required=True,max_length=500,
                                  widget=Textarea(attrs={
                                    'autofocus': False,
                                    'placeholder': FORM_PLACEHOLDER.comment,
                                    'cols': 50,
                                    'rows': 5,
                                    'title':FORM_TITLE.comment} ))
    
    def is_valid(self)->bool:
        """ method validation"""        
        if not super().is_valid():
            return False
        return True
      
    def get_msg(self) -> str:
        """ metho for get string with data attributes"""
        rval = f"firstname: {self.data['firstname']}\n"
        rval += f"lastname: {self.data['lastname']}\n"
        rval += f"email: {self.data['email']}\n"
        rval += f"comment: {self.data['comment']}\n"
        return rval


class CompanyForm(ModelForm):
    nombre:CharField = CharField(max_length=32,
                                 widget=TextInput(attrs={
                                    'autofocus': True,
                                    'placeholder': FORM_PLACEHOLDER.company_name,
                                    'title':FORM_TITLE.company_name} ))
  
    telefono1:CharField = CharField(label="Telefono Principal",
                                    widget=TextInput(attrs={
                                       'labels':'tel',
                                       'placeholder':FORM_PLACEHOLDER.company_tel1,
                                       'title':FORM_TITLE.company_tel1} ))
  
    telefono2:CharField = CharField(required=False, label="Telefono Secundario",
                                    widget=TextInput(attrs={
                                       'labels':'tel',
                                       'placeholder': FORM_PLACEHOLDER.company_tel2,
                                       'title':FORM_TITLE.company_tel2} ))
  
    email:EmailField = EmailField(required=False,label='Direccion de Correo',
                                  widget=TextInput(attrs={
                                     'placeholder': FORM_PLACEHOLDER.email,
                                     'title':FORM_TITLE.email} ))
  
    class Meta:
        """ Modelo de la tabla para Empresa
            * nombre          : Nombre de la empresa.
            * telefono1       : Telefono Principal.
            * telefono2       : Telefono secundario.
    
            * date_creacion: DateTimeField          : Fecha de creacion del registro.
            * email: EmailField             : Email General de la empresa, un contacto general.
        """
        model = Empresa
        fields = ['nombre','telefono1','telefono2','email']
  
    def save(self,**kwargs):
        """ save method """
        instacompany = kwargs.get("instance",None)
        
        data = self.data
        if instacompany is None:
            company = Empresa(nombre=data['nombre'], telefono1=data['telefono1'], 
                              telefono2=data['telefono2'],email=data['email'],
                              date_creacion=timezone.now())
            company.save()
            return company
    
        instacompany.nombre=data['nombre']
        instacompany.telefono1=data['telefono1']
        instacompany.telefono2=data['telefono2']
        instacompany.email=data['email']
        instacompany.save()
      
      
    def is_valid(self,**kwargs):
        instacompany = kwargs.get("instance",None)
        if not super().is_valid():
            return False
                
        telefono:str = self.data.get('telefono1',None)
        if telefono and not re_match(PHONE_NUMBER_PATTERN,telefono):
            self.add_error('telefono1', f"Numero de telefono invalido.")
            return False      

        telefono = self.data.get('telefono2',None)
        if telefono and not re_match(PHONE_NUMBER_PATTERN,telefono):
            self.add_error('telefono2', f"Numero de telefono invalido.")
            return False      
    
        company:Empresa = None
        try:
            company = Empresa.objects.filter(nombre=self.data['nombre'])
        except Exception as e:
            log.error(f"Error {type(e).__name__} al obteber la Empresa, detalle: {e}")
    
        if instacompany is None:
            log.debug(f'company:{company}')      
            if company is not None and len(company) != 0:
                ## self.add_error(field, error_message)
                self.add_error('nombre',
                               f"Ya Tenemos una compania con este Nombre: {self.data['nombre']}.")
                return False              
            else:
                return True
            
        ## consultamos si modifico el nombre
        if self.data['nombre'] != instacompany.nombre and company is not None and len(company) != 0:            
            self.add_error('nombre',
                           f"Ya Tenemos una compania con este Nombre: {self.data['nombre']}.")
            return False
    
        return True

 