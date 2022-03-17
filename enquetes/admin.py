from django.contrib import admin
from .models import Pergunta, Opcao, Rotulo, Autor

class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 2

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['texto', 'autor', 'imagem']}),
        ('Rótulos', {'fields': ['rotulos']}),
        ('Informações de Data', {
            'fields': ['data_publicacao', 'data_encerramento']
        }),
        ]
    inlines = [OpcaoInline]
    list_display = ('texto', 'id', 'autor', 'data_encerramento', 'publicada_recentemente')
    list_filter = ['data_publicacao']
    search_fields = ['texto']

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario','id', 'genero', 'descricao')
    search_fields = ['nome']

class RotuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'id')

admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Rotulo, RotuloAdmin)
admin.site.site_header = 'Administração das aplicações de Felipe Rocha'
#admin.site.register(Opcao)