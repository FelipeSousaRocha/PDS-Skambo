import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Pergunta

""""
Testes Unitários de Elementos de Modelo
"""
class ModelPerguntaTest(TestCase):
    def test_publicada_recentemente_com_data_no_futuro(self):
        """
        publicada_recentemente() retorna FALSE para data no futuro.
        """
        data_futura = timezone.now() + datetime.timedelta(seconds = 1)
        pergunta_no_futuro = Pergunta(data_publicacao = data_futura)
        self.assertIs(pergunta_no_futuro.publicada_recentemente(), False)

    def test_publicada_recentemente_com_data_alem_das_ultimas_24hs(self):
        """
        publicada_recentemente() retorna FALSE para data anterior às 24hs.
        """
        data_passada = timezone.now() - datetime.timedelta(days= 1, seconds=1)
        pergunta_no_passado = Pergunta(data_publicacao = data_passada)
        self.assertIs(pergunta_no_passado.publicada_recentemente(), False)

    def test_publicada_recentemente_com_pergunta_publicada_agora(self):
        """
        publicada_recentemente() retorna TRUE para data igual ao instante atual.
        """
        data = timezone.now()
        pergunta_agora = Pergunta(data_publicacao = data)
        self.assertIs(pergunta_agora.publicada_recentemente(), True)

    def test_publicada_recentemente_com_data_dentro_das_ultimas_24hs(self):
        """
        publicada_recentemente() retorna TRUE para data dentro das últimas 24hs.
        """
        data = timezone.now()-datetime.timedelta(hours=23,minutes=59,seconds=59)
        pergunta = Pergunta(data_publicacao = data)
        self.assertIs(pergunta.publicada_recentemente(), True)