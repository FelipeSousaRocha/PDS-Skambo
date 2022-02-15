from django.shortcuts import render

def skambo(request):
    #search = Produto.objects.filter(title__icontains)
    return render(request,"skambo/skambo.html")

def anuncio(request):
    return render(request,"skambo/anuncio.html")