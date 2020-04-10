from .models import Category, Section
from django.contrib import auth
from django.db.models import Sum


def nav_sections(request):
    sections_nav = Section.objects.all()
    section_list = []
    for section in sections_nav:
        categories = Category.objects.filter(section=section.id).order_by('title')
        category_list = []
        for category in categories:
            category_list.append(
                {'id': category.id, 'title': category.title, 'slug': category.slug})

        section_list.append({'id': section.id, 'title': section.title, 'slug': section.slug,
                         'category_list': category_list})

    return {"section_list": section_list}
