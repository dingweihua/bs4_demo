#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dwh@dobechina.com)
#
# Created: 2017/12/18 下午4:11

import requests
from bs4 import BeautifulSoup


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
    BT天堂获取电影搜索列表
    :param name:
    :return:
    """
    host = 'http://www.bttiantangs.com'
    search_url = 'http://www.bttiantangs.com/e/search/new.php'
    param = {'keyboard': name}
    res_search = requests.post(
        search_url, param, headers=headers, timeout=TIMEOUT_SEC)
    soup_search = BeautifulSoup(res_search.content, 'html.parser')
    # 搜索列表
    content_tag = soup_search.find(id='post_list')
    if not content_tag:
        return []
    search_list = []
    # 链接信息
    for table_tag in content_tag.find_all(class_='info clear'):
        a_tag = table_tag.find('a')
        detail_url = a_tag.attrs.get('href', '')
        if detail_url:
            search_list.append(host + detail_url)
    return search_list


def get_movie_resource(movie_url):
    """
    根据BT天堂的影片详情链接获取下载资源
    :param movie_url:
    :return:
    """
    res_detail = requests.get(movie_url, headers=headers, timeout=TIMEOUT_SEC)
    soup_detail = BeautifulSoup(res_detail.content, 'html.parser')
    # 下载资源列表
    content_tag = soup_detail.find(class_='dlist')
    if not content_tag:
        return []
    resources = []
    for a_tag in content_tag.find_all('a'):
        # 下载资源
        class_list = a_tag.attrs.get('class') or []
        # 过滤BT类型text
        if 'd-bt' in class_list:
            continue
        resource = a_tag.attrs.get('href')
        if resource:
            resources.append(resource)
    return resources


def bt_demo(name):
    """
    BT天堂获取下载资源列表demo
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
    movie_name_list = [u'辛德勒的名单']
    for name in movie_name_list:
        resource_list = bt_demo(name)
        print(resource_list)
