# Generated by Django 5.1.4 on 2024-12-30 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_categoria', models.CharField(max_length=250, unique=True, verbose_name='Nome da Categoria')),
                ('slug_categoria', models.SlugField(default='default-slug', unique=True, verbose_name='Slug da Categoria')),
                ('icone_categoria', models.CharField(blank=True, max_length=100, verbose_name='Icone da Categoria')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categorias',
                'ordering': ['nome_categoria'],
            },
        ),
    ]
