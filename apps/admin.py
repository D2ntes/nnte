from django.contrib import admin
from .models import New, Article, Category, Section, Company, Department, Question, Vacancy
from .forms import ReviewArticle, ReviewNew, ReviewCompany
from django.utils.safestring import mark_safe


def make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)


make_visible.short_description = "Сделать видимыми"


def make_invisible(modeladmin, request, queryset):
    queryset.update(visible=False)


make_invisible.short_description = "Сделать невидимыми"


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'sequence', 'visible',)
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_visible, make_invisible]


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'section', 'sequence', 'visible',)
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_visible, make_invisible]
    list_editable = ['visible', 'sequence', ]


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    form = ReviewArticle
    fields = ['title', 'category', 'text', 'file', 'published_at', ]
    list_display = ('title', 'category', 'file', 'published_at',)
    list_filter = ('category', 'published_at',)


@admin.register(New)
class NewsAdmin(admin.ModelAdmin):
    form = ReviewNew
    fields = ['title', 'text', 'published_at', 'file', 'image']
    list_display = ('title', 'text', 'published_at', 'file', 'image',)
    list_filter = ('published_at',)
    search_fields = ['title', 'text', ]
    save_on_top = True


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    form = ReviewCompany
    list_display = ('name', 'address', 'tel', 'fax', 'email',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = ['name', 'address', 'tel', 'fax', 'email', 'sequence', ]
    list_display = ('name', 'address', 'tel', 'fax', 'email',)
    actions = [make_visible, make_invisible]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['question', 'answer', ]
    list_display = ('question', 'answer',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'published_at', 'visible',)
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_visible, make_invisible]
    list_editable = ['visible']
# class OrderHasDetailsInline(admin.TabularInline):
#     model = DetailOrder
#     extra = 0
