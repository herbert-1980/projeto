from django.contrib import admin
from django.utils.html import format_html
from apps.signos.models import Signo


admin.site.site_title = 'Administração CoophaNews'
admin.site.site_header = 'Administração CoophaNews'
admin.site.index_title = 'CoophaNews'


@admin.register(Signo)
class SignoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_icone_class', 'data_inicio', 'data_fim')  # Mostra essas colunas na lista do admin
    search_fields = ('nome',)  # Adiciona barra de busca pelo nome
    list_filter = ('data_inicio', 'data_fim')  # Filtros laterais
    fieldsets = (
        (None, {
            'fields': ('nome', 'icone_class', 'data_inicio', 'data_fim',)
        }),
    )

    def get_icone_class(self, obj):
        if obj.icone_class:
             return format_html('<i class="{}" style="font-size: 20px;"></i>', obj.icone_class)
        return 'Ícone não disponível'
 
    get_icone_class.short_description = 'Ícone'
