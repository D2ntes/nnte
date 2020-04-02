from django.db import models
from django.utils.timezone import now


class New(models.Model):
    title_new = models.CharField(max_length=64, verbose_name='Название', )
    text_new = models.CharField(verbose_name='Текст', max_length=256, )
    published_at = models.DateTimeField(default=now, editable=True, verbose_name='Дата публиуации',)
    file_new = models.FileField(upload_to='news/', max_length=5000, verbose_name='Документ')
    image_new = models.ImageField(null=True, blank=True, upload_to='news/image/', verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

