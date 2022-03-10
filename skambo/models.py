from django.db import models
from django.forms import ModelForm
from django.conf import settings

GENERO = [
    (1, "masculino"),
    (2, "feminino")
    ]

class Usuario(models.Model):
    nome = models.CharField(max_length = 50)
    genero = models.IntegerField(choices = GENERO, default = 1)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
	null = True
	)
    def __str__(self):
        return self.nome

class Anuncio(models.Model):
    descricao = models.CharField(max_length=500)
    interesses = models.CharField(max_length=300)
    data = models.DateField(auto_now_add = True)
    contato = models.CharField(max_length=20)
    cidade = models.CharField(max_length=30)
    bairro = models.CharField(max_length=20)
    imagem = models.ImageField(upload_to='media', null=True, blank=True)
    ativo = models.BooleanField()
    anunciante = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    def __str__(self):
        return self.descricao

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
    (5, "beleza"),
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
    def __str__(self):
        return self.descricao

class Servico(Anuncio):
    categoria = models.IntegerField(choices = CATEGORIA_SERVICO, default = 1)
    def __str__(self):
        return self.descricao

class ServicoForm(ModelForm):
    class Meta:
        model = Servico
        fields = [
            'descricao', 'interesses', 'contato', 'cidade', 'bairro',
            'categoria', 'imagem'
        ]

class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = [
            'marca', 'descricao', 'interesses', 'contato', 'cidade', 'bairro',
            'categoria', 'imagem', 'estado', 'anos_de_uso'
        ]

class Proposta(models.Model):
    #proposta = models.ForeignKey(Anuncio, on_delete = models.CASCADE, related_name = "proposta")
    data = models.DateField(auto_now_add = True)
    aceita = models.BooleanField(null = True)
    imagem = models.ImageField(upload_to='media')
    proponente = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    #oferta = models.ForeignKey(Anuncio, on_delete = models.CASCADE, related_name = "oferta")
    data_da_troca = models.DateField(null = True)


"""
class PropostaForm(ModelForm):
    class Meta:
        model = Proposta
       fields = [
            'proposta',
        ]
"""

"""
class PropostaView(generic.View):
    def post(self, request, *args, **kwargs):
        id_anuncio = kwargs['pk']
        anuncio = get_object_or_404(Anuncio, pk = id_anuncio)
        try:
            op_votada = anuncio.opcao_set.get(pk = request.POST['opcao'])
        except (KeyError, Opcao.DoesNotExist):
            return render(request, 'skambo/anuncio.html', {
                'anuncio': anuncio,
                'erro': "Uma opção precisa ser selecionada!",
            })
        op_votada.save()
        return HttpResponseRedirect(
            reverse('skambo:troca', args=(anuncio.id,))
)
"""

"""
class Troca(models.Model):
    data = models.DateField(auto_now_add = True)
    anuncio_ofertado = models.ForeignKey(Anuncio, on_delete = models.CASCADE)
    anuncio_aceito = models.ForeignKey(Anuncio, on_delete = models.CASCADE)
"""
