from django.urls import path
from apps.banners import views
from apps.banners.views import BannerView, BannersPorCategoriaView
from apps.banners.views import get_banner_images


urlpatterns = [
    path('', BannerView.as_view(), name='banners'),
    path('vip/', views.banners_vip, name='banners_vip'),
    path('banners/<int:categoria_id>/', BannersPorCategoriaView.as_view(), name='banners_por_categoria'),
    path('banners/<int:banner_id>/images/', get_banner_images, name='get_banner_images'),
]
