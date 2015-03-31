# coding=utf-8
print('正在初始化...')
import requests
import re
from lxml.html import fromstring
from multiprocessing.dummy import Pool
from lxml import _elementpath


class Youku_comment:

    """docstring for Youku_comment"""

    def __init__(self, raw_url):

        self.pid = re.findall('/id_(.*?)\.html', raw_url)[0]
        r1 = requests.get(raw_url)
        title = re.findall('<title>(.*?)</title>', r1.text)[0]
        title = re.sub('\W', '', title).replace('在线播放优酷网视频高清在线观看', '')
        totalpn = self.get_totalpn(self.pid)
        print('视频ID：%s' % self.pid, '\n视频标题：%s' %
              title, '\n总页码数：%s\n正在抓取...' % totalpn)

        pp = Pool(30)
        pagenums = range(1, totalpn + 1)
        result = pp.map(self.get_comment, pagenums)
        pp.close()
        pp.join()
        result = [i for i in result if i]
        jieguo = '\n'.join(result).replace(
            ',//', '').replace('//', '').replace(',#', '')
        with open('%s.csv' % title, 'w', encoding='gbk') as f:
            f.write(jieguo.encode('gbk', 'ignore').decode('gbk'))

    def get_totalpn(self, pid):
        r = requests.get(
            'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap={"videoid":"%s","page":1}' % pid)
        totalpn = (int(r.json()['totalSize'].replace(',', '')) // 30) + 1
        return totalpn

    def get_comment(self, pagenum):
        for _ in range(5):
            try:
                r = requests.get(
                    'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap={"videoid":"%s","page":%s}' % (self.pid, pagenum), timeout=3)
                sjson = r.json()
                scode = sjson['con']
                nxpath = fromstring(scode).xpath
                ss = nxpath('//p[@id]')
                ss = [i.text for i in ss if i.text]
                if ss:
                    return ','.join(ss)
            except:
                pass


print('注：试用版没有多次抓取、切换代理、GUI、回复包括原文、批量抓取、提取关键词等功能\n\n\n\n\n初始化结束，请输入优酷视频网址。')
while 1:
    try:
        url = input('请输入网址：')
        Youku_comment(url)
        break
    except:
        print('错误，请重试')
