from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = 'skambo'
urlpatterns = [
    path('', views.skambo, name="index"),
    path('skambo/login/', auth_views.LoginView.as_view(template_name='skambo/login.html'), name='skambo_login'),
    path('anuncio/<int:pk>/', views.AnuncioView.as_view(), name="anuncio"),
    path('products/', views.ProductsView.as_view(), name="products"),
    path('services/', views.ServicesView.as_view(), name="services"),
    path('trocas/', views.TrocasView.as_view(), name="trocas"),
    path('about/', views.about, name="about"),
    path('proposal/<int:pk>/', views.ProposalView.as_view(), name="proposal"),
    path('troca/', views.TrocaView.as_view(), name="troca"),
    path('register/', views.register, name="register"),
    path('registerproduct/', views.RegisterProductView.as_view(), name="registerproduct"),
    path('registerservice/', views.RegisterServiceView.as_view(), name="registerservice"),
    path('search/', views.SearchView.as_view(), name="search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)