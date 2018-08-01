#!/usr/bin/python3
# 文件名: excelexport.py
import xlwt


# 设置表格样式
def set_style(name, height, bold=False):
	style = xlwt.XFStyle()
	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.height = height
	style.font = font
	borders = xlwt.Borders()
	borders.left = borders.DASHED
	style.borders = borders
	return style


# 写Excel
def write_excel(i, lens, sheet1, f):
	row0 = ["歌名", "歌手", "豆瓣评分", "标题", "连接", "评价人数"]
	if 0 == i:
		for j in range(0, len(row0)):
			sheet1.write(0, j, row0[j], set_style('Times New Roman', 220, True))
	else:
		for j in range(0, len(lens)):
			sheet1.write(i, j, lens[j], set_style('Times New Roman', 220, True))
	f.save('test.xls')


# if __name__ == '__main__':
# 	write_excel(0, ["1", "2", "3", "4"])
