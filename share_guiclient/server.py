#########################################################
#-*- coding: utf-8 -*-
# 简易文件贡献服务器实现。
# @Coder: Xinjie Wong
# @Time: 2014/09/01
#########################################################
from xmlrpclib import ServerProxy, Fault, Binary
from os.path import join, abspath, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys
import os
import logging


logging.basicConfig(filename=os.path.join(os.getcwd(), 'server_message.log'), 
	level=logging.DEBUG,
	format='%(asctime)s: %(message)s',
	datefmt='%a, %Y %b %d %H:%M:%S')

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 100
ACCDESS_DENIED = 200

class UnhandledQuery(Fault):
	def __init__(self, message="Couldn't handle the query"):
		Fault.__init__(self, UNHANDLED, message)

class AccessDenied(Fault):
	def __init__(self, message="Access denied"):
		Fault.__init__(self, ACCDESS_DENIED, message)

def inside(dir, name):
	dir = abspath(dir)
	name = abspath(name)
	return name.startswith(join(dir, ''))

def getPort(url):
	name = urlparse(url)[1]
	parts = name.split(':')
	return int(parts[-1])


class Node:

	def __init__(self, url, dirname, password):
		self.url = url
		self.dirname = dirname
		self.password = password
		self.known = set()

	def query(self, query, history=[]):
		try:
			return self._handle(query)
		except UnhandledQuery:
			history = history + [self.url]
			if len(history) >= MAX_HISTORY_LENGTH: raise
			return self._broadcast(query, history)

	def hello(self, other):
		self.known.add(other)
		return 0

	def fetch(self, query, password):
		if password != self.password: raise AccessDenied
		result = self.query(query)
		f = open(query, 'wb')
		#print result 
		f.write(result)
		f.close()
		logging.info(query)
		return 0

	def _start(self):
		s = SimpleXMLRPCServer(("", getPort(self.url)), logRequests = False)
		s.register_instance(self)
		s.serve_forever()

	def _handle(self, query):
		dir = self.dirname
		name = join(dir, query)
		if not isfile(name): raise UnhandledQuery
		if not inside(dir, name): raise AccessDenied
		with open(name, 'rb') as handle:
			return Binary(handle.read()).data
		#return open(name).read()

	def _broadcast(self, query, history):
		for other in self.known.copy():
			if other in history: continue
			try:
				s = ServerProxy(other)
				return s.query(query, history)
			except Fault, f:
				if f.faultCode == UNHANDLED: pass 
				else: self.known.remove(other)
			except:
				self.known.remove(other)
			raise UnhandledQuery

def main():
	url, directory, password = sys.argv[1:]
	n = Node(url, directory, password)
	n._start()


if __name__ == '__main__':
	main()
	
