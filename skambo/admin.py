from django.contrib import admin
from .models import Usuario, Proposta, Produto, Servico

admin.site.register(Usuario)
admin.site.register(Proposta)
admin.site.register(Produto)
admin.site.register(Servico)