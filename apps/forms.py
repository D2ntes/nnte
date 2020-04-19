from django import forms
from .models import Article, New, Company

from ckeditor.widgets import CKEditorWidget


class Review(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        abstract = True


class ReviewArticle(Review):

    class Meta:
        model = Article
        fields = ['title', 'published_at', 'file']
        verbose_name = 'Текст'


class ReviewNew(Review):

    class Meta:
        model = New
        fields = ['title', 'published_at', 'file', 'image']
        verbose_name = 'Текст'


class ReviewCompany(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget())
    important =  forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Company
        fields = ['name', 'fullname', 'address', 'tel', 'fax', 'email', 'about']
        verbose_name = 'О компании'
