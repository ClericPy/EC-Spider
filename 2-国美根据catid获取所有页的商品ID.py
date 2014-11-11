
# coding:utf-8
try:
    from gevent import monkey
    monkey.patch_all()
    from gevent.pool import Pool
except:
    from multiprocessing.dummy import Pool
import sys
import requests
# 在windows的终端CMD下会有进度显示，总过程耗费时间看网速


def getgome(cat):
    for i in range(3):
        try:
            url = ''.join(('http://www.gome.com.cn/p/json?module=async_search&paramJson={%22pageNumber%22%3A', '1', '%2C%22envReq%22%3A{%22catId%22%3A%22', str(
                cat), '%22%2C%22regionId%22%3A%2231010100%22%2C%22et%22%3A%22%22%2C%22XSearch%22%3Afalse%2C%22pageNumber%22%3A1%2C%22pageSize%22%3A48}}'))
            r = requests.get(url)
            totalpage = int(r.json()['num']['totalPage'])
            urls = [''.join(('http://www.gome.com.cn/p/json?module=async_search&paramJson={%22pageNumber%22%3A', str(i), '%2C%22envReq%22%3A{%22catId%22%3A%22', str(
                cat), '%22%2C%22regionId%22%3A%2231010100%22%2C%22et%22%3A%22%22%2C%22XSearch%22%3Afalse%2C%22pageNumber%22%3A1%2C%22pageSize%22%3A48}}')) for i in xrange(1, totalpage + 1)]

            def ff(url):
                while 1:
                    try:
                        r = requests.get(url, timeout=3)
                        return '\n'.join([i['pId'] for i in r.json()['products']])
                    except:
                        continue
            pp = Pool(30)
            ss = pp.map(ff, urls)
            global jishu
            jishu += 1
            sys.stderr.write(str(jishu) + ' / ' + zongshu + '\r')
            return '\n'.join(ss) + '\n'
        except:
            continue

with open('allcategory.txt') as f:
    allcategory = [i.strip() for i in f.readlines()]
zongshu = str(len(allcategory))
jishu = 0
with open('allids.txt', 'w') as f:
    # 这里又开了Pool，但一开始我是用for单线程做的，因为每个类目已经开了多线程，结果用了很久
    p1 = Pool(50)
    ss = p1.map(getgome, allcategory)
    f.writelines(ss)
