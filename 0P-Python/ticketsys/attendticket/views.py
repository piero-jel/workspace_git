# buil-in import
from logging import getLogger,Logger
from collections import defaultdict
from datetime import datetime

# framework import
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpRequest,HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.db.models.query import QuerySet

# Project Modules import
from Buttons.apps import BtnWithImage
from Ticket.forms import (
    FormularioRegistroTrabajo, FormularioRegisterWork,FormularioEditRegistroTrabajo
)
from Ticket.models import RegisterWork, Tickets ,Desarrollo,RegistroTrabajo
from Login.contexto import EmailThread
from Login.models import Programador,User
from Login.constants import GROUPS
from attendticket.forms import FormSearchIssueAttend
from administrator.forms import FormEditClient
from cbviewsbase.viewsbase import GroupMemberBaseView


log:Logger = getLogger('attendticket')


class AttendTicketViewBase(GroupMemberBaseView):
    """Clase base con la verificacion y redirecionamiento"""
    group_name:str = GROUPS.programmer
    method_set_attr:str = 'set_attr' 
    redirect_err_set_attr:str  = '/attend_ticket/'

    # custom attr
    programmer:Programador = None

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")

        try:
            self.programmer = Programador.objects.get(programador=request.user.id)
        except Exception as e:
            log.error("Exception<%s> try get Programador for user id <%s>, detail: %s",
                        type(e).__name__,request.user.id,e)
            return False
        
        return True


class AttendTicketView(AttendTicketViewBase):
    template_name:str = "attendticket/view_attend_ticket.html"
    set_querys:dict = None    

    STATICT_ITEMS:tuple[str] = ( 
        'nticke_asign'   ,
        'nticke_open'    ,
        'nticke_close'   ,
        'nticke_pending' ,
        'ndesarr_asign'  ,
        'ndesarr_open'   ,
        'ndesarr_close'  ,
        'ndesarr_pending'
    )

    def statitics(self)->dict:
        """ calcula la estadistica para el programador"""
        ret:defaultdict = defaultdict(int)      
        for k in type(self).STATICT_ITEMS:
            ret[k] = 0 

        tickets:QuerySet[Tickets] = None
        desarrollos:QuerySet[Desarrollo] = None
        try:
            tickets = Tickets.objects.filter(attend=self.programmer)
            desarrollos = Desarrollo.objects.filter(asistente=self.programmer)
        except Exception as e:
            log.error(f'Exception<{type(e).__name__}>, detail: {e}')
            return ret
        
        ret['nticke_asign'] = len(tickets)
        ret['ndesarr_asign'] = len(desarrollos)
        for tk in tickets:
            if tk.estado and tk.register_estado :
                ret['nticke_open'] += 1
                continue
    
            if not tk.estado and not tk.register_estado:
                ret['nticke_close'] += 1
                continue
    
            if tk.estado and not tk.register_estado:
                ret['nticke_pending'] += 1
        
        for it in desarrollos:
            if it.estado:
                ret['ndesarr_open'] += 1
            else:
                ret['ndesarr_close'] += 1

        ret['ndesarr_pending'] = ret['ndesarr_open']
        return ret
    
    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""        
        log.debug(f"{type(self).__name__}::render() kwargs: {kwargs}, Programmer:{self.programmer}")        
        if self.set_querys is None:
            # valor por defecto de los choice 
            self.set_querys = {
                'Tickets'   : None,
                'Desarrollo': None,
                'Tickets'   : {'attend' : self.programmer},
                'Desarrollo': {'asistente' : self.programmer},
            }

        log.debug(f"{type(self).__name__}::render() self.set_querys: {self.set_querys}")        
        ## Buscamos los Ticket y pedidos de desarrollos:
        tickets:QuerySet[Tickets] = None
        desarrollos:QuerySet[Desarrollo] = None
        asignacion:str = self.set_querys.get('asingacion',None)
        qticket:dict = self.set_querys.get('Tickets',None)
        qdesa:dict = self.set_querys.get('Desarrollo',None)
        
        if asignacion is not None and asignacion == 'other':
            try:
                tickets = Tickets.objects.filter(**self.set_querys['Tickets']).order_by('-id') & \
                    Tickets.objects.filter(~Q(attend=None),
                                        ~Q(attend__programador=self.programmer))            
            except Exception as e:
                log.error("%s::render() Exception<%s>, try get reg from Tickets .Detail: %s."\
                          "With Programmer <%s>. Detail: %s.",
                          type(self).__name__,type(e).__name__,self.programmer,e),
                          
            try:
                desarrollos = Desarrollo.objects.filter(
                    **self.set_querys['Desarrollo']).order_by('-id') & Desarrollo.objects.filter(
                        ~Q(asistente=None),~Q(asistente__programador=self.programmer.programador)
                )                
            except Exception as e:
                log.error("%s::render() Exception<%s>, try get reg from Desarrollo. "\
                          "With Programmer <%s>. Detail: %s.",
                          type(self).__name__,type(e).__name__,self.programmer,e)
        else:
            try:
                if qticket is not None and qdesa is not None:
                    tickets=Tickets.objects.filter(**qticket).order_by('-id')
                    desarrollos=Desarrollo.objects.filter(**qdesa).order_by('-id')
                else:
                    tickets = Tickets.objects.all().order_by('-id')
                    desarrollos = Desarrollo.objects.all().order_by('-id')
            except Exception as e:
                log.error("%s::render() Exception<%s>, try get reg from Tickets .Detail: %s."\
                          "With qticket <%s> and qdesa<%s>. Detail: %s.",
                          type(self).__name__,type(e).__name__,qticket,qdesa,e),

        try:    
            pass            
        except Exception as e:
            log.debug(f"User: {request.user} and set_querys: {self.set_querys}")
            log.error(f"{type(self).__name__}::render() Exception<{type(e).__name__}>, detail: {e}")
            #return redirect('/')

        contexto:dict = {
            'tab_title': 'tickets',
            'head_title':'Tickets',
            'listbtn': ( 
                BtnWithImage(path='config.png',url='/administrator/view_config_nonadmuser/',
                             label='config user',msg=f"Configuracion del usuario '{request.user}'"),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
            'urllink_ViewSelectedTicket'    : 'ViewSelectedTicket',
            'urltitle_ViewSelectedTicket'   : 'Click para ver el Ticket ',
            'urllink_ViewDesarrolloWorks'   : 'ViewDesarrolloWorks'    ,
            'urltitle_ViewDesarrolloWorks'  : 'Click para ver la Orden de Trabajo ',
            'statistics' : self.statitics(),
            'listTicket'     : tickets,
            'listDesarrollo' : desarrollos
        }
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        contexto['search_form'] = FormSearchIssueAttend()
        return render(request,self.template_name,contexto)

    def post_form(self, request, *args, **kwargs)->HttpResponse:
        """ handler for post from page """        
        log.debug(f"{type(self).__name__}::post_form() kwargs:{kwargs}, Programmer:{self.programmer}")

        # debemos rescatar la info desde el formulario luego de que realiza el submit
        #if not request.POST.get("search") and not request.POST.get("nok"):            
        #    return self.render(request,*args,**kwargs)
        #
        #if request.POST.get("nok"):            
        #    return self.render(request,*args,**kwargs)
    
        if request.POST.get("search"):
            form = FormSearchIssueAttend(request.POST)
            contexto:dict = {
                'search_form' : form
            }
            if form.is_valid():              
                self.set_querys = form.getSelection(programador=self.programmer)                
            else:
                log.debug(f'Form No validado')
                #messages.error(request, 'Error al intentar realizar la busqueda. '\
                #               'Corrija y vuelva a intentarlo.')
            return self.render(request,context_ext=contexto,*args, **kwargs)
        
        return self.render(request,*args,**kwargs)


class SelectedTicketView(AttendTicketViewBase):
    LOCAL_TIME:datetime = timezone.now()
    template_name:str = "attendticket/view_selected_ticket.html"
    #method_set_attr:str = 'set_attr'
    #redirect_err_set_attr:str  = '/attend_ticket/'
    ## custom attr
    ticket:Tickets = None
    owner:bool = False
    registerWork_all:QuerySet[RegisterWork] = None 

    def set_attr(self,request:HttpRequest,*args, **kwargs)->bool:
        """metodo para establecer los atributos necesarios"""
        super().set_attr(request,*args,**kwargs)
        log.debug(f"{type(self).__name__}::set_attr() programmer: {self.programmer}")
        ticket_id = kwargs.get('id',None)
        if ticket_id is None:
            return False

        try:
            self.ticket = Tickets.objects.get(id = ticket_id)
        except Exception as e:
            log.error(f"Expetion<{type(e).__name__}>, detail: {e}")
            return False

        self.owner = self.ticket.attend is not None \
            and self.ticket.attend.programador.username == request.user.username
            
        try:
            self.registerWork_all = RegisterWork.objects.filter(
                ticket=self.ticket.id).order_by('-id')
        except Exception as e:
            log.debug(f"Error {e} para el Ticket ID: {self.ticket.id}")
        
        return True
    
    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de renderizar sobre el template"""
        buttons:list[BtnWithImage] = [ 
            BtnWithImage(path='go-previous.svg',url='/attend_ticket/',label='Volver')
        ]
        word:str = kwargs.get('word',None)
        contexto:dict = {
            'usuario' : self.programmer,
            'lticket' : self.ticket,
        }

        if self.owner:
            if self.ticket.register_estado:
                contexto['btn_new'] = 'Nuevo Mensaje'
            elif not self.ticket.register_estado and self.ticket.estado:
                contexto['btn_stedit'] = 'Edit Estado'
            elif not self.ticket.register_estado and not self.ticket.estado:
                contexto['btn_streopen'] = 'Reabrir Ticket'

        contexto['registerWork_all'] = self.registerWork_all
        if self.ticket.estado:
            if self.ticket.attend is None:                
                buttons.append(BtnWithImage(
                    path='dialog-information.png',url='take',label='Asignar',
                    msg=f'Comenzar la atencion del Ticket {self.ticket.id}'))
    
            elif self.owner:
                buttons.append(BtnWithImage(
                    path='rechazado.png',url='leave',label='Desasignar',
                    msg=f'Dejar de atender el Ticket {self.ticket.id}'))
    
        buttons.append(BtnWithImage(path='exit.png',url='/logout',label='Salir'))  
        contexto['listbtn'] = buttons
        contexto['tab_title'] = 'ticket, detalle'  
        contexto['head_title'] = f'Detalle del Ticket, Id: {self.ticket.id}'  
        
        if self.owner:
            contexto['url_edit'] = 'edit'
            contexto['title_edit'] = 'Click para editar este Registro'

        if word is not None:
            if word == 'take' and self.ticket.attend is None:
                self.ticket.attend = self.programmer
                self.ticket.save() 
                EmailThread(attend=True,registro=self.ticket,
                            msg=f'El Prg {request.user} tomo el Ticket "{self.ticket.id}"',
                            header=f'Prg {request.user} Take Ticket "{self.ticket.id}"').start()
                
                EmailThread(registro=self.ticket,
                            msg=f'El Prg {request.user} tomo el Ticket "{self.ticket.id}"',
                            header=f'Prg {request.user} Take Ticket "{self.ticket.id}"').start()
                
                return redirect(f'/attend_ticket/view_selected_ticket/{self.ticket.id}/')
                
            elif word == 'leave' and self.owner:
                self.ticket.attend = None
                self.ticket.save()
                return redirect(f'/attend_ticket/view_selected_ticket/{self.ticket.id}/')
        
            elif word == 'new' and self.owner:
                contexto['edit_form'] = False
                contexto['form_msg'] = FormularioRegisterWork()
                contexto['btn_cancel'] = 'Cancelar'
                type(self).LOCAL_TIME = timezone.now()
                            
            elif word == 'edit' and self.owner:
                if self.registerWork_all[0].register_work.username != request.user.username:
                      log.debug('El usuario %s No es propietario del registro RegisterWork %s',
                                request.user.username,self.registerWork_all[0].id)
                                      
                contexto['edit_form'] = True
                contexto['form_msg'] = FormularioRegisterWork(instance=self.registerWork_all[0])
                contexto['btn_cancel'] = 'Cancelar'
                type(self).LOCAL_TIME = timezone.now()
            
            elif word == 'cancel' and self.owner:
                log.debug(f'Se cancelo la carga de un Nuevo mensaje peticionado ')
        
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        return render(request,self.template_name,contexto)
    
    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de manejar el post del form"""
        word:str = kwargs.get('word',None)        
        if not request.POST.get("ok") and not request.POST.get("nok") and \
            not request.POST.get("popup01-yes") and not request.POST.get("popup03-yes"):

            log.debug(f"{type(self).__name__}::post_form() request.POST {request.POST}")
            return self.render(request,*args,**kwargs)
    
        if request.POST.get("nok"):
            # button clena presionado
            log.debug(f"{type(self).__name__}::post_form() request.POST nok")
            return redirect(f'/attend_ticket/view_selected_ticket/{self.ticket.id}/new')
      
        if request.POST.get("popup01-yes") or request.POST.get("popup03-yes"):
            log.debug(f'Volvemos a habilitar el Ticket por parte del Cliente')
        
            if len(self.registerWork_all) != 0:
                thinstance = RegisterWork.objects.get(id=self.registerWork_all[0].id)      
                log.debug(f'thinstance : {thinstance}')
                # actualizamos la fecha de actualizacion
                thinstance.date_update = timezone.now()
                thinstance.save()
        
            self.ticket.register_estado = True
            if request.POST.get("popup03-yes"):
                self.ticket.estado = True

            self.ticket.fecha_update = timezone.now()
            self.ticket.fecha_cierre = None
            self.ticket.save()
            log.debug(f'timezone.now() : {timezone.now()}')
            ## send email a ambos grupos 
            EmailThread(attend=True,registro=self.ticket,
                        msg=f'Se volvio a abrir el Ticket "{self.ticket.id}"',
                        header=f'Re Open Ticket "{self.ticket.id}"').start()
            EmailThread(registro=self.ticket,msg=f'Se volvio a abrir el Ticket "{self.ticket.id}"',
                        header=f'Re Open Ticket "{self.ticket.id}"').start()

            return redirect(f'/attend_ticket/view_selected_ticket/{self.ticket.id}')
    
        formulario = FormularioRegisterWork(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            if word == 'edit':
                formulario.save(instance=self.registerWork_all[0],
                                localtime = type(self).LOCAL_TIME )
            else:
                formulario.save(ticket=self.ticket,register_work=self.programmer,
                                programmer = True,localtime = type(self).LOCAL_TIME)
        
            return redirect(f'/attend_ticket/view_selected_ticket/{self.ticket.id}') 
    
        log.debug(f'Formulario no Valido: {formulario} ')
        contexto:dict = {'form_msg' : formulario }        
        return self.render(request,context_ext=contexto,*args,**kwargs)


class SelectedDesarrolloView(AttendTicketViewBase):
    LOCAL_TIME:datetime = timezone.now()
    template_name:str = "attendticket/view_desarrollos_works.html"
    #method_set_attr:str = 'set_attr'
    #redirect_err_set_attr:str  = '/attend_ticket/'

    ## custom attr
    development_id:int = None
    development:Desarrollo = None
    developmen_works:QuerySet[RegistroTrabajo] = None

    def set_attr(self,request:HttpRequest,*args, **kwargs)->bool:
        """metodo para establecer los atributos necesarios"""
        if not super().set_attr(request,*args,**kwargs):
            return False

        log.debug(f"{type(self).__name__}::set_attr() programmer: {self.programmer}")
        self.development_id = kwargs.get('id',None)
        if self.development_id is None:
            log.debug(f'{type(self).__name__}::set_attr() No se paso developmenr_id')
            return False

        try: # Estes puede ser None, Desarrollo aun no creador
            self.development = Desarrollo.objects.get(id=self.development_id,
                                                      asistente=self.programmer)
        except Exception as e:
            log.error("%s::set_attr() Expetion<%s>, try get register from Desarrollo with "\
                      "development_id<%d>. Detail: %s",
                      type(self).__name__,type(e).__name__,self.development_id,e)
            messages.warning(
                request,
                f"No tienes asignada la Orden de trabajo<{self.development_id}>"
            )
            return False
            
        
        try:
            self.developmen_works = RegistroTrabajo.objects.filter(
                desarrollo=self.development_id).order_by('-id')
            
        except Exception as e:
            log.error("%s::set_attr() Expetion<%s>, try get register from RegistroTrabajo with ."\
                      "development_id<%d>. Detail: %s",
                      type(self).__name__,type(e).__name__,self.development_id,e)
            return False
        
        return True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render() kwargs:{kwargs}, Programmer:{self.programmer}")
        word:str  = kwargs.get('word','')
        word2:str = kwargs.get('word2','')
        cls = type(self)
        contexto:dict = {
            'tab_title': f'developmen {self.development_id}, details',
            'head_title': f'Detalle de la Orden de Desarrollo {self.development_id}',
            'listbtn': ( 
                BtnWithImage(path='go-previous.svg',url='/attend_ticket/',label='Volver'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir') 
            ),
            'urlticket'        : 'EditTicket',
            'developmen'       : self.development,
            'developmenIdWork' : self.developmen_works,
        }

        if word == 'add' and self.development.estado:
            if word2 == 'close':
                return redirect(f'/attend_ticket/view_desarrollos_works/{self.development_id}/')

            cls.LOCAL_TIME = timezone.now()
            contexto['launch_form_popup01'] = True
            contexto['form_popup01'] = FormularioRegistroTrabajo()
            return render(request,self.template_name,contexto)
  
        elif word == 'edit' and self.development.estado:
            if word2 == 'close':
                return redirect(f'/attend_ticket/view_desarrollos_works/{self.development_id}/')
                        
            if len(self.developmen_works) > 0 and self.developmen_works[0].programmer:
                cls.LOCAL_TIME = timezone.now()
                contexto['launch_form_popup02'] = True
                contexto['form_popup02'] = FormularioEditRegistroTrabajo(
                    instance=self.developmen_works[0])
                contexto['id_form_popup02'] = self.developmen_works[0].id
                return render(request,self.template_name,contexto)
            
            log.debug("%s::render() se presiono la lupa y no tenemos developmen_works",
                      type(self).__name__)
            return redirect(f'/attend_ticket/view_desarrollos_works/{self.development_id}/')
        
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})
        
        contexto['launch_form_popup02'] = False
        contexto['launch_form_popup01'] = False
        return render(request,self.template_name,contexto)
    
    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo Abstracto que se encarga de manejar el post del form"""
        log.debug(f"{type(self).__name__}::post_form() kwargs:{kwargs}, Programmer:{self.programmer}")
        cls = type(self)
        contexto:dict = {}
        if request.POST.get("okpopUp01"):
            formulario = FormularioRegistroTrabajo(data=request.POST,files=request.FILES)
            if formulario.is_valid():
                formulario.save(desarrollo=self.development,register_work=self.programmer,
                                programmer=True,localtime = cls.LOCAL_TIME)
                
                return redirect(f'/attend_ticket/view_desarrollos_works/{self.development_id}/')
            else:
                log.debug(f"{type(self).__name__}::post_form() okpopUp01 {request.POST}")
                contexto['err_form_popup01'] = True
                contexto['form_popup01'] = formulario
                return self.render(request,context_ext=contexto,*args, **kwargs)
    
        elif request.POST.get("okpopUp02"):
            formulario = FormularioEditRegistroTrabajo(data=request.POST,files=request.FILES)
            if formulario.is_valid():
                formulario.save(instance=self.developmen_works[0],
                                localtime=cls.LOCAL_TIME)
                return redirect(f'/attend_ticket/view_desarrollos_works/{self.development_id}/')
            else:
                messages.warning(request, 'Datos Invalidos')
                contexto['err_form_popup02'] = True
                contexto['form_popup02'] = formulario
                return self.render(request,context_ext=contexto,*args, **kwargs)
            
        elif(request.POST.get("nok")):
            log.debug(f"{type(self).__name__}::post_form() nok {request.POST}")
            return redirect(f'/attend_ticket/view_desarrollos_works/{self.development_id}/')
        
        log.debug(f"{type(self).__name__}::post_form() {request.POST}")
        return self.render(request,*args, **kwargs)



# FIXME Sin uso, la vista esta generalizada en el administrator ConfigUserClientView()
class ConfigUserAttendView(GroupMemberBaseView):
    """ Vista para la Configuracion de usuario Cliente  """
    template_name:str = "Login/view_company_clients.html"
    group_name:str = GROUPS.client
    
    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::remder(), User {request.user}, kwargs: {kwargs}")
        user:User = request.user
        
        contexto:dict = {
            'tab_title'    : f'{user.empresa} {user}',
            'head_title'   : f'{user.empresa}, {user}',
            'listbtn': (
                BtnWithImage(path='go-previous.svg',
                                                url=f'/register_ticket/',
                                                label='Volver', 
                                                msg = 'Volver al listado de Tickets'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
            'client'        : True,
            'titlebtn_edit' : f'Click para editar el usuario {user}',
            'labelbtn_edit' : 'Editar',
            'luser'         : user,
            # debemos armarla en un popup, para que quede en la vista actual
            #'urlbtn_cleanpass'   : '/administrator/change_passwords/',
            'urlbtn_cleanpass'   : 'administrator_app:ChangePassword',
            'titlebtn_cleanpass' : 'Click para realizar el cambio de Contraseña',
            'labelbtn_cleanpass' : 'Change Pass',
        }
        context_err = kwargs.get('context_err',None)
        if context_err is not None:            
            return render(request,self.template_name,context={**contexto,**context_err})
                
        contexto['user_form'] = FormEditClient(data=user)
        return render(request,self.template_name,contexto)
    
    def post_form(self, request, *args, **kwargs)->HttpResponse:
        """ metodo que se encarga de manejar los post desde los forms """
        log.debug(f"{type(self).__name__}::post_form(), User {request.user}")
        user:User = request.user
    
        if request.POST.get("edit_nok"):            
            log.debug(f"{type(self).__name__}::post_form(), request.POST.edit_nok")   
            return self.render(request,*args, **kwargs)
    
        if request.POST.get("edit_ok"):
            log.debug(f"{type(self).__name__}::post_form(), request.POST.edit_ok")
            user_form = FormEditClient(request.POST)
            
            if user_form.is_valid():
                log.debug(f"{type(self).__name__}::post_form(), save(), {request.POST}")
                user_form.save(instance=user)
                return self.render(request,*args, **kwargs)
            
            log.debug(f'{type(self).__name__}::post_form(), Form No validado')
            contexto:dict = {
                'user_form'      : user_form,
                'user_form_popUp': True,
            }
            return self.render(request,context_err=contexto,*args, **kwargs)

        return self.render(request,*args, **kwargs)

