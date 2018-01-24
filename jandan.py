# coding=utf-8
import requests
from requests import ConnectionError
from bs4 import BeautifulSoup
import re
import os
from sys import argv
import time
from random import randint


def generate_header():
    # 构建requests请求头
    with open('./header', 'r') as f:
        data = f.readlines()
    data = [i.strip('\n') for i in data]
    dic = {}
    for line in data:
        index = line.find(':')
        key = line[:index]
        value = line[index + 2:]
        dic[key] = value
    return dic


def to_tags(url):
    # 从目标url提取各comment的soup tag
    try:
        print('reading %s' % url)
        r = requests.get(url, headers=generate_header(), timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html5lib')
            comment_tags = soup.find_all('li')
            comment_tags = [i for i in comment_tags if i.get(
                'id') and i.get('id').startswith('comment')]
        else:
            pass
    except ConnectionError:
        print('reading %s error' % url)
        pass
    time.sleep(randint(1,4))
    return comment_tags


class Comment(object):
    """docstring for Comment"""

    def __init__(self, tag):
        super(Comment, self).__init__()
        self.tag = tag
        self.hash = self.tag.find('span', class_='img-hash').getText()
        self.url = self.get_url()
        self.id = self.tag.get('id')
        self.vote_lst = re.findall(r'\[\d.*?\]', tag.get_text())
        def vote_format(x): return int(x[1:-1])
        self.like = vote_format(self.vote_lst[0])
        self.unlike = vote_format(self.vote_lst[1])
        if self.like + self.unlike:
            self.rate = self.like / (self.like + self.unlike) * 100
        else:
            self.rate = 0.01
        self.rate = round(self.rate, 2)

    def get_url(self):
        # 利用js脚本将hash转为图片url
        command = 'node ./turn_url/turn_url.js %s' % self.hash
        result = os.popen(command).read().strip('\n')
        result = 'http:' + result
        return result

    def to_html_tag(self):
        url = self.url
        line1 = '<a target="_blank" href="%s">' % url
        line2 = '<img src="%s", height="320">' % url
        line3 = '%s ' % self.rate
        line4 = '</a>'
        result = ''.join([line1, line2, line3, line4])
        return result

    def __repr__(self):
        return self.id


def sort_pics(comment_obj_lst):
    # 按rate高低排序
    lst = comment_obj_lst[:]
    lst = sorted(lst, key=lambda x: float(x.rate), reverse=True)
    return lst


def divide_lst(pics, n=40):
    pics = sort_pics(pics)
    total_pic = len(pics)
    # pages = total_pic // n
    result_lst = [pics[m: m + n] for m in range(total_pic) if m % n == 0]
    return result_lst


def generate_a_page_html(index, pages_count, pics_in_the_page):
    filename = './page' + str(index + 1) + '.html'
    pics_strings = [i.to_html_tag() for i in pics_in_the_page]
    pic_html_join = ''.join(pics_strings)
    # page_html_format = '<a href="">previous</a>'
    page_part_htmls = ['<a href="./page%s.html">' %
                       (i) + str(i) + ' </a>' for i in range(1, pages_count + 1)]
    page_bar = ''.join(page_part_htmls)
    with open('./format.html', 'r') as f:
        format_html = f.read()
    result = re.sub(r'\<insert\>', pic_html_join, format_html)
    result = re.sub(r'\<page\>', page_bar, result)
    with open(filename, 'w') as f:
        f.write(result)


if __name__ == "__main__":
    start = int(argv[1])
    end = int(argv[2])
    url_head = 'http://jandan.net/ooxx/page-'
    url_tail = '#comments'
    url_lst = [url_head + str(i) + url_tail for i in range(start, end + 1)]
    tag_lst = []
    for url in url_lst:
        tags = to_tags(url)
        tag_lst += tags
    comments = [Comment(i) for i in tag_lst]
    comments = sort_pics(comments)
    comments_divided_lst = divide_lst(comments)
    pages_count = len(comments_divided_lst)
    for index, content in enumerate(comments_divided_lst):
        generate_a_page_html(index, pages_count, content)
