# buil-in import
from abc import ABC, abstractmethod
from logging import getLogger,Logger

# framework import
from django.views import View
from django.shortcuts import render, redirect 
from django.http import HttpRequest,HttpResponse
from django.views.generic import TemplateView #,FormView
from django.contrib.auth.mixins import LoginRequiredMixin


log:Logger = getLogger('cbviewsbase')


class FormViewBase(View):
    FORM_TAG:str = None
    form_class = None
    template_name:str = None
    context:dict = None

    def render(self,request:HttpRequest=None):
       return render(request,self.template_name,self.context)
    
    def get(self, request:HttpRequest, *args, **kwargs):
        """ get method from form """
        #form = self.form_class(initial=self.initial)
        log.info(f"{type(self).__name__}::get()")
        self.context[self.FORM_TAG] = self.form_class()
        return self.render(request)


class VerifyUserAccess:
    """ Case que realiza la verificacion de usuario sobre un request:HttpRequest """
    
    group_name:str|tuple[str]|list[str] = None  # los grupos que pueden acceder a la vista    
    is_superuser:bool = False  # si superuser puede acceder a la vista
    in_group:str = None # donde se almacenamos el grupo del user

    def verify_user_access(self,request:HttpRequest)->bool:
        """ Metodo que se encarga de verificar si el usuario esta dentro del grupo """
        log.info(f"{type(self).__name__}::verify_user_access() user: {request.user} ")

        if self.group_name is None and not self.is_superuser:
            raise ValueError(f"{type(self).__name__} no se establecio el atributo 'group_name'")
        
        if self.group_name is not None and not isinstance(self.group_name, (str,list,tuple)):
            raise TypeError(f"{type(self).__name__} error en el tipo de dato de 'group_name'")
        
        if request.user.is_superuser:
            if self.is_superuser:
                return True

            log.error("%s::get() access denied for superuser %s, disabled",type(self).__name__,request.user)                
            return False        
        
        if self.group_name is None and self.is_superuser:
            log.error("%s::get() access denied user %s is not superuser",
                      type(self).__name__,request.user)
            return False
        
        if isinstance(self.group_name,str):
            if request.user.groups.filter(name=self.group_name).exists():
                self.in_group = self.group_name
                return True

            log.error("%s::get() access denied, user %s is not in group %s",
                      type(self).__name__,request.user,self.group_name)
            return False
            
        
        if isinstance(self.group_name,(list,tuple)):            
            for group in self.group_name :
                if request.user.groups.filter(name=group).exists():
                    self.in_group = group
                    return True

            log.error("%s::get() access denied, user %s is not in any of the groups <%s>",
                      type(self).__name__,request.user,self.group_name)
        return False           
        

class TemplateViewsWithLoginRequired(LoginRequiredMixin,TemplateView,VerifyUserAccess):
    """ Modelo Base de CBV para vistas que solo necesitan renderizar sobre un template 
    Atributos Basicos:
    - template_name  : para establecer la ruta al template
    - access_denied_redirect:str : Opcional (default login) p/redirecionamiento por acceso denegado
    - get_next_method:str : Opcional, nombre del metodo a ejecutar en lugar get() base sigannture 
        `fn(self,request:HttpRequest,*args, **kwargs)->HttpResponse`. Este cancela el llamado a
        `def get_context_data(self,**kwargs)->dict:`

    Para el VerifyUserAccess contamos con:
    - group_name:str|tuple[str]|list[str]   grupos que pueden acceder a la vista    
    - is_superuser:bool = False             si superuser puede acceder a la vista
    - in_group:str                          donde se almacenamos el grupo del user


    """
    template_name:str = None
    extra_context:dict = None
    access_denied_redirect:str = None # redirecionamiento, si es none toma login_url
    get_next_method:str = None # nombre del metodo a ejecutar en el success del get
                               # este cancela el llamado a 'get_context_data(self,**kwargs)->dict'
    
    # Configuras la redirección aquí mismo
    login_url:str = '/' 
    redirect_field_name:str = 'next'
    
    #def get_context_data(self, **kwargs)->dict:
    #    """ metodo abstracto que se encarga de armar el contexto necesario para el 
    #    renderizar la info sobre el template"""

    def get(self, request, *args, **kwargs):
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::get() user: {request.user}")

        if self.access_denied_redirect is None:
            self.access_denied_redirect = self.login_url

        if not self.verify_user_access(request):
            return redirect(self.access_denied_redirect)
        
        if self.get_next_method is None:
            return super().get(request, *args, **kwargs)
        
        return getattr(self,self.get_next_method)(request, *args, **kwargs)        


class GroupMemberBaseView(LoginRequiredMixin,TemplateView,ABC,VerifyUserAccess):
    """ Clase base para View con template/post form y verificacion de grupo p/user
    
    Atributos Basicos:
    - template_name  : para establecer la ruta al template
    - access_denied_redirect:str : Opcional (default login) p/redirecionamiento por acceso denegado
    
    - method_set_attr:str : Opcional, nombre del metodo el cual establecera atributos disponibles
    tanto pata el `render()` como para el `post_form()`. El signature de este debe ser
        `fn(self,request:HttpRequest,*args, **kwargs)->bool`. Si devuelve `True` establecio los 
        atributos correctamente. De lo contrario `False` implica un redireccionamiento a 
        `redirect_err_set_attr`
    
    - redirect_err_set_attr : Opcional (default toma login) redireccionamiento para el item anterior.

    Para el VerifyUserAccess contamos con:
    - group_name:str|tuple[str]|list[str]   grupo/s que pueden acceder a la vista    
    - is_superuser:bool = False             si el superuser puede acceder a la vista
    - in_group:str                          donde almacenamos el grupo del user que accedio

    Metodos Abrastracto a definir por implementador:
    - `def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:`
    - `def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:`
    
    """
    template_name:str = None   # nombre del template
    access_denied_redirect:str = None # redirecionamiento, para user no permitidos   
    
    method_set_attr:str = None # Opcional metodo que se encarga del set de atributos
    redirect_err_set_attr:str  = None # redireccionamiento en caso del method_set_attr

    # Configuracion de la redirección si el user no paso por login
    login_url:str = '/' 
    redirect_field_name:str = 'next'

    @abstractmethod
    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de renderizar sobre el template"""

    @abstractmethod
    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de manejar el post del form"""

    def __set_default(self)->None:
        if self.access_denied_redirect is None:
            self.access_denied_redirect = self.login_url

        if self.redirect_err_set_attr is None and self.method_set_attr is not None:
            self.redirect_err_set_attr = self.login_url

    def get(self, request:HttpRequest, *args, **kwargs)->HttpResponse:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::get() user: {request.user} | kwargs: {kwargs}")        
        self.__set_default()

        if not self.verify_user_access(request):
            return redirect(self.access_denied_redirect)

        if self.method_set_attr is not None:
            if not getattr(self,self.method_set_attr)(request, *args, **kwargs):
                return redirect(self.redirect_err_set_attr)

        log.info(f"{type(self).__name__}::get() in_group: {self.in_group}")
        return self.render(request,*args, **kwargs)
    
    def post(self, request, *args, **kwargs)->HttpResponse:
        """ handler for post from page """        
        log.debug(f"{type(self).__name__}::post() kwargs: {kwargs}")
        self.__set_default()

        if not self.verify_user_access(request):
            return redirect(self.access_denied_redirect)

        if self.method_set_attr is not None:
            if not getattr(self,self.method_set_attr)(request, *args, **kwargs):
                return redirect(self.redirect_err_set_attr)

        return self.post_form(request,*args, **kwargs)
