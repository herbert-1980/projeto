# Generated by Django 5.1.4 on 2025-01-09 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
        ('categorias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='categorias',
            field=models.ManyToManyField(related_name='banners', to='categorias.categoria', verbose_name='Categorias'),
        ),
    ]
