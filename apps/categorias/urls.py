from django.urls import path
from . import views
from apps.categorias.views import BannersPorCategoriaView, BannersPorCategoriaView


urlpatterns = [
    path('', views.CategoriaListView.as_view(), name='categorias'),
    path('categorias/<int:categoria_id>/', views.BannersPorCategoriaView.as_view(), name='banners_por_categoria'),
]
