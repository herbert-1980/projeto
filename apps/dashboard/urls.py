from django.urls import path
from . import views
from apps.accounts.views import logout_view, list_users_dashboard
from . views import excluir_usuario
from apps.perfil.views import editar_perfil, perfil_view



urlpatterns = [
    path('', views.index, name='dashboard'),
    path('logout/', logout_view, name='logout'), 
    ###########PERFIL############################################
    path('perfil/<str:username>/', perfil_view, name = 'perfil'),
    path('perfil/editar/<int:usuario_id>/', editar_perfil, name='editar_perfil'),
    ###########USUARIOS###############################################
    path('users/', list_users_dashboard, name='list_users_dashboard'),
    path('usuarios/excluir/<int:user_id>/', excluir_usuario, name='excluir_usuario'), 
    ###########NOTICIAS###############################################
    path('news/create/', views.DashboardNewsCreateView.as_view(), name='create_news'),
    path('news/list/', views.DashboardNewsListView.as_view(), name='dashboard_news_list'),
    path('news/<int:pk>/update/', views.DashboardNewsUpdateView.as_view(), name='update_news'),
    path('news/<int:pk>/delete/', views.DashboardNewsDeleteView.as_view(), name='delete_news'),
     ###########ENQUETES###############################################
    path('enquetes/create/', views.DashboardEnqueteCreateView.as_view(), name='enquete_create'),
    path('enquetes/list/', views.DashboardEnqueteListView.as_view(), name='enquete_list'),
    path('enquetes/<int:pk>/update/', views.DashboardEnqueteUpdateView.as_view(), name='enquete_update'),
    path('enquetes/<int:pk>/delete/', views.DashboardEnqueteDeleteView.as_view(), name='enquete_delete'),
    #path('enquetes/<int:pk>/', views.EnqueteDetailView.as_view(), name='enquete_detail'),
]
