from django.shortcuts import render
from django.template import loader
from .models import Anuncio
from django.http import HttpResponse

def skambo(request):
    #search = Produto.objects.filter(title__icontains)
    anuncios = Anuncio.objects.all()
    template = loader.get_template('skambo/skambo.html')
    contexto = {
        'anuncios': anuncios,
        }
    return HttpResponse(template.render(contexto, request))

def anuncio(request):
    return render(request,"skambo/anuncio.html")

