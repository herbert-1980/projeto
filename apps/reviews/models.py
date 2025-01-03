from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Quem fez o review
    rating = models.PositiveSmallIntegerField()  # Avaliação de 1 a 5
    comment = models.TextField(blank=True, null=True)  # Comentário opcional
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # O tipo do objeto a ser revisado
    object_id = models.PositiveIntegerField()  # ID do objeto a ser revisado
    content_object = GenericForeignKey('content_type', 'object_id')  # Referência genérica ao objeto

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.content_object} by {self.user} - {self.rating} stars'
