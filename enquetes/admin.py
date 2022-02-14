from django.contrib import admin
from .models import Pergunta, Opcao

class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 2

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Texto da Pergunta', {'fields': ['texto']}),
        ('Informações da Data',{'fields': ['data_publicacao']}),
        ]
    inlines = [OpcaoInline]
    list_display = ('texto', 'id', 'data_publicacao', 'publicada_recentemente')
    list_filter = ['data_publicacao']
    search_fields = ['texto']

admin.site.register(Pergunta, PerguntaAdmin)
admin.site.site_header = 'Administração das aplicações de Felipe Rocha'
#admin.site.register(Opcao)