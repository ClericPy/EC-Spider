# coding:utf-8
try:
    from gevent import monkey
    monkey.patch_all()
    from gevent.pool import Pool
except:
    from multiprocessing.dummy import Pool

import requests
import re
from lxml.html import fromstring

headers = {'Cookie': 'wsid=1001'}
jishu = 0


def getbypn(url1, pn):
    while 1:
        try:
            url = url1 + 'all/----1--{}---------.html'.format(pn)
            r = requests.get(url, headers=headers).text
            print('.')
            return '\n'.join(re.findall('commid="(\d+)"', r))
        except:
            pass


def getid(url1):
    while 1:
        try:
            url = url1 + 'all/----1--1---------.html'
            r = requests.get(url, headers=headers).text
            ss = re.findall('commid="(\d+)"', r)
            if not ss:
                global jishu
                jishu += 1
                print('=' * 20, jishu, '/', zongshu, '=' * 20)
                return
            pn = fromstring(r).xpath(
                '//div[@class="sort_page_num"]/span/text()')[0].replace('/', '')
            if pn == '1':
                result = '\n'.join(ss) + '\n'
            else:
                pns = range(2, int(pn) + 1)
                pp = Pool(30)
                dd = pp.map(lambda x: getbypn(url1, x), pns)
                ss += dd
                result = '\n'.join(ss) + '\n'
            with open('all_id.txt', 'a') as f:
                f.write(result)
            global jishu
            jishu += 1
            print('=' * 20, jishu, '/', zongshu, '=' * 20)
            return
        except:
            pass
with open('all_cat.txt') as f:
    all_cat = [i.strip() for i in f.readlines()]


zongshu = len(all_cat)
pp = Pool(55)
pp.map(getid, all_cat)
