from django.urls import path
from . import views


urlpatterns = [
    path('', views.enquete, name='index'),
    path('<int:enquete_id>/', views.enquete_detail, name='enquete_detail'),
    path('<int:enquete_id>/results/', views.enquete_results, name='enquete_results'),
    path('<int:enquete_id>/vote/', views.enquete_vote, name='enquete_vote'),
]