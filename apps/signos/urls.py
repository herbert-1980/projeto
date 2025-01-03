from django.urls import path
from apps.signos import views


urlpatterns = [
    path('descobrir-signo/', views.signo_view, name='descobrir_signo'),  # URL para o formulário
    #path('verificar-signo/', views.verificar_signo, name='verificar_signo'),  # URL para verificar o signo
]
