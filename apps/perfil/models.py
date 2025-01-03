import os
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from apps.empresas.models import Empresa


def get_photo_upload_path(instance, filename):
    # Utilize o atributo direto da instância
    if instance.usuario:
        return os.path.join(f'perfil/{instance.usuario.username}', filename)
    return os.path.join('perfil/default', filename)



class Perfil(models.Model):
    STATE_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
        ]
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ]
    GROUP_BLOOD = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
        ]
    RH_FACTOR = [
        ('+', 'Rh Positivo'),
        ('-', 'Rh Negativo'),
    ]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, related_name='perfil')
    photo = models.ImageField(upload_to=get_photo_upload_path, blank=True)
    occupation = models.CharField(max_length=120, blank=True, verbose_name="Ocupação ou Empresa")
    description = models.TextField(blank=True, verbose_name="Sobre mim")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Gênero')
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    group_blood = models.CharField(max_length=2, choices=GROUP_BLOOD, default='A', verbose_name='Grupo Sanguíneo')
    rh_factor = models.CharField(max_length=1, blank=True, choices=RH_FACTOR, default='+', verbose_name='Fator Rh')
    weight = models.CharField(max_length=3, blank=True, verbose_name='Peso')
    street = models.CharField(max_length=100, blank=True, verbose_name="Rua/Logradouro/Trav.")
    house_number = models.IntegerField(default=0, verbose_name="Número")
    neighborhood = models.CharField(max_length=100, default="Bairro Desconhecido", verbose_name="Bairro")
    city = models.CharField(max_length=20, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='AC', verbose_name='Estado')
    cpf = models.CharField(max_length=11, blank=True, null=True)
    rg = models.CharField(max_length=11, blank=True, null=True)
    academic_qualification = models.TextField(blank=True, verbose_name="Qualificações Academicas")
    is_cnpj = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f' Perfil: {self.usuario.email}'

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_perfil(sender, instance, created, **kwargs):
    if created:  # Verifica se o usuário foi criado
        Perfil.objects.create(usuario=instance)  # Corrigido para usar instance diretamente

        