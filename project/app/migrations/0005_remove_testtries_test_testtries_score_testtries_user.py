# Generated by Django 5.1.3 on 2024-11-21 13:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_testtries'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testtries',
            name='test',
        ),
        migrations.AddField(
            model_name='testtries',
            name='score',
            field=models.IntegerField(blank=True, null=True, verbose_name='Оценка'),
        ),
        migrations.AddField(
            model_name='testtries',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='test_user_tries', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
    ]
