from django.contrib import admin
from .models import New, Article, Category

@admin.register(New)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'published_at', 'file', 'image')

@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'published_at', 'file', 'category')

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title',)
