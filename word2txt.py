################################################
#适用系统：Windows XP/Windows 7
#Function: 将word文档转化成txt文档。
# @Author: Xinjie Wong
# @Time: 2014/09/01
################################################
import os
import sys
import fnmatch
import logging
import win32com.client

logging.basicConfig(filename = os.path.join(os.getcwd(), 'word2txterror.log'), level = logging.ERROR)

def word_to_txt(direction):
	wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")

	try:
		for path, dirs, files in os.walk(sys.argv[1]):
			for filename in files:
				if not fnmatch.fnmatch(filename, '*.doc'): continue
				doc = os.path.abspath((os.path.join(path, filename)))
				print "processing %s" % doc
				wordapp.Documents.Open(doc)
				docastxt = doc[:-3] + "txt"
				wordapp.ActiveDocument.SaveAs(docastxt, FileFormat = win32com.client.constants.wdFormatText)
				wordapp.ActiveDocument.Close()
	except Exception as error:
		logging.error(error)
	finally:
		wordapp.Quit()

def main():
	if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
		print 'usage: {0} dir1 [dir2 [...]]'.format(os.path.basename(sys.argv[0]))
		sys.exit()

	dir_list = sys.argv[1:]
	for direction in dir_list:
		word_to_txt(direction)
		print '%s done' % direction

if __name__ == '__main__':
	main()


	
