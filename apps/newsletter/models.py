from django.db import models
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your models here.
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
