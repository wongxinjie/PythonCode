#########################################################################
#Function:在网页中提取前缀为http://或者前缀为https://的超链接。
#HTMLParser更实际的应用大概是提出tag里面的内容。
# @Author: Xinjie Wong
# @Time: 2014/08/31
#########################################################################
import os
import sys
from urllib import urlopen
from HTMLParser import HTMLParser


class URLParser(HTMLParser):
	def __init__(self):
		self.data = []
		self.url = []
		self.is_href = False
		self.linkname = ''
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for name, value in attrs:
				if name == 'href':
					self.is_href = True
					if value.startswith('http:') or value.startswith('https://'):
						self.url.append(value)


	def handle_data(self, data):
		if self.is_href:
			self.linkname.join(data)


	def handle_endtag(self, tag):
		if tag == 'a':
			self.linkname = ''.join(self.linkname.split())
			self.linkname = self.linkname.strip()
			if self.linkname:
				self.data.append(self.linkname)
			self.linkname = ''
			self.is_href = False

	def print_result(self):
		print 'All the url link in this page:'
		for value in self.url:
			print value

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        print 'usage: {0} url'.format(os.path.basename(sys.argv[0]))
        sys.exit()

    url = sys.argv[1]
    print 'URL is %s' % url 
    text = urlopen(url).read()
    urlparser = URLParser()
    urlparser.feed(text)
    urlparser.print_result()
    urlparser.close()


if __name__ == '__main__':
	main()
	
