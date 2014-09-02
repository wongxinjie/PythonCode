#####################################
# -*- coding: utf-8 -*-
#Function: 指定URL将网页下载到本地
# @Coder: Xinjie Wong
# @Time: 2014/08/31
#**********************
import os
import sys
import urllib
import logging

#日志文件
logging.basicConfig(filename = os.path.join(os.getcwd(), 'urlerror.txt'), level = logging.ERROR)

def download(url, filename=""):
    def reporthook(block_count, block_size, file_size):
        if file_size == -1:
            print "未知文件大小，已下载：", block_count*block_size
        else:
            precentage = int((block_count*block_size*100.0)/file_size)
            if percentage > 100:
                print "100%"
            else:
                print "%d %" % (percentage)

    try:
        filehandler, m = urllib.urlretrieve(url, filename, reporthook=reporthook)
    except ContentTooShortError as e:
        logging.error(e)
    else:
        print "下载完成！"
        return filehandler

def main():
    if len(sys.argv) != 3 or sys.argv[1] in {'-h', '--help'}:
        print 'usage: {0} url filename'.format(os.path.basename(sys.argv[0]))
        sys.exit()

    url = sys.argv[1]
    filename = sys.argv[2]
    download(url, filename)


if __name__ == "__main__":
    main()

    
