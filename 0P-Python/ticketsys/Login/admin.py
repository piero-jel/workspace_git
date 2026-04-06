from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Login.models import Empresa , User , Programador
from Login.forms import CustomUserCreationForm, CustomUserChangeForm



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username','email','first_name','last_name', 'telefono','is_staff',
                    'is_active','empresa')
    list_filter = ('username','email','first_name','last_name', 'telefono', 'is_staff',
                   'is_active','empresa','groups')
  
    ## Cuando Ingresamos, indicamos que campos son visibles y cuales de ellos alterables
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('email','first_name','last_name', 'telefono','is_staff',
                                    'is_active','empresa','groups',)}),
    )
    ## Cuando agregamos un nuevo usuario, indicamos cuales son los campos visibles
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','first_name', 'telefono','last_name', 'password1',
                       'password2', 'is_staff', 'is_active','empresa')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


class ProgramadorAdmin(admin.ModelAdmin):
    #readonly_fields=('fecha_inicio','legajo')
    model = Programador
    list_display = ('id','programador','fecha_inicio')
    list_filter = ('id','programador','fecha_inicio')
  
    ## Cuando Ingresamos, indicamos que campos son visibles y cuales de ellos alterables
    fieldsets = (
        (None, {'fields': ('programador',)}),
        ('Permissions', {'fields': ('fecha_inicio',)}),        
    )
    ## Cuando agregamos un nuevo usuario, indicamos cuales son los campos visibles
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('programador','fecha_inicio',)}
        ),
    )
    search_fields = ('id','programador',)
    ordering = ('id',)

class EmpresaAdmin(admin.ModelAdmin):
    """ Modelo de la tabla para Empresa
        * nombre          : Nombre de la empresa.
        * telefono1       : Telefono Principal.
        * telefono2       : Telefono secundario.
        * date_creacion   : Fecha/Hora de creacion del registro.
        * email           : Email General de la empresa, un contacto general.
    """
    model = Empresa
    list_display = ('nombre','telefono1', 'telefono2','email')
    list_filter = ('nombre','telefono1', 'telefono2','email')
  
    ## Cuando Ingresamos, indicamos que campos son visibles y cuales de ellos alterables
    fieldsets = (
        (None, {'fields': ('nombre',)}),
        ('Permissions', {'fields': ('telefono1', 'telefono2','email',)}),        
    )
    ## Cuando agregamos un nuevo usuario, indicamos cuales son los campos visibles
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre','telefono1', 'telefono2','email',)}
        ),
    )
    search_fields = ('id','nombre',)
    ordering = ('id',)


admin.site.register(User, CustomUserAdmin)
# admin.site.register(CustomUser)
admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(Programador, ProgramadorAdmin)
