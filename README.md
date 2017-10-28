# trumpcrawler
Trumpcrawler is a website that crawls latest (up to 25) articles related to Trump from CNN.com and latest tweets from Trump's official Twitter account (https://twitter.com/realDonaldTrump).

Table Of Contents
1-Installation
2-Usage
3- Notes

# 1-Installation

This project is a Django project. You need to install the specified version of Django in requirements.txt.
Some of the libraries used in this project differs from Python2 to Python3. Therefore there are two branched namely; develop_py2 and develop_py3. Clone the appropriate one for you.

# 2- Usage

First run the command .\manage.py runserver in trumpcrawler directory.  This will start Django server, if you installed Django correctly. Then go to http://localhost:8000/crawl/main url on your web browser. This will birng you to main page. You can choose to see the latest article or latest tweets on this page.
If you choose articles, this will navigate you to another page. At the left you will see the headlines of the articles. If you click on of the headlines you will see the content of the article on the left. 
If you choose to see the tweets, you will end up with a different page showing Trump's latest tweets. You can click the links on tweets.

# 3- Notes

Python code in this project is PEP-8 formatted. 
Pylint score is 8.16
The project has to branches for Python2 and Python3.
