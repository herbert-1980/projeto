from django.urls import path
from django.views.generic import TemplateView
from apps.news import views
from apps.signos.views import signo_view

urlpatterns = [
    path('', views.NewsIndex.as_view(), name='home'),
    path('news/<slug:slug_title>/', views.NewsDetail.as_view(), name='news_detail'),
    path('news/<int:news_id>/', views.newsShare, name='news_share'),
    path('search/', views.NewsSearch.as_view(), name='news_search'),
    path('termos-de-uso/', TemplateView.as_view(template_name="news/termos_de_uso.html"), name='termos_de_uso'),
    path('signos/', signo_view, name='signos'),

]
