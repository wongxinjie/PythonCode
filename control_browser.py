################################################################
# -*- coding: utf-8 -*-
#python 自带的webbrowser模块的简单应用，用来控制系统默认浏览器的
#动作。
# @Author: Xinjie Wong
# @Time: 2014/09/01
###############################################################
import os
import sys
import logging
import webbrowser

#日志记录
logging.basicConfig(filename= os.path.join(os.getcwd(), 'control_browser.log'), level = logging.ERROR)

def control_browser(url='http://www.baidu.com'):
	try:
		webbrowser.open(url)
	except webbrowser.ERROR as e:
		logging.error(e)
	else:
		print 'Done!'

def main():
	if len(sys.argv) > 1 and sys.argv[1] in {'-h', '--help'}:
		print 'usage: {0} [url1 [ur2 [...]]]'.format(os.path.basename(sys.argv[0]))
		sys.exit()

	if len(sys.argv) > 1:
		url_list = sys.argv[1:]
		for url in url_list:
			control_browser(url)
	else:
		control_browser()



if __name__ == '__main__':
	main()
