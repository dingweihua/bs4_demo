#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dwh@dobechina.com)
#
# Created: 2017/12/23 上午10:48

import re
import requests
from bs4 import BeautifulSoup


HOST = 'http://www.lbldy.com'
SEARCH_URL = 'http://www.lbldy.com/search'
TIMEOUT_SEC = 5
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}


def get_movie_search_list(name):
    """
    龙部落获取电影搜索列表
    :param name:
    :return:
    """
    search_url = '{}/{}'.format(SEARCH_URL, name)
    res_search = requests.get(search_url, headers=headers, timeout=TIMEOUT_SEC)
    soup_search = BeautifulSoup(res_search.content, 'html.parser')
    # 搜索列表
    content_tag = soup_search.find('div', id='center')
    if not content_tag:
        return []
    search_list = []
    # 电影详情信息
    for table_tag in content_tag.find_all(class_='postlist'):
        a_tag = table_tag.find('a', rel='bookmark')
        if not a_tag:
            continue
        detail_url = a_tag.attrs.get('href', '')
        if detail_url:
            search_list.append(detail_url)
    return search_list


def get_movie_resource(movie_url):
    """
    根据影片详情链接获取下载资源
    :param movie_url:
    :return:
    """
    res_detail = requests.get(movie_url, headers=headers, timeout=TIMEOUT_SEC)
    soup_detail = BeautifulSoup(res_detail.content, 'html.parser')
    # 下载资源列表
    content_tag = soup_detail.find('div', class_='entry')
    if not content_tag:
        return []
    resources = []
    res_starts = False
    for p_tag in content_tag.find_all('p'):
        # <p>下载地址：</p>之后的<p>为下载资源
        p_tag_text = p_tag.get_text()
        if p_tag_text.startswith(u'下载地址'):
            res_starts = True
        if not res_starts:
            continue

        a_tag = p_tag.find('a')
        if not a_tag:
            continue
        resource = a_tag.get('href')
        # 判断网盘/云盘
        if u'网盘' in p_tag_text or u'云盘' in p_tag_text:
            resource = re.sub(r'<a>.*</a>', resource, p_tag_text)
        # 只抓取下载资源
        if resource.startswith(('http://', 'https://')):
            continue
        resources.append(resource)
    return resources


def crawler_demo(name):
    """
    龙部落获取下载资源列表demo
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
    movie_name_list = [u'人在囧途']
    for name in movie_name_list:
        resource_list = crawler_demo(name)
        print(resource_list)
