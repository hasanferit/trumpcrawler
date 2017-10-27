from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse
# import urllib2
from urllib.request import urlopen
import re
import json

# Create your views here.

def get_home(request):
    
    # opener = urllib2.build_opener()
    # opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    # page_opener = opener.open('http://edition.cnn.com/')
    html = urlopen('http://edition.cnn.com/')
    fw = open('source_file', 'w')
    # fw.write(str(page_opener.read()))
    fw.write(str(html.read()))
    fw.close()

    fr = open('source_file', 'r')
    lines = fr.readlines()
    fr.close()
    trump_news = []

    for line in lines:
        matches = re.findall(r'{\"uri.*?}', line, re.M|re.I)
        for match in matches:
            if 'trump' in match.lower():
                trump_news.append(match)

    headlines = []
    descriptions = []
    uris = []
    head_indices = []
    for news in trump_news: 
        news_json = json.loads(news.replace("\\'", "'").replace('\\\\"',"'"),  strict=False)
        headlines.append(news_json['headline'])
        head_indices.append(trump_news.index(news))
        descriptions.append(news_json['description'])
        uris.append(news_json['uri'])

    headlines_zipped = zip(head_indices, headlines)
    return render(request, 'crawl/main.html', {'headlines_zipped': headlines_zipped, 'descriptions':descriptions, 
        'uris': uris})

@csrf_exempt
def get_content(request):

    index = request.POST.get('index')
    index = int(index)
    uris = request.POST.get('uris')
    uris = uris.split('&#39;, u&#39;')
    uris[0] = uris[0].replace('[u&#39;','')
    uris[-1] = uris[-1].replace('&#39;]','')
    uri = uris[index]
    # opener = urllib2.build_opener()
    # opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    # page_opener = opener.open('http://edition.cnn.com'+uri)
    html = urlopen('http://edition.cnn.com/'+uri)
    fw = open('source_file_2', 'w')
    # fw.write(str(page_opener.read()))
    fw.write(str(html.read()))
    fw.close()
    fr = open('source_file_2', 'r')
    lines = fr.readlines()
    content = ''
    for line in lines:
        matches = re.findall(r'<div class=\"zn-body__paragraph\">.*?</div>', line, re.M|re.I)
        for match in matches:
            content += match
    content = content.replace('<div class=\"zn-body__paragraph\">', '')
    content = content.replace('</div>', '')
    return JsonResponse({'content': content})