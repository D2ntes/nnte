# Generated by Django 3.0.4 on 2020-04-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_auto_20200418_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='fullname',
            field=models.CharField(max_length=150, unique=True, verbose_name='Полное название'),
        ),
    ]
