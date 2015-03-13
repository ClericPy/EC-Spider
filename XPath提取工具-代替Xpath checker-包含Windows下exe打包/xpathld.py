from tkinter import *
import requests
from lxml.html import fromstring


def getit(url1, xpath1, np1):
    cout = []
    if '----' in np1:
        np, domain = np1.split('----')
    else:
        np = np1
        domain = ''
    if '----' in url1:
        url, host = url1.split('----')
    else:
        url = url1
        host = ''
    while 1:
        zhuangtai.set(url)
        headers = {'Referer': url, 'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'}
        try:
            r = requests.get(url, headers=headers)
        except:
            zhuangtai.set('网址错误')
            return
        scode = r.content
        try:
            ss = scode.decode('utf-8')
        except:
            try:
                ss = scode.decode('gb18030')
            except:
                return '该网页编码不是utf-8或gb18030'
        xpath = fromstring(ss).xpath
        result = []
        for x in xpath1.strip().split('\n'):
            tt = xpath(x)
            if x.endswith('@href') and host:
                tt = [host + i for i in tt]
            result.append(tt)
        result = ['\t'.join(i) for i in list(zip(*result))]
        cout += result
        if np.strip() == '':
            break
        nextpage = xpath(np)
        if not nextpage:
            break
        if nextpage and domain:
            url = domain + nextpage[0]
        else:
            url = nextpage[0]

    return '\n'.join(cout)


def settext(ss=None):
    text1.delete(0.0, END)
    text1.insert(0.0, getit(wangzhi.get(), xpath1.get(0.0, END), nppath.get()))


def getabout(ss=None):
    text1.delete(0.0, END)
    text1.insert(
        0.0, '简介\n\n\n结果：\n\t多行Xpath的返回结果按顺序用Tab分隔，可以直接复制到Excel\n\n输入URL：\n\n\t如果@href属性是相对地址，可在末尾用四个-隔开带上缺失域名，如：http://em.scnu.edu.cn/article/xueyuantongzhi/yanban/----http://em.scnu.edu.cn\n\n<下一页>Xpath：\n\n\t如果下一页URL是相对地址，请在末尾用四个-隔开带上缺失路径，如：//li/a[text()="下一页"]/@href----http://em.scnu.edu.cn/article/xueyuantongzhi/yanban/\n\n\n\n注：该程序仅做交流使用，如有问题联系lidongone@qq.com，当前版本0.1处于alpha测试阶段，功能仅限于自动查找下一页的单线程爬虫（可以只抓单页）。待完成功能：切换代理、动态页面、多线程加速等')


root = Tk()
# root.update()  # update window ,must do
# curWidth = 800  # root.winfo_reqwidth()  # get current width
# curHeight = 600  # root.winfo_height()  # get current height
scnWidth, scnHeight = root.maxsize()  # get screen width and height
# now generate configuration information
# tmpcnf = '%dx%d+%d+%d' % (curWidth, curHeight,
#                           (scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
root.geometry('800x600+%d+%d' % (scnWidth / 5, scnHeight / 6))
# root.resizable(width=0, height=0)


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


root.title("Xpath版网页提取工具(手工爬虫) 0.10v - Alpha")

#########
jieguolab = LabelFrame(root, text='结果：')
jieguolab.rowconfigure(0, weight=1)
# jieguolab.columnconfigure(0, weight=1)
jieguolab.grid(row=0, columnspan=2, column=0,  sticky=W + E + S + N)
ss = StringVar()
text1 = Text(jieguolab)
text1.pack(expand=1, side=LEFT, fill=BOTH)
###
xpathframe = LabelFrame(
    jieguolab, width=300, text="输入Xpath：")
xpathframe.pack(side=RIGHT, fill=BOTH)


xpath1 = Text(xpathframe)
xpath1.bind('<F5>', settext)

xpath1.pack(expand=1, fill=BOTH)
#######
urlframe = LabelFrame(
    root, text="输入URL：")
urlframe.grid(row=1, column=0, sticky=W + E)
wangzhi = StringVar()
urlentry = Entry(urlframe, textvariable=wangzhi)
urlentry.bind('<F5>', settext)
urlentry.pack(expand=1, fill=BOTH)
#######
pagenumframe = LabelFrame(
    root, text='输入<下一页>Xpath：')
pagenumframe.grid(row=2, column=0, sticky=W + E)
nppath = StringVar()
nextpagexpath = Entry(pagenumframe, textvariable=nppath)
nextpagexpath.bind('<F5>', settext)
nextpagexpath.pack(expand=1, fill=BOTH)

###
start_button = Button(root, text='开始<F5>', height=3, command=settext)
start_button.grid(column=0, columnspan=2,  sticky=W + E)
guanyu = Button(root, text='关于<F1>', height=3, command=getabout)
root.bind('<F1>', getabout)
guanyu.grid(column=0, columnspan=2,  sticky=W + E)
zhuangtai = StringVar()
dangqianurl = Label(root, textvariable=zhuangtai, wraplength=600)
zhuangtai.set('当前网址：')
dangqianurl.grid(column=0, columnspan=2, sticky=W)
getabout()
root.mainloop()
