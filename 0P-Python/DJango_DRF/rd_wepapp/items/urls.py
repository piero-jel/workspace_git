from django.urls import path # type: ignore pylint: disable=import-error

from . import views

urlpatterns = [
    path("", views.index, name=""),
    path("items_vs_seller/", views.items_vs_seller, name="items_vs_seller"),
    path("items/", views.items, name="items"),
    path('api/items/', views.ItemsView.as_view(), name='api/items'),
]
