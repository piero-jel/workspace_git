from django.contrib import admin

# Register your models here.
from .models import Tickets, RegisterWork,Modulos 
from .models import Desarrollo,RegistroTrabajo



class TicketsAdmin(admin.ModelAdmin):
    model = Tickets
    readonly_fields=('id','fecha_creacion','register')
    
    list_display = (
        'id','register','estado', 'attend', 'brief','email','fecha_creacion','fecha_update',
        'fecha_cierre','file1','file2','file3', 'edit_register','register_estado' 
    )
    list_filter = ('register','attend' )
  
    ## Cuando Ingresamos, indicamos que campos son visibles y cuales de ellos alterables
    fieldsets = (
        (None, {'fields': ('fecha_creacion', 'register')}),
        ('Permissions', {'fields': ( 'estado','brief','detail','attend', 'email','fecha_update',
                                     'fecha_cierre','file1','file2','file3',
                                      'edit_register','register_estado')}), 
    )
    ## Cuando agregamos un nuevo tickets, indicamos cuales son los campos visibles
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'attend', 'brief', 'detail', 'email','fecha_cierre','fecha_update',
                        'file1','file2','file3', 'edit_register','register_estado')}
        ),
    )
    search_fields = ('register',)


class RegisterWorkAdmin(admin.ModelAdmin):  
    model = RegisterWork
    """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un ticket.
      * ticket          : Ticket sobre el cual se registrara el trabajo, Modelo Tickets
      * register_work   : quien registra el trabajo sobre el ticket en cuestion, Modelo Programador    
      * date_creacion   : Fecha en la cual se creo el registro del nuevo trabajo.
      * msg             : Detalle del trabajo realizado o mensage descriptivo.    
      * file1           : Archivo para acompañar el detalle del trabajo realizado.
      * file2           : Archivo para acompañar el detalle del trabajo realizado.    
      * tiempo          : Tiempo consumido para realizar el trabajo.    
      * date_update     : Hora y Fecha de actualizacion del registro.      
    """
    readonly_fields=('id','ticket','date_creacion')  
    list_display = (
        'id','ticket','register_work','date_creacion','msg', 'file1','file2','tiempo',
        'date_update','programmer'
    )        
  
    list_filter = ('date_creacion',)
  
    fieldsets = (
        (None, {'fields': ('ticket','register_work','date_creacion',)}),
        ('Permissions', {'fields': ('msg', 'file1','file2','tiempo','programmer')}),
    )
    
    ## Cuando agregamos un nuevo usuario, indicamos cuales son los campos visibles
    add_fieldsets = (
        (None, {
                'classes': ('wide',),
                'fields': ( 'ticket','register_work','date_creacion','msg', 'file1','file2',
                            'tiempo','date_update','programmer' )
            }
        ),
      )
    search_fields = ('ticket',)
  
  

class ModulosAdmin(admin.ModelAdmin):  
    model = Modulos
    """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un ticket.
      * nombre      : Nombre del Modulo.
      * descripcion : Descripcion del Modulo.
    """
    readonly_fields=('id','nombre')  
    list_display = ('id','nombre','descripcion')
      
    list_filter = ('nombre',)
  
    fieldsets = (
        (None, {'fields': ('nombre',)}),('Permissions', {'fields': ('descripcion',)}),
    )
    
    ## Cuando agregamos un nuevo usuario, indicamos cuales son los campos visibles
    add_fieldsets = (
        (None, {'classes': ('wide',),'fields': ( 'nombre','descripcion' )}),
      )
    search_fields = ('nombre',)

admin.site.register(RegisterWork,RegisterWorkAdmin)
admin.site.register(Tickets,TicketsAdmin)
admin.site.register(Modulos,ModulosAdmin)
# admin.site.register(TicketsHistory,TicketsHistoryAdmin)


class DesarrolloAdmin(admin.ModelAdmin):
    """ Descripcion del modelo
      * registro    : quien registra el pedido de un nuevo desarrollo 
      * empresa     : Para que empresa, peude ser interno (opcionale)
      * asistente   : quien esta trabajando actualmente en el desarrollo, Modelo Programador    
      * descripcion : Descripcion del desarrollo a realizar.
      * email       : Lista de meil a quien notificar los trabajos registrados sobre el desarrollo
      * fecha_creacion : Fecha en la cual se creo el issue.
      * fecha_actualizacion  : Fecha de la ultima actualizacion (en la cual se registro un nuevo trabajo )
      * fecha_cierre  : Fecha de cierre del Desarrollo (None, valor por defecto)
      * file1     : Archivo uno para acompañar el detalle del Desarrollo
      * file2     : Archivo dos para acompañar el detalle del Desarrollo
      * file3     : Archivo dos para acompañar el detalle del Desarrollo
      * estado    : Estado Actual del issue
    """
    model = Desarrollo
    readonly_fields=('id','fecha_creacion','estado')
    
    list_display = (
        'id','registro','empresa', 'asistente', 'descripcion','email','fecha_creacion',
        'fecha_actualizacion', 'fecha_cierre','file1','file2','file3',
    )

    list_filter = ('registro','empresa','asistente' )  

    ## Cuando agregamos un nuevo desarrollos, indicamos cuales son los campos visibles
    fieldsets = (
        (None, {'fields': ('fecha_creacion',)}),
        ('Permissions', {
                'fields': ( 'registro','empresa','asistente','descripcion', 'email',
                        'file1','file2','file3' )
            }), 
      )
    ## Cuando Ingresamos, indicamos que campos son visibles y cuales de ellos alterables
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'registro', 'empresa', 'asistente', 'descripcion','email',
                        'file1','file2','file3', 'estado','fecha_actualizacion','fecha_cierre')}
        ),
    )
    search_fields = ('registro','empresa','asistente',)


class RegistroTrabajoAdmin(admin.ModelAdmin):  
    model = RegistroTrabajo
    """ Modelo de la tabla para Hilo del Historial de registros de trabajo de un desarrollo.
      * desarrollo      : desarrollo sobre el cual se registrara el trabajo, Modelo desarrollos
      * register_work   : quien registra el trabajo sobre el desarrollo en cuestion, Modelo Programador    
      * fecha_creacion  : Fecha en la cual se creo el registro del nuevo trabajo.    
      * msg             : Detalle del trabajo realizado o mensage descriptivo.    
      * file1           : Archivo para acompañar el detalle del trabajo realizado.
      * file2           : Archivo para acompañar el detalle del trabajo realizado.    
      * tiempo          : Tiempo consumido para realizar el trabajo.    
      * date_update     : Hora y Fecha de actualizacion del registro.
      * programmer      : True | False , especifica si es programador quien registra
    """
    readonly_fields=('id','fecha_creacion')  
    list_display = (
        'id','desarrollo','register_work','fecha_creacion','msg', 'file1','file2','tiempo',
        'date_update','programmer'
    )
  
    list_filter = ('fecha_creacion',)
  
    fieldsets = (
        (None, {'fields': ('desarrollo','register_work','fecha_creacion',)}),
        ('Permissions', {'fields': ('msg', 'file1','file2','tiempo','programmer')}),
    )
    ## Cuando agregamos un nuevo usuario, indicamos cuales son los campos visibles
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'desarrollo','register_work','fecha_creacion','msg', 'file1',
                        'file2','tiempo','date_update','programmer' )}
        ),
    )
    search_fields = ('desarrollo',)

admin.site.register(Desarrollo,DesarrolloAdmin)
admin.site.register(RegistroTrabajo,RegistroTrabajoAdmin)


