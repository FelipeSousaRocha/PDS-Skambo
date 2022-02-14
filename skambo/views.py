from django.shortcuts import render, Produto

def index(request):
    produto = Produto.objects.filter(descricao__icontains=search)

    return render(request,"skambo/index.html")