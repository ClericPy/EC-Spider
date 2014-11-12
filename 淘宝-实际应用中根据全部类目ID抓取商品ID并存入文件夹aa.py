# coding:utf-8
try:
    from gevent import monkey
    monkey.patch_all()
    from gevent.pool import Pool
except:
    from multiprocessing.dummy import Pool
import re
import requests
import glob
''' 
淘宝并行开太多会需要验证码，只要浏览器打完验证码，把cookies里的那句sec的放入header就可以跳过去了,目前测试Pool大小设定在5比较持久……但还是会要验证码，10以上都会要打验证码
'''

proxies = {}

headers = {'Host': 'list.taobao.com', 'User-Agent':
           'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0', 'Cookie': 'sec=5462c34d67e290446e405972f4d684630f8b4046'}


def get_taobao_ids(catid, pagenum):
    if pagenum == 1:
        pagenum = 1
    else:
        pagenum = (pagenum - 1) * 96
    while 1:
        try:
            # print pagenum
            url = 'http://list.taobao.com/itemlist/default.htm?_input_charset=utf-8&json=on&cat={0}&sort=biz30day&msp=1&as=1&viewIndex=1&atype=b&style=list&same_info=1&tid=0&isnew=2&pSize=96&data-key=s&data-value={1}&data-action&module=page&s=0'.format(
                catid, pagenum)
            r = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            ss = r.text
            ids = '\n'.join(re.findall('itemId":"(.*?)"', ss))
            print pagenum / 96, 'get'
            return ids
        except Exception as e:
            print('retry fen')
            continue


def get_ids_by_cat(catid):
    while 1:
        try:
            url = 'http://list.taobao.com/itemlist/default.htm?_input_charset=utf-8&json=on&cat={0}&sort=biz30day&msp=1&as=1&viewIndex=1&atype=b&style=list&same_info=1&tid=0&isnew=2&pSize=96&data-key=s&data-value=1&data-action&module=page&s=0'.format(
                catid)
            r = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            ss = r.text
            # print ss
            if '"itemList":null' in ss:
                return
            totalPage = int(re.findall('totalPage":"(\d+)"', ss)[0])
            print 'start', catid, '=' * 50, '\ntotalPage', totalPage
            pagenums = range(1, totalPage + 1)
            pp = Pool(5)
            ss = pp.map(lambda x: get_taobao_ids(catid, x), pagenums)
            ss = '\n'.join(ss) + '\n'
            with open('./aa/' + str(catid) + '.txt', 'w') as f:
                f.write(ss)
            jishu = len(glob.glob('./aa/*.*'))
            print jishu, '/', zongshu, 'completed'
            return
        except Exception as e:
            print('retry zong', catid, e)
            continue
with open('all_catid.txt') as f:
    cats = [i.strip() for i in f.readlines()]
zongshu = len(cats)

cats = set(cats) - set([re.search('aa.*?(\d+)\.txt', i).group(1)
                        for i in glob.glob('./aa/*')])

for i in cats:
    # print i
    get_ids_by_cat(i)
