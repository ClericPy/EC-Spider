#! python2
# coding:utf-8
import requests
from lxml.html import fromstring

r = requests.get('http://searchex.yixun.com/')
r.encoding = 'gbk'
ss = r.text
aa = fromstring(ss).xpath('//dd/a/@href')
aa = '\n'.join(aa)
with open('all_cat.txt', 'w') as f:
    f.write(aa)
