# Generated by Django 5.1.2 on 2024-11-20 10:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_fllow'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Fllow',
            new_name='Follow',
        ),
    ]