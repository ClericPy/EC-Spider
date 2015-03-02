
# coding:utf-8
try:
    from gevent import monkey
    monkey.patch_all()
    from gevent.pool import Pool
except:
    from multiprocessing.dummy import Pool
import requests
from lxml.html import fromstring
headers = {'Cookie': 'wsid=1001'}


def getid(pid):
    while 1:
        try:
            pid = str(pid)
            url = 'http://item.yixun.com/item-{}.html'.format(pid)
            r = requests.get(url)
            xpath = fromstring(r.text).xpath
            title = xpath('/html/head/title/text()')[0]
            desc = xpath(
                '/html/head/meta[@name="description"]/@content|/html/head/meta[@name="Description"]/@content')[0]
            try:
                kw = xpath(
                    '/html/head/meta[@name="Keywords"]/@content|/html/head/meta[@name="keywords"]/@content')[0]
            except:
                kw = 'Null'
            cat = '-'.join(xpath('//div[@class="mod_crumb"]/a/text()'))
            result = '\t'.join((pid, title, url, kw, desc, cat)) + '\n'
            # print result
            # return result
            with open('jieguo.txt', 'a') as f:
                f.write(result.encode('utf-8'))
            global jishu
            jishu += 1
            print('=' * 20, jishu, '/', zongshu, '=' * 20)
            return
        except:
            pass
            # print pid, 'retry'
with open('all_id.txt') as f:
    all_id = set([i.strip() for i in f.readlines()])

zongshu = len(all_id)
jishu = 0
pp = Pool(200)
pp.map(getid, all_id)
try:
    pp.close()
    pp.join()
except:
    pass
