import re
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from core import settings  # Para o campo de usuário em Feedback
from django.core.validators import RegexValidator, EmailValidator



class PublicUtility(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    contact_info = models.CharField(max_length=200, blank=True, verbose_name='Contato')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Utilidade Pública"
        verbose_name_plural = "Utilidades Públicas"


class LostAndFound(models.Model):
    CATEGORY_CHOICES = [
        ('lost', 'Perdido'),
        ('found', 'Achado'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('resolved', 'Resolvido'),
    ]

    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    categoria = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='lost', verbose_name='Categoria')
    contact_info = models.CharField(max_length=200, blank=True, verbose_name='Seu contato')
    def clean(self):
        super().clean()  # Certifique-se de chamar o método clean da classe base
        if self.contact_info:
            # Verificar se é um e-mail válido
            email_validator = EmailValidator('E-mail inválido.')
            try:
                email_validator(self.contact_info)
            except ValidationError:
                # Se não for um e-mail, verificar se é um telefone válido
                phone_regex = r'^\+?1?\d{9,15}$'
                if not re.match(phone_regex, self.contact_info):
                    raise ValidationError(
                        'O campo de contato deve ser um número de telefone válido ou um e-mail válido.'
                    )
                    
    location = models.CharField(max_length=200, blank=True, verbose_name='Local para Entrega')
    latitude = models.FloatField(blank=True, null=True, verbose_name='Latitude')
    longitude = models.FloatField(blank=True, null=True, verbose_name='Longitude')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    image = models.ImageField(upload_to='lost_and_found/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False, verbose_name='Aprovado')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    class Meta:
        verbose_name = "Achados e Perdidos"
        verbose_name_plural = "Achados e Perdidos"
        ordering = ['-created_at']  # Itens mais recentes primeiro


class LostAndFoundImage(models.Model):
    lost_and_found = models.ForeignKey('LostAndFound', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='lost_and_found/', verbose_name='Imagem')

    def __str__(self):
        return f"Imagem de {self.lost_and_found.title}"


class LostAndFoundUpdate(models.Model):
    lost_and_found = models.ForeignKey('LostAndFound', on_delete=models.CASCADE, related_name='updates')
    comment = models.TextField(verbose_name='Comentário')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atualização em {self.created_at.strftime('%d/%m/%Y')} - {self.lost_and_found.title}"


class Feedback(models.Model):
    item = models.ForeignKey(LostAndFound, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ajuste aqui
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Nota')  # De 1 a 5 estrelas
    comment = models.TextField(blank=True, null=True, verbose_name='Comentário')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.user.username} para {self.item.title}"


def clean(self):
    if not self.title or not self.description:
        raise ValidationError("O título e a descrição são obrigatórios.")
    
    if (self.latitude is not None and self.longitude is None) or (self.longitude is not None and self.latitude is None):
        raise ValidationError("Latitude e longitude devem ser preenchidas juntas.")
    
    if not self.comment:
        raise ValidationError("O comentário não pode estar vazio.")
    
    if self.rating < 1 or self.rating > 5:
        raise ValidationError("A nota deve estar entre 1 e 5.")
    
    