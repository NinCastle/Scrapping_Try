import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class TestTwitter:
    def __init__(self):
        self.keyword = ''
        
    def crawling_twitter(self, keyword, driver_path):
        driver = webdriver.Chrome(driver_path)
#         keyword = kw
        url = 'https://twitter.com/search?q='+keyword+'&src=typd&lang=ko'
        driver.get(url)

        # 스크롤 마지막을 가져오기
        last_height = driver.execute_script("return document.body.scrollHeight")
        page_number = 0
        while page_number < 20:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(2) # 페이지 잠시 기다리기

            # 새롭게 증가된 웹페이지를 길이를 계산한다.
            new_height = driver.execute_script("return document.body.scrollHeight")

            # 새롭게 창을 증가시키기 위해 2400 위치까지 이동
            driver.execute_script("window.scrollTo(0, 2400);")

            # 웹 창이 증가지 않을 경우 나간다.
            if new_height == last_height:
                break

            last_height = new_height
            page_number += 1
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.close()
        return soup, url
    
    def make_result(self, soup, url, keyword):
        hashtag_regex = "#([0-9a-zA-Z가-힣]*)"
        p = re.compile(hashtag_regex)

        total_info = []
        for tw_text in soup.findAll('div', {'class':'js-tweet-text-container'}):
            all_hash_tag = []
            text_sentens = []
            for text in tw_text.text.split('\n'):
                if len(text) != 0:
                    text_sentens.append(text)
                    r = p.findall(text)
                    for i in r:
                        all_hash_tag.append('#'+i)
            total_info.append({'keyword':keyword,'url':url, 'hash_tag':all_hash_tag, 'text':text_sentens, 'category':'twitter'})
        return total_info
