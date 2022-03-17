from django.urls import path
from . import views

app_name = "enquetes"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('cadastro', views.CadastroView.as_view(), name="cadastro"),
    path('<int:pk>/', views.DetalhesView.as_view(), name="detalhes"),
    path('<int:pk>/votacao/', views.VotacaoView.as_view(), name="votacao"),
    path('<int:pk>/resultado/', views.ResultadoView.as_view(), name="resultado"),
    path('encerradas/', views.EncerradasView.as_view(), name='encerradas'),
    path('autor/<int:pk>/', views.AutorView.as_view(), name='autor'),
    path('autor/<int:pk>/editar/', views.PerfilView.as_view(), name='editar_perfil'),
    path('rotulo/<int:pk>/', views.RotuloView.as_view(), name='rotulo'),
    path('busca/', views.BuscaView.as_view(), name='busca'),
    path('cadastro/', views.NovoAutorView.as_view(), name='novo_autor'),
]