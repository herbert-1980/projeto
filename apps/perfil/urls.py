from django.urls import path
from apps.perfil.views import perfil_view
from apps.perfil.views import criar_perfil, listar_perfis, editar_perfil, excluir_perfil


urlpatterns = [
    path('<slug:username>/', perfil_view, name='perfil'),
    path('criar/', criar_perfil, name='criar_perfil'),
    path('listar/', listar_perfis, name='listar_perfis'),
    path('editar/<int:usuario_id>/', editar_perfil, name='editar_perfil'),
    path('excluir/<int:usuario_id>/', excluir_perfil, name='excluir_perfil'),
]
