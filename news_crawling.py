""" ����Ź� Ư�� Ű���带 �����ϴ�, Ư�� ��¥ ���� ��� ���� ũ�ѷ�(��Ȯ���� �˻�)
    python [��� �̸�] [Ű����] [������ ������ ����] [��� ���ϸ�]
    �� �������� ��� 10��
"""
 
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from urllib.request import Request, urlopen
 
TARGET_URL_BEFORE_PAGE_NUM = "http://search.khan.co.kr/search.html?stb=khan"
TARGET_URL_BEFORE_KEWORD = '&q='
TARGET_URL_PAGE = '&pg='
TARGET_URL_SORT = '&sort=2'
 
 
# ��� �˻� ���������� ��� ���� ��ũ�� ��� ���� �ּ� �޾ƿ���
def get_link_from_news_title(page_num, URL, output_file):
    for i in range(page_num):
        current_page_num = i + 1
        URL_with_page_num = URL + TARGET_URL_PAGE + str(current_page_num) + TARGET_URL_SORT
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')
        for title in soup.find_all('dl', 'phArtc'):
            title_link = title.select('a')
            article_URL = title_link[0]['href']
            get_text(article_URL, output_file)
 
 
# ��� ���� ���� �ܾ���� (�� �Լ� ���ο��� ��� ���� �ּ� �޾� ���Ǵ� �Լ�)
def get_text(URL, output_file):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    source_code_from_url = urlopen(req).read()
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    
    # ����
    content_of_article = soup.select('div.subject')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
        output_file.write(string_item)
    
    # ����
    content_of_article = soup.select('div.art_body')
    for item in content_of_article:
        string_item = str(item.find_all("p", {"class": "content_text"}))
        output_file.write(string_item)
 
 
# �����Լ�
def main(argv):
    if len(argv) != 4:
        print("python [����̸�] [Ű����] [������ ������ ����] [��� ���ϸ�]")
        return
    keyword = argv[1]
    page_num = int(argv[2])
    output_file_name = argv[3]
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD \
                 + quote(keyword)
    output_file = open(output_file_name, 'w', encoding='UTF-8')
    get_link_from_news_title(page_num, target_URL, output_file)
    output_file.close()
 
 
if __name__ == '__main__':
    main(sys.argv)