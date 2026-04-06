# buil-in import
from datetime import datetime
from logging import getLogger,Logger

# framework import
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.db.models.query import QuerySet
from django.http import HttpRequest,HttpResponse

# Project Modules import
from Buttons.apps import BtnWithImage
from Ticket.models import Tickets, RegisterWork
from Ticket.forms import FormularioTicket, FormularioRegisterWork
#from Login.models import User
from Login.contexto import (EmailThread, Choice)
from Login.constants import GROUPS
from cbviewsbase.viewsbase import GroupMemberBaseView
#from administrator.forms import FormEditClient


log:Logger = getLogger('registerticket')



class RegisterTicketViewBase(GroupMemberBaseView):
    method_set_attr:str = 'set_attr' # Opcional metodo que se encarga del set de atributos
    redirect_err_set_attr:str = '/register_ticket/' # redireccionamiento en caso del method_set_attr
    group_name:str = GROUPS.client
    # custom attributes
    ticket_id:int  = None
    ticket:Tickets = None # atributo donde almacenara la instancia del ticket

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")
                
        self.ticket_id = kwargs.get('ticket_id',None)
        if self.ticket_id is None:
           log.error(f"{type(self).__name__}::get() No se paso un ticket id valido")
           return False
                
        try:
            self.ticket = Tickets.objects.get(id=self.ticket_id)
        except Exception as e:
            log.error("Exception<%s> try get ticket for id <%s>, detail: %s",
                        type(e).__name__,self.ticket_id,e)
            return False
        
        if self.ticket.register.empresa != request.user.empresa:
            log.error("La empresa %s asociada al ticket id %s, no se corresponde a usuario %s",
                      self.ticket.register.empresa,self.ticket_id,request.user)

            return False
        
        return True
        #return self.render(request,*args, **kwargs)


class RegisterTicketViews(GroupMemberBaseView):
    """CBV para la Vista de quien registra tickets  """
    template_name:str = "registerticket/register_ticket.html"
    group_name:str = GROUPS.client
    id_choice:str = None

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render(), User {request.user}")
        buttonradio:list[dict] = [
            {'value':'opt4', 'groups':'choice', 'id':'choice4', 'label': 'Todos Mis Tickets' },
            {'value':'opt1', 'groups':'choice', 'id':'choice1', 'label': 'Ticket Abiertos'   },
            {'value':'opt2', 'groups':'choice', 'id':'choice2', 'label': 'Ticket Pendientes' },
            {'value':'opt3', 'groups':'choice', 'id':'choice3', 'label': 'Ticket Cerrados'   }
        ]
    
        query_filter = {'register': request.user }
        tickets:QuerySet[Tickets] = None
        
        if self.id_choice:
            if self.id_choice == 'opt1':
                query_filter.update({'estado': True })

            elif self.id_choice=='opt2':
                query_filter.update({'register_estado': False })

            elif self.id_choice=='opt3':
                query_filter.update({'estado': False })
        
        tickets = Tickets.objects.filter(**query_filter)
        contexto:dict = {
            'tabla_body'    : tickets,
            'table_head'    : {
                # Attribute name  | Label in table
                'id'              : 'ID',
                #'empresa'         : None,
                #'register'        : 'Quien Registro',
                'attend'          : 'Quien Atiende',
                'brief'           : 'Descripcion',
                'detail'          : 'Detalle',
                'email'           : 'Email',
                'fecha_creacion'  : 'Fecha de Creacion',
                'fecha_cierre'    : 'Fecha de Cierre',
                'file1'           : 'Ajunto 1',
                'file2'           : 'Ajunto 2',
                #'estado'          : '',
                'fecha_update'    : 'Ultima Modificacion',
                #'edit_register'   : '',
                'register_estado' : 'Estado'
            },
            'on_click_url'  : 'ExapandViewsTicket',
            'head_title'    : 'Tickets Registrados',
            'tab_title'     : 'tickets registrados',
            'current_user'  : request.user,
            'button_radio'  : buttonradio,
            'idchoice'      : self.id_choice,
            'listbtn'       : (
                BtnWithImage(path='add.png',url='/register_ticket/create_new_ticket/',
                             label='Nuevo Ticket',msg = 'Crear un Nuevo Ticket'),
                BtnWithImage(path='config.png',url='/administrator/view_config_nonadmuser/',
                             label='config user',msg='Configuracion del usaurio'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')          
            ),
        }
        return render(request,self.template_name,contexto)

    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
       """ handler for post from page """
       log.debug(f"{type(self).__name__}::post(), User {request.user}")
       self.id_choice = Choice().get(post=request.POST)
       return self.render(request,*args,**kwargs)



class CreateNewTicketView(GroupMemberBaseView):
    """CBV para la Vista de quien registra tickets  """
    template_name:str      = "registerticket/form_ticket.html"
    redirect_error_url:str = '/register_ticket/'
    group_name:str = GROUPS.client

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de renderizar sobre el template"""
        ## Botones del Formulario    
        contexto:dict = {
            'tab_title'  : 'create ticket',
            'head_title' : 'Creando Ticket',
            'listbtn'    : (
                BtnWithImage(path='go-previous.svg',url='/register_ticket/',label='Volver', 
                            msg = 'Volver a la Vista Anterior'),
            ),
        }

        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        ## renderizamos el formulario vacio 
        formulario = FormularioTicket()  
        contexto['form'] = formulario
        return render(request,self.template_name,contexto)
    
    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de manejar el post del form"""
        formulario = FormularioTicket(request.POST,request.FILES) 

        if not request.POST.get("ok") and not request.POST.get("nok"):
            ## No se recibio de los submi pre establecidos
            # Devolvemos el formulario tal cual, con un mensaej de warning
            contexto:dict = {'form' : formulario} 
            #return render(request,"Ticket/form_ticket.html",contexto)
            return self.render(request,context_ext=contexto,*args, **kwargs)
    
        if request.POST.get("nok"):
            ## Se preciono el clean del formulario
            #contexto['form'] =  FormularioTicket() 
            #return render(request,"Ticket/form_ticket.html",contexto)
            return self.render(request,*args,**kwargs)
        
        if formulario.is_valid():            
            formulario.save(register = request.user)
            return redirect('/register_ticket/')
    
        ## Si el formulario no es valido lo vuleve a cargar con los mismos datos que vino
        messages.warning(request, 'Datos Invalidos, verifique y vuelva a intentarlo.')
        contexto:dict = {'form' : formulario} 
        #return render(request,"Ticket/form_ticket.html",contexto)
        return self.render(request,context_ext=contexto,*args, **kwargs)


class ExpandTicketViews(RegisterTicketViewBase):
    """CBV para la Vista de quien registra tickets  """
    template_name:str      = "registerticket/register_views_ticket.html"
    redirect_error_url:str = '/register_ticket/'

    # custom 
    LOCAL_TIME:datetime    = timezone.now()   

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render() kwargs: {kwargs}")
               
        word = kwargs.get('word',None) 
        buttons:list[BtnWithImage] = [
           BtnWithImage(path='go-previous.svg',url='/register_ticket/',label='Volver')
        ]

        registerWork_all:QuerySet[RegisterWork] = None
        try:
            registerWork_all = RegisterWork.objects.filter(ticket=self.ticket_id).order_by('-id')        
        except IndexError:
            log.error("No tenemos registros en la tabla RegisterWork para el Ticket ID: %s",
                      self.ticket_id)
        
        if self.ticket.register_estado and len(registerWork_all) != 0:
            buttons.append( BtnWithImage(path='stock_exit.svg',
                                          url='cerrar',label='Cerrar Ticket',
                                          msg=f'Cerrar el Ticket {self.ticket_id}'))
        
        buttons.append(BtnWithImage(path='exit.png',url='/logout',label='Salir'))
        contexto:dict = {
            'tab_title'         : 'ticket, detalle',
            'head_title'        : 'Detalle del Ticket',
            'lticket'           : self.ticket,
            'urlticket'         : 'EditTicket',
            'registerWork_all'  : registerWork_all  ,
            'listbtn'           : buttons,
            ## FIXME el siguente es siempre True, lo verifica get() y si no redirecciona
            'ticket_access'     : self.ticket.register.username == request.user.username
        }
        
        if not self.ticket.register_estado or word is None:
            return render(request,self.template_name,contexto)

        context_err = kwargs.get('context_err',None)
        if context_err is not None:            
            return render(request,self.template_name,context={**contexto,**context_err})

        if word == 'cerrar':
            ## cerramos el ticket e impactamos la fecha de cierre
            if len(registerWork_all) != 0:
                thinstance = RegisterWork.objects.get(id=registerWork_all[0].id)                
                thinstance.date_update = timezone.now()
                thinstance.save()

            self.ticket.register_estado = False    
            self.ticket.fecha_cierre = timezone.now()
            self.ticket.save()

            EmailThread(attend=True,registro=self.ticket,
                        msg=f'Cliente Pidio Cierre del Ticket "{self.ticket.id}"',
                        header=f'closing petition Ticket"{self.ticket.id}"').start()

            EmailThread(registro=self.ticket,
                        msg=f'Cliente Pidio Cierre del Ticket "{self.ticket.id}"',
                        header=f'closing petition Ticket"{self.ticket.id}"').start()
            buttons.pop(1) # quitamos el boton de cerrar ticket
            contexto['listbtn'] = buttons
            return render(request,self.template_name,contexto)

        map_form:dict = {
            # word     |  form name
            'new'      : 'form_msg',
            'newPopUp' : 'popup_form_msg'
        }
        ## Por captura
        if word in map_form.keys():
            type(self).LOCAL_TIME = timezone.now()
            contexto[map_form[word]] = FormularioRegisterWork()
  
        return render(request,self.template_name,contexto)

    def post_form(self, request, *args, **kwargs)->HttpResponse:
        """ handler for post from page """
        log.debug(f"{type(self).__name__}::post() kwargs: {kwargs}")
        formulario = FormularioRegisterWork(data=request.POST,files=request.FILES)
    
        if not request.POST.get("ok") and not request.POST.get("nok"):
            log.debug(f'request.POST => !"ok" and !"nok" : request.POST {request.POST}')
            #return redirect(f'/register_ticket/')
            return self.render(request,*args,**kwargs)
    
        if request.POST.get("nok"):
            log.debug(f'"nok" cancel or X')
            return self.render(request,*args,**kwargs)
      
        if formulario.is_valid():
            # Para el post self._ticket es None, ya que se usa para el fill del form            
            formulario.save(ticket=self.ticket,register_work=request.user,
                            localtime=type(self).LOCAL_TIME )

            return redirect(f'/register_ticket/expand_ticket/{self.ticket_id}')
            
        contexto:dict = {
            'form_msg'      : formulario,
        }
        return self.render(request,context_err=contexto,*args, **kwargs)
    

class EditTicketViews(RegisterTicketViewBase):
    """CBV para la Vista de quien registra tickets  """
    template_name:str      = "Ticket/form_ticket.html"   
    redirect_error_url:str = '/register_ticket/'

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render() kwargs: {kwargs} | ticket: {self.ticket}")
        contexto:dict = { 
            'tab_title'    : 'edit ticket',
            'head_title'   : 'Editando Ticket',
            'listbtn'      : (
                BtnWithImage(path='go-previous.svg',
                            url=f'/register_ticket/expand_ticket/{self.ticket_id}',
                            label='Volver', msg = 'Volver a la Vista Anterior'),
                BtnWithImage(path='home.svg',url='/register_ticket/',
                            label='Home', msg = 'Ir a la pagina Principal Home') 
            ),
            'edit_form'    : True,
            'cancel_link'  : f'/register_ticket/expand_ticket/{self.ticket_id}',
        }  

        context_err = kwargs.get('context_err',None)
        if context_err is not None:            
            return render(request,self.template_name,context={**contexto,**context_err})

        contexto['form'] = FormularioTicket(instance=self.ticket)
        return render(request,self.template_name,contexto)
  
    def post_form(self, request, *args, **kwargs)->HttpResponse:
        """ handler for post from page """
        log.debug(f"{type(self).__name__}::post() kwargs: {kwargs} | ticket {self.ticket}")        

        formulario = FormularioTicket(data=request.POST,files=request.FILES)        
        if not request.POST.get("ok") and not request.POST.get("nok"):
            contexto:dict = {'form' : formulario}
            return self.render(request,context_err=contexto,*args, **kwargs)
    
        if request.POST.get("nok"):
            return self.render(request,*args,**kwargs)

        if formulario.is_valid():            
            formulario.save(instance=self.ticket)
            return redirect(f'/register_ticket/expand_ticket/{self.ticket_id}')
            #return self.render(request,*args,**kwargs)
    
        #messages.warning(request, 'Datos Invalidos')
        contexto:dict = {'form' : formulario}
        return self.render(request,context_err=contexto,*args, **kwargs)        
