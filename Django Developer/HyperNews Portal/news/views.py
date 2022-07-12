from datetime import datetime
import json
import random

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect


def coming_soon(request):
    return redirect('/news/')


def list(request):
    with open(settings.NEWS_JSON_PATH, 'r') as f:
        news = json.load(f)
    news_by_date = {}
    query_filter = ''
    if 'q' in request.GET:
        query_filter = request.GET.get('q')
    for article in news:
        if query_filter in article['title']:
            date = datetime.strptime(article['created'],
                                     '%Y-%m-%d %H:%M:%S').date()
            news_by_date.setdefault(date.strftime('%Y-%m-%d'), [])
            news_by_date[date.strftime('%Y-%m-%d')].append(article)
    news = sorted(news_by_date.items(), key=lambda x: x[0], reverse=True)
    return render(request, 'news/list.html', context={'news_by_date': news})


def detail(request, article_id):
    with open(settings.NEWS_JSON_PATH, 'r') as f:
        news = json.load(f)
    article = next((n for n in news if n['link'] == int(article_id)), None)
    if article is None:
        raise Http404
    return render(request, 'news/detail.html', context={'news': article})


def create(request):
    if request.method == 'GET':
        return render(request, 'news/create.html')
    data = request.POST
    article = {
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'text': data.get('text'),
        'title': data.get('title'),
        'link': random.randint(10, 1000)
    }
    with open(settings.NEWS_JSON_PATH, 'r') as f:
        news = json.load(f)
    news.append(article)
    with open(settings.NEWS_JSON_PATH, 'w') as f:
        json.dump(news, f)
    return redirect('/news/')