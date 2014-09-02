###############################################################################################
#The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, 
#and obtain their return codes. This module intends to replace several other, older modules and functions
# @Coder：Xinjie Wong
# @Time: 2014/08/31
#############################################################################################
import os 
import sys
import subprocess


def ping_sample(command, shell=True):
	pingProcess =subprocess.Popen(args = command, shell=shell)
	pingProcess.wait()
	print 'The process ID is %d' % pingProcess.pid

def main():
	if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
		print 'usage: {0} ping -n number website\n e.g. {1} ping -n 4 www.baidu.com'.format(os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]))
		sys.exit()

	command = sys.argv[1:]
	ping_sample(command)

if __name__ == '__main__':
	main()



