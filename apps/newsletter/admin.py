from django.contrib import admin
from .models import NewsletterSubscriber

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')  # Mostra a lista de emails e data de criação
    search_fields = ('email',)  # Permite pesquisar por email no painel
    list_filter = ('created_at',)  # Permite filtrar por data de criação    

