from django.contrib import admin
from .models import New, Article, Category, Section, Company, Department, Question
from .forms import ReviewArticle, ReviewNew, ReviewCompany


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'section')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    form = ReviewArticle
    fields = ['title',  'category', 'text', 'file', 'published_at', ]
    list_display = ('title',  'category', 'file', 'published_at',)
    list_filter = ('category', 'published_at',)


@admin.register(New)
class NewsAdmin(admin.ModelAdmin):
    form = ReviewNew
    fields = ['title', 'text', 'published_at', 'file', 'image']
    list_display = ('title', 'published_at', 'file', 'image',)
    list_filter = ('published_at',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    form = ReviewCompany
    list_display = ('name', 'address', 'tel', 'fax', 'email', )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = ['name',  'address', 'tel', 'fax', 'email', ]
    list_display = ('name', 'address', 'tel', 'fax', 'email',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['question',  'answer', ]
    list_display = ('question',  'answer', )




# class OrderHasDetailsInline(admin.TabularInline):
#     model = DetailOrder
#     extra = 0
