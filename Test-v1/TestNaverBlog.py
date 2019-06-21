import re
import time
import pandas as pd
import requests
import urllib.request as req
# from itertools import count
from collections import OrderedDict
from bs4 import BeautifulSoup

class TestNaverBlog:
    def __init__(self):
        self.query = ''
    
    def make_url(self, start_date, end_date, query):
        '''
        start, end는 날짜를 입력해야한다.
        '''
        url = 'https://search.naver.com/search.naver'
        header = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}

        post_dict = OrderedDict()    #중복 여부를 체크하기 위한 딕셔너리 변수
        cnt = 1                      #갯수를 세기위한 변수
        breaker = False
        for page in range(1, 5): #range가 100인 이유는? test
            param = {
                'where' : 'post',
                'query' : query,
                'date_from' : start_date, #'20190511'
                'date_to' : end_date, # '20190611'
                'date_option' : '8', # 잘모르는 옵션
                'start': (page - 1) * 10 + 1
            }

            response = requests.get(url, params=param, headers=header)
            soup = BeautifulSoup(response.text, 'html.parser')
            area = soup.find('div', {'class':'blog section _blogBase _prs_blg'}).find_all('a', {'class':'url'})
            time.sleep(1) # 페이지 잠시 기다리기

            for tag in area:
                url1=tag.get('href')
                if 'blog.naver.com' not in tag['href']:
                    continue


                if tag['href'] in post_dict:
                    print("마지막 페이지 마지막블로그입니다. 링크추출을 종료합니다.")
                    breaker = True
                    break

                post_dict[tag['href']] = tag.text
                cnt +=1

            if breaker == True:
                break
        return post_dict
    
    def make_result(self, post_dict, query):
        def no_space(text):
            out_text = []
            for j in text:
                text1 = re.sub('&nbsp; | &nbsp;|\n|\t|\r|\u200b|\xa0', '', j)
                text2 = re.sub('\n\n|\xa0', '', j)
                out_text.append(text2)
            return out_text
        content_list = []
        for link, disp in post_dict.items():
            time.sleep(1) # 페이지 잠시 기다리기
            url_first = link
            html_result = requests.get(url_first)
            soup_temp = BeautifulSoup(html_result.text, 'html.parser')
            area_temp = soup_temp.find(id='mainFrame')
            url_2 = area_temp.get('src')
            final_url = 'https://blog.naver.com' + url_2

            response = req.urlopen(final_url)
            soup = BeautifulSoup(response, 'html.parser')

            dates = soup.findAll("span", {"class":"se_publishDate pcol2"})

            if len(dates) == 0:
                dates = soup.findAll('p', {'class':'date fil5 pcol2 _postAddDate'})

            for date in dates:
                refined_date = date.get_text()

            contents = soup.findAll("div", {"id":"postViewArea"})
            refined_content = []
            for content in contents:
                for do_n in content.text.split('\n'):
                    if do_n != '':
                        for u200_del in do_n.split('\u200b'):
                            if u200_del != '':
                                refined_content.append(u200_del)
            if len(refined_content) == 0:
                contents = soup.findAll("div", {"class":"se-main-container"})
                for content in contents:
                    for do_n in content.text.split('\n'):
                        if do_n != '':
                            for u200_del in do_n.split('\u200b'):
                                if u200_del != '' and u200_del != ' ':
                                    refined_content.append(u200_del)
        #     content_list.append({'date' : refined_date, 'contents':no_space(refined_content)}) #'title':refined_title
            content_list.append({'keyword':query, 'category' : 'naver blog','contents':no_space(refined_content), 'url':final_url}) #'title':refined_title
        return content_list
        