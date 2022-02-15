from django.urls import path
from . import views

urlpatterns = [
    path('', views.skambo, name="skambo"),
    path('', views.anuncio, name="anuncio"),
    #django-allauth
    ]