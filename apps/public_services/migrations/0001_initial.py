# Generated by Django 5.1.4 on 2024-12-30 20:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LostAndFound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('categoria', models.CharField(choices=[('lost', 'Perdido'), ('found', 'Achado')], default='lost', max_length=10, verbose_name='Categoria')),
                ('contact_info', models.CharField(blank=True, max_length=200, verbose_name='Seu contato')),
                ('location', models.CharField(blank=True, max_length=200, verbose_name='Local para Entrega')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('resolved', 'Resolvido')], default='pending', max_length=10, verbose_name='Status')),
                ('image', models.ImageField(blank=True, null=True, upload_to='lost_and_found/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Achados e Perdidos',
                'verbose_name_plural': 'Achados e Perdidos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PublicUtility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('contact_info', models.CharField(blank=True, max_length=200, verbose_name='Contato')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Utilidade Pública',
                'verbose_name_plural': 'Utilidades Públicas',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Nota')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comentário')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='public_services.lostandfound')),
            ],
        ),
        migrations.CreateModel(
            name='LostAndFoundImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='lost_and_found/', verbose_name='Imagem')),
                ('lost_and_found', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='public_services.lostandfound')),
            ],
        ),
        migrations.CreateModel(
            name='LostAndFoundUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Comentário')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lost_and_found', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='public_services.lostandfound')),
            ],
        ),
    ]
