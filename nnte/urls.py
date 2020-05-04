"""nnte URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.views import index, news, category, new, article, vacancy, vacancies, back_url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import include, url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('news/', news, name='news'),
    path('category/<slug:the_slug>/', category, name='category'),
    path('new/<int:id_new>/', new, name='new'),
    path('article/<int:id_article>/', article, name='article'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
    path('vacancy/<slug:the_slug>/', vacancy, name='vacancy'),
    path('vacancies/', vacancies, name='vacancies'),
    url(r'^back_url/', back_url),

]

# В конце файла:
# if settings.DEBUG:
if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Эта строка опциональна и будет добавлять url'ы только при DEBUG = True

    urlpatterns += staticfiles_urlpatterns()
