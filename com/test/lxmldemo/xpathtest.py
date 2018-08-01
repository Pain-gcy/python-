# coding:utf-8


from urllib.request import urlopen
from lxml import etree
from com.test.lxmldemo import excelexport
import xlwt


# 爬虫豆瓣的一个评论

# 获取页面地址

def getUrl():
	f = xlwt.Workbook()
	sheet1 = f.add_sheet('音乐爬虫', cell_overwrite_ok=True)
	for i in range(10):
		size = i * 25  # 当前爬虫的位置
		url = 'https://music.douban.com/top250?start={}'.format(size)
		scrapyPage(url, sheet1, f, size)


# 爬取每页数据
def scrapyPage(url, sheet1, f, size):
	html = urlopen(url)  # 通过urlopen方法访问拼接好的url
	res = html.read().decode()  # read()方法是读取返回数据内容，decode是转换返回数据的bytes格式为str
	s = etree.HTML(res)
	trs = s.xpath('//*[@id="content"]/div/div[1]/div/table/tr')
	for tr in trs:
		lens = []
		href = tr.xpath('./td[2]/div/a/@href')[0]
		name = tr.xpath('./td[2]/div/p/text()')[0].split("/")[0]
		title = tr.xpath('./td[2]/div/a/text()')[0].rstrip("\n            "[::-1]).lstrip("\n            ")
		score = tr.xpath('./td[2]/div/div/span[2]/text()')[0]
		number = tr.xpath('./td[2]/div/div/span[3]/text()')[0].rstrip("\n                    )\n"[::-1])
		number = number.lstrip("\n                    (\n                            ")
		img = tr.xpath('./td[1]/a/img/@src')[0]
		titles = tr.xpath('./td[1]/a/@title')[0]
		lens.append(title)
		lens.append(name)
		lens.append(score)
		lens.append(titles)
		lens.append(href)
		lens.append(number)
		# print(lens)
		excelexport.write_excel(size, lens, sheet1, f)
		size += 1


# 爬去单个数据
def getheader():
	url = 'https://music.douban.com/top250'
	html = urlopen(url)  # 通过urlopen方法访问拼接好的url
	res = html.read().decode()  # read()方法是读取返回数据内容，decode是转换返回数据的bytes格式为str
	s = etree.HTML(res)
	href = s.xpath('//*[@id="content"]/div/div[1]/div/table[1]/tr/td[2]/div/a/@href')[
		0]  # 因为要获取标题，所以我需要这个当前路径下的文本，所以使用/text()
	title = s.xpath('//*[@id="content"]/div/div[1]/div/table[1]/tr/td[2]/div/a/text()')[
		0]  # 因为要获取标题，所以我需要这个当前路径下的文本，所以使用/text()
	score = s.xpath('//*[@id="content"]/div/div[1]/div/table[1]/tr/td[2]/div/div/span[2]/text()')[
		0]  # 因为要获取文本，所以我需要这个当前路径下的文本，所以使用/text()
	numbers = s.xpath('//*[@id="content"]/div/div[1]/div/table[1]/tr/td[2]/div/div/span[3]/text()')[
		0]  # 因为要获取文本，所以我需要这个当前路径下的文本，所以使用/text()
	print(href, title, score, numbers)


if '__main__':
	getUrl()
