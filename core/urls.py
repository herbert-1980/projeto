from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('banners/', include('banners.urls')),
    path('categorias/', include('categorias.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('promocoes/', include('promocoes.urls')),
    path('django_summernote/', include('django_summernote.urls')),
    path('perfil/', include('perfil.urls')),
    path('utilidade-publica/', include('public_services.urls')),
    path('enquetes/', include(('enquetes.urls', 'enquetes'), namespace='enquetes')),
    path('reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),
    path('signos/', include('signos.urls')), 

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

