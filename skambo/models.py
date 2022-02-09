from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length = 50)

class Anuncio(models.Model):
    descricao = models.CharField(max_length=500)
    interesses = models.CharField(max_length=300)
    data = models.DateField(auto_now_add = True)
    contato = models.CharField(max_length=20)
    cidade = models.CharField(max_length=30)
    bairro = models.CharField(max_length=20)
    imagem = models.ImageField(max_length=100)
    ativo = models.BooleanField()
    anunciante = models.ForeignKey(Usuario, on_delete = models.CASCADE)

ESTADO_PRODUTO = [
    (1, "novo"),
    (2, "semi-novo"),
    (3, "usado"),
    (4, "defeito"),
]

CATEGORIA_PRODUTO = [
    (1, "esporte"),
    (2, "moveis"),
    (3, "eletronicos"),
    (4, "livros"),
]

CATEGORIA_SERVICO = [
    (1, "beleza"),
    (2, "contabilidade"),
    (3, "educacao"),
    (4, "design"),
    (5, "informatica"),
]

class Produto(Anuncio):
    estado = models.IntegerField(choices = ESTADO_PRODUTO, default = 1)
    anos_de_uso = models.IntegerField()
    marca = models.CharField(max_length=20)
    categoria = models.IntegerField(choices = CATEGORIA_PRODUTO, default = 1)

class Servico(Anuncio):
    categoria = models.IntegerField(choices = CATEGORIA_SERVICO, default = 1)

class Proposta(models.Model):
    oferta = models.CharField(max_length = 200)
    data = models.DateField(auto_now_add = True)
    aceita = models.BooleanField()
    imagem = models.ImageField(max_length=100)
    proponente = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    anuncio = models.ForeignKey(Anuncio, on_delete = models.CASCADE)
    data_da_troca = models.DateField(null = True)

