import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Pergunta

def criar_enquete(texto, quant_dias):
    """
    Cria uma equete no banco com o texto e uma quantidade de dias (+/-)
    """
    data = timezone.now() + datetime.timedelta(days = quant_dias)
    return Pergunta.objects.create(texto = texto, data_publicacao = data)

"""
Testes Funcionais de Elementos de Visão
"""
class IndexViewTests(TestCase):
    def test_nenhuma_enquete_cadastrada(self):
        """
        Caso não existam enquetes cadastradas é exibida uma mensagem específica.
        """
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, 'Nenhuma enquete cadastrada')
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'], [])

    def test_enquete_no_passado(self):
        """
        Exibida corretamente enquete com data de publicação no passado.
        """
        criar_enquete(texto='enquete no passado', quant_dias=-10)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, 'enquete no passado')
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],
            ['<Pergunta: enquete no passado>'])

    def test_enquete_no_futuro(self):
        """
        Enquete com data de publicação no futuro NÃO deve ser exibida.
        """
        criar_enquete(texto='enquete no futuro', quant_dias=1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, 'Nenhuma enquete cadastrada')
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'], [])

    def test_enquete_no_futuro_e_enquete_no_passado(self):
        """
        Exibe a enquete com data no passado e omite a enquete com data no futuro.
        """
        criar_enquete(texto='enquete no passado', quant_dias=-1)
        criar_enquete(texto='enquete no futuro', quant_dias=1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, 'enquete no passado')
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],
            ['<Pergunta: enquete no passado>'])

    def test_duas_enquetes_no_passado(self):
        """
        Exibe corretamente todas as enquetes com data no passado.
        """
        criar_enquete(texto='enquete no passado 1', quant_dias=-1)
        criar_enquete(texto='enquete no passado 2', quant_dias=-2)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, 'enquete no passado 1')
        self.assertContains(resposta, 'enquete no passado 2')
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'],
            ['<Pergunta: enquete no passado 1>',
            '<Pergunta: enquete no passado 2>'])

class DetailViewTests(TestCase):
    def test_com_enquete_no_futuro(self):
        """
        É exibido o erro 404 ao acessar detalhes de uma enquete no futuro.
        """
        enquete = criar_enquete(texto='Enquete no futuro', quant_dias=5)
        resposta = self.client.get(reverse('enquetes:detalhes', args=(enquete.id,)))
        self.assertEquals(resposta.status_code, 404)

    def test_com_enquete_no_passado(self):
         enquete = criar_enquete(texto='Enquete no passado', quant_dias=-5)
         resposta = self.client.get(reverse('enquetes:detalhes', args=(enquete.id,)))
         self.assertEquals(resposta.status_code, 200)
         self.assertContains(resposta, 'Enquete no passado')
