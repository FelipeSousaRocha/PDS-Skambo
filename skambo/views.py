from django.shortcuts import render, Produto

def index(request):
    #busca
    search = request.GET.get('search')

    if search:
        list = Produto.objects.filter(descricao__icontains=search)


    return render(request,"skambo/index.html")


