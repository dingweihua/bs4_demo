#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dwh@dobechina.com)
#
# Created: 2017/12/24 上午11:18

import re
import requests
from bs4 import BeautifulSoup


HOST = 'http://www.ed2000.com'
SEARCH_URL = 'http://www.ed2000.com/FileList.asp'
TIMEOUT_SEC = 10
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
    search_url = SEARCH_URL
    data = {'SearchWord': name}
    res_search = requests.post(
        search_url, data, headers=headers, timeout=TIMEOUT_SEC)
    soup_search = BeautifulSoup(res_search.content, 'html.parser')
    # 搜索列表
    content_tag = soup_search.find('table', class_='CommonListArea')
    if not content_tag:
        return []
    search_list = []
    # 电影详情信息
    for table_tag in content_tag.find_all('tr', class_='CommonListCell'):
        is_movie = False
        for a_tag in table_tag.find_all('a'):
            a_tag_href = a_tag.attrs.get('href', '')
            if not is_movie:
                if a_tag_href == u'/Type/电影':
                    is_movie = True
                    continue
            if re.match(r'^/ShowFile/.*\.html', a_tag_href):
                search_list.append(HOST + a_tag_href)
                break
    return search_list


def get_movie_resource(movie_url):
    """
    根据影片详情链接获取下载资源
    :param movie_url:
    :return:
    """
    res_detail = requests.get(movie_url, headers=headers, timeout=TIMEOUT_SEC)
    soup_detail = BeautifulSoup(res_detail.content, 'html.parser')
    resources = []
    ignore_starts = ('/Profile.asp', 'http://', 'https://')
    # 下载资源列表
    for table_tag in soup_detail.find_all('table', class_='CommonListArea'):
        for tr_tag in table_tag.find_all('tr', class_='CommonListCell'):
            for a_tag in tr_tag.find_all('a'):
                if a_tag.parent.name != 'td':
                    continue
                resource = a_tag.get('href')
                if resource.startswith(ignore_starts):
                    continue
                resources.append(resource)
        # 下载链接可能是通过<script></script>渲染出来的
        script_tag = table_tag.find('script')
        if not script_tag:
            continue
        script_text = script_tag.get_text()
        if 'ShowMagnet' in script_text:
            magnets = re.findall(r'ShowMagnet\(\"(.*)\"\)', script_text)
            if magnets:
                resources.extend(magnets)
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
    movie_name_list = [u'辛德勒的名单']
    for name in movie_name_list:
        resource_list = crawler_demo(name)
        print(resource_list)
