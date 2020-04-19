from .models import Category, Section, Company, Question
from django.contrib import auth
import random

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


def contacts(request):
    contacts_company = Company.objects.all()
    return {'company': contacts_company[0]}


def questions(request):
    questions = Question.objects.all()
    rand_count = random.randint(0, len(questions) - 2)
    return {'most_questions': questions[rand_count]}