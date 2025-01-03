from django.urls import path
from apps.empresas import views


urlpatterns = [
    # Views baseadas em classe
    path('empresas/list/', views.EmpresaListView.as_view(), name='empresa_list'),
    path('empresas/create/', views.EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresas/<int:pk>/detail/', views.EmpresaDetailView.as_view(), name='empresa_detail'),
    path('empresas/<int:pk>/update/', views.EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresas/<int:pk>/delete/', views.EmpresaDeleteView.as_view(), name='empresa_delete'),
]
