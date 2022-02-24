import datetime
from django.db import models
from django.utils import timezone

class Rotulo(models.Model):
    titulo = models.CharField(max_length=20)
    class Meta:
        verbose_name_plural = 'Rótulos'
    def __str__(self):
        return self.titulo

class Autor(models.Model):
    nome = models.CharField(max_length=80)
    genero = models.CharField(max_length=100,null=True)
    descricao = models.TextField()
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Autores'
    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    texto = models.CharField(max_length=200, unique=True)
    data_publicacao = models.DateTimeField('Data de publicação')
    imagem = models.ImageField(upload_to='enquetes',null=True, blank=True)
    data_encerramento = models.DateField(null=True)
    rotulos = models.ManyToManyField(Rotulo)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.texto
    def publicada_recentemente(self):
        agora = timezone.now()
        return agora-datetime.timedelta(days=1) <= self.data_publicacao <= agora
    publicada_recentemente.admin_order_field = 'data_publicacao'
    publicada_recentemente.boolean = True
    publicada_recentemente.short_description = 'É recente?'

class Opcao(models.Model):
    texto = models.CharField(max_length=100)
    votos = models.IntegerField(default=0)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    def __str__(self):
        return self.texto
    class Meta:
        verbose_name_plural = 'Opções'

