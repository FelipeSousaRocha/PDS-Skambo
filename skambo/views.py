from django.shortcuts import render, get_object_or_404
from .models import Anuncio

def skambo(request):
    #search = Produto.objects.filter(title__icontains)
    anuncios = Anuncio.objects.order_by('-data')[:10]
    contexto = {
        'anuncios': anuncios,
        }
    return render(request, 'skambo/index.html', contexto)

def anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk = pk)
    return render(request, 'skambo/anuncio.html', {'anuncio': anuncio})

def products(request):
    return render(request, 'skambo/products.html')

def about(request):
    return render(request, 'skambo/about.html')

def contact(request):
    return render(request, 'skambo/contact.html')

def singleproduct(request):
    return render(request, 'skambo/singleproduct.html')