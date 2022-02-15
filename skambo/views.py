from django.shortcuts import render, Produto

def skambo(request):
    search = Produto.objects.filter(title__icontains)
    return render(request,"skambo/skambo.html")