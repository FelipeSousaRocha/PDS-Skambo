from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'skambo'
urlpatterns = [
    path('', views.skambo, name="index"),
    path('anuncio/<int:pk>/', views.anuncio, name="anuncio"),
    path('products/', views.products, name="products"),
    path('services/', views.services, name="services"),
    path('singleproduct/', views.singleproduct, name="singleproduct"),
    path('about/', views.about, name="about"),
    #django-allauth
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)