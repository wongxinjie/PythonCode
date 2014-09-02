##########################################
#-*- coding: utf-8 -*-
#简易聊天室的客户端代码。
# @Author: Xinjie Wong
# @Time: 2014/09/01
#########################################
import os
import sys
import subprocess

def chat_client(host='localhost', port='5005'):
	command = 'telnet {0} {1}'.format(host, port)
	telnet_process = subprocess.Popen(args= command, shell=True)
	telnet_process.wait()

def main():
	if len(sys.argv) > 1 and sys.argv[1] in {'-h', '--help'}:
		print 'usage: {0} host_name port'.format(os.path.basename(sys.argv[0]))
		sys.exit()

	if len(sys.argv) == 3:
		host = sys.argv[1]
		port = sys.argv[2]
		chat_client(host, port)
	else:
		chat_client()



if __name__ == '__main__':
	main()

