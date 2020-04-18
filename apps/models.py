from django.db import models
from django.utils.timezone import now


class Post(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=64, verbose_name='Название', )
    text = models.CharField(max_length=100000, verbose_name='Текст',)
    published_at = models.DateTimeField(default=now, editable=True,
                                        verbose_name='Дата публиуации', )
    background = models.ImageField(null=True, blank=True, upload_to='background/',
                                   verbose_name='Фон', )


class New(Post):
    file = models.FileField(upload_to='news/', null=True, blank=True, verbose_name='Документ')
    image = models.ImageField(upload_to='image/', null=True, blank=True,
                              verbose_name='Изображение', )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Article(Post):
    file = models.FileField(upload_to='article/', null=True,  blank=True, verbose_name='Документ')
    text = models.CharField(null=True, max_length=10000, blank=True, verbose_name='Текст')
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Category(models.Model):
    title = models.CharField(max_length=30, verbose_name='Имя', )
    slug = models.SlugField(max_length=30, unique=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, null=True,
                                verbose_name='Раздел')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.section} - {self.title}'


class Section(models.Model):
    title = models.CharField(max_length=30, verbose_name='Имя', )
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title
