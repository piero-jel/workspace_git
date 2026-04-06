# buil-in import
#import sys
from random import seed,randrange
from datetime import datetime
from logging import getLogger,Logger

# framework import
from django.views import View
from django.views.generic import FormView #,TemplateView
from django.views.defaults import page_not_found
from django.urls import reverse_lazy#,reverse
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect 

# Project Modules import
from Login.models import User
from Login.forms import FormularioContacto, FormUserLogin
from Login.constants import GROUPS
from Login.contexto import EmailThread
from cbviewsbase.viewsbase import FormViewBase

log:Logger = getLogger('Login')


class UserLoginView(FormView):
    """ class-based views for Login User """
    # Establecemos el template para el render
    template_name = 'Login/login.html'
    
    # Modelo del Form de autenticacion
    #form_class = AuthenticationForm
    form_class = FormUserLogin
    
    # Establecemso el redirecionamiento en caso de succes
    # en urlpatterns[] localiza la vista con el name='Home'
    success_url = reverse_lazy('Home')

    def get_form_kwargs(self):
        """Pass the request object to AuthenticationForm."""
        log.info(f"{type(self).__name__}::get_form_kwargs()")
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Log the user in after form validation."""
        log.info(f"{type(self).__name__}::form_valid()")
        login(self.request, form.get_user())
        return super().form_valid(form)


class UserChangePasswordView(FormViewBase):
    FORM_TAG:str = "miFormulario"
    form_class = FormularioContacto    
    template_name = "Login/password_change_request.html"
    context:dict = { FORM_TAG : None}


    def post(self, request, *args, **kwargs):
        """ post method from form """
        log.info(f"{type(self).__name__}::send_mail()")
        if not request.POST.get("ok") and not request.POST.get("nok"):
            log.info(f"{type(self).__name__}::post() POST.get() not in ok or nok")
            self.context[self.FORM_TAG] = self.form_class(request.POST)
            return self.render(request)
    
        if request.POST.get("nok"):
            log.info(f"{type(self).__name__}::post() POST.get() in nok")
            ## Se preciono Cancelar realizamos el clean del formulario
            self.context[self.FORM_TAG] = self.form_class()
            return self.render(request)
            
        ## Se presionao ok btn
        log.info(f"{type(self).__name__}::post() POST.get() in ok")
        form:FormularioContacto = self.form_class(data=request.POST)
        self.context[self.FORM_TAG] = form
        if form.is_valid():
            self.send_mail()            
            #return self.render(request)
            messages.info(request,'Nueva Contraseña enviada a su Correo electronico.')
            return redirect('/')

        log.info(f"{type(self).__name__}::post() is_valid() is False")
        ## valid check que el nombre de usuario este en user      
        messages.error(request, 'Por Favor Corrija el error y vuelva a intentarlo.')
        return self.render(request)

    def send_mail(self):
        """Metodo que se encarga de enviar email con la clave temporal"""
        log.info(f"{type(self).__name__}::send_mail()")
        form:FormularioContacto = self.context[self.FORM_TAG]
        luser:User = User.objects.get(username = form.data['nombre'])
        ## Obtenemos el permiso, para luego usarlo en has_perm()
        new_pass = self.get_temporalpass()
        #log.debug(f'luser: {luser} pass: {new_pass}')
        luser.set_password(new_pass)
        luser.save()
        mensage = f'Pedido de Blanqueo de Contraseña, Nombre de Usuario {luser}'
        em_header = f'Clean de Contraseña User "{luser}"'        
        EmailThread(registro=luser, password = {'new_password':new_pass},
                    msg=mensage,
                    header=em_header).start()
        
        ## queda el envio de la observacion a los Admins y programadores
        if form.data['contenido'] not in (None, ''):
            mensage += f" Contenido del Mensage: \n{form.data['contenido']}"
            EmailThread(registro='admin',msg=mensage,
                        header=em_header).start()
        
            self.context['email'] = form.data['email']
        
    def get_temporalpass(self) -> str:
        """ metodo que genera una clave temporal """        
        letterToNumber = {'a':4 , 'b':8, 'e':3, 'i':1, 'o':0, 'q':9,'s':5 , 'p':2}
        numberToLetter = {'4':'a' , '8':'b', '3':'e', '1':'i', '0':'o', '9':'q','5':'s' , '2':'p' }

        def cifra2name(cifra:int) -> str:
            """
            Funcion para convertir una cifra numerica convertida en string
            en una cifra de nombre conformada por numero y letras, dentro de un string
            * cifra : cifra numerica como string
            """
            scifra = str(cifra)
            rval = ''
            for it in scifra:    
                if it in numberToLetter.keys():
                    rval += numberToLetter[it]
                else:
                    rval += it

            return rval

        form:FormularioContacto = self.context[self.FORM_TAG]
        username = form.data['nombre']
        if username is None or not isinstance(username,str):
            return None
    
        rval = ''
        for it in username.lower():    
            if it in letterToNumber.keys():
                rval += str(letterToNumber[it])
            else:
                rval += it

        if len(rval) < 5:
            seed(int(datetime.now().strftime('%Y%m%d%H%M%S%f')))    
            a = randrange(1, ((1024*1024)/pow(2,len(rval))) )        
            rval += cifra2name(a)

        return rval


class HomeView(View):
    permanent:bool = False  # Set to True for a 301 redirect

    def dispatch(self, request, *args, **kwargs):
        # si no esta logueado redireccionamos a la pagina de login
        if not request.user.is_authenticated:
            log.debug('User %s, No autentificado',request.user)
            return redirect('/')
        
        # Verificamos el grupo al cual pertenece el usuario logueado
        if request.user.groups.filter(name=GROUPS.admin).exists():
            return redirect('/administrator/')
            
        if request.user.groups.filter(name=GROUPS.programmer).exists():
            return redirect('/attend_ticket/')
            
        elif request.user.groups.filter(name=GROUPS.client).exists():
            return redirect('/register_ticket/')
        
        if request.user.is_superuser:
            return redirect('/administrator/')
        
        messages.warning(request, 'No tine los permisos suficientes')
        return super().dispatch(request, *args, **kwargs)



def Error_404(request,exception):
    """ page not found 404 """
    tamplate_name = 'Login/404.html'
    return page_not_found(request,exception=None, template_name=tamplate_name)


def Error_500(request, *args, **argv):
    """ Error 500 """
    return render(request, 'Login/500.html', status=500)  
