#!/usr/bin/env python
# encoding: utf-8

'''
  @author: Forme
  @license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
  @contact: 425953474@qq.com
  @file: subthread.py
  @time: 2022/11/20 17:20
  @desc:
'''

import random
import time

import pyautogui
from PyQt5.QtCore import QThread, pyqtSignal

import global_vals as gv

class StayAwakeThread(QThread):
	# 信号
	signal = pyqtSignal()
	def __init__(self):
		super().__init__()

	def run(self):
		print('运行中...')
		time.sleep(gv.static_idle_time)
		self.stayAlive()

	def stayAlive(self):
		while (True):
			try:
				if not gv.running:
					break
				x = random.randint(50, 1500)
				y = random.randint(50, 500)
				pyautogui.moveTo(x, y, duration=0.3)
				time.sleep(2)
				# 按键
				pyautogui.press('shift')
			except Exception as e:
				gv.running = False
				self.signal.emit()
				print('stopped')