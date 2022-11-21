# encoding: utf-8

'''
  @author: Forme
  @license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
  @contact: 425953474@qq.com
  @time: 2022/11/20 17:20
  @desc:
'''

import sys

from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication

from window import MainWindow

timeText = None
class Main:
	def __init__(self):
		self.app = QApplication(sys.argv)
		self.initWindow()
		self.app.exec_()

	def initWindow(self):
		self.main_window = MainWindow()

if __name__ == '__main__':
	try:
		app = QApplication(sys.argv)
		serverName = 'AppServer'
		socket = QLocalSocket()
		socket.connectToServer(serverName)
		# 判定应用服务是否正常链接，如正常则证明程序实例已经在运行
		if socket.waitForConnected(500):
			app.quit()
		# 如果没有实例运行，则创建应用服务器并监听服务
		else:
			localServer = QLocalServer()
			localServer.listen(serverName)
			# 原始处理逻辑
			mw = Main()
	except Exception as e:
		print('程序启动异常：{}'.format(e))