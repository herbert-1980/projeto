from django.db import models
from django.conf import settings


class Enquete(models.Model):
    pergunta = models.CharField(max_length=255, verbose_name='Pergunta')
    ativo = models.BooleanField(default=False, verbose_name='Ativo')  
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.pergunta

class Escolha(models.Model):
    enquete = models.ForeignKey(Enquete, related_name='escolha', on_delete=models.CASCADE)
    escolha_text = models.CharField(max_length=255)
    votos = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='img/enquetes/', blank=True, null=True)

    def __str__(self):
        return self.escolha_text


class Voto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    escolha = models.ForeignKey(Escolha, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'enquete')
        # Garantir que um usuário possa votar apenas uma vez por enquete
        