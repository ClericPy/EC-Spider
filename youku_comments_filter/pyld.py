# coding:utf-8
print('正在初始化...')
import requests
import re
from lxml.html import fromstring
import pyautogui
import sys
import os
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
        self.aa = sum(result, [])
        # print(jieguo)
        # with open('%s.csv' % title, 'w', encoding='gbk') as f:
        #     f.write(jieguo.encode('gbk', 'ignore').decode('gbk'))

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
                ss = re.findall('<p id=".*?">.*?</p>', scode, flags=re.S)
                ss = [re.sub('<.*?>', '', i) for i in ss]
                if ss:
                    return ss
            except:
                pass


def filt1(str1, kws):
    kws = kws.split(' ') if kws else 'OST 背景 音乐 旋律 歌曲 调子 music 耳熟 BGM 谁唱的 来自 出自 原声'.split(
        ' ')
    for i in kws:
        if i in str1:
            return str1


def quchong(ll):
    ss = ''
    for i in ll:
        if i in ss:
            continue
        else:
            ss = ss + '\n' + i
    return ss

while 1:
    try:
        url = pyautogui.prompt('请输入网址：')
        if not url:
            break
        tt = Youku_comment(url)
        pinglun = tt.aa
        while 1:
            kws = pyautogui.prompt('请输入关键词，多个请用空格隔开（直接回车则代表找背景音乐）：')
            kws = kws if kws else 0
            ss = [filt1(i, kws) for i in pinglun]
            ss = [i for i in ss if i]
            ss = quchong(ss)
            print('检索结果：\n')
            print(ss)
            jixu = pyautogui.confirm(
                text='是否要继续检索', title='请确认', buttons=['是', '否'])
            if jixu == '否':
                break

    except Exception as e:
        print(e)
        print('错误，请重试')
os.system('pause')
