# buil-in import
#from datetime import datetime
from collections import defaultdict,namedtuple
from logging import getLogger,Logger

# framework import
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db.models.query import QuerySet
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group, Permission


# Project Modules import
from Buttons.apps import BtnWithImage
from Ticket.models import Tickets, Modulos, Desarrollo, RegistroTrabajo
from Ticket.forms import ( 
    FormularioModulos,FormEditTicket,FormularioDesarrollo,FormularioRegistroTrabajo,
    FormularioSetDesarrollo, FormularioEditRegistroTrabajo,FormularioEditDesarrollo 
)
from Login.models import User,Empresa,Programador
from Login.contexto import EmailThread
from Login.constants import GROUPS,PERMISSION
from Login.forms import CompanyForm, CustomUserCreationForm#, FormularioContacto
from cbviewsbase.viewsbase import TemplateViewsWithLoginRequired,GroupMemberBaseView
from administrator.forms import (
    NewUserForm, FormularioCheckUser, FormEditUser,FormEditClient,FormSearchTicket
)


log:Logger = getLogger('administrator')

class AdminViews(TemplateViewsWithLoginRequired):
    """Vista Prinicipal de la aplicacion """
    template_name:str = "administrator/view_admin.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    def get_context_data(self, **kwargs)->dict:
        # 1. Call the base implementation first to get a context
        context:dict = super().get_context_data(**kwargs)
        list_btn:list[BtnWithImage] = [
            BtnWithImage(path='Config_02.svg',url='/admin/',label='Sys Admin',
                         msg='Ingresar al Administrador del Sistema'),
            BtnWithImage(path='config.png',
                         url=f'/administrator/view_config_user/{self.request.user.id}',
                         label='config user',msg=f'Configuracion del usuario {self.request.user}'),            
        ]
        if self.request.user.is_superuser:
            list_btn.append( BtnWithImage(path='preferences-system-search.png',
                                          url='/administrator/view_useradmin/',
                                          label='users admins',
                                          msg='Usuarios Administradores')
            )

        list_btn.append(BtnWithImage(path='exit.png',url='/logout',label='Salir'))
        local_context:dict = {             
            'tab_title': 'admin',
            'head_title':'Administracion', 
            'listlink':(
                {'name':'Empresas',     'link':'/administrator/view_companies/',   'title':'Empresas'},
                {'name':'Modulos',      'link':'/administrator/view_modulos/',     'title':'Modulos'},
                {'name':'Programadores','link':'/administrator/view_programmers/', 'title':'Programadores'},
                {'name':'Tickets',      'link':'/administrator/view_tickets/',     'title':'Tickets'},
                {'name':'Desarrollos',  'link':'/administrator/view_desarrollos/', 'title':'Desarrollos Actuales'},
                ## FIXME solo para superuser add list all users
                #{'name':'Reporte',      'link':'/view_reporte/','title':'Generacion de Reporte'}
            ),
            'listbtn':list_btn 
        }
        if context is None:
            return local_context
        
        return {**context, **local_context}


class ListAdminViews(TemplateViewsWithLoginRequired):
    template_name:str = "administrator/view_user_admins.html"    
    is_superuser:bool = True

    def get_context_data(self, **kwargs):
        # 1. Call the base implementation first to get a context
        context:dict = super().get_context_data(**kwargs)
        buttons:tuple[BtnWithImage] = (
            BtnWithImage(path='go-previous.svg',url='/administrator/',label='Volver',
                         msg='Volver a la Vista de Admin'),
            BtnWithImage(path='config.png',url='/admin/',label='Sys Admin',
                         msg='Ingresar al Administrador del Sistema'),
            BtnWithImage(path='exit.png',url='/logout',label='Salir')
        )

        users_administrator:QuerySet[User] = None
        try:        
            users_administrator = User.objects.filter(groups=Group.objects.get(name=GROUPS.admin))    
        except Exception as e:
            log.error('Exception<%s> in get user for group %s. Detail %s',
                      type(e).__name__,GROUPS.admin,e)

        local_context:dict = { 
            'tab_title'    : 'users admin',
            'head_title'   : 'Lista de Administradores',
            'users_administrator'  : users_administrator,
            'listbtn'      : buttons,
            'urllink'      : 'administrator_app:UserConfigurationView',
            'urltitle'     : 'Click para ver informacion de ',
            'urlbtn_add'   : '/administrator/new_administrador/',
            'titlebtn_add' : "Agregar Nuevo Programador"
        }
        if context is None:
            return local_context
        
        return {**context, **local_context}


class ListProgammersViews(TemplateViewsWithLoginRequired):
    template_name:str = "administrator/view_programmers.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    def get_context_data(self,**kwargs)->dict:
        """metodo que se encarga de armar el contexto para el fill del template"""
        context:dict = super().get_context_data(**kwargs)
        
        programmers_all:QuerySet[Programador] = None
        try:
            programmers_all = Programador.objects.all().order_by('id')
        except:            
            log.error("%s::get_context_data() kwargs: %s.",
                    type(self).__name__,kwargs)
            programmers_all = []
    
        local_contex:dict = {
            'tab_title': 'programmers',
            'head_title':'Lista de Programadores',
            'programmers_all' : programmers_all ,
            'listbtn'     : ( 
                BtnWithImage(path='go-previous.svg',url='/administrator/',label='Volver',
                                msg = 'Volver a la Vista de Admin'),
                BtnWithImage(path='config.png',url='/admin/',label='Sys Admin',
                                msg='Ingresar al Administrador del Sistema'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')    
            )    
            ,
            'urllink'     : 'administrator_app:UserConfigurationView',
            'urltitle'    : 'Click para Editar la informacion del Programador '  ,
            'urlbtn_add'  : '/administrator/new_programmer/',
            'titlebtn_add': "Agregar Nuevo Programador"    ,
        }
        if context is None:
            return local_contex
        
        return {**context , **local_contex}


class ListCompaniesView(TemplateViewsWithLoginRequired):
    """Modelo para la vista de listas de Empresas"""
    template_name = "administrator/view_companies.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True
    get_next_method:str = 'render'
    
    ROWS:set[str] = {
        # item dentro de Empresa
        'id', 'nombre', 'telefono1', 'telefono2', 'email', 'date_creacion',
        # Nombre de un metodo y attr de render que realiza calculo con los anteriores
        'nro_empleados'
    }    
    
    def nro_empleados(self,row:Empresa)->int:
        """ Meotod dentro de ROWS que se encarga de calcular el numero de empleados
        para que estos sean almacenado en la nametuple que armada la lista a renderizar
        - row : representa el registro con el cual se realizar el calculo
        """
        try:
            return len(User.objects.filter(empresa=row))
        except Exception as e:
            log.error("%s::nro_empleados() Exception<%s> try get User for company <%s>. Detail: %s",
                    type(self).__name__,type(e).__name__,row,e)
        return 0

    def get_rows(self,queryset:QuerySet)->list[tuple]:
        """ """
        cls = type(self)
        Rows = namedtuple('Rows', list(cls.ROWS))
        ret:list[Rows] = []

        for row in queryset:
            lst:list = []
            for it in cls.ROWS:
                if hasattr(row,it):
                    lst.append(getattr(row,it))
                elif hasattr(self,it):
                    lst.append(getattr(self,it)(row))
                else:
                    lst.append(None)
            
            ret.append(Rows(*lst))
        
        return ret

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::remder(), User {request.user}, kwargs: {kwargs}")
        company_all:QuerySet[Empresa] = None    
        try:
            company_all = Empresa.objects.all().order_by('id')
        except Exception as e:
            log.error("%s::render() Exception<%s> in query for Empresa. Detail %s",
                      type(self).__name__,type(e).__name__,e)
            #messages.warning(request,f"No tenemos Empresas Registradas.")
            company_all = []
    
        contexto:dict = {
            'tab_title'          : 'companies',
            'head_title'         : 'Lista de Empresas Registradas',
            'company_enum_items' : [len(User.objects.filter(empresa=it)) for it in company_all],
            'listbtn'            : ( 
                BtnWithImage(path='go-previous.svg',url='/administrator/',label='Volver',
                            msg = 'Volver a la Vista de Admin'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
            'urllink'            : 'administrator_app:CompanyView',
            'urltitle'           : 'Click para expandir la Informacion de ',
            'urlbtn_add'         : '/administrator/new_company/',
            'titlebtn_add'       : 'Agregar Nuevo Empresa',
            'urlbtn_del'         : '/delete_register/',
            'titlebtn_del'       : 'Eliminar Empresa ?',
            'company_all'        : self.get_rows(company_all)
        }            
        return render(request,self.template_name,contexto)


class ListModulosView(GroupMemberBaseView):
    """Modelo para la vista de listas de Empresas"""
    template_name = "administrator/view_modulos.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True
    method_set_attr:str = 'set_attr'
    # custom attributes
    modulo_id:int = None
    modulo:Modulos = None
    modulos:QuerySet[Modulos] = None

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")

        self.modulo_id:int = kwargs.get('modulo_id',None)        
        try:
            self.modulos = Modulos.objects.all().order_by('id')
        except Exception as e:
            log.error("%s::render() Exception<%s> in query for Modulos. Detail %s",
                      type(self).__name__,type(e).__name__,e)
            self.modulos = []

        if self.modulo_id is None or len(self.modulos) == 0:
            return True
        
        self.modulo = next((mod for mod in self.modulos if mod.id == self.modulo_id), None)
        return True
    
    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::remder(), User {request.user}, kwargs: {kwargs}")               
        contexto:dict = {
            'tab_title'        : 'modules',
            'head_title'       : 'Lista de Modulos',
            'modules_all'      : self.modulos,
            'listbtn'          : ( 
                BtnWithImage(path='go-previous.svg',url='/administrator/',label='Volver',
                            msg = 'Volver a la Vista de Admin'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
            'urlbtn_add'       : '/administrator/new_modulo/',
            'titlebtn_add'     : "Agregar Nuevo Modulo",
            'urllink'          : 'administrator_app:ListModulosView',
            'urltitle'         : 'Click para expandir la Informacion del modulo: '            
        }

        if self.modulo_id is None:
            return render(request,self.template_name,contexto)
                        
        if self.modulo is None:
            messages.warning(request,f"No tenemos un Modulo con id '{self.modulo_id}'.")
            return redirect('/administrator/view_modulos/')
        
        form_edit:FormularioModulos = FormularioModulos(instance=self.modulo)            
        contexto['form_edit'] = form_edit
        contexto['inst_edit'] = self.modulo
        contexto['popup_btn_delete'] = False # no es necesari read post_form()
        return render(request,self.template_name,contexto)
    
    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ """          
        if not request.POST.get("ok") and not request.POST.get("nok") and\
              not request.POST.get("del"):
            return redirect('/administrator/view_modulos/')
    
        if request.POST.get("nok"):
            ## Se preciono No
            return redirect('/administrator/view_modulos/')
        
        if request.POST.get("del"):
            # Debemos habilitar el delete en cascada, para todos los 
            # Tickets y Desarrollo (`on_delete=CASCADE`)            
            mod_name = str(self.modulo)
            self.modulo.delete()
            log.debug("%s::post_form() Modulo <%s> Eliminado",type(self).__name__,mod_name)
            return redirect('/administrator/view_modulos/')

        if not request.POST.get("ok"):
            form_edit = FormularioModulos(request.POST )    
            if form_edit.is_valid(edit=True):
                form_edit.save(instance=self.modulo)
                log.debug("%s::post_form() Modulo <%s> Modificado",type(self).__name__,self.modulo)

        return redirect('/administrator/view_modulos/')


class NewModuloView(GroupMemberBaseView):
    """ Vista para crear un nuevo modulo """
    template_name = "administrator/form_new_modulo.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ """
        contexto = {
        'tab_title': 'new modules',
        'head_title':'Agregando un Nuevo Modulo',
        'listbtn': ( 
                BtnWithImage(path='go-previous.svg',url='/administrator/view_modulos/',
                             label='Volver', msg = 'Volver a la Vista de Admin'),

                BtnWithImage(path='home.svg',url='/administrator/',label='Home', 
                            msg = 'Ir a la pagina Principal Home'),
                
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            )
        }
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        contexto['form'] = FormularioModulos()
        return render(request,self.template_name,contexto)
    
    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ """
        if request.POST.get("nok"):
            return self.render(request,*args,**kwargs)

        if request.POST.get("ok"):
            form = FormularioModulos(request.POST )
            if form.is_valid():
                mod = form.save()            
                log.debug("%s::post_form() Se crea un nuevo Modulo '%s' de forma Sastifactoria!",
                          type(self).__name__,mod)
                return redirect('/administrator/view_modulos/')        
            
            messages.error(request, 'Por Favor Corrija el error y vuelva a intentarlo.')
            context = {'form' : form}
            return self.render(request,context_ext=context,*args,**kwargs)
            
        return self.render(request,*args,**kwargs)


class NewCompanyView(GroupMemberBaseView):
    """ Vista para un modulo en particular, ver o editar el mismo"""
    template_name = "administrator/form_new_company.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ """
        contexto:dict = {
            'tab_title': 'new company',
            'head_title':'Agregando una Nueva Compania',
            'listbtn'   : (
                BtnWithImage(path='go-previous.svg',url='/administrator/view_companies/',
                             label='Volver',msg = 'Volver a la Vista de Admin'),
                BtnWithImage(path='home.svg',url='/administrator/',label='Home',
                            msg = 'Ir a la pagina Principal Home') 
            ) 
        } 

        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        contexto['form'] = CompanyForm()
        return render(request,self.template_name,contexto)

    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ """          
        if request.POST.get("nok"):
            return self.render(request,*args,**kwargs)
    
        if request.POST.get("ok"):
            form = CompanyForm(request.POST )
            if form.is_valid():
                nw_cmp = form.save()                      
                log.debug(f"Se crea una nueva Compania '{nw_cmp}' de forma Sastifactoria!")      
                return redirect('/administrator/view_companies/')
        
            messages.error(request, 'Por Favor Corrija el error y vuleva a intentarlo.')
            log.error('%s::post_form() form not valid',type(self).__name__)
            contexto = {'form' : form }
            return self.render(request,context_ext=contexto,*args, **kwargs)

        return self.render(request,*args,**kwargs)


class NewProgrammerView(GroupMemberBaseView):
    """ Vista para un modulo en particular, ver o editar el mismo"""
    template_name = "administrator/form_new_user.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ """
        contexto:dict = {
            'tab_title'   : 'new programmer',
            'head_title'  : 'Agregando un Nuevo Programador',
            'listbtn'     : (
                BtnWithImage(path='go-previous.svg',url='/administrator/view_programmers/',
                             label='Volver',msg=f'Volver a la Vista anterior'),
                BtnWithImage(path='home.svg',url='/administrator/',label='Home',
                            msg='Administracion, Vista Principal'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
        }

        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        contexto['form'] = CustomUserCreationForm()
        return render(request,self.template_name,contexto)

    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ """
        if request.POST.get("nok"):
            return self.render(request,*args,**kwargs)
    
        if request.POST.get("ok"):
            form = CustomUserCreationForm(request.POST )
            if not form.is_valid():
                messages.error(request, 'Por Favor Corrija el error y vuelva a intentarlo.')
                contexto = {'form' : form  }
                return self.render(request,context_ext=contexto,*args, **kwargs)

            nuser:User = form.save()
            prg = Programador(programador=nuser)
            prg.save()
            try:
                new_group, st = Group.objects.get_or_create(name=GROUPS.programmer)
                if st:
                    permission = Permission.objects.get(codename=PERMISSION.programmer) 
                    new_group.permissions.add(permission)
                ## volvemos a intentar agregar al grupo
                nuser.groups.add(Group.objects.get(name = GROUPS.programmer))
                log.info("%s::post_form() Get or Create Group, Status '%s' Name %s",
                        type(self).__name__,st,GROUPS.client)
            except Exception as e: 
                log.error("%s::render() Exception<%s> try create user, detail: e",
                          type(self).__name__,type(e).__name__,e)
                messages.error(request,f"No tenemos un Grupo con el nombre '{GROUPS.programmer}'.")
                return redirect('/administrator/')
        
            return redirect('/administrator/view_programmers/')

        return self.render(request,*args,**kwargs)


class NewAdministratorView(GroupMemberBaseView):
    """ Vista para un modulo en particular, ver o editar el mismo"""
    template_name = "administrator/form_new_user.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render(), User {request.user}")
        contexto:dict = {
            'tab_title'   : 'new administrator',
            'head_title'  : 'Agregando un Nuevo Administrador',
            'listbtn'     : (
                BtnWithImage(path='go-previous.svg',url='/administrator/view_useradmin/',
                             label='Volver',msg=f'Volver a la Vista anterior'),
                BtnWithImage(path='home.svg',url='/administrator/',label='Home',
                            msg='Administracion, Vista Principal'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
        }
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        contexto['form'] = CustomUserCreationForm()
        return render(request,self.template_name,contexto)
    

    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ handler for post from page """
        log.debug(f"{type(self).__name__}::post(), User {request.user}")

        if request.POST.get("nok"):
            return self.render(request,*args,**kwargs)
    
        if request.POST.get("ok"):
            form = CustomUserCreationForm(request.POST )
            if not form.is_valid():
                messages.error(request, 'Por Favor Corrija el error y vuelva a intentarlo.')
                contexto = {'form' : form  }
                return self.render(request,context_ext=contexto,*args, **kwargs)

            nuser:User = form.save()
            ## ahora le damos el permiso de staff
            nuser.is_staff = True
            nuser.save()
            try:
                new_group, st = Group.objects.get_or_create(name=GROUPS.admin)
                if st:
                    permission = Permission.objects.get(codename=PERMISSION.admin) 
                    new_group.permissions.add(permission)

                nuser.groups.add(Group.objects.get(name = GROUPS.admin))
                log.info("%s::post_form() Get or Create Group, Status '%s' Name %s",
                        type(self).__name__,st,GROUPS.client)
            except Exception as e: 
                log.error("%s::render() Exception<%s> try create user, detail: e",
                          type(self).__name__,type(e).__name__,e)
                messages.error(request,f"No tenemos un Grupo con el nombre '{GROUPS.admin}'.")
                return redirect('/administrator/')
        
            return redirect('/administrator/view_useradmin/')

        return self.render(request,*args,**kwargs)


class CompanyView(GroupMemberBaseView): 
    """ visualiza los datos de una compania (solo admin) """
    template_name:str = "administrator/view_company.html"
    method_set_attr:str = 'set_attr' 
    redirect_err_set_attr:str = '/administrator/view_companies/'

    group_name:str = GROUPS.admin
    is_superuser:bool = True

    # custom attributes
    company_id:int = None
    company:Empresa = None
    employees:QuerySet[User] = None
    STATICT_ITEMS:tuple[str] = ('nempleados', 'nticket_total', 'nticket_activos', 
                                'nticket_pendientes', 'nticket_cerrados'
                            )

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")
        self.company_id = kwargs.get('company_id',None)

        if self.company_id is None:
            log.error(f"{type(self).__name__}::set_attr() No se paso un company id valido")
            return False
        
        self.company:Empresa = None
        try:
            self.company = Empresa.objects.get(id=self.company_id)
        except Exception as e:
            log.error("Exception<%s> try get company for id <%s>, detail: %s",
                        type(e).__name__,self.company_id,e)
            messages.warning(request,f"No tenemos una empresa con el ID {self.company_id}.")
            return False
        
        try:
            self.employees = User.objects.filter(empresa=self.company)
        except Exception as e:
            log.error("Exception<%s> try User for company for id <%s>, detail: %s",
                        type(e).__name__,self.company_id,e)
            
        return True

    def statitics(self)->dict:
        """ calcula la estadistica para la empresa"""
        cls = type(self)
        ret:defaultdict = defaultdict(int)
        if self.employees is None:
            for k in cls.STATICT_ITEMS:
                ret[k] = 0
            return ret
                
        ret['nempleados'] = len(self.employees)

        for emp in self.employees:
            tickets:QuerySet[Tickets] = None
            try:
                tickets = Tickets.objects.filter(register=emp)
            except:
                continue
            ret['nticket_total'] += len(tickets)
            for tk in tickets:
                if tk.estado:
                    ret['nticket_activos'] += 1
                if not tk.register_estado and tk.estado:
                    ret['nticket_pendientes'] +=1
                
                if not tk.register_estado and not tk.estado:
                    ret['nticket_cerrados'] +=1

        return ret
    
    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::remder(), User {request.user}")
        contexto:dict = {
            'tab_title'     : 'company',
            'head_title'    : f'Informacion de la Compania "{self.company.nombre}"',
            'company'       : self.company,
            'companyinfo'   : self.statitics(),
            'list_users'    : self.employees,
            'listbtn'       : (
                BtnWithImage(path='go-previous.svg',url='/administrator/view_companies/',
                             label='Volver',msg = 'Volver a la Vista de Admin'),
                BtnWithImage(path='home.svg',url='/administrator/',label='Home', 
                            msg = 'Ir a la pagina Principal Home'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
            'urllink'       : 'administrator_app:UserConfigurationView',
            'urltitle'      : 'Click para expandir la Informacion de '  ,
            'urlbtn_add'    : f'/administrator/add_new_client/{self.company_id}',
            'titlebtn_add'  : f'Agregar Nuevo Cliente para la Empresa "{self.company.nombre}"'  ,
            'urlbtn_edit'   : '#',
            'titlebtn_edit' : f'¿Editar los Datos de la Empresa "{self.company.nombre}"?'  ,
            'urlbtn_del'    : '#',
            'titlebtn_del'  : f'¿Desea Eliminar la Empresa "{self.company.nombre}"?'
        }
        # titlebtn_edit, # titlebtn_del Son el text title de los botones y Titulos de los pop-up
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        contexto['auth_form'] = FormularioCheckUser()
        contexto['edit_companyForm'] = CompanyForm(instance=self.company)
        return render(request,self.template_name,contexto)

    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ handler for post from page """
        log.debug(f"{type(self).__name__}::post(), User {request.user}")

        if request.POST.get("ok"):        
            auth_form=FormularioCheckUser(data=request.POST)            
            if auth_form.check_pass(user=request.user):
                log.debug('%s::post_form() Se valido, la eliminacion de la empresa %s '\
                          'con el Usuario %s',type(self).__name__,self.company,request.user)
                
                try:
                    self.company.delete()
                except Exception as e:
                    # Falla la clave foranea con los Registros de Desarrollo
                    log.error('%s::post_form() Exception<%s> try delete regiseter Empresa<%s> '\
                              '.Detail %s.',
                              type(self).__name__,type(e).__name__,self.company,e)

                return redirect('/administrator/view_companies/')
            
            messages.error(request,f'La Contraseña Ingresada para "{request.user}" es incorrecta.')
            return self.render(request,*args,**kwargs)
  
        if request.POST.get("edit_nok"):            
            return self.render(request,*args,**kwargs)

        if request.POST.get("edit_ok"):        
            edit_companyForm=CompanyForm(request.POST)        
            if edit_companyForm.is_valid(instance=self.company):
                log.debug(f'Validamos, ahora podemos editar la empresa "{self.company}"')
                edit_companyForm.save(instance=self.company)
                return redirect(f'/administrator/view_company/{self.company_id}')
            
            else:
                messages.error(request,
                               'Fallo la Validacion Al intentar Editar el contendido '\
                               f'de la empresa "{self.company}".')
                contexto:dict = {
                    'auth_form'         : FormularioCheckUser(),
                    'edit_companyForm'  : edit_companyForm,
                    'companyForm_popUp' : True,
                }
                return self.render(request,context_ext=contexto,*args, **kwargs)
            
        return self.render(request,*args,**kwargs)


class UserConfigurationView(GroupMemberBaseView):
    """Modelo para la vista de configuracion de cada usuario"""
    template_name = "administrator/view_company_clients.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    redirect_err_set_attr:str  = '/administrator/'
    method_set_attr:str = 'set_attr'
    ## custom attribute
    user_id:int = None
    user:User = None
    user_group:str = None

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")

        self.user_id:int = kwargs.get('user_id',None)
        if self.user_id is None:
            return False
        
        try:
            self.user = User.objects.get(id=self.user_id)
        except Exception as e:
            log.error("%s::set_attr() Exception<%s> try get User for user id <%s>, detail: %s",
                type(self).__name__,type(e).__name__,self.user_id,e)
            return False
        
        if self.user.groups.filter(name=GROUPS.client).exists():
            self.user_group = GROUPS.client            
        elif self.user.groups.filter(name=GROUPS.programmer).exists():
            self.user_group = GROUPS.programmer
        else:
            self.user_group = GROUPS.admin
        
        return True


    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::remder(), User {request.user}, kwargs: {kwargs}")
        btn_prev_url:str = '/administrator/'
        if self.user_group == GROUPS.client:
            btn_prev_url:str = f'/administrator/view_company/{self.user.empresa.id}/'
        elif self.user_group == GROUPS.admin:
            btn_prev_url:str = f'/administrator/'
        else:
            btn_prev_url:str = f'/administrator/view_programmers/'

        contexto:dict = {
            'tab_title'  : f'config user {self.user}',
            'head_title' : f'Config User: {self.user}',
            'listbtn':  (
                BtnWithImage(path='go-previous.svg',url=btn_prev_url,
                                label='Volver', msg = f'Volver a la Vista principal'),
                BtnWithImage(path='home.svg',url='/administrator/',label='Home', 
                            msg = 'Ir a la pagina Principal Home'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),
            'titlebtn_edit' : f'Click para editar el usuario {self.user}',
            #'titlebtn_edit' : f'Click para editar el usuario {self.user.empresa.id}',
            'labelbtn_edit' : 'Editar',
            'luser'         : self.user,
            'statistics'    : self.statitics(),
        }
        if self.user == request.user:
            contexto['urlbtn_resetpass']   = 'administrator_app:ChangePassword'
            contexto['titlebtn_resetpass'] = 'Click para realizar el clean del Password de'
            contexto['labelbtn_resetpass'] = 'Reset Pass'
            contexto['change_self'] = True
        
        
        
        
        context_err = kwargs.get('context_err',None)
        if context_err is not None:            
            return render(request,self.template_name,context={**contexto,**context_err})
        
        contexto['auth_form'] = FormularioCheckUser()
        contexto['user_form'] = FormEditUser(data=self.user)
        return render(request,self.template_name,contexto)
    
    def post_form(self, request, *args, **kwargs)->HttpResponse:
        """ metodo que se encarga de manejar los post desde los forms """
        log.debug("%s::post_form(), User %s, request.POST %s",
                  type(self).__name__,request.user,request.POST)
                       
        if request.POST.get("ok") : #and request.user.is_superuser:
            auth_form=FormularioCheckUser(data=request.POST)
            ## Si el formulario es valido, obtenemos los datos.
            if auth_form.check_pass(user=request.user):
                company_id:int = None
                if self.user.empresa:
                    company_id = self.user.empresa.id

                log.debug("%s::post_form() Validamos, ahora podemos borrar el usuario %s",
                          type(self).__name__,self.user)
                try:
                    self.user.delete()
                except Exception as e:
                     # Falla la clave foranea con los Registros de Desarrollo
                    log.error('%s::post_form() Exception<%s> try delete regiseter User<%s> '\
                              '.Detail %s.',
                              type(self).__name__,type(e).__name__,self.user,e)

                if company_id is None:
                    return redirect('/administrator/')

                return redirect(f'/administrator/view_company/{company_id}/')
            
            log.debug("%s::post_form() La Contraseña Ingresada para <%s> es incorrecta.",
                        type(self).__name__,request.user)            
            messages.error(request,f'La Contraseña Ingresada para "{request.user}" es incorrecta.')
            
            self.render(request,*args, **kwargs)
    
        if request.POST.get("edit_nok"):            
            return self.render(request,*args, **kwargs)
    
        if request.POST.get("edit_ok"):
            log.debug(f"{type(self).__name__}::post(), request.POST.edit_ok")
            user_form = FormEditUser(request.POST)
            if user_form.is_valid(instance=self.user):
                log.debug(f"{type(self).__name__}::post(), save(), {request.POST}")
                user_form.save(instance=self.user)
                return self.render(request,*args, **kwargs)
            else:
                log.debug(f'{type(self).__name__}::post(), Form No validado')
                contexto:dict = {
                    'auth_form'      : FormularioCheckUser(),
                    'user_form'      : user_form,
                    'user_form_popUp': True,
                }
                return self.render(request,context_err=contexto,*args, **kwargs)

        return self.render(request,*args, **kwargs)

    def statitics(self)->dict:
        """ """        
        if self.user_group == GROUPS.admin:
            return None
        
        ret:dict = {
            'nticket'          : 0,
            'nticket_open'     : 0,
            'nticket_close'    : 0,
            'nticket_pending'  : 0,
            'nworks'           : 0,
            'nworks_open'      : 0,
            'nworks_close'     : 0,
            'nworks_pending'   : 0
        }
        tickets:QuerySet[Tickets] = None
        programmer:Programador = None
        works:QuerySet[Desarrollo] = None
        try:
            if self.user_group == GROUPS.client:
                tickets = Tickets.objects.filter(register=self.user)
            else:
                programmer = Programador.objects.get(programador=self.user)
                tickets = Tickets.objects.filter(attend=programmer)
                works = Desarrollo.objects.filter(asistente=programmer)

        except Exception as e:
            log.error(f'Exception<{type(e).__name__}>, detail: {e}')
            return ret
        
        ret['nticket'] = len(tickets)
        
        for tk in tickets:
            if tk.estado and tk.register_estado :
                ret['nticket_open'] += 1
                continue
    
            if not tk.estado and not tk.register_estado:
                ret['nticket_close'] += 1
                continue
    
            if tk.estado and not tk.register_estado:
                ret['nticket_pending'] += 1
            
        if programmer is None:
            return ret
                
        ret['nworks'] = len(works)
        for wk in works:
            if wk.estado:
                ret['nworks_open'] += 1
            else:            
                ret['nworks_close'] += 1

        ret['nworks_pending'] = ret['nworks_open']    
        return ret


class ConfigUserClientView(GroupMemberBaseView):
    """ Vista para la Configuracion de usuario no staff Cliente o programador"""
    template_name:str = "administrator/view_company_clients.html"
    group_name:tuple[str] = (GROUPS.client,GROUPS.programmer)
    
    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::remder(), User {request.user}, kwargs: {kwargs}")
        user:User = request.user
        
        company:str = user.empresa
        btn_prev_url:str = '/register_ticket/'

        if self.in_group == GROUPS.programmer:
            btn_prev_url:str = '/attend_ticket/'
            company = GROUPS.programmer

        
        contexto:dict = {
            'tab_title'    : '{} {}'.format(company,user),
            #'head_title'   : '{}, {}'.format(company.title(), user),
            'head_title'   : '{}, {}'.format(company, user),
            'listbtn': (
                BtnWithImage(path='go-previous.svg',
                                url = btn_prev_url,
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


class ChangePasswordView(GroupMemberBaseView):
    """ Vista para la Configuracion de usuario Cliente  """
    template_name:str = "administrator/clean_password.html"
    #group_name:tuple[str] = (GROUPS.client,GROUPS.programmer)
    group_name:tuple[str] = GROUPS
    is_superuser:bool = True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render(), User {request.user}, kwargs: {kwargs}")
        user:User = request.user
        
        contexto:dict = {
            'tab_title':'clean password'
        }

        match self.in_group:
            case  GROUPS.client:
                contexto['head_title'] = f'Clean del Password "{user.empresa}, {user.username}"'
                contexto['urlbtn_cancel'] = '/administrator/view_config_nonadmuser/'

            case GROUPS.programmer:
                contexto['head_title'] = f'Clean del Password Programador "{user.username}"'
                contexto['urlbtn_cancel'] = '/administrator/view_config_nonadmuser/'
            
            case _: # self.in_group == GROUPS.admin or request.user.is_superuser                
                contexto['head_title'] = f'Clean del Password Administrador "{user.username}"'
                contexto['urlbtn_cancel'] = '/administrator/'
            

        log.debug(f"{type(self).__name__}::render(), in_group {self.in_group}")
        contexto['listbtn'] = (
            BtnWithImage(path='go-previous.svg',url=contexto['urlbtn_cancel'], label='Volver', 
                    msg = 'Volver a la Vista de Admin'),        
            BtnWithImage(path='exit.png',url='/logout',label='Salir') 
        )

        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})

        contexto['form'] = SetPasswordForm(user=user)     
        return render(request,self.template_name,contexto)
    
    def post_form(self, request, *args, **kwargs)->HttpResponse:
        """ metodo que se encarga de manejar los post desde los forms """
        log.debug(f"{type(self).__name__}::post_form(), User {request.user}")
        user:User = request.user

        if not request.POST.get("ok") and not request.POST.get("nok"):
            contexto:dict = { 'form':SetPasswordForm(user=user, data=request.POST )}            
            return self.render(request,context_ext=contexto,*args, **kwargs)
          
        if request.POST.get("nok"):
            return self.render(request,*args,**kwargs)
    
        form = SetPasswordForm(user=user, data=request.POST )    
        if form.is_valid():
            user = form.save()            
            EmailThread(registro=user, password = {'new_password':request.POST["new_password2"]},
                        msg=f'clean of password user {user}',
                        header=f'Clean de Contraseña User "{user}"').start()
      
            ## Importante actualizamos la sesion para el usuario que setablecio su nueva password
            update_session_auth_hash(request, user)  
            messages.success(request, 
                            f"La Contraseña para el usuario '{user.username}' "\
                            "se modifico de forma Sastifactoria!")
            
            url_redirect:str = None
            if self.in_group == GROUPS.client:                
                url_redirect = '/register_ticket/'

            elif self.in_group == GROUPS.programmer:                
                url_redirect = '/attend_ticket/'

            elif self.in_group == GROUPS.admin or request.user.is_superuser:                
                url_redirect = '/administrator/'
            
            return redirect(url_redirect)

        
        messages.error(request, 'Por Favor Corrija el error y vuelva a intentarlo.')
        contexto:dict = {'form': form}
        return self.render(request,context_ext=contexto,*args, **kwargs)


class AddNewClientView(GroupMemberBaseView):
    """ Vista para la Configuracion de usuario Cliente  """
    template_name:str = "administrator/form_new_user.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True
    method_set_attr:str = 'set_attr'
    redirect_err_set_attr:str  = '/administrator/view_companies/'
    # custom attrubutes
    company:Empresa = None
    company_id:int = None

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")
        
        self.company_id = kwargs.get('company_id',None)
        if self.company_id is None:
            log.error("%s::set_attr() se apso un company_id valido",type(self).__name__)
            return False

        try:
            self.company = Empresa.objects.get(id=self.company_id)
        except Exception as e:
            log.error("Exception<%s> try get Empresa for company id <%s>, detail: %s",
                        type(e).__name__,self.company_id,e)
            return False
        
        return True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render(), User {request.user}, kwargs: {kwargs}")

        contexto:dict = {
            'tab_title'  : 'new client',
            'head_title' : f'Agregando un Nuevo Cliente para la empresa: "{self.company}"',
            'listbtn'    : (
                BtnWithImage(path='go-previous.svg',url=f'/administrator/view_company/{self.company_id}',
                            label='Volver',msg = f'Volver a la Vista anterior'),
                BtnWithImage(path='home.svg',url='/administrator/',label='Home',
                            msg='Administracion, Vista Principal'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ),            
            'is_superuser': request.user.is_superuser,
        }

        new_user:User = None
        try:
            # No deberiamos lanzar exception
            new_user:User = User(empresa = self.company)
        except Exception as e:    
            log.error('%s::render() Exception<%s>, detail: %s',
                      type(self).__name__,type(e).__name__,e) 

        log.debug('%s::render() company <%s>, user: %s',
                  type(self).__name__,self.company,new_user.to_str())
        
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})
        
        if new_user is not None:
            contexto['form'] = NewUserForm(instance=new_user)
        else:            
            contexto['form'] = NewUserForm()
                
        return render(request,self.template_name,contexto)

    def post_form(self, request, *args, **kwargs)->HttpResponse:
        """ metodo que se encarga de manejar los post desde los forms """
        log.debug(f"{type(self).__name__}::post_form(), User {request.user}")

        contexto:dict = {}
        log.debug(f"{type(self).__name__}::post_form(), POST: {request.POST}") 

        if request.POST.get("nok"):
            return self.render(request,*args,**kwargs)
    
        if request.POST.get("ok"):
            form = NewUserForm(request.POST )        
            if not form.is_valid():
                messages.error(request, 'Por Favor Corrija el error y vuelva a intentarlo.')
                contexto:dict = {'form' : form}                
                return self.render(request,context_ext=contexto,*args, **kwargs)

            nuser:User = form.save()
            if nuser.empresa is None:
                nuser.empresa = self.company
                nuser.save()

            try:                
                new_group, st = Group.objects.get_or_create(name=GROUPS.client)                  
                permission = Permission.objects.get(codename=PERMISSION.client)
                new_group.permissions.add(permission)
                ## volvemos a intentar agregar al grupo
                nuser.groups.add(Group.objects.get(name = GROUPS.client))                
                log.info("%s::post_form() Get or Create Group, Status '%s' Name %s",
                        type(self).__name__,st,GROUPS.client)
            except Exception as e:
                log.info("%s::post_form() try create Group %s, detail %s",
                        type(self).__name__,GROUPS.client,e)
                
                messages.error( request,
                                f"Error al intentar Obtener o Crear el Grupo '{GROUPS.client}'.")
                return redirect('/administrator/view_admin/')

            log.info("%s::post_form() Se creo Nuevo Cliente <%s> para la Empresea <%s>",
                        type(self).__name__,nuser.to_str(),self.company)
            
            return redirect(f"/administrator/view_company/{self.company_id}")

        contexto:dict = {'form' : NewUserForm(request.POST)}
        return self.render(request,context_ext=contexto,*args, **kwargs)
    

class ListTicketsViews(GroupMemberBaseView):
    """ Vista para listado de tockets """
    template_name:str = "administrator/view_ticket.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True
    method_set_attr:str = 'set_attr'
    redirect_err_set_attr:str  = '/administrator/view_tickets/'
    
    # custom attributes
    tickets:QuerySet[Tickets] = None
    ticket_id:int = None
    ticket:Tickets = None

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")
        self.ticket_id = kwargs.get('ticket_id',None)
        try:
            self.tickets = Tickets.objects.all().order_by('id')
        except Exception as e:
            log.error("%s::render() Exception<%s> in query for Tickets. Detail %s",
                      type(self).__name__,type(e).__name__,e)
            self.tickets = []

        if self.ticket_id is None or len(self.tickets) == 0:
            return True
        
        self.ticket = next((tk for tk in self.tickets if tk.id == self.ticket_id), None)        
        return True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render(), User {request.user}")

        contexto:dict = {
            'tab_title'  : 'ticket',
            'head_title' : 'Lista de Tickets',
            'listbtn'    : (
                BtnWithImage(path='go-previous.svg',url=f'/administrator/',label='Volver',
                            msg = 'Administracion, Vista Principal'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')),
            'luser'      : request.user,
            'all_ticket' : self.tickets,
            'urllink'    : 'administrator_app:ListTicketsViews',
            'urltitle'   : 'Click para editar la Informacion del Ticket '              
        }
        
        if self.ticket_id is None:
            context_ext = kwargs.get('context_ext',None)
            if context_ext is not None:            
                return render(request,self.template_name,context={**contexto,**context_ext})
            
            contexto['form_search'] = FormSearchTicket()
            return render(request,self.template_name,contexto)
        
        if self.ticket is None:
            messages.warning(request,f"No tenemos un Ticket con id '{self.ticket_id}'.")
            return redirect('/administrator/view_tickets/')
        

        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})
        
        contexto['lticket'] = self.ticket
        contexto['ticket_form'] = FormEditTicket(instance=self.ticket)
        

        return render(request,self.template_name,contexto)

    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ handler for post from page """
        log.debug(f"{type(self).__name__}::post(), User {request.user}")
        log.debug(f"{type(self).__name__}::post_form() POST: {request.POST}")

        
        if request.POST.get("edit_nok") :#or request.POST.get("tk_nsearch"):
            return redirect('/administrator/view_tickets/')
    
        if request.POST.get("edit_ok"):
            ticket_form = FormEditTicket(request.POST)            
            if ticket_form.is_valid():
                ticket_form.save(instance=self.ticket)
                return redirect('/administrator/view_tickets/')
            # Es un pop-up no es enecesario automaticamente lo coloca
            #messages.error(request,
            #               f'Error Intentado Editar el ticket "{self.ticket_id}" '\
            #                'Corrija y vuelva a intentarlo.')
            
            contexto:dict = {'ticket_form' :ticket_form}                          
            return self.render(request,context_ext=contexto,*args, **kwargs)        
        
        if request.POST.get("tk_search"):
            search_form = FormSearchTicket(data=request.POST)
            log.debug(f"{type(self).__name__}::post_form() Search: {request.POST['tk_search']}")
            contexto:dict = {
                'all_ticket' : search_form.get_queryset(self.tickets),
                'form_search' : search_form
            }
            return self.render(request,context_ext=contexto,*args, **kwargs)
        
        if request.POST.get("tk_nsearch"):
            # clean del search form            
            contexto:dict = {                
                'form_search' : FormSearchTicket()
            }
            return self.render(request,context_ext=contexto,*args, **kwargs)

        if request.POST.get("company") != '':
            search_form = FormSearchTicket(data=request.POST)          
            contexto:dict = {                
                'form_search' : search_form.update_form(company=request.POST.get("company"))
            }
            return self.render(request,context_ext=contexto,*args, **kwargs)
        
        return self.render(request,*args,**kwargs)


class ListDesarrollosViews(GroupMemberBaseView):
    """ Vista para listado de tockets """
    template_name:str = "administrator/view_desarrollos.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render(), User {request.user}")
        
        desarrollos:QuerySet[Desarrollo] = None
        try:
            desarrollos = Desarrollo.objects.all().order_by('id')
        except Exception as e:
            log.error("%s::render() Exception<%s> try get Object in table Desarrollo. Detail %s.",
                      type(self).__name__,type(e).__name__,e)

        contexto = {
            'tab_title'       : 'developing',
            'head_title'      :'Lista de Pedidos de Desarrollos',
            'desarrollos_all' : desarrollos,
            'listbtn'         : (
                BtnWithImage(path='go-previous.svg',url='/administrator/',label='Volver',
                            msg = 'Volver a la Vista de Admin'),
                BtnWithImage(path='config.png',url='/admin/',label='Sys Admin',
                            msg='Ingresar al Administrador del Sistema'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir')
            ) ,
            'urllink'         : 'administrator_app:DesarrolloViews',
            'urltitle'        : 'Click para ver la Orden de Trabajo ',
            'urlbtn_add'      : '/new_development_order/',
            'titlebtn_add'    : "Crear un Nuevo Pedido de Desarrollo"
        }
        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})
        
        contexto['form'] = FormularioDesarrollo()
        return render(request,self.template_name,contexto)


    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ handler for post from page """
        log.debug(f"{type(self).__name__}::post(), User {request.user}")

        if request.POST.get("formok"):
            form = FormularioDesarrollo(request.POST,files=request.FILES )
            if form.is_valid():
                norderwork = form.save(register=request.user)
                log.debug("%s::post_form() Se creo una nueva Orden de Trabajo '%s'",
                          type(self).__name__,norderwork)
                
                return redirect('/administrator/view_desarrollos/')
            
            contexto:dict = {
                'form' : form,
                'err_form' : form
            }
            return self.render(request,context_ext=contexto,*args, **kwargs)

        #if request.POST.get("nok"):
        #    return redirect('/administrator/view_desarrollos/')
        
        return self.render(request,*args, **kwargs)


class DesarrolloViews(GroupMemberBaseView):
    """ Vista para listado de tockets """
    LOCAL_TIME = timezone.now()
    template_name:str = "administrator/view_desarrollos_works.html"
    group_name:str = GROUPS.admin
    is_superuser:bool = True
    method_set_attr:str = 'set_attr'
    redirect_err_set_attr:str  = '/administrator/view_desarrollos/'
    
    # custom attributes
    registro_trabajo:QuerySet[RegistroTrabajo] = None
    desarrolo:Desarrollo = None
    develop_id:int = None

    def set_attr(self, request:HttpRequest, *args, **kwargs)->bool:
        """metodo get que se encarga de validar que los usaurios se corresponda a la vista"""
        log.info(f"{type(self).__name__}::set_attr() user: {request.user} | kwargs: {kwargs}")
        self.develop_id = kwargs.get('develop_id',None)
        if self.develop_id is None:
            return False

        try:
            self.desarrolo = Desarrollo.objects.get(id=self.develop_id)
            self.registro_trabajo = RegistroTrabajo.objects.filter(
                desarrollo=self.develop_id).order_by('-id')
        except Exception as e:
            log.error("%s::set_attr() Exception<%s> in get Desarrollo and RegistroTrabajo"\
                      " develop_id: %d. Detail: %s",
                    type(self).__name__,type(e).__name__,self.develop_id,e)
            return False

        return True    

    def render(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """Metodo que se encarga de renderizar sobre el template"""
        log.debug(f"{type(self).__name__}::render(), User {request.user}")
        contexto:dict = {
            'tab_title'  : f'developmen {self.develop_id}, details',
            'head_title' : f'Detalle de la Orden de Desarrollo {self.develop_id}',
            'listbtn'    : (
                BtnWithImage(path='go-previous.svg',url='/administrator/view_desarrollos/',
                             label='Volver'),
                BtnWithImage(path='home.svg',url='/administrator/',label='Home',
                            msg = 'Administracion, Vista Principal'),
                BtnWithImage(path='exit.png',url='/logout',label='Salir') 
            ),
            'developmen' : self.desarrolo,
            'developmenIdWork' : self.registro_trabajo
        }

        word:str = kwargs.get('word','')
        if word == 'close' and self.desarrolo.estado:
            self.desarrolo.estado = False
            self.desarrolo.save()
            ## enviamos los emails
            EmailThread(registro=self.desarrolo,msg=f'close development order {self.desarrolo.id}',
                        header=f'Orden de Desarrollo "{self.desarrolo.id}" Cerrada').start()
            
            EmailThread(attend=True,registro=self.desarrolo,
                        msg=f'close development order {self.desarrolo.id}',
                        header=f'Orden de Desarrollo "{self.desarrolo.id}" cerrada').start()

            return redirect(f'/administrator/view_desarrollos_works/{self.develop_id}/')
        
        elif word == 'open' and not self.desarrolo.estado:
            self.desarrolo.estado = True
            self.desarrolo.save()
            EmailThread(
                registro=self.desarrolo,msg=f'open development order {self.desarrolo.id}',
                header=f'Orden de Desarrollo "{self.desarrolo.id}" Abierta'
            ).start()
            
            EmailThread(
                attend=True,registro=self.desarrolo,
                msg=f'open development order {self.desarrolo.id}',
                header=f'Orden de Desarrollo "{self.desarrolo.id}" Abierta'
            ).start()
            ## nos redirecionamos a esta vista, para actualizar el contexto
            return redirect(f'/administrator/view_desarrollos_works/{self.develop_id}/')
        

        context_ext = kwargs.get('context_ext',None)
        if context_ext is not None:            
            return render(request,self.template_name,context={**contexto,**context_ext})


        ## add forms data
        contexto['form_popup02'] = FormularioRegistroTrabajo()
        contexto['form_popup03'] = FormularioSetDesarrollo(instance=self.desarrolo) 
    
        ## consultamos si debemos embiar el formulario para editar un Registro de Trabajo.
        if len(self.registro_trabajo) > 0 and not self.registro_trabajo[0].programmer:
            contexto['form_popup04'] = FormularioEditRegistroTrabajo(instance=self.registro_trabajo[0])
            contexto['id_form_popup04'] = self.registro_trabajo[0].programmer
        
        if self.registro_trabajo is not None and len(self.registro_trabajo) == 0:
            contexto['form_popup01'] = FormularioEditDesarrollo(instance=self.desarrolo)          
        
        #contexto['launch_form_popup01'] = False
        return render(request,self.template_name,contexto)

    def post_form(self,request:HttpRequest,*args, **kwargs)->HttpResponse:
        """ handler for post from page """
        log.debug(f"{type(self).__name__}::post(), User {request.user}")
        cls = type(self)

        if request.POST.get("okpopUp01"):
            formulario = FormularioEditDesarrollo(data=request.POST,files=request.FILES)
            if formulario.is_valid():
                formulario.save(instance=self.desarrolo)
                return redirect(f'/administrator/view_desarrollos_works/{self.develop_id}/') 

            contexto = {
                'err_form_popup01' : True,
                'form_popup01'     : formulario
            }
            return self.render(request,context_ext=contexto,*args, **kwargs)
    
        elif request.POST.get("okpopUp02"):
            formulario = FormularioRegistroTrabajo(data=request.POST,files=request.FILES)
            if formulario.is_valid():
                formulario.save(desarrollo=self.desarrolo,
                                register_work=request.user,
                                localtime = cls.LOCAL_TIME)
                return redirect(f'/administrator/view_desarrollos_works/{self.develop_id}/') 
            
            contexto = {
                'form_popup02' : formulario,
                'err_form_popup02' : True
            }
            return self.render(request,context_ext=contexto,*args, **kwargs)
    
        elif request.POST.get("okpopUp03"):
            formulario = FormularioSetDesarrollo(data=request.POST)                        
            if formulario.is_valid():              
                formulario.save(instance=self.desarrolo)
                return redirect(f'/administrator/view_desarrollos_works/{self.develop_id}/') 

            messages.warning(request, 'Datos Invalidos')
            contexto = {'form_popup03':formulario}
            return self.render(request,context_ext=contexto,*args, **kwargs)
    
        elif request.POST.get("okpopUp04"):
            formulario = FormularioEditRegistroTrabajo(data=request.POST,files=request.FILES)                        
            if formulario.is_valid():
                formulario.save(instance=self.registro_trabajo[0])
                return redirect(f'/administrator/view_desarrollos_works/{self.develop_id}/') 
            
            contexto:dict = {
                'err_form_popup04' : True,
                'form_popup04' : formulario
            }
            messages.warning(request, 'Datos Invalidos')
            return self.render(request,context_ext=contexto,*args, **kwargs)
              
        elif request.POST.get("nok"):          
            return redirect(f'/administrator/view_desarrollos_works/{self.develop_id}/') 
                
        # 
        return self.render(request,*args, **kwargs)