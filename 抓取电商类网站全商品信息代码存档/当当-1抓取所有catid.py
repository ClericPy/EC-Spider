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

# 先抓下所有三级类目的href
# 123654
r = requests.get('http://category.dangdang.com/')
aa = fromstring(r.text).xpath('//div[@class="cfied-list"]/div/a/@href')

# 删除电子书部分
aa = [re.sub('#.*', '', i) for i in aa if 'e.dangdang' not in i]
# 将所有网址尾巴改成第一页带页码的
aa = [i.replace('.html', '') for i in aa]
aa = [i + '-pg1.html' for i in aa]
aa = [i for i in aa if 'http' in i]
aa = '\n'.join(aa)
# 将图书的网址改成重定向以后的第一页
aa = re.sub('all/\?category_path=', 'cp', aa)

with open('all_cat.txt', 'w') as f:
    f.write(aa)
