# Generated by Django 3.0.4 on 2020-04-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_auto_20200419_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.TextField(max_length=1000, unique=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(max_length=500, unique=True, verbose_name='Вопрос'),
        ),
    ]
