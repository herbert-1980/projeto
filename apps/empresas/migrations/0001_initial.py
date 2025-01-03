# Generated by Django 5.1.4 on 2024-12-30 20:44

import apps.empresas.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razao', models.CharField(max_length=255)),
                ('fantasia', models.CharField(max_length=255)),
                ('cnpj', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='O CNPJ deve ter 14 dígitos numéricos.', regex='^\\d{14}$')])),
                ('logo', models.ImageField(upload_to=apps.empresas.models.get_logo_upload_path)),
                ('telefone', models.CharField(max_length=15)),
                ('rua', models.CharField(max_length=255)),
                ('num', models.CharField(max_length=5)),
                ('bairro', models.CharField(max_length=255)),
                ('cep', models.CharField(max_length=9)),
                ('cidade', models.CharField(blank=True, max_length=100)),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], default='AC', max_length=2, verbose_name='Estado')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('mapa_url', models.TextField(blank=True, null=True)),
                ('categorias', models.ManyToManyField(blank=True, related_name='empresas', to='categorias.categoria')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='HorarioFuncionamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_da_semana', models.CharField(choices=[('Seg', 'Segunda-Feira'), ('Ter', 'Terça-Feira'), ('Qua', 'Quarta-Feira'), ('Qui', 'Quinta-Feira'), ('Sex', 'Sexta-Feira'), ('Sab', 'Sábado'), ('Dom', 'Domingo')], max_length=3, verbose_name='Dia da Semana')),
                ('abertura', models.TimeField(blank=True, null=True, verbose_name='Horário de Abertura')),
                ('fechamento', models.TimeField(blank=True, null=True, verbose_name='Horário de Fechamento')),
                ('fechado', models.BooleanField(default=False, verbose_name='Fechado')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='empresas.empresa')),
            ],
            options={
                'verbose_name': 'Horário de Funcionamento',
                'verbose_name_plural': 'Horários de Funcionamento',
                'db_table': 'empresas',
                'ordering': ['empresa__razao', 'dia_da_semana'],
                'unique_together': {('empresa', 'dia_da_semana')},
            },
        ),
    ]
