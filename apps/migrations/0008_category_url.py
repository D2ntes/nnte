# Generated by Django 3.0.4 on 2020-04-09 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20200409_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url',
            field=models.URLField(default='/teplo', verbose_name='Ссылка'),
            preserve_default=False,
        ),
    ]