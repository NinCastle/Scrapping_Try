import requests
from bs4 import BeautifulSoup

class TestWiki:
    def __init__(self):
        keyword = ''
    
    def make_result(self, keyword):
        url = 'https://ko.wikipedia.org/wiki/'+keyword
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        doc = soup.find('div', {'class':'mw-parser-output'})
        n_docs = []
        for n_doc in doc.text.split('\n'):
            n_docs.append(n_doc)
        #     print(s_doc)
        p_docs = []
        for p_doc in doc.find_all('p'):
            p_docs.append(p_doc.text)
        total_info = {'keyword':keyword,'url':url, 'category':'wikipedia','text-type1':n_docs, 'text-type2':p_docs}
        return total_info