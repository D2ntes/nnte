from django.db import models
from django.utils.timezone import now


class Post(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=64, verbose_name='Название', )
    text = models.CharField(verbose_name='Текст', max_length=256, )
    published_at = models.DateTimeField(default=now, editable=True, verbose_name='Дата публиуации',)
    file = models.FileField(upload_to='news/', max_length=5000, verbose_name='Документ')

    background = models.ImageField(null=True, blank=True, upload_to='background/', verbose_name='Фон',)

class New(Post):
    file = models.FileField(upload_to='news/',)
    image = models.ImageField(null=True, blank=True, upload_to='image/',
                              verbose_name='Изображение', )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Article(Post):
    file = models.FileField(upload_to='article/',)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model):
    title = models.CharField(max_length=30, verbose_name='Имя', )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
