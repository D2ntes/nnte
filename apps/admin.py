from django.contrib import admin
from .models import New

@admin.register(New)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title_new', 'text_new', 'published_at', 'file_new', 'image_new')
