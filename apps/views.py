from django.shortcuts import render
from .models import New, Category, Article
from django.core.paginator import Paginator


def index(request):
    template = 'index.html'
    list_news = []
    news_last = New.objects.all().order_by('-published_at')[:6]
    for new in news_last:
        object_new = {'id': new.id,
                      'title': new.title,
                      'text': new.text,
                      'image': new.image,
                      'file': new.file,
                      }
        list_news.append(object_new)
    return render(request, template, context={'first_new':list_news[0], 'list_news': list_news[1:]})


def news(request):
    template = 'news.html'
    list_news = []
    news = New.objects.all().order_by('-published_at')
    for new in news:
        object_new = {'id': new.id,
                      'title': new.title,
                      'text': new.text,
                      'image': new.image,
                      'file': new.file,
                      }
        list_news.append(object_new)

    stops_page, current_page, prev_page_url, next_page_url = pagination(request, list_news, 5)

    context = {
        'list_news': stops_page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }

    return render(request, template, context=context)


def category(request, the_slug):
    template = 'category.html'
    list_articles = []
    category_article = Category.objects.get(slug=the_slug)
    articles = Article.objects.filter(category=category_article.id).order_by('-published_at')
    for article in articles:
        object_article = {'id': article.id,
                          'title': article.title,
                          'text': article.text,
                          'file': article.file,
                          }
        list_articles.append(object_article)

    stops_page, current_page, prev_page_url, next_page_url = pagination(request, list_articles, 10)

    context = {
        'list_articles': stops_page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'category': category_article,
    }
    return render(request, template, context=context)


def pagination(request, list_object, max_object=2):
    if request.GET.get('page'):
        page_number = int(request.GET.get('page'))
    else:
        page_number = 1
    p = Paginator(list_object, max_object)
    if page_number in range(1, p.num_pages):
        stops_page = p.page(page_number)
    else:
        stops_page = p.page(p.num_pages)
    current_page = stops_page.number
    prev_page_url = f'?page={stops_page.previous_page_number()}' \
        if stops_page.has_previous() else None
    next_page_url = f'?page={stops_page.next_page_number()}' \
        if stops_page.has_next() else None
    return stops_page, current_page, prev_page_url, next_page_url


def new(request, id_new):
    template = 'new.html'
    new = New.objects.get(id=id_new)
    context = {'new': new}
    return render(request, template, context)


def article(request, id_article):
    template = 'article.html'
    article = Article.objects.get(id=id_article)
    print(request, id_article, article)
    context = {'article': article}
    return render(request, template, context)