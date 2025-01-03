from django.contrib import admin
from django.utils.html import format_html
from apps.enquetes.models import Enquete, Escolha


class EscolhaInLine(admin.TabularInline):
    model = Escolha
    extra = 3
    fields = ['escolha_text', 'imagem', 'imagem_preview']  # Adiciona pré-visualização ao admin
    readonly_fields = ['imagem_preview']  # Campo somente leitura para exibir a imagem

    def imagem_preview(self, obj):
        """
        Retorna uma pré-visualização da imagem se ela existir.
        """
        if obj.imagem:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.imagem.url)
        return "Sem imagem"
    imagem_preview.short_description = "Pré-visualização"  # Nome do campo no admin


class EnqueteAdmin(admin.ModelAdmin):
    list_display = ['pergunta', 'ativo', 'created_at']  # Adiciona campos à listagem do admin
    list_filter = ['ativo', 'created_at']  # Permite filtrar por estes campos
    search_fields = ['pergunta']  # Permite buscar pela pergunta no admin
    inlines = [EscolhaInLine]


admin.site.register(Enquete, EnqueteAdmin)
