from django.shortcuts import render, get_object_or_404
from .models import Anuncio, Produto, Servico, ServicoForm, Usuario, ProdutoForm, PropostaForm, TrocaForm, Proposta, Troca
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

@method_decorator(login_required(login_url='/skambo/login/'), name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'


def skambo(request):
    produtos = Produto.objects.order_by('-data')[:10]
    servicos = Servico.objects.order_by('-data')[:10]
    contexto = {
        'produtos': produtos,
        'servicos': servicos,
        }
    return render(request, 'skambo/index.html', contexto)

class AnuncioView(generic.ListView):
    def get(self, request, *args, **kwargs):
        id_anuncio = kwargs['pk']
        anuncio = get_object_or_404(Anuncio, pk = id_anuncio)
        return render(request, 'skambo/anuncio.html', {'anuncio':anuncio})

class ProductsView(generic.ListView):
    template_name = "skambo/products.html"
    context_object_name = 'produtos'
    def get_queryset(self):
        return Produto.objects.order_by('-data')

class ServicesView(generic.ListView):
    template_name = "skambo/services.html"
    context_object_name = 'servicos'
    def get_queryset(self):
        return Servico.objects.order_by('-data')

def about(request):
    return render(request, 'skambo/about.html')

@method_decorator(login_required, name='dispatch')
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
            produto.anunciante = request.user.usuario
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

@method_decorator(login_required, name='dispatch')
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
            servico.anunciante = request.user.usuario
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

class ProposalView(generic.View):
    def get(self, request, *args, **kwargs):
        id_anuncio = kwargs['pk']
        anuncio = get_object_or_404(Anuncio, pk = id_anuncio)
        form = PropostaForm()
        contexto = {'form': form, 'anuncio': anuncio}
        return render(request, 'skambo/proposal.html', contexto)
    def post(self, request, *args, **kwargs):
        #recuperar parametros do formulario
        id_anuncio = kwargs['pk']
        anuncio_desejado = get_object_or_404(Anuncio, pk = id_anuncio)
        id2 = request.POST['proposta']
        if id2:
            anuncio_proposto = get_object_or_404(Anuncio, pk = id2)
            Proposta.objects.create(
                anuncio_desejado = anuncio_desejado,
                anuncio_proposto = anuncio_proposto
            )
        else:
            contexto = {'anuncio': anuncio_desejado}
            return render(request, 'skambo/proposal.html', contexto)
        return HttpResponseRedirect(
            reverse('skambo:index', args=())
        )

class TrocaView(generic.View):
    def get(self, request, *args, **kwargs):
        form = TrocaForm()
        contexto = {'form': form}
        return render(request, 'skambo/troca.html', contexto)
    def post(self, request, *args, **kwargs):
        #recuperar parametros do formulario
        id = request.POST['id_proposta']
        resposta = request.POST['resposta']
        if id and resposta:
            proposta = get_object_or_404(Proposta, pk = id)
            if resposta == 'Aceitar':
                proposta.respondida = True
                proposta.aceita = True
                proposta.save()
                Troca.objects.create(anuncio_desejado = proposta.anuncio_desejado, anuncio_proposto = proposta.anuncio_proposto)
            else:
                proposta.respondida = True
                proposta.aceita = False
                proposta.save()
        else:
            return render(request, 'skambo/troca.html')
        return HttpResponseRedirect(
            reverse('skambo:index', args=())
        )

class TrocasView(generic.ListView):
    def get(self, request, *args, **kwargs):
        trocas = Troca.objects.all()
        return render(request, 'skambo/trocas.html', {'trocas':trocas})

class SearchView(generic.View):
    def get(self, request, *args, **kwargs):
        str_busca = request.GET['str_busca']
        anuncios = Anuncio.objects.filter(data__lte = timezone.now()).order_by('-data')
        if str_busca:
           anuncios = anuncios.filter(descricao__icontains = str_busca)
        contexto = {'anuncios': anuncios,}
        return render(request, 'skambo/search.html', contexto)

def register(request):
    return render(request, 'skambo/register.html')