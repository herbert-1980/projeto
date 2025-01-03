from django.urls import path
from . import views
from apps.accounts.views import logout_view, list_users_dashboard
from . views import excluir_usuario
from apps.perfil.views import editar_perfil, perfil_view
from apps.news.views import DashboardNewsView


urlpatterns = [
    path('', views.index, name='dashboard'),
    path('logout/', logout_view, name='logout'), 
    #path('news-dashboard/', DashboardNewsView.as_view(), name='news_dashboard'),
    path('perfil/<str:username>/', perfil_view, name = 'perfil'),
    path('perfil/editar/<int:usuario_id>/', editar_perfil, name='editar_perfil'),
    path('users/', list_users_dashboard, name='list_users_dashboard'),
    path('usuarios/excluir/<int:user_id>/', excluir_usuario, name='excluir_usuario'), 
    path('news/create/', DashboardNewsView.as_view(), name='create_news'),

]
