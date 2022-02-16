from django.shortcuts import render, get_object_or_404
from .models import Anuncio

def skambo(request):
    #search = Produto.objects.filter(title__icontains)
    anuncios = Anuncio.objects.order_by('-data')[:10]
    contexto = {
        'anuncios': anuncios,
        }
    return render(request, 'skambo/skambo.html', contexto)

def anuncio(request, id_anuncio):
    anuncio = get_object_or_404(Anuncio, pk = id_anuncio)
    return render(request, 'skambo/anuncio.html', {'anuncio': anuncio})

