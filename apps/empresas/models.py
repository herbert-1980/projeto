import os
import unicodedata
from django.db import models
from django.core.validators import RegexValidator
from apps.categorias.models import Categoria
from django.utils import timezone



def normalize_filename(filename):
    return unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('utf-8')


def get_logo_upload_path(instance, filename):
    normalized_filename = normalize_filename(filename)
    if instance.fantasia:
        normalized_fantasia = normalize_filename(instance.fantasia)
        return os.path.join(f'logo/{normalized_fantasia}', normalized_filename)
    return os.path.join('logo/default', normalized_filename)


class Empresa(models.Model):
    # Lista de estados do Brasil
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
    razao = models.CharField(max_length=255)
    fantasia = models.CharField(max_length=255)
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message='O CNPJ deve ter 14 dígitos numéricos.'
            )
        ]
    )
    logo = models.ImageField(upload_to=get_logo_upload_path)
    telefone = models.CharField(max_length=15)
    rua = models.CharField(max_length=255)
    num = models.CharField(max_length=5)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, choices=STATE_CHOICES, default='AC', verbose_name='Estado')
    categorias = models.ManyToManyField(Categoria, related_name='empresas', blank=True)
    # Pegar as coordenadas do Google Maps
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    mapa_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.fantasia}'
    
    def is_open(self, current_datetime=None):
        if current_datetime is None:
            current_datetime = timezone.localtime()
        dia_semana = current_datetime.strftime('%a')[:3]
        hora_atual = current_datetime.time()

        horarios = self.horarios.filter(dia_da_semana=dia_semana, fechado=False)
        for horario in horarios:
            if horario.abertura <= hora_atual <= horario.fechamento:
                return True
        return False
    
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        
        
        
class HorarioFuncionamento(models.Model):
    DIA_DA_SEMANA_CHOICES = [
        ('Seg', 'Segunda-Feira'),
        ('Ter', 'Terça-Feira'),
        ('Qua', 'Quarta-Feira'),
        ('Qui', 'Quinta-Feira'),
        ('Sex', 'Sexta-Feira'),
        ('Sab', 'Sábado'),
        ('Dom', 'Domingo'),
    ]

    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='horarios')
    dia_da_semana = models.CharField(max_length=3, choices=DIA_DA_SEMANA_CHOICES, verbose_name="Dia da Semana")
    abertura = models.TimeField(null=True, blank=True, verbose_name="Horário de Abertura")
    fechamento = models.TimeField(null=True, blank=True, verbose_name="Horário de Fechamento")
    fechado = models.BooleanField(default=False, verbose_name="Fechado")

    class Meta:
        db_table = 'empresas'
        unique_together = ('empresa', 'dia_da_semana')  # Corrigido o nome do campo
        verbose_name = "Horário de Funcionamento"
        verbose_name_plural = "Horários de Funcionamento"
        ordering = ['empresa__razao', 'dia_da_semana']

    def __str__(self):
        if self.fechado:
            return f'{self.empresa.fantasia} - {self.get_dia_da_semana_display()}: Fechado'
        return f'{self.empresa.fantasia} - {self.get_dia_da_semana_display()}: {self.abertura} às {self.fechamento}'
    
    

    # Método para verificar se a empresa está aberta no momento atual
    @property
    def is_open_now(self):
        current_datetime = timezone.localtime()
        dia_semana = current_datetime.strftime('%a')[:3]
        hora_atual = current_datetime.time()

        if self.dia_da_semana == dia_semana:
            if self.fechado:
                return False
            return self.abertura <= hora_atual <= self.fechamento
        return False
