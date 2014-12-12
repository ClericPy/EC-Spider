# coding:utf-8
# Compatible with Python2.x & 3.x
# Email：lidongone@qq.com
try:
    from gevent import monkey  # 有gevent就用它比较快，没有就用内置多线程，同时也为py3兼容
    monkey.patch_all()
    from gevent.pool import Pool
except:
    from multiprocessing.dummy import Pool  # py2和3通用的多线程
import requests
import json
import uniout
import re
# import uniout。这个库可以让python2像3一样print中文列表


'''
#声明：
该源码仅为学习交流使用，不用于商业用途，如有侵权问题

请及时联系lidongone@qq.com撤销全部代码

##介绍：

文件名：get_jd.py
用途：非官方-京东商品爬虫API（包括价格、评论等），评分在评价的返回页面里有，销量暂时无法抓取。

抓取所有评论页耗费时间：

Python2 :3.19 s

Python3 :4.21 s

## 函数说明：
get_jd_rate：根据商品ID与页码获得评论页面的源代码，后续解析工作暂时不做了，就是解析Json

get_jd_rate_totalpagenum：根据商品ID得到评论页码范围，返回值是整型数字，最大页码-1，因为从0开始

get_jd_rate_all：根据商品ID抓取所有评论，返回结果是按顺序存放页面源码的列表

get_jd_price：根据商品ID抓取价格，这个速度最快，而且从来不会封IP

######modifie：2014-11-09 11:23:36
'''
# 没这header就抓不到
headers = {'Host': 'club.jd.com',
           'Referer': 'http://item.jd.com/0.html'}


def get_jd_rate(pid, pagenum):
    '''页码从0开始，在网页上显示的第一页'''
    for i in range(20):
        # 因为经常抓到空数据，所以重试20次（本来是while 1）
        try:
            r = requests.get(
                'http://club.jd.com/productpage/p-{}-s-0-t-3-p-{}.html'.format(pid, pagenum), timeout=1, headers=headers)
            if 'content-length' in r.headers:
                # 一般它的值要么是0说明没抓到数据(包括页码超出)，要么不存在
                # print('retry')
                continue
            else:
                # print(pid, pagenum, 'get it')
                return r.text
                # continue
                break
        except Exception as e:
            # print e
            continue
    # print(pid, pagenum, 'failed')


def get_jd_rate_totalpagenum(pid):
    # 得到的是pagenum的最大数字，页面上显示的页码，还要+1
    try:
        totalpn = json.loads(get_jd_rate(pid, 0))[
            'productCommentSummary']['commentCount']
        return totalpn // 10
    except:
        # print('failed')
        return -1


def get_jd_rate_all(pid):
    maxpn = get_jd_rate_totalpagenum(pid)
    if maxpn == -1:
        # print('null')
        return
    pp = Pool(50)
    result = pp.map(
        lambda x: get_jd_rate(x[0], x[1]), list(zip([pid] * (maxpn + 1), range(maxpn + 1))))
    return result


def get_jd_price(*pid):
    # 可以是多个PID
    pids = ','.join(['J_{}'.format(i) for i in pid])
    url = 'http://p.3.cn/prices/mgets?skuids=' + pids
    r = requests.get(url)
    return r.content


def getjd(pid):
    aa = get_jd_rate_all(pid)
    # print aa[0]

    aa = [json.loads(i)['comments'] for i in aa if i]
    aa = sum(aa, [])
    aa = [i['content'].strip() for i in aa]

    return '\n'.join(aa)
if __name__ == '__main__':
    print(getjd(919979))
