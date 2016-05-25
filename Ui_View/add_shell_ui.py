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
import base64
import ui  #UI变量
import json
import ConfigParser  #INI读取数据
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from Clicked_Controller import treeWidget_work #目录操作
from Clicked_Controller import msg #消息提示

#class add_shell_ui(QWidget):
class add_shell_ui(QDialog):
    insert = pyqtSignal(str,str,str,str,str,str,str)  #添加
    update = pyqtSignal(str,str,str,str,str,str,str,str)  #修改
    # siteurl #URL
    # sitepass  #密码
    # config   #配置
    # remarks  备注
    # type_id #类别
    # script  #脚本类型  asp   php
    # coding   #编码方式
    #def __init__(self):
    #    super(add_shell_ui, self).__init__()
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        try:
            uic.loadUi("ui/add_shell_ui.ui", self)
            self.setWindowIcon(QtGui.QIcon("system/main.ico"))
            flags = 0  #设置禁止最大化
            flags|= Qt.WindowMinimizeButtonHint  #设置禁止最大化
            self.setWindowFlags(flags)  #设置禁止最大化
            #禁止最大化按钮
            self.setWindowFlags(Qt.WindowMinimizeButtonHint)
            #禁止拉伸窗口大小
            self.setFixedSize(self.width(), self.height())
            self.insert_update=True   #0是True添加    1是False  修改
            self.id=""  #ID
            self.json_data={}
            self.list_data=[]
            self.INI_config = ConfigParser.ConfigParser()
            self.INI_config.readfp(open("system/Server.ini"))

            if(int(self.INI_config.get("add_shell", "pass_checkBox"))): #选中
                self.sitepass.setEchoMode(QLineEdit.Normal)
                self.pass_checkBox.setChecked(True)    #设置复选框为选择状态
            else:
                self.sitepass.setEchoMode(QLineEdit.Password)

            self.pushButton.clicked.connect(self.add_Button)  #确定
            self.siteurl.textChanged.connect(self.GetExt)  #输入URL地址
            self.pass_checkBox.clicked.connect(self.pass_click)  #密码显示
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def pass_click(self): #密码显示
        try:
            if(self.pass_checkBox.isChecked()): #选中
                self.sitepass.setEchoMode(QLineEdit.Normal)
                self.INI_config.set('add_shell', 'pass_checkBox', str("1"))
            else:
                self.sitepass.setEchoMode(QLineEdit.Password)
                self.INI_config.set('add_shell', 'pass_checkBox', str("0"))
            self.INI_config.write(open("system/Server.ini", "w"))  #保存配置
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def INI(self):  #INI配置信息
        try:
            checkbox_x = int(self.INI_config.get("add_shell", "checkbox"))
            if checkbox_x:
                self.checkBox.setChecked(True)    #设置复选框为选择状态
                type_id = int(self.INI_config.get("add_shell", "type_id"))
                self.type_id.setCurrentIndex(type_id)
                script = int(self.INI_config.get("add_shell", "script"))
                self.script.setCurrentIndex(script)
                coding = int(self.INI_config.get("add_shell", "coding"))
                self.coding.setCurrentIndex(coding)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def Box_click(self):  #选择保存配置信息
        try:
            if self.checkBox.isChecked(): #选择
                self.INI_config.set('add_shell', 'checkBox', '1')
                type_id = self.type_id.currentIndex()
                script = self.script.currentIndex()
                coding = self.coding.currentIndex()
                self.INI_config.set('add_shell', 'type_id', str(type_id))
                self.INI_config.set('add_shell', 'script', str(script))
                self.INI_config.set('add_shell', 'coding', str(coding))
            else:
                self.INI_config.set('add_shell', 'checkBox', '0')

            self.INI_config.write(open("system/Server.ini", "w"))  #保存配置
                #self.type_id.currentIndex()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def GetExt(self):
        try:
            #siteurl=self.siteurl.toPlainText()
            siteurl=unicode(QtCore.QString(self.siteurl.toPlainText())) #URL
            siteurl=siteurl.upper()
            if (".PHP" in str(siteurl)):
                self.script.setCurrentIndex(1)#php
            if (".ASP" in str(siteurl)):
                self.script.setCurrentIndex(2)#.ASP
            if ("ASPX" in str(siteurl)):
                self.script.setCurrentIndex(3)#ASPX
            else:
                self.script.setCurrentIndex(0)#脚本类型
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def set_data(self,**kwargs):  #远程参数
        try:
            if "title" in kwargs:  #标题
                self.setWindowTitle(u'%s'%(kwargs['title']))
            if "siteurl" in kwargs:  #URL
                self.insert_update=True   #0是True添加    1是False  修改
                self.siteurl.setText(u'%s'%(kwargs['siteurl']))
            if "sitepass" in kwargs:  #密码
                self.sitepass.setText(u'%s'%(kwargs['sitepass']))
            if "config" in kwargs:  #配置
                self.config.setText(u'%s'%(kwargs['config']))
            if "type_id" in kwargs:  #类别
                self.type_id.addItem(QtGui.QIcon('system/main.png'),_fromUtf8(str("站点类别")))
                #self.type_id.addItems(kwargs['type_id'])
                self.json_data=json.loads(kwargs['type_id'])
                for colour in self.json_data:
                    #print "xxxx",colour
                    self.type_ICO=treeWidget_work.sql_type_ICO(str(colour))
                    self.type_id.addItem(QtGui.QIcon(str(self.type_ICO)),_fromUtf8(str(self.json_data.get(str(colour)))))
                    self.list_data.append(colour)
            # list_script=["PHP(Eval)","ASP(Eval)","ASPX(Eval)","Customize"]
            # list_coding=["UTF-8","GB2312","BIG5","Euc-KR","Euc-JP","Shift_JIS","Windows-1251","Windows-874","ISO-8859-1"]
            # if "script" in kwargs:  #脚本类型  asp   php
            #     self.script.addItem(QtGui.QIcon('ico/time.ico'),_fromUtf8(str("脚本类型")))
            #     self.script.addItems(kwargs['script'])
            # if "coding" in kwargs:  #编码方式
            #     self.coding.addItem(QtGui.QIcon('ico/coding.ico'),_fromUtf8(str("字符编码")))
            #     self.coding.addItems(kwargs['coding'])
            #脚本类型  asp   php
            self.script.addItem(QtGui.QIcon('system/script.ico'),_fromUtf8(str("脚本类型")))
            self.script.addItem(QtGui.QIcon('system/php.ico'),_fromUtf8(str("PHP(Eval)")))
            self.script.addItem(QtGui.QIcon('system/asp.ico'),_fromUtf8(str("ASP(Eval)")))
            self.script.addItem(QtGui.QIcon('system/aspx.ico'),_fromUtf8(str("ASPX(Eval)")))
            self.script.addItem(_fromUtf8(str("Customize")))
            #self.script.setCurrentIndex(0)
            #编码方式
            self.coding.addItem(QtGui.QIcon('system/coding.ico'),_fromUtf8(str("字符编码")))
            self.coding.addItem(_fromUtf8(str("UTF-8")))
            self.coding.addItem(_fromUtf8(str("GB2312")))
            self.coding.addItem(_fromUtf8(str("BIG5")))
            self.coding.addItem(_fromUtf8(str("Euc-KR")))
            self.coding.addItem(_fromUtf8(str("Euc-JP")))
            self.coding.addItem(_fromUtf8(str("Shift_JIS")))
            self.coding.addItem(_fromUtf8(str("Windows-1251")))
            self.coding.addItem(_fromUtf8(str("Windows-874")))
            self.coding.addItem(_fromUtf8(str("ISO-8859-1")))
            #self.coding.setCurrentIndex(0)
            #修改传入
            int_ini=1
            if "id_key" in kwargs:  #id
                self.id= u'%s'%(kwargs['id_key'])
                self.pushButton.setText(u'修改数据')
                int_ini=0
            else:
                self.pushButton.setText(u'添加数据')
                int_ini=1
            if "type_id_key" in kwargs:  #类别
                self.insert_update=False   #0是True添加    1是False  修改
                x= self.list_data.index(u'%s'%(kwargs['type_id_key']))
                # if self.type_id.currentIndex()>=int(x): #返回Item数目
                #     print self.type_id.currentIndex(),"bbbbb",x
                try:
                    self.type_id.setCurrentIndex(int(x)+1)
                except BaseException, e:
                    pass
            try: #没有选择分组时选择默认分组
                if self.type_id.currentIndex()==0:
                    self.type_id.setCurrentIndex(int(1))
            except BaseException, e:
                pass
            try: #没有选择编码时 选择默认编码
                if self.coding.currentIndex()==0:
                    self.coding.setCurrentIndex(int(1))
            except BaseException, e:
                pass
            if "sitepass_key" in kwargs:  #密码
                self.sitepass.setText(u'%s'%(kwargs['sitepass_key']))
            if "config_key" in kwargs:  #配置
                self.config.setText(u'%s'%(kwargs['config_key']))
            if "coding_key" in kwargs:  #编码方式
                self.insert_update=False   #0是True添加    1是False  修改
                coding="0"
                if int(kwargs['coding_key'])==65001:#"UTF-8":
                    coding="1"
                elif int(kwargs['coding_key'])==936:#"GB2312":
                    coding="2"
                elif int(kwargs['coding_key'])==950:#"BIG5":
                    coding="3"
                elif int(kwargs['coding_key'])==949:#"Euc-KR":
                    coding="4"
                elif int(kwargs['coding_key'])==20932:#"Euc-JP":
                    coding="5"
                elif int(kwargs['coding_key'])==932:#"Shift_JIS":
                    coding="6"
                elif int(kwargs['coding_key'])==1251:#"Windows-1251":
                    coding="7"
                elif int(kwargs['coding_key'])==874:#"Windows-874":
                    coding="8"
                elif int(kwargs['coding_key'])==1252:#"ISO-8859-1":
                    coding="9"
                self.coding.setCurrentIndex(int(coding))
            if "script_key" in kwargs:  #脚本类型  asp   php
                self.insert_update=False   #0是True添加    1是False  修改
                self.script.setCurrentIndex(int(kwargs['script_key']))
            if "remarks_key" in kwargs:  #备注
                self.remarks.setText(u'%s'%(kwargs['remarks_key']))

            if int_ini:
                self.INI()  #加载配置信息
            else:
                self.checkBox.setEnabled(0)  #给改成禁用
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def add_Button(self):
        try:
            if self.type_id.currentIndex()==0 or \
               self.script.currentIndex()==0 or \
               self.coding.currentIndex()==0:
               msg.msg_box(u"操作提示",u"请注意选择 脚本类型 和 字符编码！")
            else:
                siteurl=unicode(QtCore.QString(self.siteurl.toPlainText())) #URL
                sitepass=unicode(QtCore.QString(self.sitepass.text()))  #密码
                config=unicode(QtCore.QString(self.config.toPlainText()))   #配置
                #remarks=unicode(QtCore.QString(self.remarks.toPlainText().toLocal8Bit()))   #在备注
                remarks=unicode(self.remarks.toPlainText())   #在备
                #type_id=unicode(QtCore.QString(self.type_id.currentText())) #类别
                type_id_id=self.type_id.currentIndex()
                #print type_id_id
                type_id=self.list_data[type_id_id-1]
                #print self.json_data.has_key(str(type_id_id))
                #script=unicode(QtCore.QString(self.script.currentText()))  #脚本类型  asp   php
                #script=self.script.currentIndex()  #脚本类型  asp   php
                script=self.script.currentText()
                if str(script)=="PHP(Eval)":
                    script="1"
                elif str(script)=="ASP(Eval)":
                    script="2"
                elif str(script)=="ASPX(Eval)":
                    script="3"
                elif str(script)=="Customize":
                    script="4"
                #coding=unicode(QtCore.QString(self.coding.currentText()))   #编码方式
                #coding=self.coding.currentIndex()  #编码方式
                coding=self.coding.currentText()
                if str(coding)=="UTF-8":
                    coding="65001"
                elif str(coding)=="GB2312":
                    coding="936"
                elif str(coding)=="BIG5":
                    coding="950"
                elif str(coding)=="Euc-KR":
                    coding="949"
                elif str(coding)=="Euc-JP":
                    coding="20932"
                elif str(coding)=="Shift_JIS":
                    coding="932"
                elif str(coding)=="Windows-1251":
                    coding="1251"
                elif str(coding)=="Windows-874":
                    coding="874"
                elif str(coding)=="ISO-8859-1":
                    coding="1252"

                self.Box_click()  #选择保存配置信息
                if self.insert_update:   #0是True添加    1是False  修改
                    self.insert.emit(str(siteurl),str(sitepass),str(config),remarks,str(type_id),str(script),str(coding))  #添加获取文件名  并返回到主窗口
                else:
                    self.update.emit(str(self.id),str(siteurl),str(sitepass),str(config),remarks,str(type_id),str(script),str(coding))  #
                self.close()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


