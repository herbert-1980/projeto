from django.contrib import admin
from .models import News, Tag
from django_summernote.admin import SummernoteModelAdmin


class NewsAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'status', 'published_at', 'is_published')
    prepopulated_fields = {'slug_title': ('title',)}
    search_fields = ('title', 'author__username', 'content')
    list_display_links = ('title',)
    readonly_fields = ('created_at', 'updated_at', 'views', 'share', )
    list_filter = ('status', 'categorias', )
    summernote_fields = ('content',)


    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'slug_title', 'author', 'status', 'content',
                       'resume', 'principal_image', 'video', 'source', 'views', 'share', 'categorias',
                       'published_at', 'seo_title', 'seo_description', 'is_published')
        }),
    )

    def display_categorias(self, obj):
        return ", ".join([categorias.nome for categorias in obj.categorias.all()])
    display_categorias.short_description = 'categorias'

"""@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug_title': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )"""

admin.site.register(News, NewsAdmin)
