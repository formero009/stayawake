#!/usr/bin/env python
# encoding: utf-8

'''
  @author: Forme
  @license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
  @contact: 425953474@qq.com
  @file: window.py
  @time: 2022/11/20 17:20
  @desc:
'''

import keyboard
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QAction, QSystemTrayIcon, \
	QMenu, QLabel

import global_vals as gv
from subthread import StayAwakeThread

class MainWindow(QWidget, QObject):
	def __init__(self):

		self.thread = StayAwakeThread()
		super().__init__()

	def paintEvent(self, event):
		painter = QPainter(self)
		pixmap = QPixmap("./bg.jpg")
		painter.drawPixmap(self.rect(), pixmap)

	def init_ui(self):
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowTitle('Stay Awake')
		self.setWindowIcon(QIcon('dram.ico'))
		self.setGeometry(600, 300, 540, 315)
		self.setFixedSize(self.size())
		self.trayIconMenu = QMenu(self)
		self.openAction = QAction("打开", self)
		self.openAction.triggered.connect(self.openup)
		self.trayIconMenu.addAction(self.openAction)
		self.quitAction = QAction("退出", self)
		self.quitAction.triggered.connect(self.quit)
		self.trayIconMenu.addAction(self.quitAction)
		self.trayIcon = QSystemTrayIcon(self)
		self.trayIcon.setContextMenu(self.trayIconMenu)
		self.trayIcon.setIcon(QIcon("dram.ico"))
		self.trayIcon.activated.connect(self.iconActivated)
		self.trayIcon.setToolTip("不忘初心！萌萌加油！")
		# self.trayIcon.showMessage(u"提示", u"程序后台待命中！")
		self.trayIcon.show()

		gv.timeText = QLabel(self)
		gv.timeText.setText('<font color=black size=20 >点击开始，程序将于{0}秒后运行...'.format(gv.static_idle_time))

		start_text = QLabel(
			'<font color=black weight=300 size=15 >按下 <font color=red size=15 > Ctrl+Alt+F9 <font color=black size=15 >开始',
			self)

		stop_text = QLabel(
			'<font color=black size=15 >按下 <font color=red size=15 > Ctrl+Alt+F10 <font color=black size=15 >暂停',
			self)

		self.setStyleSheet("QLabel{font-weight:bold;font-family:Roman times;background:white; background-color:rgba(255,255,255,0.4);}")

		self.btn = QPushButton('开始', self)
		# 设置按钮大小
		self.btn.setFixedSize(100, 50)
		self.btn.setStyleSheet("QPushButton{font-weight:bold;font-family:Roman times;background: white;}"
							   "QPushButton:hover{background:rgba(0,129,204,1); font-weight:bold; color:white;}")
		self.btn.setCursor(Qt.PointingHandCursor)
		self.btn.setFont(QFont("Roman times", 15, QFont.Bold))
		self.btn.clicked.connect(self.startThread)
		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.btn)
		hbox.addStretch(1)
		vbox = QVBoxLayout()
		vbox.addWidget(gv.timeText)
		vbox.addStretch(1)
		vbox.addWidget(start_text)
		vbox.addStretch(1)
		vbox.addWidget(stop_text)
		vbox.addStretch(3)
		vbox.addLayout(hbox)
		self.setLayout(vbox)
		keyboard.add_hotkey("ctrl+alt+f9", lambda: self.startWithHotkey())
		keyboard.add_hotkey("ctrl+alt+f10", lambda: self.stopWithHotkey())

	def iconActivated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick and self.isHidden():
			self.showNormal()
		elif reason == QSystemTrayIcon.DoubleClick and not self.isHidden():
			self.hide()

	def openup(self, event):
		self.showNormal()

	def quit(self):
		exit(0)

	# 重写关闭事件， 修改为最小化到托盘
	def closeEvent(self, event):
		event.ignore()
		self.hide()

	def startThread(self):
		print('start')
		gv.timeText.setText('<font color=green size=20 > 运行中...')
		gv.running = True
		self.btn.setDisabled(True)
		self.thread.start()

	def startWithHotkey(self):
		if not gv.running:
			self.startThread()

	def stopWithHotkey(self):
		if gv.running:
			self.killThread()

	def killThread(self):
		gv.running = False
		self.btn.setDisabled(False)
		self.thread.quit()
		print('thread killed')
		gv.timeText.setText('<font color=black size=15 >点击开始，程序将于{0}秒后运行'.format(gv.static_idle_time))
		print('stoped with hotkey')