from django.shortcuts import render
from .models import New
from django.core.paginator import Paginator


def index(request):
    template = 'index.html'
    list_news = []
    news = New.objects.all().order_by('-published_at')[:2]
    print(news)
    for new in news:
        object_new = {'id': new.id,
                      'title_new': new.title_new,
                      'text_new': new.text_new,
                      'image_new': new.image_new,
                      'file_new': new.file_new,
                      }
        list_news.append(object_new)
    return render(request, template, context={'list_news': list_news})


def news(request):
    template = 'news.html'
    list_news = []
    news = New.objects.all().order_by('-published_at')
    for new in news:
        object_new = {'id': new.id,
                      'title_new': new.title_new,
                      'text_new': new.text_new,
                      'image_new': new.image_new,
                      'file_new': new.file_new,
                      }
        list_news.append(object_new)

    if request.GET.get('page'):
        page_number = int(request.GET.get('page'))
    else:
        page_number = 1
    p = Paginator(list_news, 2)
    if page_number in range(1, p.num_pages):
        stops_page = p.page(page_number)
    else:
        stops_page = p.page(p.num_pages)
    current_page = stops_page.number
    prev_page_url = f'?page={stops_page.previous_page_number()}' \
        if stops_page.has_previous() else None
    next_page_url = f'?page={stops_page.next_page_number()}' \
        if stops_page.has_next() else None

    context = {
        'list_news': stops_page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }

    return render(request, template, context=context)
