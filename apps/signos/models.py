from django.db import models


class Signo(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    data_inicio = models.CharField(max_length=10)
    data_fim = models.CharField(max_length=10)
    icone_class = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        verbose_name = "Signo"
        verbose_name_plural = "Signos"
        ordering = ['nome']
        

    def __str__(self):
        return self.nome

