#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dwh@dobechina.com)
#
# Created: 2017/12/9 上午10:59

import requests
from bs4 import BeautifulSoup


def dytt_demo(movie_name):
    """
    电影天堂获取下载资源列表demo
    :param movie_name:
    :return:
    """
    host = 'http://s.dydytt.net'
    dytt_search_url = 'http://s.dydytt.net/plus/search.php?kwtype=0&keyword={}'
    encoded_name = str(movie_name.encode('gbk')).replace(r'\x', '%')
    quote_url = dytt_search_url.format(encoded_name)
    res_search = requests.get(
        quote_url,
        headers={'user-agent': 'Mozilla/5.0'},
        timeout=5
    )
    soup_search = BeautifulSoup(res_search.content, 'html.parser')
    content_tag = soup_search.find(class_='co_content8')
    search_list = []
    for table_tag in content_tag.find_all('table'):
        a_tag = table_tag.find('a')
        detail_url = a_tag.attrs.get('href', '')
        if detail_url:
            search_list.append(host + detail_url)
    print(search_list)


if __name__ == '__main__':
    movie_name = u'战狼'
    dytt_demo(movie_name)
