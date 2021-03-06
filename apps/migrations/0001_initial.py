# Generated by Django 3.0.4 on 2020-04-18 15:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Название')),
                ('address', models.CharField(max_length=100, unique=True, verbose_name='Адрес')),
                ('tel', models.CharField(max_length=20, unique=True, verbose_name='Телефон')),
                ('fax', models.CharField(max_length=20, unique=True, verbose_name='Факс')),
            ],
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
                ('text', models.CharField(max_length=100000, verbose_name='Текст')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публиуации')),
                ('file', models.FileField(blank=True, null=True, upload_to='news/', verbose_name='Документ')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Имя')),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('about_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apps.About')),
                ('fullname', models.CharField(max_length=30, unique=True, verbose_name='Полное название')),
                ('about', models.CharField(default='', max_length=3000, unique=True, verbose_name='О компании')),
            ],
            options={
                'verbose_name': 'Информация о компании',
                'verbose_name_plural': 'Информация о компании',
            },
            bases=('apps.about', models.Model),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='Имя')),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Section', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публиуации')),
                ('file', models.FileField(blank=True, null=True, upload_to='article/', verbose_name='Документ')),
                ('text', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Текст')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=20, unique=True, verbose_name='E-mail')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
    ]
