from django.contrib import admin
from . import models


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_categoria', 'slug_categoria', 'icone_categoria',)
    search_fields = ('id', 'nome_categoria',)
    list_per_page = 10


admin.site.register(models.Categoria, CategoriaAdmin)