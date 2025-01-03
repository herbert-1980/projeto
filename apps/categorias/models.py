from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=250, unique=True, verbose_name='Nome da Categoria')
    slug_categoria = models.SlugField(default='default-slug', unique=True, verbose_name='Slug da Categoria')
    icone_categoria = models.CharField(max_length=100, blank=True, verbose_name='Icone da Categoria')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Se o slug estiver vazio, gera automaticamente
        if not self.slug_categoria:
            self.slug_categoria = slugify(self.name_categoria)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'categorias'
        ordering = ['nome_categoria']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome_categoria
