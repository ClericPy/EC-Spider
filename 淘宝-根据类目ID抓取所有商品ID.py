# coding:utf-8
try:
    from gevent import monkey
    monkey.patch_all()
    from gevent.pool import Pool
except:
    from multiprocessing.dummy import Pool
import re
import requests
'''Python2和3通用，注意下载好支持库，因为淘宝最大显示页数100页，为了使结果更有价值，按销量排序抓取，而且选中了合并同款商品'''

def get_taobao_ids(catid, pagenum):
    if pagenum == 1:
        pagenum = 1
    else:
        pagenum = (pagenum - 1) * 96
    # print pagenum
    url = 'http://list.taobao.com/itemlist/default.htm?_input_charset=utf-8&json=on&cat={0}&sort=biz30day&msp=1&as=1&viewIndex=1&atype=b&style=list&same_info=1&tid=0&isnew=2&pSize=96&data-key=s&data-value={1}&data-action&module=page&s=0'.format(
        catid, pagenum)
    r = requests.get(url)
    ss = r.text
    ids = '\n'.join(re.findall('itemId":"(.*?)"', ss))
    return ids


def get_ids_by_cat(catid):
    url = 'http://list.taobao.com/itemlist/default.htm?_input_charset=utf-8&json=on&cat={0}&sort=biz30day&msp=1&as=1&viewIndex=1&atype=b&style=list&same_info=1&tid=0&isnew=2&pSize=96&data-key=s&data-value=1&data-action&module=page&s=0'.format(
        catid)
    r = requests.get(url)
    ss = r.text
    totalPage = int(re.findall('totalPage":"(\d+)"', ss)[0])
    pagenums = range(1, totalPage + 1)
    pp = Pool(30)
    ss = pp.map(lambda x: get_taobao_ids(catid, x), pagenums)
    return '\n'.join(ss)
if __name__ == '__main__':
    print(get_ids_by_cat(50052124).count('\n'))
