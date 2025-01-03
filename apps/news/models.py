from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.accounts.models import MyUser
from apps.categorias.models import Categoria
from django.urls import reverse


class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
        ('priority', 'Prioridade'),
    ]
    # Identificação e MetaDados
    title = models.CharField(max_length=255, verbose_name='Título')
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name='Sub Título')
    slug_title = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                               null=True, related_name='news', verbose_name='Autor')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft', verbose_name='Status')

    # Conteúdo da Notícia
    content = models.TextField(verbose_name='Conteúdo da Notícia')
    resume = models.TextField(max_length=500, blank=True, null=True, verbose_name='Resumo da Notícia')
    principal_image = models.ImageField(upload_to='news/images/%Y/%m/%d', blank=True, null=True,
                                        verbose_name='Imagem Principal')
    video = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=255, null=True, blank=True, verbose_name='Fonte da Notícia')
    views = models.IntegerField(default=0, verbose_name='Visualizações')
    share = models.PositiveIntegerField(default=0, verbose_name='Compartilhamentos')

    # Categorias e Tags
    categorias = models.ManyToManyField(Categoria, related_name='news', verbose_name='Escolha as Categorias')

    # Publicação e Datas
    published_at = models.DateTimeField(default=timezone.now, verbose_name='Publicada em')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True)
    

    # SEO e Social Media
    seo_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Título do SEO')
    seo_description = models.TextField(max_length=160, blank=True, null=True, verbose_name='Descrição do SEO')
    is_published = models.BooleanField(default=False,
                                       verbose_name='Publicar Notícia?')  # Campo booleano para publicar ou não a notícia

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug_title])

    class Meta:
        db_table = 'news'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_given', verbose_name='Autor')
    news = models.ForeignKey(News, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])

    class Meta:
        unique_together = (('user', 'news'),)
        db_table = 'ratings'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
