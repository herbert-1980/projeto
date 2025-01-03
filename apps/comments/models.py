from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Comment(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    comment_name = models.CharField(max_length=150)
    comment_email = models.EmailField()
    comment = models.TextField()
    comment_news = models.ForeignKey('news.News', on_delete=models.CASCADE, related_name='comments')
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    comment_date = models.DateTimeField(default=timezone.now)
    comment_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        
    def __str__(self):
        return self.comment_name
    