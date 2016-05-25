#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#from PyQt4.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt4 import uic
from PyQt4 import QtCore, QtGui ,QtNetwork
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from ctypes import *
from PyQt4.QtGui import *
from Clicked_Controller import log #日志记录
import ConfigParser  #INI读取数据
#class Action_ui(QWidget):
class Action_ui(QDialog):
    # def __init__(self):
    #     super(Action_ui, self).__init__()
    form_close=pyqtSignal()  #关闭窗体
    def __init__(self,form=0,parent=None):
        QtGui.QWidget.__init__(self,parent)
        uic.loadUi("ui/Action_ui.ui", self)
        self.form=form  #窗体关闭
        self.setWindowIcon(QtGui.QIcon("system/main.ico"))
        flags = 0  #设置禁止最大化
        flags|= Qt.WindowMinimizeButtonHint  #设置禁止最大化
        self.setWindowFlags(flags)  #设置禁止最大化
        #禁止最大化按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        if int(self.form)==1:
            self.setWindowFlags(Qt.SubWindow)
        #禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        try:
            self.INI_config = ConfigParser.ConfigParser()
            self.INI_config.readfp(open("system/Server.ini"))
            if(int(self.INI_config.get('Action', 'declaraction'))): #选中
                self.checkBox.setChecked(True)    #设置复选框为选择状态

            self.checkBox.clicked.connect(self.Box_click)  #阅读声明
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def Box_click(self):
        try:
            if(self.checkBox.isChecked()): #选中
                self.INI_config.set('Action', 'declaraction', str("1"))
                self.INI_config.write(open("system/Server.ini", "w"))  #保存配置
                if int(self.form)==1:
                    self.close_form()
            else:
                self.INI_config.set('Action', 'declaraction', str("0"))
                self.INI_config.write(open("system/Server.ini", "w"))  #保存配置
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def close_form(self):  #关闭窗口
        try:
            #在这应该发送个信号回去让  这个属性页关闭
            self.form_close.emit()
            self.close()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))







