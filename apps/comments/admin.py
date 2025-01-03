from django.contrib import admin
from apps.comments.models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_name', 'comment_email', 'comment_user', 'comment_news', 
                    'comment_date', 'comment_published', )
    list_editable = ('comment_published', )
    list_display_links = ('id', 'comment_name', 'comment_email', )
    readonly_fields = ('comment_date',)
    search_fields = ('comment_name', 'comment_email', 'comment')
    actions = ['aprovar_comentarios']

admin.site.register(Comment, CommentAdmin)