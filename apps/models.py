from django.db import models
from django.utils.timezone import now


class Post(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=64, verbose_name='Название', )
    text = models.TextField(max_length=100000, verbose_name='Текст', )
    published_at = models.DateTimeField(default=now, editable=True,
                                        verbose_name='Дата публикации', )

    def __str__(self):
        return self.title


class New(Post):
    file = models.FileField(upload_to='news/', null=True, blank=True, max_length=120,
                            verbose_name='Документ')
    image = models.ImageField(upload_to='image/', null=True, blank=True,
                              verbose_name='Изображение', )

    def cropped_text(self, count_stroke, len_stroke):
        end_symbols = '...'
        cropped_text = []
        count = -count_stroke + 1
        for word in self.text.split():
            cropped_text.append(word)
            if len(' '.join(cropped_text)) > len_stroke * (count_stroke + count):

                if count == 0:
                    cropped_text.append(end_symbols)
                    break
                else:
                    count += 1
                cropped_text.append('<br />')

        description = ' '.join(cropped_text)
        while description.count('<br />') <= 4:
            description += '<br />'

        return description

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Article(Post):
    file = models.FileField(upload_to='article/', null=True, blank=True, max_length=120,
                            verbose_name='Документ')
    text = models.TextField(null=True, max_length=10000, blank=True, verbose_name='Текст')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 verbose_name='Категория', related_name='category', null=True, )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Имя', )
    slug = models.SlugField(max_length=50, unique=True)
    sequence = models.IntegerField(verbose_name='Порядок следования', null=False)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL,
                                verbose_name='Раздел', related_name='section', null=True, )
    visible = models.BooleanField(verbose_name='Видимый', default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.section} - {self.title}'


class Section(models.Model):
    title = models.CharField(max_length=30, verbose_name='Имя', )
    slug = models.SlugField(max_length=30, unique=True)
    sequence = models.IntegerField(unique=True, verbose_name='Порядок следования')
    visible = models.BooleanField(verbose_name='Видимый', default=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class About(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название', )
    address = models.CharField(max_length=100, unique=True, verbose_name='Адрес', )
    tel = models.CharField(max_length=20, unique=True, verbose_name='Телефон', )
    fax = models.CharField(max_length=20, unique=True, verbose_name='Факс', )
    email = models.EmailField(max_length=20, unique=True, verbose_name='E-mail', )

    def __str__(self):
        return self.name


class Company(SingletonModel, About):
    fullname = models.CharField(max_length=150, unique=True, verbose_name='Полное название', )
    about = models.TextField(max_length=3000, unique=True, verbose_name='О компании', default='', )
    important = models.TextField(max_length=3000, unique=True, verbose_name='О компании',
                                 default='', )

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'


class Department(models.Model):
    name = models.CharField(max_length=30, unique=False, verbose_name='Название', )
    address = models.CharField(max_length=100, unique=False, verbose_name='Адрес', )
    tel = models.CharField(max_length=20, unique=False, verbose_name='Телефон', )
    fax = models.CharField(max_length=20, unique=False, verbose_name='Факс', )
    email = models.CharField(max_length=20, unique=False, verbose_name='E-mail', )
    company = models.ForeignKey('Company', on_delete=models.SET_NULL,
                                verbose_name='Компания', default=1, related_name='company',
                                null=True, )
    sequence = models.IntegerField(unique=True, verbose_name='Порядок следования')

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Question(models.Model):
    question = models.TextField(max_length=500, unique=True, verbose_name='Вопрос', )
    answer = models.TextField(max_length=1000, unique=True, verbose_name='Ответ', )

    class Meta:
        verbose_name = 'Часто задаваемые вопросы'
        verbose_name_plural = 'Часто задаваемые вопросы'


class Vacancy(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Назавание', )
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, verbose_name='Описание', )
    published_at = models.DateTimeField(default=now, editable=True,
                                        verbose_name='Дата публикации', )
    visible = models.BooleanField(verbose_name='Видимый', default=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансия'
