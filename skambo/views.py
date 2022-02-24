from django.shortcuts import render, get_object_or_404
from .models import Anuncio, Produto, Servico, ServicoForm, Usuario
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

def skambo(request):
    #search = Produto.objects.filter(title__icontains)
    produtos = Produto.objects.order_by('-data')[:10]
    servicos = Servico.objects.order_by('-data')[:10]
    contexto = {
        'produtos': produtos,
        'servicos': servicos,
        }
    return render(request, 'skambo/index.html', contexto)

def anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk = pk)
    return render(request, 'skambo/anuncio.html',{'anuncio': anuncio})

class ProductsView(generic.ListView):
    template_name = "skambo/products.html"
    context_object_name = 'produtos'
    def get_queryset(self):
        return Produto.objects.order_by('-data')[:10]

class ServicesView(generic.ListView):
    template_name = "skambo/services.html"
    context_object_name = 'servicos'
    def get_queryset(self):
        return Servico.objects.order_by('-data')[:10]

def about(request):
    return render(request, 'skambo/about.html')

#def pesquisa(request):
#    return render(request, 'skambo/search.html')

class RegisteradView(generic.View):
    def get(self, request, *args, **kwargs):
        form = ServicoForm()
        contexto = {'form': form}
        return render(request, 'skambo/register.html', contexto)
    def post(self, request, *args, **kwargs):
        #recuperar parametros do formulario
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            servico = form.save(commit=False)
            # servico.anunciante = request.user.usuario
            usuario = Usuario.objects.get(pk=1)
            servico.anunciante = usuario
            servico.ativo = True
            servico.save()
        else:
            contexto = {'form': form}
            return render(request, 'skambo/register.html', contexto)
        #descricao = request.POST['descricao']
        #interesses = request.POST['interesses']
        #data = request.POST['data']
        #contato = request.POST['contato']
        #cidade = request.POST['cidade']
        #bairro = request.POST['bairro']
        #imagem = request.POST['imagem']

        #a1 = Anuncio(descricao = descricao, interesses = interesses, data = data,contato = contato, cidade = cidade, bairro = bairro, imagem = imagem)
        #a1.save()
        return HttpResponseRedirect(
            reverse('skambo:index', args=())
        )