# Generated by Django 5.1.3 on 2024-12-01 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_testquestion_max_score_testtries_attempts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='max_score',
            field=models.IntegerField(default=10, verbose_name='Максимальная оценка'),
        ),
        migrations.AlterField(
            model_name='homeworksubmission',
            name='score',
            field=models.IntegerField(default=0, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='testtries',
            name='score',
            field=models.IntegerField(default=0, verbose_name='Оценка'),
        ),
    ]
