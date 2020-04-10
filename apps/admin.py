from django.contrib import admin
from .models import New, Article, Category


@admin.register(New)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'published_at', 'file', 'image',)
    list_filter = ('published_at',)


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'published_at', 'file', 'category',)
    list_filter = ('category', 'published_at',)


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    prepopulated_fields = {"slug": ("title",)}


# class OrderHasDetailsInline(admin.TabularInline):
#     model = DetailOrder
#     extra = 0
