#-*- coding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import re
import random
import datetime

random.seed(datetime.datetime.now())

def getLink(url):
    html = urllib.request.urlopen("http://en.wikipedia.org"+url)
    bsObj = BeautifulSoup(html, 'html.parser')
    return bsObj.find('div', id="body   Content").find_all('a', href=re.compile("^(/wiki/)((?!;)\S)*$"))

url = "/wiki/Kevin_Bacon"
file = open("wiki.txt", "w")
links = getLink(url)
while len(links)>0:
    newArticle = links[random.randint(0,len(links)-1)].attrs['href']
    file.write(newArticle + " from " + url + "\n")
    print (newArticle + " from " + url)
    url = newArticle
    links = getLink(newArticle)
file.close()