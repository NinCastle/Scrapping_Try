import os
import re
import ssl
import json
import time
import urllib
import requests
# import urllib.requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class cr_instagram:
    def __init__(self):
        self.driver_path = ''
        self.keyword = ''
#         url_list = []
        
    def make_url_list(self, keyword, driver_path):
#         print(self.driver_path)
        driver = webdriver.Chrome(driver_path)
        driver.get('https://www.instagram.com/explore/tags/'+keyword+'/?hl=ko')
        test_list=[]
        down = 0
        b=driver.find_element_by_tag_name('body')## body 부분의 코드를 가져오고
        while down < 3:
            b.send_keys(Keys.PAGE_DOWN)##셀레니움을 이용해 페이지 down을 시키며 
            href = driver.find_elements_by_css_selector('div > a')
            time.sleep(2)
            for i in range(len(href)):
                try:
                    test_list.append(href[i].get_attribute('href'))
                except:
                    pass
            down = down + 1 
        test_list = list(set(test_list))
        orgin_list = []
        for true_link in test_list:
            if true_link.split('/')[3] == 'p':
                orgin_list.append(true_link)
        driver.close()
        return orgin_list
    
    def make_result(self, url_list):
        total_info = []
        for url in url_list:
            time.sleep(2)
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            script = soup.find('script', text=lambda t: \
                               t.startswith('window._sharedData'))
            page_json = script.text.split(' = ', 1)[1].rstrip(';')
            data = json.loads(page_json)
            img_url = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_resources'][2]['src']
            text = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text'].split('\n')
            hashtag_regex = "#([0-9a-zA-Z가-힣]*)"
            p = re.compile(hashtag_regex)
            all_hash_tag = []
            for hash_data in text:
                r = p.findall(hash_data)
                for i in r:
                    all_hash_tag.append('#'+i)
            total_info.append({'keyword':self.keyword, 'img_url':img_url, 'text':text, 'hash_tag': all_hash_tag, 'instargram_url':url, 'category':'instagram'})
        return total_info