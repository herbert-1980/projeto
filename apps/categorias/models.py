from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=250, unique=True, verbose_name='Nome da Categoria')
    slug_categoria = models.SlugField(unique=True, blank=True, verbose_name='Slug da Categoria')
    icone_categoria = models.CharField(max_length=100, blank=True, verbose_name='Icone da Categoria')
    master_categoria = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategorias')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Se o slug estiver vazio, gera automaticamente
        if not self.slug_categoria: 
            base_slug = slugify(self.nome_categoria)
            slug = base_slug
            count = 1
            self.slug_categoria = slugify(self.nome_categoria)
            while Categoria.objects.filter(slug_categoria=slug).exists():
                slug = f"{ base_slug }-{ count }"
                count += 1
            self.slug_categoria = slug
        super().save(*args, **kwargs)

    
    def __str__(self):
        if self.master_categoria:
            return F"{ self.master_categoria } > { self.nome_categoria }"
        return self.nome_categoria

    class Meta:
        db_table = 'categorias'
        ordering = ['nome_categoria']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'