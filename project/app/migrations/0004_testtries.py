# Generated by Django 5.1.3 on 2024-11-21 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_test_max_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_tries', to='app.test', verbose_name='Вопрос')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tries', to='app.test', verbose_name='Тест')),
            ],
        ),
    ]
