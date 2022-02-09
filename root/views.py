#from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    html = '<a href="/enquetes/">Link para a aplicação de Enquetes</a>'
    return HttpResponse(html)