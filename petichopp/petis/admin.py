from django.contrib import admin
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'especie', 'raca', 'idade', 'dono', 'telefone_dono', 'ativo')
    list_filter = ('ativo', 'especie', 'raca')
    search_fields = ('nome', 'dono', 'telefone_dono')
    
from django.contrib import admin
from .models import Pet, Servico, Atendimento

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco_padrao')

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'pet', 'valor_total')
    list_filter = ('data',)