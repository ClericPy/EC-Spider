# coding:utf-8
from multiprocessing.dummy import Pool
import requests
import json
import re
from lxml.html import fromstring
from lxml import _elementpath

# 没这header就抓不到
headers = {'Host': 'club.jd.com',
           'Referer': 'http://item.jd.com/0.html'}


def get_jd_rate(pid, pagenum):
    '''!页码从0开始，在网页上显示的第一页'''
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
                print('.', end=' ')
                return r.text
                # continue
                break
        except Exception as e:
            # print e
            continue
    return ''
    # print(pid, pagenum, 'failed')


def get_jd_rate_totalpagenum(pid):
    # !得到的是pagenum的最大数字，页面上显示的页码，还要+1
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
        return ''
    pp = Pool(100)
    result = pp.map(
        lambda x: get_jd_rate(x[0], x[1]), list(zip([pid] * (maxpn + 1), range(maxpn + 1))))
    pp.close()
    pp.join()
    result = '\n'.join(re.findall(r'content":"(.*?)"', str(result)))
    result = re.sub('<.*?>', '', result)
    return result


def get_list_ids(url):
    r = requests.get(url, headers={'Host': 'list.jd.com',
                                   'Referer': 'http://channel.jd.com/jewellery.html'})
    try:
        scode = r.content.decode('utf-8')
    except:
        scode = r.content.decode('gbk')
    xpath = fromstring(scode).xpath
    ids = xpath('//a/@wareid|//i/@name|//a/@data-tag')
    nextpage = xpath('//a[@class="pn-next"]/@href|//a[@class="next"]/@href')
    nextpage = nextpage[0] if nextpage else False
    stopmsg = '已有0人评价' in scode or '0</a>个评论' in scode
    return (ids, nextpage, stopmsg)


def get_list(url):
    r = requests.get(url, headers={'Host': 'list.jd.com',
                                   'Referer': 'http://channel.jd.com/jewellery.html'})
    try:
        scode = r.content.decode('utf-8')
    except:
        scode = r.content.decode('gbk')
    xpath = fromstring(scode).xpath
    title = xpath('/html/head/title/text()')[0]
    title = re.sub('\s.*', '', title)
    result = []
    while 1:
        ids, nextpage, stopmsg = get_list_ids(url)
        print('get %s' % url)
        result += ids
        if stopmsg:
            print('已经出现评价数量为0的商品，程序终止...')
            break
        if not nextpage:
            print('已达最大页码数，程序终止...')
            break

        url = nextpage if nextpage.startswith(
            'http') else 'http://list.jd.com' + nextpage
    with open('./files/%s.txt' % title, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
        print('结果已存入%s.txt' % title)
    print(result)
    return result
import os
if not os.path.exists("files"):
    os.makedirs('files')


def main(url):
    pid = re.findall('jd\.com/(\d+)\.htm', url)
    if pid:
        print(pid[0])
        with open('./files/%s.txt' % pid[0], 'w', encoding='utf-8') as f:
            f.write(get_jd_rate_all(pid[0]))
            print('%s已完成，结果已存入%s.txt' % (pid[0], pid[0]))

    else:
        print('start the mission for product-list pages...')
        get_list(url)


# print(main('http://list.jd.com/list.html?cat=6144,6167,6173'))
while 1:
    print('\n' + '=' * 80 + '\n')
    try:
        command = input(
            '为了避免拿来主义，本程序功能仅限以下内容：\n1. 输入单个商品页地址或商品ID========>导出评论(pid.ini)\n2. 输入商品列表页地址（比如某类目，不是搜索结果页，事先最好按评论数排序）========>该类目下有评论的ID（类目标题.txt）\n3. 输入文件名（类目标题.txt）========>得到该类目下所有商品评论（类目.ini）\n4. 输入exit或quit退出程序\n注：所有非程序文件读写都在files目录下\n以上模式自动识别，请输入指令：\n')
        if command == 'exit' or command == 'quit':
            print('程序结束...')
            break
        if command.isalnum():
            print(command)
            with open('./files/%s.txt' % command, 'w', encoding='utf-8') as f:
                f.write(get_jd_rate_all(command))
                print('%s已完成，结果已存入%s.txt' % (command, command))
                continue
        if '.txt' in command:
            with open('./files/' + command) as ff:
                ids = ff.read().split()
            fname = command.replace('.txt', '.ini')
            print(ids)
            zongshu = len(ids)
            jishu = 0
            with open('./files/' + fname, 'w', encoding='utf-8') as f:
                for i in ids:
                    f.write(get_jd_rate_all(i) + '\n')
                    jishu += 1
                    print('%s已完成-%s/%s' % (i, jishu, zongshu))
                    print('所有结果已存入%s' % fname)
            continue

        main(command)
    except Exception as e:
        print(e)
        print('错误..')
