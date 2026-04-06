# framework import
from django.urls import path

# Project Modules import
from attendticket.views import (AttendTicketView,SelectedTicketView,SelectedDesarrolloView)


urlpatterns = [    
    ## vista prinicpal de la aplicacion -> /attend_ticket/
    path('', AttendTicketView.as_view(),name="ViewAttendTicket"),

    ## vista p/expandir un ticket -> /attend_ticket/view_selected_ticket/tk_id/
    path('view_selected_ticket', SelectedTicketView.as_view(),
         name="ViewSelectedTicket"),
    path('view_selected_ticket/<int:id>/', SelectedTicketView.as_view(),
         name="ViewSelectedTicket"),
    path('view_selected_ticket/<int:id>/<str:word>',SelectedTicketView.as_view(),
         name="ViewSelectedTicket"),
    
    ## vista p/expandir pedido de trabajao -> /attend_ticket/view_desarrollos_works/wrk_id/
    path('view_desarrollos_works/<int:id>/', SelectedDesarrolloView.as_view(),name="ViewDesarrolloWorks"),    
    path('view_desarrollos_works/<int:id>/<str:word>/', SelectedDesarrolloView.as_view(),name="ViewDesarrolloWorks_word"),
    path('view_desarrollos_works/<int:id>/<str:word>/<str:word2>/',SelectedDesarrolloView.as_view(),name="ViewDesarrolloWorks_word2"),    
]
