from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from apps.promocoes.models import Promocao, ImagemPromocao

class ImagemPromocaoInline(admin.TabularInline):
    model = ImagemPromocao
    extra = 1  # Número de campos extras para adicionar no início
    max_num = 5  # Limita a quantidade de imagens por promoção
    fields = ('imagem', 'legenda', 'preview_image')  # Campos exibidos no admin
    readonly_fields = ('preview_image',)  # Campo somente leitura para prévia da imagem

    def preview_image(self, obj):
        """Mostra uma prévia da imagem no admin."""
        if obj.imagem:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagem.url)
        return "Nenhuma imagem"
    preview_image.short_description = "Prévia"

@admin.register(Promocao)
class PromocaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'data_inicio', 'data_fim')  # Campos exibidos no admin
    list_filter = ('empresa', 'data_inicio', 'data_fim')  # Filtros laterais
    search_fields = ('titulo', 'descricao', 'empresa__nome')  # Campos pesquisáveis no admin
    inlines = [ImagemPromocaoInline]  # Relaciona o Inline de imagens adicionais
    fieldsets = (
        ("Detalhes da Promoção", {
            'fields': ('empresa', 'titulo', 'descricao', 'imagem_principal', 'data_inicio', 'data_fim')
        }),
    )

@admin.register(ImagemPromocao)
class ImagemPromocaoAdmin(admin.ModelAdmin):
    list_display = ('promocao', 'legenda', 'preview_image')  # Campos exibidos no admin
    search_fields = ('legenda', 'promocao__titulo')  # Campos pesquisáveis
    list_filter = ('promocao',)  # Filtros laterais

    def preview_image(self, obj):
        """Mostra uma prévia da imagem no admin."""
        if obj.imagem:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagem.url)
        return "Nenhuma imagem"
    preview_image.short_description = "Prévia"
