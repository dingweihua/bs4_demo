#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 布丁(dwh@dobechina.com)
#
# Created: 2017/12/12 下午12:06

import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0'}
url = 'http://www.xicidaili.com/nn/'
n = 50
with open('host.txt', 'w') as fp:
    for num in range(n):
        s = requests.get(url + str(num+1), headers=headers)
        soup = BeautifulSoup(s.text, 'lxml')
        ips = soup.select('#ip_list tr')
        for i in ips:
            ipp = i.select('td')
            if len(ipp) < 3:
                continue
            ip = ipp[1].text
            port = ipp[2].text
            fp.write('{}:{}\n'.format(ip, port))
