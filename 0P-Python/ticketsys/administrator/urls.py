# framework import
from django.urls import path

# Project Modules import
from administrator.views import (
    AdminViews,ChangePasswordView,AddNewClientView,
    ListAdminViews,UserConfigurationView,
    ListCompaniesView,CompanyView,ConfigUserClientView,
    ListProgammersViews,ListModulosView,
    NewModuloView,NewCompanyView,NewProgrammerView,NewAdministratorView,
    ListTicketsViews,ListDesarrollosViews,DesarrolloViews
)

urlpatterns = [
    # vista principal de la app (superuser y admin) -> /administrator/
    path('', AdminViews.as_view(),name="view_admin"),
    
    # vista p/administracion de usuarios solo superuser -> /administrator/view_useradmin/
    path('view_useradmin/', ListAdminViews.as_view(),name="ListAdminViews"),    

    # vista p/configuracion de usuario del staff -> /administrator/view_config_user/    
    path('view_config_user/<int:user_id>', UserConfigurationView.as_view(),
        name="UserConfigurationView"),


    # vista que lista las companias (solo admin) -> /administrator/view_companies/
    path('view_companies/', ListCompaniesView.as_view(),name="ListCompaniesView"),

    # visualiza los datos de una compania (solo admin) -> /administrator/view_company/company_id/
    path('view_company/<int:company_id>/', CompanyView.as_view(),name="CompanyView"),

    # vista para el cambio de contraseña -> /administrator/change_passwords/
    path('change_passwords/', ChangePasswordView.as_view(),name="ChangePassword"),

    # vista p/la creacion de nuevo ciente -> /administrator/add_new_client/<int:company_id>/
    path('add_new_client/<int:company_id>/', AddNewClientView.as_view(),name="AddNewClient"),
        
    # vista p/configuracion del Cliente -> /administrator/view_config_user/
    path('view_config_nonadmuser/', ConfigUserClientView.as_view(),name="ConfigUserClientView"),

    # vista que lista los programadores (solo admin) -> /administrator/view_programmers/
    path('view_programmers/', ListProgammersViews.as_view(),name="ListProgammersViews"),

    # vista que lista los modulos (solo admin) -> /administrator/view_modulos/
    path('view_modulos/', ListModulosView.as_view(),name="ListModulosView"),
    
    # vista p/editar un modulo (solo admin) -> /administrator/view_modulos/<int:modulo_id>/
    path('view_modulos/<int:modulo_id>', ListModulosView.as_view(),name="ListModulosView"),

    # vista p/crear un nuevo aministrador (solo admin) -> /administrator/new_administrador/
    path('new_administrador/', NewAdministratorView.as_view(),name="NewAdministratorView"),

    # vista p/crear un nuevo modulo (solo admin) -> /administrator/new_modulo/
    path('new_modulo/', NewModuloView.as_view(),name="NewModuloView"),

    # vista p/crear una nueva Empresa (solo admin) -> /administrator/new_company/
    path('new_company/', NewCompanyView.as_view(),name="NewCompanyView"),

    # vista p/crear un nuevo Programador (solo admin) -> /administrator/new_programmer/
    path('new_programmer/', NewProgrammerView.as_view(),name="NewProgrammerView"),

    # vista p/visualizar y o editar los tickets (solo admin) -> /administrator/view_tickets/
    path('view_tickets/', ListTicketsViews.as_view(),name="ListTicketsViews"),
    path('view_tickets/<int:ticket_id>/', ListTicketsViews.as_view(),name="ListTicketsViews"),

    # ListDesarrollosViews,DesarrolloViews
    path('view_desarrollos/', ListDesarrollosViews.as_view(),name="ListDesarrollosViews"),

    # Visuliza un desarrollo en particular
    path('view_desarrollos_works/<int:develop_id>/', DesarrolloViews.as_view(),name="DesarrolloViews"),
    path('view_desarrollos_works/<int:develop_id>/<str:word>/',DesarrolloViews.as_view(),name="DesarrolloViews"),


]
