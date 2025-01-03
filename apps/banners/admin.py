from django.contrib import admin
from django.utils.html import format_html, mark_safe
from apps.banners.models import Banner, BannerImage, BannerView

admin.site.site_title = 'Administração CoophaNews'
admin.site.site_header = 'Administração CoophaNews'
admin.site.index_title = 'CoophaNews'

# Admin para BannerImage
class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1  # Número de formulários em branco adicionais para adicionar imagens
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.additional_images:
            return mark_safe(f'<img src="{obj.additional_images.url}" width="100" />')
        return 'No Image'

    image_preview.short_description = 'Preview da Imagem'

# Admin para Banner
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'fantasia', 
        'get_company_logo', 
        'get_company_categorias', 
        'get_banner_thumbnail', 
        'destaque', 
        'data_inicio', 
        'data_final', 
        'letra',
    )
    search_fields = ('letra', 'fantasia__fantasia',)
    list_editable = ('destaque',)
    list_filter = ('destaque', 'data_inicio', 'data_final',)
    list_per_page = 10
    filter_horizontal = ('categorias',)

    fieldsets = (
        (None, {
            'fields': ('fantasia', 'banner', 'destaque', 'data_inicio', 'data_final', 'letra',)
        }),
    )
    
    inlines = [BannerImageInline]  # Registro do BannerImageInline

    def get_company_categorias(self, obj):
        return ", ".join([categoria.nome_categoria for categoria in obj.fantasia.categorias.all()])
    get_company_categorias.short_description = 'Categoria da Empresa'

    def get_company_logo(self, obj):
        if obj.fantasia.logo:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.fantasia.logo.url)
        return 'Logo não disponível'

    def get_banner_thumbnail(self, obj):
        if obj.banner:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 50px;" />', obj.banner.url)
        return 'Banner não disponível'
    
    get_banner_thumbnail.short_description = 'Miniatura do Banner'

# Admin para BannerView
@admin.register(BannerView)
class BannerViewAdmin(admin.ModelAdmin):
    list_display = ('banner', 'ip_address', 'timestamp')
    search_fields = ('ip_address',)
    list_filter = ('timestamp',)

# Registro do Banner
admin.site.register(Banner, BannerAdmin)
