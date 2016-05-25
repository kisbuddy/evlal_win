#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#WEB浏览器

from PyQt4 import uic
from PyQt4 import QtCore, QtGui,QtNetwork
from PyQt4.QtCore import pyqtSlot
from ctypes import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import socket
socket.setdefaulttimeout(10)

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from ui import tabWidget_close_lock,UIManager
from Db_Model import db_shell #常用数据库操作

from Clicked_Controller import link_shell  #链接SHELL等操作
from Clicked_Controller import eval_link  #链接SHELL
from Clicked_Controller import ShowFileManage_class  #文件管理事件响应
from Clicked_Controller import threadpool #线程操作
from Clicked_Controller import log #日志记录
import link_except_ui   #错误异常处理

class ShowWebManage_ui(QWidget):
#class ShowWebManage_ui(QDialog):
    def __init__(self,**kwargs):
        super(ShowWebManage_ui, self).__init__()
    #def __init__(self,**kwargs):
    #    QtGui.QWidget.__init__(self)
        try:
            try:
                self.main_ui=UIManager.get_ui('main_ui') #主程序UI
                #self.shell_sql=UIManager.shell_sql
                self.ShowWeb_ui = uic.loadUi("ui/ShowWebManage.ui", self)#动态加标签
                # uic.loadUi("ui/ShowWebManage.ui", self)
                # self.setWindowIcon(QtGui.QIcon("system/main.ico"))
                # flags = 0  #设置禁止最大化
                # flags|= Qt.WindowMinimizeButtonHint  #设置禁止最大化
                # self.setWindowFlags(flags)  #设置禁止最大化
                # #禁止最大化按钮
                # self.setWindowFlags(Qt.WindowMinimizeButtonHint)
                # #禁止拉伸窗口大小
                # self.setFixedSize(self.width(), self.height())
            except BaseException, e:
                log.logging.debug("except:%s"%(str(e)))
            self.url_comboBox.setMouseTracking(False)
            self.url_comboBox.setAcceptDrops(False)
            self.url_comboBox.setEditable(True)
            self.url_comboBox.setMaxVisibleItems(15)#设置下拉最大选项数为15
            Title=str('%s'%(kwargs['Title']))
            self.main_ui.tabWidget.addTab(self.ShowWeb_ui,QIcon('system/web.ico'),Title)
            if "form" in kwargs:  #名称
                if int(kwargs['form']):
                    self.main_ui.tabWidget.setCurrentIndex(self.main_ui.tabWidget.count()-1)#显示当前页

            self.webView_look(str(Title))  #浏览网站

            self.url_comboBox.setEditText(_fromUtf8(Title))  #设置当前内容
            self.url_comboBox.addItem(_fromUtf8(Title))  #添加到下拉列表

            self.url_comboBox.installEventFilter(self)#在窗体上为self.edit安装过滤器
            #=========================
            self.look_pushButton.clicked.connect(self.look_Button)    #浏览网页
            #self.url_comboBox.textChanged.connect(self.cs1)
            #=========================

        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def eventFilter(self, source, event):#事件监听
        try:
            #PyQt4.QtCore.QEvent.KeyPress
            #PyQt4.QtCore.QEvent.KeyRelease
            if event.type()==QtCore.QEvent.KeyPress:   #检测键盘事件
                if event.key()==QtCore.Qt.Key_Return:  #判断回车
                    #回车是16777220
                    self.look_Button()  #浏览网页
            return QtGui.QWidget.eventFilter(self, source, event)#将事件交给上层对话框
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def look_Button(self):
        try:
            url=str(self.url_comboBox.currentText())
            self.url_comboBox.addItem(_fromUtf8(url))  #添加到下拉列表
            self.webView_look(url)  #浏览网站
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def webView_look(self,url):  #浏览网站
        try:
            #self.webView.load(QUrl(url))
            #self.webView.show()
            self.web_lok_View.setUrl(QtCore.QUrl(str(url)))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


