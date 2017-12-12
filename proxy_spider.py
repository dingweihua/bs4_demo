#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dingweihuaic@gmail.com)
#
# Created: 2017/12/12 下午12:06

import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0'}
url = 'http://www.xicidaili.com/nn/'
validate_url = 'https://www.baidu.com/'
n = 10
with open('host.txt', 'w') as fp:
    for num in range(n):
        s = requests.get(url + str(num+1), headers=headers)
        soup = BeautifulSoup(s.text, 'lxml')
        ips = soup.select('#ip_list tr')
        for i in ips:
            ipp = i.select('td')
            if len(ipp) < 3:
                continue
            host = '{}:{}'.format(ipp[1].text, ipp[2].text)
            proxies = {'http': host}
            # 校验proxy是否可用
            try:
                s = requests.get(validate_url, proxies=proxies)
                if s.status_code == 200:
                    fp.write(host)
                    fp.write('\n')
            except Exception as e:
                print(e)
