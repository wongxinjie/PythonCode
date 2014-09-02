####################################################
#-*- coding: utf-8 -*-
# 带GUI界面的简易文件共享客户端。
# @Coder: Xinjie Wong
# @Time: 2014/09/01
####################################################
from xmlrpclib import ServerProxy, Fault
from server import Node, UNHANDLED
from client import randomString
from threading import Thread 
from time import sleep
from os import listdir
import sys
import wx
import os

HEAD_START = 0.1
PASSWORD_LENGTH = 100

class ListableNode(Node):

	def list(self):
		return listdir(self.dirname)


class Client(wx.App):

	def __init__(self, url, dirname, urlfile):
		self.password = randomString(PASSWORD_LENGTH)
		n = ListableNode(url, dirname, self.password)
		t = Thread(target=n._start)
		t.setDaemon(1)
		t.start()
		sleep(HEAD_START)
		self.server = ServerProxy(url)
		for line in open(urlfile):
			line = line.strip()
			self.server.hello(line)
		#Run GUI
		super(Client, self).__init__()


	def updateList(self):
		self.files.Set(self.server.list())


	def OnInit(self):

		win = wx.Frame(None, title="文件共享v1.0", size=(400, 200))
		bkg = wx.Panel(win)
		self.input = input = wx.TextCtrl(bkg)

		submit = wx.Button(bkg, label="Fetch", size=(80, 25))
		submit.Bind(wx.EVT_BUTTON, self.fetchHandler)

		hbox = wx.BoxSizer()
		hbox.Add(input, proportion=1, flag=wx.ALL| wx.EXPAND, border = 10)
		hbox.Add(submit, flag = wx.TOP | wx.BOTTOM | wx.RIGHT, border = 10)

		self.files = files = wx.ListBox(bkg)
		self.updateList()

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox, proportion = 0, flag = wx.EXPAND)
		vbox.Add(files, proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM , border = 10)

		bkg.SetSizer(vbox)
		win.Show()

		return True

	def fetchHandler(self, event):

		query = self.input.GetValue()
		try:
			self.server.fetch(query, self.password)
			self.updateList()
		except Fault, f:
			if f.faultCode != UNHANDLED: raise
			print "Couldn't find the file", query



def main():
	if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
		print 'usage: {0} url.txt director http://servername:port'.format(os.path.basename(sys.argv[0]))
		sys.exit()
	urlfile, directory, url = sys.argv[1:]
	client = Client(url, directory, urlfile)
	client.MainLoop()


if __name__ == '__main__':
	main()

