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

admin.site.register(Pergunta, PerguntaAdmin)
#admin.site.register(Opcao)