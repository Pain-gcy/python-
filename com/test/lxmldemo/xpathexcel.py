# coding=utf-8

import requests
import time
import xlwt
import xlrd
from lxml import etree

class ZbjData(object):

 def __init__(self):
     self.f = xlwt.Workbook()   #创建工作薄
     self.sheet1 = self.f.add_sheet(u'任务列表',cell_overwrite_ok=True)
     self.rowsTitle = [u'编号',u'标题',u'简介',u'价格',u'截止时间',u'链接']
     for i in range(0, len(self.rowsTitle)):
        self.sheet1.write(0, i, self.rowsTitle[i], self.set_style('Times new Roman', 220, True))

     self.f.save('zbj.xlsx')

 def set_style(self,name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.colour_index = 2
        font.height = height
        style.font = font
        return style

 def getUrl(self):
    for i in range(33):
        url = 'http://task.zbj.com/t-ppsj/p{}s5.html'.format(i+1)
        self.spiderPage(url)

 def spiderPage(self,url):
    if url is None:
        return None

    try:
        data = xlrd.open_workbook('zbj.xlsx')
        table = data.sheets()[0]  # 通过索引顺序获取table, 一个execl文件一般都至少有一个table
        rowCount = table.nrows      #获取行数   ，下次从这一行开始
        proxies = {
            'http': 'http://221.202.248.52:80',
        }
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400'

        headers = {'User-Agent': user_agent}
        htmlText = requests.get(url, headers=headers).text

        selector = etree.HTML(htmlText)
        tds = selector.xpath('//*[@class="tab-switch tab-progress"]/table/tr')
        m = 0
        for td in tds:
             data = []
             price = td.xpath('./td/p/em/text()')
             href = td.xpath('./td/p/a/@href')
             title = td.xpath('./td/p/a/text()')
             subTitle = td.xpath('./td/p/text()')
             deadline = td.xpath('./td/span/text()')
             price = price[0] if len(price)>0 else ''    # python的三目运算 :为真时的结果 if 判定条件 else 为假时的结果
             title = title[0] if len(title)>0 else ''
             href = href[0] if len(href)>0 else ''
             subTitle = subTitle[0] if len(subTitle)>0 else ''
             deadline = deadline[0] if len(deadline)>0 else ''

            #拼装成一个集合
             data.append(rowCount+m)    #加个序号
             data.append(title)
             data.append(subTitle)
             data.append(price)
             data.append(deadline)
             data.append(href)

             for i in range(len(data)):
                 self.sheet1.write(rowCount+m,i,data[i])    #写入数据到execl中

             m+=1   #记录行数增量
             print (m)
             print (price, title, href, subTitle, deadline)
    except Exception as e:
        print ('出错',e.message)

    finally:
        self.f.save('zbj.xlsx')


if '_main_':
    zbj = ZbjData()
    zbj.getUrl()