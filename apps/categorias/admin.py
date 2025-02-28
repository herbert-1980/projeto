from django.contrib import admin
from . import models
from .models import Categoria


class CategoriaInline(admin.TabularInline):  # Ou admin.StackedInline
    model = Categoria
    fk_name = 'master_categoria'  # Especifica a chave estrangeira para a categoria pai
    extra = 1  # Adiciona uma linha extra para novas subcategorias

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_categoria', 'slug_categoria', 'icone_categoria','master_categoria')
    search_fields = ('id', 'nome_categoria',)
    list_per_page = 10
    list_filter = ('master_categoria',)
    inlines = [CategoriaInline]

    """def master_categoria(self, obj):
        return obj.master_categoria.nome_categoria if obj.master_categoria else "Sem Categoria Master"
    master_categoria.admin.order_field = 'master_categoria'
    master_categoria.short_description = 'Categoria Mestre'
"""
    @admin.display(ordering='master_categoria', description='Categoria Mestre')
    def master_categoria(self, obj):
        return obj.master_categoria.nome_categoria if obj.master_categoria else "Sem Categoria Master"

admin.site.register(models.Categoria, CategoriaAdmin)