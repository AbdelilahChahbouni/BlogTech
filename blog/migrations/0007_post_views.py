# Generated by Django 5.1.2 on 2024-11-17 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]