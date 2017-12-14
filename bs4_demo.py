#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dwh@dobechina.com)
#
# Created: 2017/12/9 上午10:59

import requests
from bs4 import BeautifulSoup


TIMEOUT_SEC = 5
headers = {'user-agent': 'Mozilla/5.0', 'Connection': 'close'}


def get_movie_search_list(name):
    """
    电影天堂获取下载资源列表demo
    :param name:
    :return:
    """
    host = 'http://s.dydytt.net'
    dytt_search_url = 'http://s.dydytt.net/plus/search.php?kwtype=0&keyword={}'
    # TODO 优化bytes -> str
    encoded_name = str(name.encode('gbk'))[2:-1].replace(r'\x', '%')
    quote_url = dytt_search_url.format(encoded_name)
    s = requests.Session()
    s.keep_alive = False
    res_search = s.get(quote_url, headers=headers, timeout=TIMEOUT_SEC)
    soup_search = BeautifulSoup(res_search.content, 'html.parser')
    content_tag = soup_search.find(class_='co_content8')
    search_list = []
    for table_tag in content_tag.find_all('table'):
        a_tag = table_tag.find('a')
        detail_url = a_tag.attrs.get('href', '')
        if detail_url:
            search_list.append(host + detail_url)
    return search_list


def get_movie_resource(movie_url):
    """
    根据电影天堂的影片详情链接获取下载资源
    :param movie_url:
    :return:
    """
    s = requests.Session()
    s.keep_alive = False
    res_detail = s.get(movie_url, headers=headers, timeout=TIMEOUT_SEC)
    # utf-8解码
    dec_content = res_detail.content.decode('gbk').encode('utf-8')
    soup_detail = BeautifulSoup(dec_content, 'html.parser')
    # 电影详情标签
    content_tag = soup_detail.find(class_='co_content8')
    resources = []
    table_tag = content_tag.find('table')
    for a_tag in table_tag.find_all('a'):
        # 下载资源
        resource = a_tag.get_text()
        if resource:
            resources.append(resource)
    return resources


def dytt_demo(name):
    """
    电影天堂获取下载资源列表demo
    :param name:
    :return:
    """
    search_list = get_movie_search_list(name)
    multi_list = []
    for detail_url in search_list:
        resources = get_movie_resource(detail_url)
        if resources:
            multi_list.extend(resources)
    return multi_list


if __name__ == '__main__':
    movie_name_list = [u'泰囧']
    for name in movie_name_list:
        resource_list = dytt_demo(name)
        print(resource_list)
