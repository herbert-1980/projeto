from django.views.generic import ListView
from rest_framework.generics import get_object_or_404
from django.db.models import Count
from django.shortcuts import render
from apps.categorias.models import Categoria
from apps.empresas.models import Empresa
from apps.banners.models import Banner


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categorias/index.html'  # Template para listar categorias
    context_object_name = 'categorias'
    
    def get_queryset(self):
        # Aqui você anota quantas empresas estão associadas a cada categoria
        return Categoria.objects.annotate(num_empresas=Count('empresas')).order_by('nome_categoria')

    def get_context_data(self, **kwargs):
        # Chama o método da classe pai para obter o contexto padrão
        context = super().get_context_data(**kwargs)
        # Adiciona a contagem total de categorias ao contexto
        context['total_categorias'] = self.model.objects.count()  # Conta o número total de categorias
        return context

class BannersPorCategoriaView(ListView):
    model = Banner
    template_name = 'categorias/banners_por_categoria.html'  # Template para listar banners por categoria
    context_object_name = 'banners'

    def get_queryset(self):
        # Obter a categoria com get_object_or_404
        self.categoria = get_object_or_404(Categoria, id=self.kwargs['categoria_id'])
        # Retornar os banners associados à categoria
        return Banner.objects.filter(categorias=self.categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar a categoria ao contexto
        context['categoria'] = self.categoria
        return context
