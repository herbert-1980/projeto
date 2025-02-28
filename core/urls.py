from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.news.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('banners/', include('apps.banners.urls')),
    path('categorias/', include('apps.categorias.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('promocoes/', include('apps.promocoes.urls')),
    path('django_summernote/', include('django_summernote.urls')),
    path('perfil/', include('apps.perfil.urls')),
    path('utilidade-publica/', include('apps.public_services.urls')),
    path('enquetes/', include(('apps.enquetes.urls', 'enquetes'), namespace='enquetes')),
    path('reviews/', include(('apps.reviews.urls', 'reviews'), namespace='reviews')),
    path('signos/', include('apps.signos.urls')),
    path('empresas/', include('apps.empresas.urls')),
    path('contato/', include('apps.contatos.urls')),
    path('newsletter/', include('apps.newsletter.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

