from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from datetime import datetime
import random, json


class Newsview(View):
    dnews = []

    def get(self, request, news_id, **kwargs):
        news_dic = {}
        for itm in Newsview.dnews:
            if news_id == itm['link']:
                news_dic = itm
        context = {'news_dic': news_dic}
        return render(request, 'news/index.html', context=context)


def index(request):
    return HttpResponseRedirect('/news/')


def mainpage(request):
    query = request.GET.get('q', '')
    # The empty string handles an empty "request"
    results = {}
    if query:
        for itm in Newsview.dnews:
            if query in itm['title']:
                results = itm

    sorted_news = sorted(Newsview.dnews,
                         key=lambda x: datetime.strptime(x['created'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    for item in sorted_news:
        gr_date = datetime.strptime(item['created'], "%Y-%m-%d %H:%M:%S").date()
        item['datum'] = str(gr_date)
    context = {'sorted_news': sorted_news, 'results': results, 'query': query}
    return render(request, 'news/main.html', context=context)


def createnews(request):
    if request.method != 'POST':
        return render(request, 'news/create.html')
    else:
        news_dic = {}
        created = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        news_dic['created'] = created
        ntitle = request.POST.get('title')
        ntext = request.POST.get('text')
        news_dic['text'] = ntext
        news_dic['title'] = ntitle
        link = random.randint(5, 99999)
        news_dic['link'] = link
        datum = datetime.strftime(datetime.now(), '%Y-%m-%d')
        news_dic['datum'] = datum
        Newsview.dnews.append(news_dic)
        return redirect('/news/')


# Create your views here.
myjson1 = [{"created": "2020-02-02 16:40:00", "text": "A new star appeared in the sky.",
            "title": "The birth of a star", "link": 9234732}]
myjson2 = [{"created": "2020-02-02 10:40:00", "text": "A new planet appeared in the sky.",
            "title": "The rise of Jupyter", "link": 2389742}]

with open(settings.NEWS_JSON_PATH, "r") as json_file:
    news_list = json.load(json_file)
empty = False
link_list = []
for long in news_list:
    link_list.append(long['link'])
if not {2389742, 9234732}.issubset(link_list):
    news_list += myjson1 + myjson2
with open(settings.NEWS_JSON_PATH, "w") as json_file:
    json.dump(news_list, json_file)
Newsview.dnews = news_list
