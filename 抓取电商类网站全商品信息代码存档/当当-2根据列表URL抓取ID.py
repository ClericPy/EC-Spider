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
# //div[@class="inner"]/p[@class="name"]/a/@href
jishu = 0


def getbypn(url1, pn):
    while 1:
        try:
            url = re.sub('pg\d+', 'pg' + str(pn), url1)
            r = requests.get(url, timeout=5).text
            ss = fromstring(r).xpath(
                '//div[@class="inner"]/p[@class="name"]/a/@href')
            ss = re.findall('dangdang\.com/(\d+)\.html', ''.join(ss))
            print(pn)
            return '\n'.join(ss)
        except:
            pass


def getid(url1):
    global jishu
    while 1:
        try:
            url = url1
            r = requests.get(url, timeout=5).text
            ss = fromstring(r).xpath(
                '//div[@class="inner"]/p[@class="name"]/a/@href')
            ss = re.findall('dangdang\.com/(\d+)\.html', ''.join(ss))
            if not ss:
                with open('finished.txt', 'a') as f:
                    f.write(url1 + '\n')
                jishu += 1
                print('=' * 20, jishu, '/', zongshu, '=' * 20)
                return
            pn = fromstring(r).xpath(
                '//div[@name="Fy"]/span[3]/text()|//div[@class="page"]/span[3]/text()')[0].replace('/', '')
            if pn == '1':
                result = '\n'.join(ss) + '\n'
            else:
                pns = range(2, int(pn) + 1)
                pp = Pool(50)
                dd = pp.map(lambda x: getbypn(url1, x), pns)
                try:
                    pp.close()
                    pp.join()
                except:
                    pass
                ss += dd
                result = '\n'.join(ss) + '\n'
            with open('all_id.txt', 'a') as f:
                f.write(result)
            with open('finished.txt', 'a') as f:
                f.write(url1 + '\n')
            jishu += 1
            print('=' * 20, jishu, '/', zongshu, '=' * 20)
            return
        except Exception as e:
            print(url1, e)
            pass
with open('all_cat.txt') as f:
    all_cat = set([i.strip() for i in f.readlines()])
try:
    with open('finished.txt') as f:
        finish = set([i.strip() for i in f.readlines()])
except:
    finish = set()
all_cat = all_cat - finish
zongshu = len(all_cat)
pp = Pool(200)
pp.map(getid, all_cat)
try:
    pp.close()
    pp.join()
except:
    pass
