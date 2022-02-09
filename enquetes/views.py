from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Pergunta, Opcao

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        ultimas_enquetes = Pergunta.objects.filter(
            data_publicacao__lte=timezone.now()
        ).order_by('-data_publicacao')[:10]
        contexto = {
            'ultimas_enquetes': ultimas_enquetes,
        }
        return render(request, 'enquetes/index.html', contexto)

class DetalhesView(generic.View):
    def get(self, request, *args, **kwargs):
        id_enquete = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk = id_enquete)
        if pergunta.data_publicacao > timezone.now():
            raise Http404
        """
        try:
            pergunta = Pergunta.objects.filter(
            data_publicacao__lte = timezone.now()
            ).get(pk=id_enquete)
        except (Pergunta.DoesNotExist):
            raise Htpp404
        """
        return render(request, 'enquetes/enquete.html', {'pergunta': pergunta})

class ResultadoView(generic.View):
    def get(self, request, *args, **kwargs):
        id_enquete = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk = id_enquete)
        return render(request, 'enquetes/resultado.html', {'pergunta':pergunta})

class VotacaoView(generic.View):
    def post(self, request, *args, **kwargs):
        id_enquete = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk = id_enquete)
        try:
            op_votada = pergunta.opcao_set.get(pk = request.POST['opcao'])
        except (KeyError, Opcao.DoesNotExist):
            return render(request, 'enquetes/enquete.html', {
                'pergunta': pergunta,
                'error_message': "Uma opção precisa ser selecionada!",
            })
        op_votada.votos += 1
        op_votada.save()
        return HttpResponseRedirect(
            reverse('enquetes:resultado', args=(pergunta.id,))
        )

class CadastroView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'enquetes/cadastro.html')
    def post(self, request, *args, **kwargs):
        #recuperar parametros do formulario
        texto = request.POST['texto']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']
        op5 = request.POST['op5']
        op6 = request.POST['op6']
        #validar, instanciar objetos e cadastrar no banco de dados
        if texto and op1 and op2:
            p1 = Pergunta(texto= texto, data_publicacao= timezone.now())
            opcao1 = Opcao(texto= op1, pergunta=p1)
            opcao2 = Opcao(texto= op2, pergunta=p1)
            p1.save()
            opcao1.save()
            opcao2.save()
            if op3:
                opcao3 = Opcao(texto = op3, pergunta=p1)
                opcao3.save()
            if op4:
                opcao4 = Opcao(texto = op4, pergunta=p1)
                opcao4.save()
            if op5:
                opcao5 = Opcao(texto = op5, pergunta=p1)
                opcao5.save()
            if op6:
                opcao6 = Opcao(texto = op6, pergunta=p1)
                opcao6.save()
        else:
            return render(
                request, 'enquetes/cadastro.html',
                {'erro':'Precisa preencher ao menos o texto e as duas opções!'}
                )
            #redirecionar para a pagina inicial
        return HttpResponseRedirect(
            reverse('enquetes:index', args=())
        )