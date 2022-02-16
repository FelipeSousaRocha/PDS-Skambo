from django.urls import path
from . import views

app_name = 'skambo'
urlpatterns = [
    path('', views.skambo, name="index"),
    path('anuncio/<int:pk>/', views.anuncio, name="anuncio"),
    path('products/', views.products, name="products"),
    path('singleproduct/', views.singleproduct, name="singleproduct"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    #django-allauth
]