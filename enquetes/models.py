import datetime
from django.db import models
from django.utils import timezone

class Pergunta(models.Model):
    texto = models.CharField(max_length=200)
    data_publicacao = models.DateTimeField('Data de publicação')
    def __str__(self):
        return self.texto
    def publicada_recentemente(self):
        agora = timezone.now()
        return agora-datetime.timedelta(days=1) <= self.data_publicacao <= agora

class Opcao(models.Model):
    texto = models.CharField(max_length=100)
    votos = models.IntegerField(default=0)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    def __str__(self):
        return self.texto