# Generated by Django 5.1.6 on 2025-02-27 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscriber',
            new_name='NewsletterSubscriber',
        ),
    ]
