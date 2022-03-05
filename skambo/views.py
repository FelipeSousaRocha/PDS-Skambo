from django.shortcuts import render, get_object_or_404
from .models import Anuncio, Produto, Servico, ServicoForm, Usuario, ProdutoForm
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
#from django.contrib.auth.decorators import login_required
#from django.utils.decorators import method_decorator

#@method_decorator(login_required, name='dispatch')

def skambo(request):
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

class RegisterProductView(generic.View):
    def get(self, request, *args, **kwargs):
        form = ProdutoForm()
        contexto = {'form': form}
        return render(request, 'skambo/registerproduct.html', contexto)
    def post(self, request, *args, **kwargs):
        #recuperar parametros do formulario
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            # produto.anunciante = request.user.usuario
            usuario = Usuario.objects.get(pk=1)
            produto.anunciante = usuario
            produto.ativo = True
            produto.save()
        else:
            contexto = {'form': form}
            return render(request, 'skambo/registerproduct.html', contexto)
        return HttpResponseRedirect(
            reverse('skambo:register', args=())
        )

class RegisterServiceView(generic.View):
    def get(self, request, *args, **kwargs):
        form = ServicoForm()
        contexto = {'form': form}
        return render(request, 'skambo/registerservice.html', contexto)
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
            return render(request, 'skambo/registerservice.html', contexto)
        return HttpResponseRedirect(
            reverse('skambo:register', args=())
        )

#def pesquisa(request):
#    return render(request, 'skambo/search.html')

def register(request):
    return render(request, 'skambo/register.html')