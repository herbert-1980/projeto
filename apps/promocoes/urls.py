from django.urls import path
from . import views


urlpatterns = [
    path("", views.lista_promocoes, name="lista_promocoes"),
    path("<int:promocao_id>/", views.detalhes_promocao, name="detalhes_promocao"),
]
