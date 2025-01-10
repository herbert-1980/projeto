from django.urls import path
from apps.contatos.views import contato


urlpatterns = [
    path('', contato, name='contato'),
]

