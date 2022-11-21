#! python
# encoding: utf-8

'''
  @author: Forme
  @license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
  @contact: 425953474@qq.com
  @file: window.py
  @time: 2022/11/20 17:20
  @desc:
'''

from PyQt5.QtCore import QObject, Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QFont, QCursor, QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QAction, QSystemTrayIcon, \
	QMenu, QLabel, QDesktopWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QToolTip

import global_vals as gv
from subthread import StayAwakeThread


class MainWindow(QWidget, QObject):
	def __init__(self):

		self.thread = StayAwakeThread()
		self.thread.signal.connect(self.updateText)
		super().__init__()
		self.init_ui()
		self.show()

	# 背景图
	# def paintEvent(self, event):
	# 	painter = QPainter(self)
	# 	pixmap = QPixmap("./bg.jpg")
	# 	painter.drawPixmap(self.rect(), pixmap)

	def init_ui(self):
		# 初始化窗口
		self.setGeometry(0, 0, 130, 50)
		self.setCursor(QCursor(Qt.PointingHandCursor))
		# 初始化到屏幕中间
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		screen = QDesktopWidget().screenGeometry()
		self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

		# 右键菜单
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.rightMenuShow)

		# 初始化提示文字
		self.infoText = QLabel(self)
		self.infoText.setAlignment(Qt.AlignCenter)
		self.infoText.setObjectName("label")
		self.infoText.setText("程序{0}秒后运行".format(gv.static_idle_time))
		self.infoText.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
		self.setStyleSheet("QLabel{font-weight:bold;font-family:Roman times;")

		# 设置开始按钮
		self.btn = QPushButton('开始', self)
		self.btn.setToolTip('不忘初心，萌萌加油')
		self.btn.setFixedSize(80, 30)
		self.btn.setStyleSheet("QPushButton{font-weight:bold;font-family:Roman times;background: white;}"
							   "QPushButton:hover{background:rgba(0,129,204,1); font-weight:bold; color:white;}")
		self.btn.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
		self.btn.setCursor(Qt.PointingHandCursor)
		self.btn.clicked.connect(self.startThread)
		hbox = QHBoxLayout()
		hbox.addWidget(self.btn)
		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addWidget(self.infoText)
		vbox.addStretch(1)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

	def rightMenuShow(self):
		try:
			self.contextMenu = QMenu()
			self.contextMenu.addAction(QAction("彻底退出", self, triggered=self.actionHandler))
			self.contextMenu.popup(QCursor.pos())
			self.contextMenu.setStyleSheet("QMenu{background:rgb(80,127,128);color:rgb(255,255,255);font-size:15px;font-weight:bold;width:100px;}")
			self.contextMenu.show()
		except Exception as e:
			print(e)

	def actionHandler(self):
		button = QMessageBox.question(self, "提示", "确定彻底退出？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
		if button == QMessageBox.Yes:
			self.thread.stop()
			self.close()
			exit(0)

	# 重写鼠标移动事件
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.m_flag = True
			self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

	def mouseMoveEvent(self, QMouseEvent):
		if Qt.LeftButton and self.m_flag:
			self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
			QMouseEvent.accept()

	def mouseReleaseEvent(self, QMouseEvent):
		self.m_flag = False
		self.setCursor(QCursor(Qt.PointingHandCursor))

	def quit(self):
		exit(0)

	def startThread(self):
		print('start')
		gv.running = True
		self.infoText.setText("运行中...")
		self.btn.setDisabled(True)
		self.thread.start()

	def updateText(self):
		self.infoText.setText("程序{0}秒后运行".format(gv.static_idle_time))
		self.btn.setDisabled(False)