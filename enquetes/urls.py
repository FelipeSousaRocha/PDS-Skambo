from django.urls import path
from . import views

app_name = "enquetes"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('cadastro', views.CadastroView.as_view(), name="cadastro"),
    path('<int:pk>/', views.DetalhesView.as_view(), name="detalhes"),
    path('<int:pk>/votacao', views.VotacaoView.as_view(), name="votacao"),
    path('<int:pk>/resultado', views.ResultadoView.as_view(), name="resultado"),
]