# -*- coding:utf-8 -*
import re
import urllib.parse
from bs4 import BeautifulSoup

class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):

        #/item/xxx
        new_urls = set()
        links = soup.find_all('a',href=re.compile(r'/wiki/'), text = re.compile('^[A-Z]+$'))
        #links1 = links.find_all(text = re.compile('[A-Z]'))

        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin("https://en.wiktionary.org/wiki/", link.get_text())
            new_urls.add(new_full_url)
        return new_urls


    def _get_new_data(self, page_url, soup):
        res_data = {}

        #url
        res_data['url'] = page_url

        #<dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>
        #获取标题的标签
        #title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        title_node = soup.find('h1', class_="firstHeading")
        
        res_data['title'] = title_node.get_text()

        #<div class="lemma-summary" label-module="lemmaSummary">
        #summary_node = soup.find('div', class_="lemma-summary")
        div=soup.find(name='div', class_='mw-parser-output')  
        #mw-content-text > div
        ps=div.find_all(name='ol', limit=1, recursive=True) #only direct children  
        pText=""
        for p in ps:  
            pText+=p.get_text()  
            #SaveFile(pText, words[i])  
        res_data['summary'] = pText
        return res_data


    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser', from_encoding = 'utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data