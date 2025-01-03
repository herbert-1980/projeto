from django.db import models
from django.core.exceptions import ValidationError
from apps.empresas.models import Empresa

class Promocao(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="promocoes")
    titulo = models.CharField(max_length=250)
    descricao = models.TextField()
    imagem_principal = models.ImageField(upload_to="promocoes/")
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    def __str__(self):
        return self.titulo

class ImagemPromocao(models.Model):
    promocao = models.ForeignKey(Promocao, on_delete=models.CASCADE, related_name='imagens_da_promocao')
    imagem = models.ImageField(upload_to='promocoes/imagens/')
    legenda = models.CharField(max_length=255, blank=True)

    def clean(self):
        if self.promocao and self.promocao.pk and self.promocao.imagens_da_promocao.count() >= 5:
            raise ValidationError("Uma promoção pode ter no máximo 5 imagens adicionais.")


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.legenda or "Imagem adicional"
