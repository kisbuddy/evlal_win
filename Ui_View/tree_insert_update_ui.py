#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#目录操作

from PyQt4 import uic
from PyQt4 import QtCore, QtGui ,QtNetwork
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from ctypes import *
from PyQt4.QtGui import *
from Clicked_Controller import log #日志记录
from Clicked_Controller import msg #
import sys
import os
import re
from Clicked_Controller import g #公共文件
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
class tree_insert_update_ui(QWidget):
    Data = pyqtSignal(str,str,str)
    def __init__(self):
        super(tree_insert_update_ui, self).__init__()
        try:
            uic.loadUi("ui/tree_insert_update.ui", self)
            self.setWindowIcon(QtGui.QIcon("system/main.ico"))
            flags = 0  #设置禁止最大化
            flags|= Qt.WindowMinimizeButtonHint  #设置禁止最大化
            self.setWindowFlags(flags)  #设置禁止最大化
            #禁止最大化按钮
            self.setWindowFlags(Qt.WindowMinimizeButtonHint)
            #禁止拉伸窗口大小
            self.setFixedSize(self.width(), self.height())

            self.ID=None  #ID编号
            self.ico_path=""  #ICO路径
            self.label_ICO.setScaledContents(True)#;为设置QLabel自动缩放，既：显示图像大


            self.pushButton.clicked.connect(self.add_Button)  #确定
            self.pushButton_clse.clicked.connect(self.closexx)  #取消
            self.pushButton_ICO.clicked.connect(self.open_ico) #引入ICO
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def re_select(self,data1,data2):   #查询是否包含
        try:
            p = re.compile( r'%s'%(str(data1)))
            sarr = p.findall(str(data2))
            #print sarr
            return len(sarr)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def open_ico(self): #引入ICO
        try:
            fileName1 = QFileDialog.getOpenFileName(self,
                                                              "Open ICO",
                                                    g.cur_file_dir()+"\ICO",
                                                              "ICO Files (*.ico)")   #设置文件扩展名过滤,注意用双分号间隔
            if not self.re_select(g.cur_file_dir().replace("\\","/"),str(fileName1)):
                msg.msg_box(u"操作提示",u"请本目录下ICO！")
                return
            name_file=g.cur_file_dir()   #当前程序路径
            fileName1=str(fileName1)[len(str(name_file))+1:]
            self.ico_path=str(fileName1)
            from os.path import isfile
            if isfile(self.ico_path):
                try:
                    # 你的代码
                    # path=QPixmap(r'%s'%(str(self.ico_path)))
                    # self.label_ICO.setPixmap(path)
                    # self.label_ICO.resize(path.width(),path.height())
                    self.label_ICO.setStyleSheet("background: transparent url(%s) no-repeat center center;"%(str(self.ico_path)))
                except BaseException, e:
                    pass
            #from os.path import isfile
            #if isfile(self.saveHistoryFilename):
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def set_data(self,**kwargs):
        try:
            if "title" in kwargs:  #标题
                self.setWindowTitle(u'%s'%(kwargs['title']))
            if "name" in kwargs:  #文件名
                self.textEdit.setText(u'%s'%(kwargs['name']))  #文件名
            if "ID" in kwargs:  #ID
                self.ID=str(kwargs['ID'])
            if "ico_path" in kwargs:  #ICO图标
                self.ico_path=str(kwargs['ico_path'])
                try:
                    # 你的代码
                    # path=QPixmap(r'%s'%(str(self.ico_path)))
                    # self.label_ICO.setPixmap(path)
                    # self.label_ICO.resize(path.width(),path.height())
                    self.label_ICO.setStyleSheet("background: transparent url(%s) no-repeat center center;"%(str(self.ico_path)))
                except BaseException, e:
                    pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def add_Button(self):  #确定
        try:
            data=unicode(QtCore.QString(self.textEdit.toPlainText()))
            self.Data.emit(data,str(self.ID),str(self.ico_path))  #获取文件名  并返回到主窗口
            self.close()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def closexx(self):  #取消
        try:
            self.close()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
