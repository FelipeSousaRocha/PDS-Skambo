from django.contrib import admin
from .models import Usuario, Proposta, Produto, Servico

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'id', 'genero', 'descricao')
    search_fields = ['nome']

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Proposta)
admin.site.register(Produto)
admin.site.register(Servico)