# buil-in import
from logging import getLogger,Logger


# framework import
from django.forms import Form, ChoiceField, ModelChoiceField
from django.utils.translation import gettext as _
from django.forms import (Form, ModelChoiceField)


# Project Modules import
from Ticket.models import Modulos


# Get an instance of a logger
log:Logger = getLogger('attendticket') 


TICKET_STATUS_CHOICE:list[tuple] = [
    ('all'     ,'Todos'),
    ('open'    ,'Abiertos'),
    ('pending' ,'Pendientes'),
    ('close'   ,'Cerrados')
]
           
TICKET_ASIGNACION_CHOICE:list[tuple] = [
    ('to_me' ,'A mi'),
    ('all'   ,'Todos'),
    ('other' ,'A otros'),
    ('none'  ,'Sin Asignar')
]                        



class FormSearchIssueAttend(Form):
    """
      * ticketStatus
      * ticketAsignacion
      * ticketModulo
    """ 
    ticketStatus:ChoiceField =  ChoiceField(
        label = 'Estado Ticket',choices=TICKET_STATUS_CHOICE,required = False
    )
  
    ticketAsignacion:ChoiceField = ChoiceField(
        label = 'Asignacion',choices=TICKET_ASIGNACION_CHOICE,required = False
    )
  
    ticketModulo:ModelChoiceField = ModelChoiceField(
        empty_label="Todos",label = 'Modulo',queryset=Modulos.objects.all(),required=False
    )  
   
    def getSelection(self,**kwargs):
        """ Funcion que realiza la busqueda en funcion de los parametros pasados 
            en el formulario.
        kwargs
            <> context : Podemos pasarle un cotexto para que almacene los valores :
                * context['empresa']
                * context['programador']
                * context['AcuTime']
                * context['dateFrom']
                * context['dateTo']
                * context['all_regwork']
                * context['enAllMsg']
              
              Si estos son validos.
        """
        programador = kwargs.get('programador',None)
        if programador is None:
          #log.debug(f'call to FormSearchIssueAttend.getSelection() sin arg programador= ')
          return None
        
        setQuerys = {'Tickets':{},'Desarrollo':{}}
        
        ## select filter module
        if self.data['ticketModulo'] not in (None,''):
            setQuerys['Tickets'].update({'brief': self.data['ticketModulo']})
            setQuerys['Desarrollo'].update({'modulo': self.data['ticketModulo']})
          
        ## ticket status all open pending close
        if self.data['ticketStatus'] == 'open':
            setQuerys['Tickets'].update({'estado': True, 'register_estado':True})
            setQuerys['Desarrollo'].update({'estado': True})     
    
        elif self.data['ticketStatus'] == 'close':
            setQuerys['Tickets'].update({'estado': False, 'register_estado':False})
            setQuerys['Desarrollo'].update({'estado': False})
        
        elif self.data['ticketStatus'] == 'pending':
            setQuerys['Tickets'].update({'estado': True, 'register_estado':False})
            setQuerys['Desarrollo'].update({'estado': True})
          
        if self.data['ticketAsignacion'] == 'to_me':
            setQuerys['Tickets'].update({'attend': programador})
            setQuerys['Desarrollo'].update({'asistente': programador})      
    
        elif self.data['ticketAsignacion'] == 'none' :
            setQuerys['Tickets'].update({'attend': None})
            setQuerys['Desarrollo'].update({'asistente': None}) 
     
        elif self.data['ticketAsignacion'] == 'other' :
            setQuerys.update({'asingacion': 'other'})
    
        return setQuerys
  

