from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("insere_cotacao/", views.save_api, name="save_api"),
    path("grafico_cotacao/", views.cotacao, name="cotacao"),
]