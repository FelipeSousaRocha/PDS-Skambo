import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone

class Rotulo(models.Model):
    titulo = models.CharField(max_length=20)
    class Meta:
        verbose_name_plural = 'Rótulos'
    def __str__(self):
        return self.titulo

class Autor(models.Model):
    nome = models.CharField(max_length=80)
    genero = models.CharField(max_length=100, null=True)
    descricao = models.TextField()
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null = True
    )
    class Meta:
        verbose_name_plural = 'Autores'
    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    texto = models.CharField(max_length=200, unique=True)
    data_publicacao = models.DateTimeField('Data de publicação')
    data_encerramento = models.DateField('Encerramento', null=True)
    imagem = models.ImageField(upload_to='enquetes', null=True, blank=True)
    rotulos = models.ManyToManyField(Rotulo, verbose_name='Rótulos')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.texto
    def publicada_recentemente(self):
        agora = timezone.now()
        return agora-datetime.timedelta(days=1) <= self.data_publicacao <= agora
    publicada_recentemente.admin_order_field = 'data_publicacao'
    publicada_recentemente.boolean = True
    publicada_recentemente.short_description = 'É recente?'
    def total_de_votos(self):
        total = 0
        for op in self.opcao_set.all():
            total += op.votos
        return total

class Opcao(models.Model):
    texto = models.CharField(max_length=100)
    votos = models.IntegerField(default=0)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    def __str__(self):
        return self.texto
    class Meta:
        verbose_name_plural = "Opções"
    def porcentagem(self):
        total = self.pergunta.total_de_votos()
        return (self.votos / total)*100
