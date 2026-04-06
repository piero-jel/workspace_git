# framework import
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

# Project Modules import
from Login.views import (UserLoginView, UserChangePasswordView, HomeView)

admin.site.site_header = "Administracion del Sistema"
admin.site.site_title = "Administracion del Sistema"

urlpatterns = [
    # vista de login -> /
    path('', UserLoginView.as_view(),name="login"),

    ## vista para admin sistem solo superuser -> /admin/
    path('admin/', admin.site.urls,name='Admin'), 

    # logout redireciona a / 'login'
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    # vista para blanqueo de pass (sin login) -> /password_change_request/
    path('password_change_request/',UserChangePasswordView.as_view(),
         name="PasswordChangeRequest"),

    # dispatch luego del login
    path('home/', HomeView.as_view(),name="Home"),
        
]
