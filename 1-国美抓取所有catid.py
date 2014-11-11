# coding:utf-8

import requests
from lxml.html import fromstring
# import uniout
import re
r = requests.get('http://www.gome.com.cn/allcategory/')

aa = fromstring(r.text).xpath('//div[@class="in"]/a/@href')
aa = ''.join(aa)
aa = re.findall('(cat\d+)\.', aa)
with open('allcategory.txt', 'w') as f:
    f.write('\n'.join(aa))
