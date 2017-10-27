from django.shortcuts import render
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
    fw.write(html)
    fw.close()

    fr = open('source_file', 'r')
    lines = fr.readlines()
    trump_news = []

    for line in lines:
        matches = re.findall(r'{\"uri.*?}', line, re.M|re.I)
        if matches:
            for match in matches:
                if 'trump' in match.lower():
                    trump_news.append(match)
        else:
           print("No match!!")

    headlines = []
    for news in trump_news:      
        news_json = json.loads(news)
        headlines.append(news_json['headline'])
        
    print(headlines)
    return render(request, 'crawl/main.html', {'headlines': headlines})