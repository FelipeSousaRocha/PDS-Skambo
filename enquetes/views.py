from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Pergunta, Opcao, Autor, Rotulo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        enquetes = Pergunta.objects.filter(
            data_publicacao__lte = timezone.now()
        ).filter(
            data_encerramento__gte = timezone.now()
        ).order_by('-data_publicacao')
        rotulos = Rotulo.objects.all()
        contexto = {'enquetes': enquetes, 'rotulos': rotulos}
        return render(request, 'enquetes/index.html', contexto)

class BuscaView(generic.View):
    def get(self, request, *args, **kwargs):
        str_busca = request.GET['str_busca']
        enquetes = Pergunta.objects.filter(
            data_publicacao__lte = timezone.now()
        ).filter(
            data_encerramento__gt = timezone.now()
        ).order_by('-data_publicacao')
        if str_busca:
            enquetes = enquetes.filter(texto__icontains = str_busca)
        contexto = {'enquetes': enquetes,}
        return render(request, 'enquetes/busca.html', contexto)

class EncerradasView(generic.View):
    def get(self, request, *args, **kwargs):
        enquetes = Pergunta.objects.filter(
            data_encerramento__lte=timezone.now()
        ).order_by('-data_publicacao')
        contexto = {'enquetes': enquetes,}
        return render(request, 'enquetes/encerradas.html', contexto)

class AutorView(generic.View):
    def get(self, request, *args, **kwargs):
        id_autor = kwargs['pk']
        autor = get_object_or_404(Autor, pk=id_autor)
        enquetes = Pergunta.objects.filter(autor=autor).order_by('-data_publicacao')
        encerradas = enquetes.exclude(data_encerramento__gte = timezone.now())
        ativas = enquetes.exclude(data_encerramento__lt = timezone.now())
        contexto = {
            'autor': autor, 'ativas': ativas, 'encerradas': encerradas
        }
        return render(request, 'enquetes/autor.html', contexto)

class RotuloView(generic.View):
    def get(self, request, *args, **kwargs):
        id_rotulo = kwargs['pk']
        rotulo = get_object_or_404(Rotulo, pk=id_rotulo)
        enquetes = rotulo.pergunta_set.all().order_by('-data_publicacao')
        encerradas = enquetes.exclude(data_encerramento__gte = timezone.now())
        ativas = enquetes.exclude(data_encerramento__lt = timezone.now())
        contexto = {
            'rotulo': rotulo, 'ativas': ativas, 'encerradas': encerradas
        }
        return render(request, 'enquetes/rotulo.html', contexto)

class DetalhesView(generic.View):
    def get(self, request, *args, **kwargs):
        id_enquete = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk = id_enquete)
        if pergunta.data_publicacao > timezone.now():
            raise Http404
        if pergunta.data_encerramento < timezone.now().date():
            opcoes = pergunta.opcao_set.all().order_by('-votos')
            contexto = {'pergunta': pergunta, 'opcoes': opcoes}
            return render(request, 'enquetes/final.html', contexto)
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
                'erro': "Uma opção precisa ser selecionada!",
            })
        op_votada.votos += 1
        op_votada.save()
        return HttpResponseRedirect(
            reverse('enquetes:resultado', args=(pergunta.id,))
        )

class NovoAutorView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'enquetes/novo_autor.html')
    def post(self, request, *args, **kwargs):
        # recuperar parâmetros do form
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        genero = request.POST['genero']
        descricao = request.POST['descricao']
        username = request.POST['login']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']

        # validar, instanciar objetos e cadastrar no banco de dados
        if nome and sobrenome and email and genero and descricao and username and senha1 and senha2:
            if senha1 == senha2:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username, email, senha1)
                        user.first_name = nome
                        user.last_name = sobrenome
                        user.save()
                        Autor.objects.create(
                            nome = nome, genero = genero,
                            descricao = descricao, usuario = user
                        )
                    else:
                        return render(
                            request, 'enquetes/novo_autor.html',
                            {'erro': 'O e-mail informado já existe na base!'}
                        )
                else:
                    return render(
                        request, 'enquetes/novo_autor.html',
                        {'erro': 'O login informado já existe na base!'}
                    )
            else:
                return render(
                    request, 'enquetes/novo_autor.html',
                    {'erro': 'As senhas informadas precisam ser iguais!'}
                )
        else:
            return render(
                request, 'enquetes/novo_autor.html',
                {'erro': 'Todos os parâmetros precisam ser informados!'}
            )
        # Faz o login do usuário e leva à Página Principal
        login(request, user)
        return HttpResponseRedirect(reverse('enquetes:index', args=()))

@method_decorator(login_required, name='dispatch')
class PerfilView(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.autor:
            return render(request, 'enquetes/novo_autor.html')
        return render(request, 'enquetes/editar_perfil.html')
    def post(self, request, *args, **kwargs):
        # recuperar parâmetros do form
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        genero = request.POST['genero']
        descricao = request.POST['descricao']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']

        # validar, atualizar e salvar no banco de dados
        if nome and sobrenome and email:
            if request.user.first_name != nome:
                request.user.first_name = nome
            if request.user.last_name != sobrenome:
                request.user.last_name = sobrenome
            if request.user.email != email:
                if User.objects.filter(email=email).exists():
                    return render(
                        request, 'enquetes/editar_perfil.html',
                        {'erro': 'O e-mail informado deve ser único no sistema!'}
                    )
                request.user.email = email
        if senha1 and senha2:
            if not senha1 == senha2:
                return render(
                    request, 'enquetes/editar_perfil.html',
                    {'erro': 'As senhas informadas precisam ser iguais!'}
                )
            request.user.set_password(senha1)
        request.user.save()
        if nome and genero and descricao:
            if request.user.autor.nome != nome:
                request.user.autor.nome = nome
            if request.user.autor.genero != genero:
                request.user.autor.genero = genero
            if request.user.autor.descricao != descricao:
                request.user.autor.descricao = descricao
            request.user.autor.save()

        return HttpResponseRedirect(reverse('enquetes:autor', args=(request.user.autor.id,)))

@method_decorator(login_required, name='dispatch')
class CadastroView(generic.View):
    def get(self, request, *args, **kwargs):
        rotulos = Rotulo.objects.all()
        return render(request, 'enquetes/cadastro.html', {'rotulos':rotulos})
    def post(self, request, *args, **kwargs):
        # recuperar parâmetros do form
        texto = request.POST['texto']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']
        op5 = request.POST['op5']
        op6 = request.POST['op6']
        encerramento = request.POST['encerramento']
        # validar, instanciar objetos e cadastrar no banco de dados
        if texto and op1 and op2 and encerramento:
            p1 = Pergunta(
                texto=texto, data_publicacao=timezone.now(),
                data_encerramento=encerramento,
                autor=request.user.autor
            )
            opcao1 = Opcao(texto=op1, pergunta=p1)
            opcao2 = Opcao(texto=op2, pergunta=p1)
            p1.save()
            opcao1.save()
            opcao2.save()
            if op3:
                opcao3 = Opcao(texto=op3, pergunta=p1)
                opcao3.save()
            if op4:
                opcao4 = Opcao(texto=op4, pergunta=p1)
                opcao4.save()
            if op5:
                opcao5 = Opcao(texto=op5, pergunta=p1)
                opcao5.save()
            if op6:
                opcao6 = Opcao(texto=op6, pergunta=p1)
                opcao6.save()
            rotulos = request.POST.getlist('rotulos')
            if rotulos:
                for r in rotulos:
                    try:
                        rotulo = Rotulo.objects.get(pk=r)
                        p1.rotulos.add(rotulo)
                    except(Rotulo.DoesNotExist):
                        pass
        else:
            return render(
                request, 'enquetes/cadastro.html',
                {'erro': 'Precisa preencher ao menos a pergunta e duas opções!'}
            )
        # redirecionar para a página inicial
        return HttpResponseRedirect(reverse('enquetes:index', args=()))
