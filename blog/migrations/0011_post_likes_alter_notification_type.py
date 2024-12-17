# Generated by Django 5.1.2 on 2024-12-04 07:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_notification_link'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('COMMENT', 'comment'), ('LIKE', 'like'), ('FOLLOW', 'follow'), ('NEW_POST', 'new_post')], default='OTHER', max_length=255),
        ),
    ]
