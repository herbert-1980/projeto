import os
from django.db import models
from apps.categorias.models import Categoria
from apps.empresas.models import Empresa
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone


def get_banner_upload_path(instance, filename):
    if isinstance(instance, BannerImage):
        return os.path.join('banners/additional', filename)
    if instance.fantasia and instance.fantasia.fantasia:
        empresa_slug = slugify(instance.fantasia.fantasia)
        return os.path.join(f'banners/{empresa_slug}', filename)
    return os.path.join('banners/default', filename)

@property
def is_active(self):
    now = timezone.now()
    return self.data_inicio <= now <= self.data_final

class Banner(models.Model):
    OPCOES_DESTAQUE = [
        (1, 'Simples'),
        (2, 'Destaque'),
        (3, 'Vip'),
        (4, 'Capa'),
        (5, 'Extra')
    ]
    LETTER_CHOICES = [
        (chr(i), chr(i)) for i in range(65, 91)
    ]

    # Campos do modelo
    fantasia = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING, verbose_name='Escolha a Empresa')
    banner = models.ImageField(upload_to=get_banner_upload_path)
    destaque = models.IntegerField(choices=OPCOES_DESTAQUE, default='1', verbose_name='Destaque')
    data_inicio = models.DateTimeField()
    data_final = models.DateTimeField()
    letra = models.CharField(max_length=1, choices=LETTER_CHOICES, default='A')
    categorias = models.ManyToManyField(Categoria, related_name='banners')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'banners'
        ordering = ['data_inicio','fantasia']


    def clean(self):
        super().clean()
        # Validar tamanho da imagem
        if self.banner and self.banner.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("O tamanho da imagem não pode exceder 2 MB.")
        if not self.data_inicio or not self.data_final:
            raise ValidationError('As datas de início e final são obrigatórias.')
        if self.data_final <= self.data_inicio:
            raise ValidationError('A data final deve ser posterior à data de início.')

    def is_active(self):
        now = timezone.now()
        return self.data_inicio <= now <= self.data_final
    
    def __str__(self):
        return f"Banner {self.fantasia.fantasia}"

class BannerImage(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='additional_images')
    additional_images = models.ImageField(upload_to=get_banner_upload_path)

    def clean(self):
        if self.additional_images and self.additional_images.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("O tamanho da imagem não pode exceder 2 MB.")
        
    def __str__(self):
        return f"Imagem para {self.banner.fantasia.fantasia}"
    
class BannerView(models.Model):
    banner = models.ForeignKey('Banner', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.banner} - {self.ip_address} - {self.timestamp}"
    
