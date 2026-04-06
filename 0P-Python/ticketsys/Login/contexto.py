# buil-in import
import sys
import threading , time
from logging import getLogger,Logger

# framework import
from django.db.models import QuerySet
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet


# Project Modules import
from config.settings import (HOSTING_URL, EMAIL_HOST_USER,EMAIL_REPLY_TO,EMAIL_SEND_RETRY)
from Login.models import User
from Ticket.models import (Tickets, RegisterWork, Desarrollo, RegistroTrabajo)
from config.settings import DEBUG
from Login.constants import GROUPS

log:Logger = getLogger('Login')



#  Clase para obtener el 
#  choice de forma estatica, para no perder la seleccion
#  cuando se desea reordenar una columna
#  en particular
class Choice:
    _id_choice = None
  
    def get(self,**kwargs):
        """      
        kwargs:
            * post
            * groups
        """
        post   = kwargs.get('post',{})
        groups = kwargs.get('groups','choice')
        
        if groups in post.keys():
            type(self)._id_choice=post[groups]
        else:
            return None
        
        return type(self)._id_choice
  
    def set(self,**kwargs):
        choice = kwargs.get('id_choice',None)
        if choice is None:
            return
        
        type(self)._id_choice = choice


    id_choice = property(get)


class EmailThread(threading.Thread):
    def __init__(self,**kwargs):
        """ kwargs :
            + attend : False|True , indicamos 'True' si debemos mandarle el meil al programador y 
            no al cliente. Por defecto es False
            + registro
            + msg
            + header        
            + email : dict {}
                  'headerbody': <>
                  'body':<>
                  'from':<>
                  'tolist':<>
                  'reply':<>
                  'header':<>
        """
        registro = kwargs.get('registro',None)
        msg = kwargs.get('msg','')
        attend = kwargs.get('attend',False)
        password = kwargs.get('password',None)
        self.header:str = kwargs.get('header','')
        self.retry:int = EMAIL_SEND_RETRY
        self.meilList:list[str] = None
        self.email:str = None
        
        if registro is None:
            body = kwargs.get('email',None)
            if body is not None and len(body['tolist']) > 0:
                self.email = EmailMessage(body['headerbody'],body['body'],EMAIL_HOST_USER,
                                          body['tolist'],reply_to=[EMAIL_REPLY_TO],
                                          headers=body['header']) 
          
                log.debug(f'Lista de email {body["tolist"]}')
            else:
                self.email = None
    
            threading.Thread.__init__(self)
            return
   
        if not attend and isinstance(registro,RegisterWork):
            if isinstance(registro.ticket.email,str):
                self.meilList = registro.ticket.email.split()
            else:
                self.meilList = registro.ticket.email
  
            if not registro.ticket.register.email in self.meilList and\
                  registro.ticket.register.email != '':
                self.meilList.append(registro.ticket.register.email)

            self.msgBody = f'{msg} url: {HOSTING_URL}/register_ticket/expand_ticket/{registro.ticket.id}/'
            self.msgBody += f'\nMensaje: \n{registro.msg}'
            self.email = EmailMessage(self.header,self.msgBody,
                                      EMAIL_HOST_USER,self.meilList,
                                      reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'}) 
            threading.Thread.__init__(self)
            return
  
        if attend and isinstance(registro,RegisterWork):
            url = None
            if registro.ticket.attend is not None:
                self.meilList = [registro.ticket.attend.programador.email]
                url = f'url: {HOSTING_URL}/attend_ticket/expand_attend_ticket/{registro.ticket.id}/'
            else:
                self.meilList = self.GetEmailList(grupo='admin')
                url = f'url: {HOSTING_URL}/edit_ticket_register/{registro.ticket.id}/'
            self.msgBody = f'{msg} {url}'
            self.msgBody += f'\nMensaje: \n{registro.msg}' 
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'}) 
            threading.Thread.__init__(self)
            return
  
        if not attend and isinstance(registro,Tickets):
            url = None
            if isinstance(registro.email,str):
                self.meilList = registro.email.split()
            else:
                self.meilList = registro.email 
            
            if registro.register and not registro.register.email in self.meilList and registro.register.email != '':
                self.meilList.append(registro.register.email)
    
            url = f'{HOSTING_URL}/register_ticket/expand_ticket/{registro.id}/'
            self.msgBody = f'{msg} {url}'
            self.msgBody += f'\nModulo: \n\t{registro.brief}'
            self.msgBody += f'\nMensaje: \n\t{registro.detail}'
    
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'}) 
            threading.Thread.__init__(self)
            return
          
        if attend and isinstance(registro,Tickets):
            url = None        
            if registro.attend is not None:
                  self.meilList = [registro.attend.programador.email,]
                  url = f'url: {HOSTING_URL}/attend_ticket/expand_attend_ticket/{registro.id}/'
            else:
                  self.meilList = self.GetEmailList(grupo='admin')
                  url = f'url: {HOSTING_URL}/edit_ticket_register/{registro.id}/'
          
            self.msgBody = f'{msg} {url}'
            self.msgBody += f'\nModulo: \n\t{registro.brief}'
            self.msgBody += f'\nMensaje: \n\t{registro.detail}'
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,self.meilList,
                                      reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'})
            threading.Thread.__init__(self)
            return
        
        if isinstance(registro,User):
            #GetGroupCurrentUser(user=registro)
            grupo = registro.groups.values_list('name', flat=True) 
            if len(grupo) == 0:
                log.debug(f'Usuario {registro} con grupo fuera de rango')
                threading.Thread.__init__(self)
                return
            
            url = f'url: {HOSTING_URL}/view_config_user/'
            if registro.email not in (None,''):
                self.meilList = [registro.email]            
                self.msgBody = f'{msg} {url}'
    
            else:
                if grupo == 'client':
                    if registro.empresa is not None and registro.empresa.email not in (None,''):
                        self.msgBody = f'{msg}'
                        self.meilList = [registro.empresa.email]
                    else:
                        ## No tenemos listado de meil para el
                        threading.Thread.__init__(self)
                        return
      
                elif grupo in ('programador','admin','superuser'):
                    self.msgBody = f'{msg}'
                    self.meilList = self.GetEmailList(grupo='admin')

                else:
                    ## El usuario no pertenece a un grupo valido
                    log.debug('Usuario %s Grupo %s email: %s, no pertenece a un grupo valido',
                              registro,grupo,self.meilList)
                    threading.Thread.__init__(self)
                    return
    
            if self.meilList is None:
                threading.Thread.__init__(self)
                return
            
            self.msgBody += f'\nNombre Usuario: \t{registro.username}'                
            if password is not None and password in ('old_password','new_password'):
                self.msgBody += f'\nContraseña: \t Antigua: {password["old_password"]} , '
                self.msgBody += f'Nueva: {password["new_password"]}'
    
            elif password is not None and 'new_password' in password:
                self.msgBody = f'{msg} url: {HOSTING_URL}/'                  
                self.msgBody += f'\nContraseña Nueva: {password["new_password"]}'
    
            self.msgBody += f'\nNombre Completo: \t{registro.get_full_name()}'
            self.msgBody += f'\nDireccion Correo: \t{registro.email}'
            
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'})
            threading.Thread.__init__(self)
            return
  
        if not attend and isinstance(registro,Desarrollo):
            self.meilList = self.GetEmailList(grupo='admin')
            url = f'url: {HOSTING_URL}/view_desarrollos_works/{registro.id}/'
            if self.meilList is None:
                self.meilList = []
            
            if registro.email is not None and len(registro.email) > 0:
                if isinstance(registro.email,str):
                    self.meilList.extend(registro.email.split())
                else:
                    self.meilList.extend(registro.email)          
            
    
            self.msgBody = f'{msg} {url}'        
            self.msgBody += f'\nMensaje: \n\t{registro.descripcion}'
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'}) 
            threading.Thread.__init__(self)
            return
        
        if attend and isinstance(registro,Desarrollo):
            url = None        
            if registro.asistente is not None:
                self.meilList = [registro.asistente.programador.email]
                url = f'url: {HOSTING_URL}/attend_ticket/view_desarrollos_works/{registro.id}/'
    
            self.msgBody = f'{msg} {url}'        
            self.msgBody += f'\nMensaje: \n\t{registro.descripcion}'
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'}) 
            threading.Thread.__init__(self)
            return
        
        if not attend and isinstance(registro,RegistroTrabajo):
            self.meilList = self.GetEmailList(grupo='admin')
            url = f'url: {HOSTING_URL}/view_desarrollos_works/{registro.id}/'        
            if self.meilList is None:
                self.meilList = []
            
            if registro.desarrollo.email is not None and len(registro.desarrollo.email) > 0:
                if isinstance(registro.desarrollo.email,str):
                    self.meilList.extend(registro.desarrollo.email.split())
                else:
                    self.meilList.extend(registro.desarrollo.email)
            self.msgBody = f'{msg} {url}'        
            self.msgBody += f'\nMensaje: \n\t{registro.msg}'
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'})
            threading.Thread.__init__(self)
            return
        
        if attend and isinstance(registro,RegistroTrabajo):
            url = None        
            if registro.desarrollo.asistente is not None:
                self.meilList = [registro.desarrollo.asistente.programador.email]
                url = f'url: {HOSTING_URL}/attend_ticket/view_desarrollos_works/{registro.id}/'
    
            if self.meilList is None:
                self.meilList = []
            
            if registro.desarrollo.email is not None and len(registro.desarrollo.email) > 0:
                if isinstance(registro.desarrollo.email,str):
                    self.meilList.extend(registro.desarrollo.email.split())
                else:
                    self.meilList.extend(registro.desarrollo.email)
    
            self.msgBody = f'{msg} {url}'        
            self.msgBody += f'\nMensaje: \n\t{registro.msg}'
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro.id}'}) 
            threading.Thread.__init__(self)
            return
  
        if isinstance(registro,str):
            if not 'admin' in registro and not 'programador' in registro:
                log.debug(f'registro {registro} no contemplado')
                threading.Thread.__init__(self)
                return
            
            self.msgBody = f'{msg}'
            self.meilList = self.GetEmailList(grupo=registro)
   
            ## si no tenemos email cargados aun, o cuerpo para el meil salimos
            if self.meilList is None or self.msgBody is None:
              threading.Thread.__init__(self)
              return
            
            self.email = EmailMessage(self.header,self.msgBody,EMAIL_HOST_USER,
                                      self.meilList,reply_to=[EMAIL_REPLY_TO],
                                      headers={'Message-ID': f'REG-{registro}'}) 
            threading.Thread.__init__(self)
            return
        


    def GetEmailList(self,**kwargs)->list[str]:
        """ funcion para obtener el listado de meil de un grupo particular
        kwargs :    
            - grupo = admin | empresa | programador       
            
        return 
            + Failure:  []
    
            + success: list ['user': obj, 'ticket': obj, '': obj]
        """
        typeUser = kwargs.get('grupo',None)
        if typeUser is None:
            log.debug("Error falta el parametro mandatorio 'user'")
            return []
        
        targetUser:dict = {
            'admin': GROUPS.admin,
            'programador': GROUPS.programmer,
            'empresa': GROUPS.client
        }
    
        if typeUser not in targetUser.keys():
            log.debug(f"Error {typeUser} no se corresponde con ninguno de {targetUser}")
            return []
    
        allUsers:QuerySet[User] = None
        groupName = None
        groupName = targetUser[typeUser]
            
        try:
            allUsers = User.objects.filter(groups=Group.objects.get(name = groupName))
        except:
            log.debug(f"failure: query User.objects.filter(groups=Group.objects.get(name = %s) => %s",
                        groupName,sys.exc_info()[0])
    
        # targetUser = ('admin' , 'empresas' , 'programador')
        if allUsers is None or len(allUsers) == 0:
            return []
        
        rval = set()
        if  typeUser == 'empresa':
            for it in allUsers:
                if it.empresa.email in (None ,''):
                    continue

                rval.add(it.empresa.email)            
        else:
            for it in allUsers:
                if it.email in (None,''):
                    continue

                rval.add(it.email)  
    
        return list(rval)


 
    def __str__(self)->str:
        """
        self.header:str
        self.retry:int
        self.meilList:list[str]
        self.email:str
        """
        #return f'Email List: "{self.meilList}" | Header: "{self.header}" '
        return f'Email List {self.meilList} | Header {self.header} | msg: {self.msgBody}\n'
  
    def run(self):
        if self.email is None:
            ## no pudo armar el objeto email
            log.debug(f'Falta el Objeto email, Faltan parametros en la inicializacion.')
            return

        if self.meilList is not None:
            i = len(self.meilList)
            j = 0
            while j < i:        
                if(self.meilList[j] == ''):
                   self.meilList.pop(j)
                   i -= 1
                j += 1
            ## debe estar el valor para poder removerlo 
    
        if self.meilList is None or len(self.meilList) == 0:
            log.debug(f'No tenemos Correos para enviar el Mensaje. "{self}"')
            return
        
        ## testing
        if  DEBUG:
            log.debug(f'Enviando Email {self}')
            return   
    
        while self.retry > 0 and self.meilList is not None and self.email is not None:
            try:
                self.email.send()
                log.debug(f'Envio de Email Sastifactorio {self}')
                break
            except:
                log.debug(f'Fallo el envio de Email %s, error: %s, wait = 100 ms',
                          self,sys.exc_info()[0])
                self.retry -= 1
                time.sleep(0.100)
  