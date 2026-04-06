# framework import
from django.urls import path

# Project Modules import
from registerticket.views import (RegisterTicketViews,
                                  ExpandTicketViews,
                                  EditTicketViews ,CreateNewTicketView,
                                  #ConfigUserClientView
                                )

urlpatterns = [
    ## vista prinicpal de la aplicacion -> /register_ticket/
    path('', RegisterTicketViews.as_view(),name="ViewRegisteredTickets"),
    
    ## vista para crear un nuevo ticket -> /register_ticket/create_new_ticket/
    path('create_new_ticket/', CreateNewTicketView.as_view(),
        name="CreateNewTicket"),

    ## vistas del detalle de un ticket registrado -> /register_ticket/expand_ticket/tk_id/
    path('expand_ticket/<int:ticket_id>/', ExpandTicketViews.as_view(),
        name="ExapandViewsTicket"),
    path('expand_ticket/<int:ticket_id>/<str:word>', ExpandTicketViews.as_view(),
        name="ExpandTicket_word"),

    ## vista para editar un Ticket -> /register_ticket/edit_ticket/tk_id/
    path('edit_ticket/<int:ticket_id>/', EditTicketViews.as_view(),name="EditTicket"),

]
