#---------------------------------------------------------------------------
#-*- coding: utf-8  -*-
#Function:从指定的在线电子书阅读网站中将指定的内容爬下来做成txt文档。
#         程序借鉴至Wang Hay同学的博客
#URL Example: http://www.sbkk8.cn/mingzhu/waiguowenxuemingzhu/guangdaozhilian/
#URL Example: http://www.sbkk8.cn/mingzhu/waiguowenxuemingzhu/dubianchunyi/shileyuan/
# @Author: Xinjie Wong
# @Time: 2014/09/08
#-----------------------------------------------------------------------------
import os
import re
import sys
import time
import string
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError

class HTMLTool:
	begin_char_to_none_rex = re.compile("(\t|\n| |<a.*?>|<img.*>)")
	end_char_to_none_rex = re.compile('<.*?>')

	begin_part_rex = re.compile("<p.*?>")
	char_to_new_line_rex = re.compile("</br>|</p>|<div>|</div>")
	char_to_next_tab_rex = re.compile("<td>")

	replace_tab = [("<", "<"), (">", ">"), ("&", "&"), ("&","\""), (" ", " ")]

	def replace_char(self, sentence):
		sentence = self.begin_char_to_none_rex.sub("", sentence)
		sentence = self.begin_part_rex.sub("\n", sentence)
		sentence = self.char_to_new_line_rex.sub("\n", sentence)
		sentence = self.char_to_next_tab_rex.sub("\t", sentence)
		sentence = self.end_char_to_none_rex.sub("", sentence)

		for item in self.replace_tab:
			sentence = sentence.replace(item[0], item[1])
		return sentence



class TXTSpider:

	def __init__(self, url, begin_page, total_page, filename):
		self.my_url = url
		self.begin_page = begin_page
		self.total_page = total_page
		self.filename = filename
		self.page_numbers = []
		self.my_tool = HTMLTool()
		print 'TXTSpider start working...'

	def get_page_list(self):
		for n in range(0, self.total_page):
			self.page_numbers.append(self.begin_page-n)

	def txt_init(self):
		f = open(self.filename+'.txt', 'w+')
		f.close()
		self.get_page_list()
		self.get_data(self.my_url)
		print 'Finished!'


	def find_title(self, page):
		title_match = re.search(r'<h1.*?>(.*?)</h1>', page, re.S)
		title =''
		if title_match:
			title = title_match.group(1)
		else:
			print ''
		signs = ('\\', '/', ':', '*', '?', '"', '>', '<', '|')
		for sign in signs:
			if sign in title:
				title.replace(sign, '')
		return title

	def save_data(self, data):
		with open(self.filename+'.txt', 'a') as f:
			f.write(data)


	def get_data(self, url):
		for n in self.page_numbers:
			time.sleep(10)
			current_url = url+str(n)+'.html'
			print 'processing... '+current_url
			try:
				current_page = urllib2.urlopen(current_url).read()
			except URLError, e:
				if hasattr(e, 'code'):
					print 'Error code: ', e.code
				elif hasattr(e, 'reason'):
					print 'Error reason: ', e.reason
			else:
				data = self.deal_data(current_page)
				self.save_data(data)

	def deal_data(self, current_page):
		content_item = re.findall('id="f_article".*?>(.*?)</div>', current_page, re.S)
		data = self.find_title(current_page)+'\n'
		for item in content_item:
			data = data+self.my_tool.replace_char(item.replace("\n", ""))
		return data 




def main():
	if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
		print 'usage: {0} url begin_page total_page filename'.format(os.path.basename(sys.argv[0]))
		sys.exit()
	url, begin_page, total_page, filename = sys.argv[1:]
	begin_page = int(begin_page)
	total_page = int(total_page)

	txt_spider = TXTSpider(url, begin_page, total_page, filename)
	txt_spider.txt_init()


if __name__ == '__main__':
	main()
