from django.urls import path
from . import views

urlpatterns = [
    path('', views.skambo, name="skambo"),
    #django-allauth
    ]