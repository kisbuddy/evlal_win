#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#错误窗口提示
from PyQt4 import uic
from PyQt4 import QtCore, QtGui ,QtNetwork
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from ctypes import *
from PyQt4.QtGui import *
import base64
import json
import ConfigParser  #INI读取数据
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
from Clicked_Controller import threadpool  #线程
from Clicked_Controller import log #日志记录
import thread

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class link_except_ui(QWidget):
    insert = pyqtSignal(str,str)  #添加
    form_close=pyqtSignal()  #关闭窗体
    def __init__(self):
        super(link_except_ui, self).__init__()
        uic.loadUi("ui/link_except.ui", self)
        self.setWindowIcon(QtGui.QIcon("system/main.ico"))
        flags = 0  #设置禁止最大化
        flags|= Qt.WindowMinimizeButtonHint  #设置禁止最大化
        self.setWindowFlags(flags)  #设置禁止最大化
        #禁止最大化按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        #禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        try:
            #读取配置信息
            self.INI_config = ConfigParser.ConfigParser()
            self.INI_config.readfp(open("system/Server.ini"))
            try:
                self.close_form_time = int(self.INI_config.get("link_except", "close_form"))
            except BaseException, e:
                self.close_form_time = 5

            self.textEdit_data.setEnabled(0)  #给改成禁用
            self.title=u""#保存标题
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def set_data(self,**kwargs):  #远程参数
        try:
            if "title" in kwargs:  #标题
                self.setWindowTitle(u'%s'%(kwargs['title']))
                self.title=u'%s'%(kwargs['title'])
            if "except_data" in kwargs:  #错误提示
                self.textEdit_data.setText(u'%s'%(kwargs['except_data']))
            #self.close_form(5)  #关闭窗口
            t_h_Thread = threadpool.ThreadPool(1)   #创建多线程  线程池
            #t_h_i = t_h_Thread.busy()
            t_h_Thread.push(self.close_form,self.close_form_time)
            t_h_Thread.wait_for_idel(1)
            # t_h_Thread.wait()  #等待子进程结束
            #thread.start_new_thread(self.close_form,(self.close_form_time,))  #
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def close_form(self,i):  #关闭窗口
        try:
            for x in range(int(i)):
                xx=int(i)-int(x)
                self.setWindowTitle(u'%s-------------%s'%(self.title,str(xx)))
                time.sleep(1)
            #在这应该发送个信号回去让  这个属性页关闭
            self.form_close.emit()
            self.close()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


