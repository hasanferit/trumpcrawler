from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from urllib.request import urlopen
import re
import json

# Create your views here.


def get_home(request):
    return render(request, 'crawl/main.html', {})


def get_tweets(request):
    html = urlopen('https://twitter.com/realDonaldTrump')
    fw = open('source_file', 'w')
    fw.write(str(html.read()))
    fw.close()

    fr = open('source_file', 'r')
    lines = fr.readlines()
    fr.close()
    trump_tweets = []
    for line in lines:
        matches = re.findall(
            r'<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">.*?</p>', line, re.M | re.I)
        for match in matches:
            match = re.sub(
                '<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">', '', match)
            match = re.sub('</p>', '', match)
            mention_hrefs = re.findall(r'<a href=".*?" class', match)
            for mention_href in mention_hrefs:

                mention = re.findall(r'".*?"', mention_href)[0]
                if 'http' in mention:
                    continue
                match = re.sub(
                    mention, '\"https://twitter.com' + mention[1:], match)

            trump_tweets.append(match)

    return render(request, 'crawl/tweets.html', {'tweets': trump_tweets})


def get_articles(request):
    html = urlopen('http://edition.cnn.com/')
    fw = open('source_file', 'w')
    fw.write(str(html.read()))
    fw.close()

    fr = open('source_file', 'r')
    lines = fr.readlines()
    fr.close()
    trump_news = []

    for line in lines:
        matches = re.findall(r'{\"uri.*?}', line, re.M | re.I)
        for match in matches:
            if 'trump' in match.lower():
                trump_news.append(match)

    headlines = []
    descriptions = []
    uris = []
    thumbnails = []
    head_indices = []
    for news in trump_news:
        article_json = json.loads(news.replace(
            "\\'", "'").replace('\\\\"', "'"),  strict=False)
        headlines.append(article_json['headline'])
        head_indices.append(trump_news.index(news))
        descriptions.append(article_json['description'])
        thumbnails.append(str(article_json['thumbnail']))
        uris.append(str(article_json['uri']))

    titles = []
    authors = []
    datetimes = []
    contents = []
    for uri in uris:
        print(uri)
        html = urlopen('http://edition.cnn.com' + uri)
        fw = open('source_file_2', 'w')
        fw.write(str(html.read()))
        fw.close()
        fr = open('source_file_2', 'r')
        lines = fr.readlines()
        content = ''
        title = ''
        author = ''
        datetime = ''
        for line in lines:
            matches = re.findall(
                r'class=\"zn-body__paragraph.*?\">.*?<\/div>', line, re.M | re.I)
            for match in matches:
                content += match
            matches = re.findall(r'<h1 class="pg-headline">.*?<\/h1>', line)
            for match in matches:
                title += match
            matches = re.findall(
                r'<span class="metadata__byline__author">.*?<\/span>', line)
            for match in matches:
                author += match
            matches = re.findall(r'<p class="update-time">.*?<\/span', line)
            for match in matches:
                datetime += match
        content = re.sub(r'class=\"zn-body__paragraph.*?\">',
                         '', content)  # content.replace()
        content = re.sub('</div>', '<br>', content)

        title = re.sub(r'<h1 class="pg-headline">',
                       '', title)  # content.replace()
        title = re.sub('<\/h1>', '', title)

        author = re.sub(r'<span class="metadata__byline__author">',
                        '', author)  # content.replace()
        author = re.sub('<\/span>', '', author)

        datetime = re.sub(r'<p class="update-time">', '',
                          datetime)  # content.replace()
        datetime = re.sub('<\/span', '', datetime)

        contents.append(content)
        titles.append(title)
        authors.append(author)
        datetimes.append(datetime)

    headlines_zipped = zip(head_indices, headlines)
    return render(request, 'crawl/cnn.html', {'headlines_zipped': headlines_zipped, 'descriptions': descriptions,
                                              'uris': uris, 'thumbnails': thumbnails, 'contents': contents, 'titles': titles, 'authors': authors, 'datetimes': datetimes})
