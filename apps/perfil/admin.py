from django.utils.html import format_html
from django.contrib import admin
from apps.perfil.models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'phone', 'birth_date', 'get_photo_thumbnail', 'city', 'state', 'occupation')
    search_fields = ('usuario__email', 'phone', 'city', )
    list_filter = ('state',)


    def get_photo_thumbnail(self, obj):
        if obj.photo:  # Verifica se há uma imagem
            return format_html('<img src="{}" style="height: 50px; width: 50px; border-radius: 50%;">', obj.photo.url)
        return "Sem imagem"
    get_photo_thumbnail.short_description = "Foto de Perfil"
    
