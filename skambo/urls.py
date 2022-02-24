from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'skambo'
urlpatterns = [
    path('', views.skambo, name="index"),
    path('anuncio/<int:pk>/', views.anuncio, name="anuncio"),
    path('products/', views.ProductsView.as_view(), name="products"),
    path('services/', views.ServicesView.as_view(), name="services"),
    path('about/', views.about, name="about"),
    path('register/', views.RegisteradView.as_view(), name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)