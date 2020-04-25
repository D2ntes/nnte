from .models import Category, Section, Company, Question, Vacancy
from django.contrib import auth
import random


def nav_sections(request):
    sections_nav = Section.objects.filter(visible=True).order_by('sequence')
    section_list = []
    for section in sections_nav:
        categories = Category.objects.filter(section=section.id, visible=True).order_by('sequence')
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


def vacancies(request):
    vacancies = Vacancy.objects.filter(visible=True).order_by('-published_at')
    count_obj = 4
    if len(vacancies) <= count_obj:
        last_vacancies = vacancies
    else:
        last_vacancies = vacancies[:count_obj]
    return {'last_vacancies': last_vacancies}
