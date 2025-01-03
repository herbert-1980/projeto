from django.contrib import admin
from django.shortcuts import render
from apps.public_services.models import PublicUtility, LostAndFound, LostAndFoundImage, LostAndFoundUpdate


@admin.register(PublicUtility)
class PublicUtilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    search_fields = ('title',)
    list_filter = ('is_active', 'created_at')


class LostAndFoundImageInline(admin.TabularInline):
    model = LostAndFoundImage
    extra = 1
    
class LostAndFoundUpdateInline(admin.TabularInline):
    model = LostAndFoundUpdate
    extra = 1
    
@admin.register(LostAndFound)
class LostAndFoundAdmin(admin.ModelAdmin):
    list_display = ('title', 'categoria', 'status', 'is_approved', 'is_active', 'created_at')  # Corrigido: is_approved
    list_filter = ('categoria', 'status', 'is_approved', 'is_active')  # Corrigido: is_approved
    search_fields = ('title', 'description', 'location')
    ordering = ('-created_at',)
    actions = ['approve_items']
    
    @admin.action(description='Aprovar itens selecionados')
    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)




