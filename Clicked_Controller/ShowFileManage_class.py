#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
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

from Ui_View.ui import tabWidget_close_lock #线程锁
from Ui_View import ui #UI窗口
from Ui_View import Edit_file_ui #文件编辑

from Db_Model import db_shell #常用数据库操作

from Clicked_Controller import link_shell  #链接SHELL等操作
from Clicked_Controller import eval_link  #链接SHELL
from Clicked_Controller import g #公共文件
from Clicked_Controller import log #日志记录

import msg #消息提示
import treeWidget_work #目录操作

import threadpool
import time
import os
import base64
import binascii
import re
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

class   ShowFileManage_class(object):
    def __init__(self,ShowFile_ui,id):
        try:
            self.main_ui=ui.UIManager.get_ui('main_ui') #主程序UI
            self.shell_sql=ui.UIManager.shell_sql
            self.ShowFile_ui=ShowFile_ui #UI窗体
            self.id_shell_list=db_shell.id_sitetable_shell('%s'%(str(id)))  #通过ID查询SHELL的状态
            self.id_shell_list=db_shell.id_sitetable_shell('%s'%(str(id)))  #通过ID查询SHELL的状态
            self.id=str(self.id_shell_list[0])         #自动编号
            #self.type_id=str(self.id_shell_list[1])    #      类别
            self.siteurl=str(self.id_shell_list[2])    #    网址
            self.sitepass=str(self.id_shell_list[3])   #    密码
            #self.link=str(self.id_shell_list[4])         #链接状态
            #self.ip=str(self.id_shell_list[5])         #    ip地址
            #self.config=str(self.id_shell_list[6])     #    配置
            #self.coding=str(self.id_shell_list[7])     #  编码方式
            self.script=str(self.id_shell_list[8])      #   asp   php
            self.ley_operate=""   #操作方法  重命名  修改文件时间  创建文件夹
            self.ley_operate_name=""   #保存原先内容
            self.Copy_file_name=""  #复制路径
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def link_shell_file_Thread(self,Info): #链接SHELL显示文件
        try:
            #self.look_file_Thread(get_name=str(get_name),x="0")  #刷新上传内容
            self.work = Worker_Thread(name="uix1",var1=str(Info))
            self.work.Finish1.connect(self.link_shell_file)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def if_os(self,Info):  #判断操作系统
        #C:/Program Files (x86)/EasyPHP-5.3.6.0/www	C:D:E:F:G:H:I:J:	Windows NT PC-20140121PDVI 6.1 build 7601 (Unknow Windows version Ultimate Edition Service Pack 1) i586(Administrator)
        try:
            OS_data=g.if_os(Info)
            if OS_data=="":  #操作系统
                #空
                sql_data="update sitetable set os='%s' where ID='%s'"%(str("except"),str(self.id))
            else:
                #判断到操作系统
                sql_data="update sitetable set os='%s' where ID='%s'"%(str(OS_data),str(self.id))
            if self.shell_sql.mysqlite3_update(sql_data):
                pass
            #msg.msg_lower_right(u"修改目录:%s 成功"%(str(name)))  #右下角提示
            else:
                pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def link_shell_file(self,Info): #链接SHELL显示文件
        try:
            Rpath = Info.split('\t')  #分割返回的信息
            self.if_os(Info)  #判断操作系统
            path=_fromUtf8(str(Rpath[0])) # .replace("/","\\")+"\\"
            path=g.GetExt(str(path))#输入路径地址  转换路径
            self.ShowFile_ui.ComPath.setEditText(_fromUtf8(str(g.GetExt(path))))  #添加目录
            self.ShowFile_ui.ComPath.addItem(_fromUtf8(str(g.GetExt(path))))#添加到下拉列表
            #Disk = Rpath[1].split(':')
            #Disk="/www/web/www_qtgj/public_html/plus/"
            #显示磁盘
            if path[0:1]=="/" or path[0:1]=="\\":#判断是不是linux
                #self.add_top_item("/","system/file_disk.ico")  #添加目录#将磁盘信息加入Treewidget
                self.GetBaseInfo(path,"")#得到字符串后显示基本信息  添加目录
            else:
                #print path,str(Rpath[1])
                self.GetBaseInfo(path,str(Rpath[1]))#得到字符串后显示基本信息  添加目录
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def thread_Upload_files(self,Upload_files): #线程上传文件
        try:
            tree_i = treeWidget_work.add_top_item(u'上传文件','system/Upload_files.ico')
            tree_i.setExpanded(True)
            for colour in Upload_files:
                list_data=colour.split("|") #0上传文件路径 1本地路径
                #print list_data
                if self.script=="PHP":
                    psot_data=link_shell.GetPostText(self.script,"Upload_files")    #上传文件
                    psot_data="%s&z1=%s&z2=%s"% \
                         (link_shell.post_php_data(psot_data),base64.b64encode(list_data[0]),urllib.quote(ui.open_file_hex(list_data[1])))
                if self.script=="ASP":
                    psot_data=link_shell.GetPostText(self.script,"Upload_files")    #上传文件
                    psot_data="%s&z1=%s&z2=%s&z3=0"% \
                         (psot_data,binascii.b2a_hex(list_data[0]),binascii.b2a_hex(ui.open_file(list_data[1])))
                if self.script=="ASPX":
                    psot_data=link_shell.GetPostText(self.script,"Upload_files")    #上传文件
                    psot_data="%s&z1=%s&z2=%s"% \
                         (psot_data,urllib.quote(base64.b64encode(str(list_data[0]).replace('\\', '\\\\'))),urllib.quote(ui.open_file_hex(list_data[1])))
                FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                if not FALSE_bool==0:
                    if ResInfo=="1":
                        treeWidget_work.add_child_item1(tree_i, str(list_data[2]),'system/link_1.ico')  #添加数据
                        #print u"%s上传成功！！"%(str(list_data[2]))
                    else:
                        #msg.msg_lower_Left(u"%s上传文件错误"%(str(list_data[0])))#设置状态栏文字信息
                        treeWidget_work.add_child_item1(tree_i, str(list_data[2]),'system/link_0.ico')  #添加数据
                else:
                    msg.msg_lower_Left(u"%s上传文件错误"%(str(list_data[0])))#设置状态栏文字信息

            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            #self.link_file_tableWidget(str( get_name+"\\"),"0")  #刷新上传内容
            self.look_file_Thread(get_name=str( get_name+"\\"),x="0")  #刷新上传内容
            time.sleep(10)
            treeWidget_work.del_take_Top(1)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            #msg.msg_lower_Left(u"thread_Upload_files except %s"%(str(e)))#设置状态栏文字信息
            #print("thread_Upload_files except",str(e))

    def open_file_Thread(self,row,column):   #双击  文件
        try:
            self.work = Worker_Thread(name="uix2",var1=str(row),var2=str(column))
            self.work.Finish2.connect(self.open_file)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def open_file(self,row,column):   #双击  文件
        try:
            #[u'name',u'名称',u'时间',u'大小',u'属性'])
            name1=self.ShowFile_ui.file_tableWidget.item(int(row),0).text()  #获取某一格内容
            file_size=self.ShowFile_ui.file_tableWidget.item(int(row),3).text()  #获取某一格内容
            Pos=str(name1).find("/")
            if not(Pos==-1):#文件夹
                get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
                #name=get_name+str(name1).replace("/", "\\")  #当前路径
                name=get_name+g.GetExt(str(name1))#输入路径地址  转换路径
                #path=g.GetExt(str(path))#输入路径地址  转换路径
                self.ShowFile_ui.ComPath.setEditText(_fromUtf8(str(name)))
                #self.link_file_tableWidget(name,"1")#双击文件
                self.look_file_Thread(get_name=str(name),x="1")  #刷新上传内容
            else:
                #文件
                get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
                name=get_name+str(name1)
                if int(file_size)<=100000:
                    #文件
                    #name=name[name.rfind("."):len(name)]#从尾部查找字符串
                    #print name
                    if self.script=="PHP":
                        psot_data=link_shell.GetPostText(self.script,"Open_file")    #
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
                        msg.msg_lower_Left(u"%s读取文件完成"%(str(name)))#设置状态栏文字信息
                        Edit_file_ui.Edit_file(ID=self.id,data=ResInfo,name=name)  #编辑这个文件
                    else:
                        msg.msg_lower_Left(u"%s读取文件错误"%(str(name)))#设置状态栏文字信息
                else:
                    #下载文件
                    if self.script=="PHP":
                        psot_data=link_shell.GetPostText(self.script,"Download_File")    #上传文件
                        psot_data="%s&z1=%s"% \
                             (link_shell.post_php_data(psot_data),base64.b64encode(str(name)))
                    if self.script=="ASP":
                        #BUG这个存在文件比如下载RAR大文件时候   无法正确下载  找不到为什么
                        psot_data=link_shell.GetPostText(self.script,"Download_File")    #下载文件
                        psot_data="%s&z1=%s"% \
                                  (psot_data,urllib.quote(str(name)))
                    if self.script=="ASPX":
                        #BUG这个存在文件比如下载RAR大文件时候   无法正确下载  找不到为什么
                        psot_data=link_shell.GetPostText(self.script,"Download_File")    #下载文件
                        psot_data="%s&z1=%s"% \
                                  (psot_data,urllib.quote(str(name)))
                    FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                    if not FALSE_bool==0:
                        self.window = QtGui.QMainWindow()
                        fileName2 = QtGui.QFileDialog.getSaveFileName(self.window,
                                                                u"文件保存",
                                                                u"%s\\%s"%(g.cur_file_dir(),str(name)))
                        #"All Files (*);;Text Files (*.txt)")
                        if fileName2:
                            file_object = open(fileName2, 'wb')
                            file_object.writelines(ResInfo)
                            file_object.close()
                            #print fileName2
                            #print ResInfo
                            msg.msg_lower_Left(u"%s保存文件完成"%(str(name)))#设置状态栏文字信息
                    else:
                        msg.msg_lower_Left(u"%s读取文件错误"%(str(name)))#设置状态栏文字信息
                        #pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def look_file_Thread(self,**kwargs):    #读取文件
        try:
            if "get_name" in kwargs:  #
                get_name=(kwargs['get_name'])
            else:
                get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            if "x" in kwargs:  #
                x=(kwargs['x'])
            else:
                x="0"
            #self.look_file_Thread(get_name=str(get_name),x="0")  #刷新上传内容
            self.work = Worker_Thread(name="uix2",var1=str(get_name),var2=str(x))
            self.work.Finish2.connect(self.link_file_tableWidget)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def link_file_tableWidget(self,AllPath,form_tree="1"):  #双击文件
        try:
            item = QTreeWidgetItem(self.ShowFile_ui.file_treeWidget)#设置根
            #读取目录
            AllPath=g.GetExt(AllPath)
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"FileManage")    #通过目录获取文件列表信息获取代码
                psot_data=link_shell.post_php_data(psot_data)+"&z1="+base64.b64encode(str(AllPath))  #转换代码
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"FileManage")    #获取代码
                psot_data=psot_data+"&z1="+binascii.b2a_hex(str(AllPath))  #转换代码
            if self.script=="ASPX":
                psot_data=link_shell.GetPostText(self.script,"FileManage")    #获取代码
                psot_data="%s&z1=%s"%(psot_data,urllib.quote(base64.b64encode(str(AllPath).replace('\\', '\\\\'))))
            FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            if FALSE_bool==0:
                msg.msg_lower_Left(u"%s读取错误"%(AllPath))#设置状态栏文字信息
                return 0
            self.ShowFile_ui.file_tableWidget.clearContents()  #清空
            if str(ResInfo)=="":
                msg.msg_lower_Left(u"%s读取错误 返回为空"%(AllPath))#设置状态栏文字信息
                return 0
            Linestr=ResInfo.split('\n')#以换行符分割返回结果
            self.ShowFile_ui.file_tableWidget.setRowCount(0)#设置表的列数
            if not(item.childCount()==0):#判断当前节点有没有子节点
                for p in range(0, item.childCount()):
                    item.removeChild(item.child(0))#删掉所有子节点
            i=0
            self.ShowFile_ui.ComPath.setEditText(_fromUtf8(str(g.GetExt(AllPath))))  #添加目录
            self.ShowFile_ui.ComPath.addItem(_fromUtf8(str(g.GetExt(AllPath))))  #添加到下拉列表

            for k in range(0, len(Linestr)):
                Pose=str(Linestr[k]).upper().find("ERROR")  #.decode('utf-8')
                if Pose==-1:#错误信息
                    Folder=str(Linestr[k]).split('\t')#制表键分割
                    if len(Folder)!=4:  #空数据
                        continue   #跳过
                    Pos=str(Folder[0]).find("/")
                    #//名称 时间  大小  属性
                    if not(Pos==-1):#文件夹
                        if not ((link_shell.re_find(str(Folder[0]),"\./")) or (link_shell.re_find(str(Folder[0]),"\.\./"))):
                            self.ShowFile_ui.file_tableWidget.setRowCount(self.ShowFile_ui.file_tableWidget.rowCount()+1)
                            file_ICO='system/file_ico/file_file.ico'
                            color=QColor(0, 0, 0)   #黑色1链接成功
                            self.tableWidget_add(0,i,title=_fromUtf8(str(Folder[0])),color=color)
                            self.tableWidget_add(1,i,title=_fromUtf8(str(Folder[0])[0:len(str(Folder[0]))-1]),color=color,ico=file_ICO)  #名称
                            self.tableWidget_add(2,i,title=Folder[1],color=color)  #时间
                            self.tableWidget_add(3,i,title=Folder[2],color=color)  #大小
                            file_root=g.file_root(str(Folder[3])) #根据属性判断文件权限
                            self.tableWidget_add(4,i,title=file_root,color=color)  #属性
                            if int(form_tree):
                                #加载目录
                                icon = QIcon()
                                icon.addPixmap(QPixmap(_fromUtf8("system/file_close.ico")), QIcon.Normal, QIcon.Off)
                                icon.addPixmap(QPixmap(_fromUtf8("system/file_open.ico")), QIcon.Normal, QIcon.On)
                                Root = QTreeWidgetItem(item)#设置根
                                Root.setExpanded(True)#展开站点类别
                                Root.setText(0,_fromUtf8(str(Folder[0]).replace("/", "")))#载入类别
                                Root.setIcon(0, icon)
                            i=i+1
                    else:#文件
                        self.ShowFile_ui.file_tableWidget.setRowCount(self.ShowFile_ui.file_tableWidget.rowCount()+1)
                        color=QColor(0, 0, 0)   #黑色1链接成功
                        file_ICO=self.if_file_ico(str(Folder[0]))  #根据文件后缀获取ICO
                        self.tableWidget_add(0,i,title=_fromUtf8(str(Folder[0])),color=color)
                        self.tableWidget_add(1,i,title=_fromUtf8(str(Folder[0])),color=color,ico=file_ICO)  #名称
                        self.tableWidget_add(2,i,title=Folder[1],color=color)  #时间
                        self.tableWidget_add(3,i,title=Folder[2],color=color)  #大小
                        file_root=g.file_root(str(Folder[3])) #根据属性判断文件权限
                        self.tableWidget_add(4,i,title=file_root,color=color)  #属性
                        i=i+1
                    msg.msg_lower_Left(u"%s读取完成"%(AllPath))#设置状态栏文字信息
                else:
                    msg.msg_lower_Left(u"%s读取错误 %s"%(AllPath,str(ResInfo)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    #########################################################

    def GetTreeRoot(self,item):#获得点击Item的绝对路径
        try:
            item.setExpanded(True)#展开点击节点
            Text=""
            Text=item.text(0)+"\\"+Text
            itemp=item.parent()
            while not(itemp==None):
                Text=itemp.text(0)+"\\"+Text
                itemp=itemp.parent()
            self.ShowFile_ui.ComPath.setEditText(str(g.GetExt(_fromUtf8(str(g.GetExt(Text))))))  #设置当前内容
            self.ShowFile_ui.ComPath.addItem(str(g.GetExt(_fromUtf8(str(g.GetExt(Text))))))  #添加到下拉列表
            AllPath=str(g.GetExt(Text))#.replace("\\", "\\")
            msg.msg_lower_Left(u"%s请稍等正在拼命加载中............"%(AllPath))#设置状态栏文字信息
            #读取目录
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"FileManage")    #通过目录获取文件列表信息获取代码
                psot_data=link_shell.post_php_data(psot_data)+"&z1="+base64.b64encode(str(AllPath))  #转换代码
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"FileManage")    #获取代码
                psot_data=psot_data+"&z1="+binascii.b2a_hex(str(AllPath))  #转换代码
            if self.script=="ASPX":
                psot_data=link_shell.GetPostText(self.script,"FileManage")    #获取代码
                psot_data="%s&z1=%s"%(psot_data,urllib.quote(base64.b64encode(str(AllPath).replace('\\', '\\\\'))))
            FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            if FALSE_bool==0:
                msg.msg_lower_Left(u"%s读取错误"%(AllPath))#设置状态栏文字信息
                return 0
            self.ShowFile_ui.file_tableWidget.clearContents()  #清空
            if str(ResInfo)=="":
                msg.msg_lower_Left(u"%s读取错误 返回为空"%(AllPath))#设置状态栏文字信息
                return 0

            #print ResInfo
            self.tableWidget_file_add(ResInfo,AllPath,item) #添加目录
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def tableWidget_file_add(self,ResInfo,AllPath,item): #添加目录
        try:
            Linestr=ResInfo.split('\n')#以换行符分割返回结果
            self.ShowFile_ui.file_tableWidget.setRowCount(0)#设置表的列数
            if not(item.childCount()==0):#判断当前节点有没有子节点
                for p in range(0, item.childCount()):
                    item.removeChild(item.child(0))#删掉所有子节点
            i=0
            for k in range(0, len(Linestr)):
                Pose=str(Linestr[k]).upper().find("ERROR")  #.decode('utf-8')
                if Pose==-1:#错误信息
                    Folder=str(Linestr[k]).split('\t')#制表键分割
                    if len(Folder)!=4:  #空数据
                        continue   #跳过
                    Pos=str(Folder[0]).find("/")
                    #//名称 时间  大小  属性
                    if not(Pos==-1):#文件夹
                        if not ((link_shell.re_find(str(Folder[0]),"\./")) or (link_shell.re_find(str(Folder[0]),"\.\./"))):
                            self.ShowFile_ui.file_tableWidget.setRowCount(self.ShowFile_ui.file_tableWidget.rowCount()+1)
                            file_ICO='system/file_ico/file_file.ico'
                            color=QColor(0, 0, 0)   #黑色1链接成功
                            self.tableWidget_add(0,i,title=_fromUtf8(str(Folder[0])),color=color)
                            self.tableWidget_add(1,i,title=_fromUtf8(str(Folder[0])[0:len(str(Folder[0]))-1]),color=color,ico=file_ICO)  #名称
                            self.tableWidget_add(2,i,title=Folder[1],color=color)  #时间
                            self.tableWidget_add(3,i,title=Folder[2],color=color)  #大小
                            file_root=g.file_root(str(Folder[3])) #根据属性判断文件权限
                            self.tableWidget_add(4,i,title=file_root,color=color)  #属性
                            #加载目录
                            icon = QIcon()
                            icon.addPixmap(QPixmap(_fromUtf8("system/file_close.ico")), QIcon.Normal, QIcon.Off)
                            icon.addPixmap(QPixmap(_fromUtf8("system/file_open.ico")), QIcon.Normal, QIcon.On)
                            Root = QTreeWidgetItem(item)#设置根
                            Root.setExpanded(True)#展开站点类别
                            Root.setText(0,_fromUtf8(str(Folder[0]).replace("/", "")))#载入类别
                            Root.setIcon(0, icon)
                            i=i+1
                    else:#文件
                        self.ShowFile_ui.file_tableWidget.setRowCount(self.ShowFile_ui.file_tableWidget.rowCount()+1)
                        color=QColor(0, 0, 0)   #黑色1链接成功
                        file_ICO=self.if_file_ico(str(Folder[0]))  #根据文件后缀获取ICO
                        self.tableWidget_add(0,i,title=_fromUtf8(str(Folder[0])),color=color)
                        self.tableWidget_add(1,i,title=_fromUtf8(str(Folder[0])),color=color,ico=file_ICO)  #名称
                        self.tableWidget_add(2,i,title=Folder[1],color=color)  #时间
                        self.tableWidget_add(3,i,title=Folder[2],color=color)  #大小
                        file_root=g.file_root(str(Folder[3])) #根据属性判断文件权限
                        self.tableWidget_add(4,i,title=file_root,color=color)  #属性
                        i=i+1
                    msg.msg_lower_Left(u"%s读取完成"%(AllPath))#设置状态栏文字信息
                else:
                    msg.msg_lower_Left(u"%s读取错误 %s"%(AllPath,str(ResInfo)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def if_file_ico(self,DATA):  #根据文件类型查找ICO图标
        try:
            DATA=DATA.capitalize()  #转换成小写
            name=DATA[DATA.rfind(".")+1:]#从尾部查找字符串
            name="system/file_ico/%s.ico"%(name)
            if os.path.exists(name):  #判断文件是否存在
                return name
            else:
                return "system/file_ico/except.ico"
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            return "system/file_ico/except.ico"

    #添加数据
    def tableWidget_add(self,x, y,**kwargs):
        #self.file_tableWidget.setRowCount(self.file_tableWidget.rowCount()+1)  #行  len(node)  #加一行
        try:
            item = QTableWidgetItem()
            try:
                if "ico" in kwargs:  #ICO 图标
                    item.setIcon(QtGui.QIcon(u'%s'%(kwargs['ico'])))
                if "color" in kwargs:  #颜色
                    item.setTextColor(kwargs['color']) #字体变色
                if(("title" in kwargs) and (not self.GetData(kwargs['title'])=='')):  #内容
                    item.setText(u'%s'%(kwargs['title']))
                if not(x==0 or x==1):
                    item.setTextAlignment(Qt.AlignCenter)#设置字体居中
            except BaseException, e:
                log.logging.debug("except:%s"%(str(e)))
            self.ShowFile_ui.file_tableWidget.setItem(y, x, item)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def GetData(self,Data):#该函数用于防止数据为空时显示None
        try:
            EndData=_fromUtf8(str(Data))
            if EndData=="None":
                EndData=""
            return (EndData)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def GetBaseInfo(self,path,disks):#得到字符串后显示基本信息  添加目录
        try:
            Rpath = str(disks)#磁盘符号
            Root = str(path).replace("/","\\")
            #Root = str(path).replace("/","\\")#路径replace("\\","/")
            if Root[0:1]=="/" or Root[0:1]=="\\":#判断是不是linux
                Roott = QTreeWidgetItem(self.ShowFile_ui.file_treeWidget)#设置根
                icon10 = QIcon()
                #icon10.addPixmap(QPixmap(_fromUtf8("system/file_disk_linux.ico")), QIcon.Normal, QIcon.On)
                Roott.setIcon(0, icon10)
                Roott.setText(0, _fromUtf8("\\"))
                Path=Root.split('\\')#返回每一级路径
                Roott.setExpanded(True)#展开站点类别
                Items = QTreeWidgetItem(Roott)#设置子类
                for k in range(1, len(Path)):
                    if len(Path[k])==0:
                        continue  #跳过   这一次
                    Items.setText(0,str(Path[k]))#载入类别
                    icon10.addPixmap(QPixmap(_fromUtf8("system/file_close.ico")), QIcon.Normal, QIcon.Off)
                    icon10.addPixmap(QPixmap(_fromUtf8("system/file_open.ico")), QIcon.Normal, QIcon.On)
                    Items.setIcon(0, icon10)
                    Items.setExpanded(True)#展开站点类别
                    if not(k==len(Path)-2):
                        Items = QTreeWidgetItem(Items)#设置子类
                    else:
                        Items.setSelected(True)#设置最后一个节点选中
                        self.GetTreeRoot(Items)#获得wwwroot文件信息
            else:  #win
                Disk = Rpath.split(':')
                for k in range(0, len(Disk)-1):
                    Roott = QTreeWidgetItem(self.ShowFile_ui.file_treeWidget)#设置根
                    icon10 = QIcon()
                    icon10.addPixmap(QPixmap(_fromUtf8("system/file_disk_close.ico")), QIcon.Normal, QIcon.Off)
                    icon10.addPixmap(QPixmap(_fromUtf8("system/file_disk_open.ico")), QIcon.Normal, QIcon.On)
                    if Disk[k]:
                        Roott.setText(0,str(Disk[k])+":")#载入类别
                        Roott.setIcon(0, icon10)
                        Roott.setExpanded(True)#展开根
                for n in range(0, self.ShowFile_ui.file_treeWidget.topLevelItemCount()): #self.ShowFile_ui.file_treeWidget.topLevelItemCount()-1
                    Path=Root.split('\\')#返回每一级路径
                    if str(self.ShowFile_ui.file_treeWidget.topLevelItem(n).text(0))==str(Path[0]).upper():#str(Path[0]).upper() 转换成大写
                        Items = QTreeWidgetItem(self.ShowFile_ui.file_treeWidget.topLevelItem(n))#跟踪根路径
                        #self.ShowFile_ui.file_treeWidget.topLevelItem(n).setExpanded(True)#展开站点类别
                        for k in range(1, len(Path)):
                            if len(Path[k])==0:
                                continue  #跳过   这一次
                            Items.setText(0,str(Path[k]))#载入类别
                            icon10.addPixmap(QPixmap(_fromUtf8("system/file_close.ico")), QIcon.Normal, QIcon.Off)
                            icon10.addPixmap(QPixmap(_fromUtf8("system/file_open.ico")), QIcon.Normal, QIcon.On)
                            Items.setIcon(0, icon10)
                            Items.setExpanded(True)#展开站点类别
                            if not(k==len(Path)-2):
                                Items = QTreeWidgetItem(Items)#设置子类
                            else:
                                Items.setSelected(True)#设置最后一个节点选中
                                self.GetTreeRoot(Items)#获得wwwroot文件信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def add_top_item(self,title,ico):  #添加目录
        try:
            item = QTreeWidgetItem(self.ShowFile_ui.file_treeWidget)
            item.setText(0, title)
            try:  # 你的代码
                item.setIcon(0,QtGui.QIcon(str(ico)))
            except BaseException, e:
                log.logging.debug("except:%s"%(str(e)))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    ########################################################
    def tab_close_Thread(self):  #关闭属性页
        try:
            t_h_Thread = threadpool.ThreadPool(1)   #创建多线程  线程池
            t_h_Thread.push(self.form_close,"close")
            t_h_Thread.wait_for_idel(1)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def form_close(self,data): #关闭窗体
        try:
            global tabWidget_close_lock
            i=0
            while True:
                try:
                    i = i+1
                    if i>=5:
                        break #跳出
                    if tabWidget_close_lock.acquire():
                        #tabWidget_close_lock.acquire() #创建锁
                        #tabWidget_close_lock.allocate()  #创建锁
                        id=self.main_ui.tabWidget.count()-1
                        if int(id)>=1:
                            self.main_ui.tabWidget.removeTab(id)
                        tabWidget_close_lock.release()  #释放锁
                        break #跳出
                except BaseException, e:
                    tabWidget_close_lock.release()  #释放锁
                    break #跳出
                finally:  #不管错误不错误都会执行
                    time.sleep(0.1)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    ########################################################
    def file_Refresh_shell(self):  #刷新当前目录
        try:
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            #self.link_file_tableWidget(str( get_name+"\\"),"0")  #刷新上传内容
            self.look_file_Thread(get_name=str(get_name+"\\"),x="0")  #刷新上传内容
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_Upload_shell(self):  #上传文件
        try:
            self.window = QtGui.QMainWindow()
            files = QtGui.QFileDialog.getOpenFileNames(self.window,
                                                           u"选取文件"
                                                            #g.cur_file_dir()
                                                            u"%s\\"%(g.cur_file_dir())
                                                            )   #"All Files (*);"设置文件扩展名过滤,注意用双分号间隔
            if len(files):
                self.Upload_files=[] #上传文件
                for i in range(0, len(files)):
                    #url=files[i]
                    file=str(files[i]).decode('UTF-8').encode('GBK').replace("/", "\\")
                    name=file[file.rfind("\\")+1:]#从尾部查找字符串
                    if name.rfind("."):  #判断是否是文件
                        file="%s%s|%s|%s"%(str(self.ShowFile_ui.ComPath.currentText()),str(name),str(file),str(name))  #获取当前内容
                        self.Upload_files.append(file)  #添加数据
                if len(self.Upload_files):
                    t_h_Thread = threadpool.ThreadPool(1)   #创建多线程  线程池
                    t_h_Thread.push(self.thread_Upload_files,self.Upload_files) #"Upload_files"
                    t_h_Thread.wait_for_idel(1)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_Download_shell_Thread(self):  #下载文件
        try:
            self.work = Worker_Thread(name="uix0")
            self.work.Finish.connect(self.file_Download_shell)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_Download_shell(self):  #下载文件
        try:
            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            name1=self.ShowFile_ui.file_tableWidget.item(int(ranges),1).text()  #获取某一格内容
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            name=get_name+str(name1)
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"Download_File")    #下载文件
                psot_data="%s&z1=%s"% \
                          (link_shell.post_php_data(psot_data),base64.b64encode(str(name)))
            if self.script=="ASP":
                #BUG这个存在文件比如下载RAR大文件时候   无法正确下载  找不到为什么
                psot_data=link_shell.GetPostText(self.script,"Download_File")    #下载文件
                psot_data="%s&z1=%s"% \
                          (psot_data,urllib.quote(str(name)))
            if self.script=="ASPX":
                #BUG这个存在文件比如下载RAR大文件时候   无法正确下载  找不到为什么
                psot_data=link_shell.GetPostText(self.script,"Download_File")    #下载文件
                psot_data="%s&z1=%s"% \
                          (psot_data,urllib.quote(str(name)))
            FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            if not FALSE_bool==0:
                self.window = QtGui.QMainWindow()
                fileName2 = QtGui.QFileDialog.getSaveFileName(self.window,
                                                              u"文件保存",
                                                              u"%s\\%s"%(g.cur_file_dir(),str(name)))
                #"All Files (*);;Text Files (*.txt)")
                if fileName2:
                    if self.script=="PHP" :
                        file_object = open(fileName2, 'wb')
                        file_object.writelines(ResInfo)
                        file_object.close()
                    if self.script=="ASP" or self.script=="ASPX":
                        file_object = open(fileName2, 'wb')
                        file_object.writelines(ResInfo)
                        file_object.close()
                    msg.msg_lower_Left(u"%s保存文件完成"%(str(name)))#设置状态栏文字信息
            else:
                msg.msg_lower_Left(u"%s读取文件错误"%(str(name)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_edit_shell_Thread(self):  #编辑文件
        try:
            self.work = Worker_Thread(name="uix0")
            self.work.Finish.connect(self.file_edit_shell)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_edit_shell(self):  #编辑文件
        try:
            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            name1=self.ShowFile_ui.file_tableWidget.item(int(ranges),1).text()  #获取某一格内容
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            name=get_name+str(name1)
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"Open_file")    #获取文件内容
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
                msg.msg_lower_Left(u"%s读取文件完成"%(str(name)))#设置状态栏文字信息
                Edit_file_ui.Edit_file(id=self.id,data=ResInfo,name=name)  #编辑这个文件
            else:
                msg.msg_lower_Left(u"%s读取文件错误"%(str(name)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_delete_shell_Thread(self):  #删除文件
        try:
            self.work = Worker_Thread(name="uix0")
            self.work.Finish.connect(self.file_delete_shell)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_delete_shell(self):   #删除文件
        try:
            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            name1=self.ShowFile_ui.file_tableWidget.item(int(ranges),1).text()  #获取某一格内容
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            name=u"%s%s"%(get_name,str(name1))
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"del_file")    #
                psot_data="%s&z1=%s"% \
                          (link_shell.post_php_data(psot_data),base64.b64encode(str(name)))
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"del_file")    #
                psot_data="%s&z1=%s"% \
                          (psot_data,urllib.quote(str(name)))
            if self.script=="ASPX":
                psot_data=link_shell.GetPostText(self.script,"del_file")    #
                psot_data="%s&z1=%s"% \
                          (psot_data,urllib.quote(str(name)))
            FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
            if not ((FALSE_bool==0)and(str(ResInfo)=="1")):
                self.file_Refresh_shell()  #刷新当前目录
                msg.msg_lower_Left(u"%s删除文件完成"%(str(name)))#设置状态栏文字信息
            else:
                msg.msg_lower_Left(u"%s删除文件错误"%(str(name)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_rename_shell(self):  #重命名
        try:
            #pTableWidget->editItem(pTableWidget->item(row,col))
            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            name1=self.ShowFile_ui.file_tableWidget.item(int(ranges),1).text()  #获取某一格内容
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            self.ley_operate_name=str(get_name)+str(name1)
            self.ley_operate="rename"   #操作方法  重命名  修改文件时间  创建文件夹

            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            self.ShowFile_ui.file_tableWidget.editItem(self.ShowFile_ui.file_tableWidget.item(int(ranges),1))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_copy_shell(self): #复制
        try:
            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            name1=self.ShowFile_ui.file_tableWidget.item(int(ranges),1).text()  #获取某一格内容
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            self.Copy_file_name=str(get_name)+str(name1)+"|"+name1  #复制路径
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_paste_shell_Thread(self): #粘贴
        try:
            self.work = Worker_Thread(name="uix0")
            self.work.Finish.connect(self.file_paste_shell)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_paste_shell(self): #粘贴
        try:
            #print self.Copy_file_name  #复制路径
            if len(self.Copy_file_name):
                ss = self.Copy_file_name.split("|") #1复制路径 2文件名
                get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
                #z2_name=str(get_name)+"_eval"+ss[1]
                z2_name=str(get_name)+ss[1]
                if self.script=="PHP":
                    psot_data=link_shell.GetPostText(self.script,"Copy_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (link_shell.post_php_data(psot_data),base64.b64encode(str(ss[0]).replace("\\","\\\\")),base64.b64encode(str(z2_name).replace("\\","\\\\")))
                if self.script=="ASP":
                    psot_data=link_shell.GetPostText(self.script,"Copy_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (psot_data,urllib.quote(str(ss[0]).replace("\\","\\\\")),urllib.quote(str(z2_name).replace("\\","\\\\")))
                if self.script=="ASPX":
                    psot_data=link_shell.GetPostText(self.script,"Copy_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (psot_data,urllib.quote(str(ss[0]).replace("\\","\\\\")),urllib.quote(str(z2_name).replace("\\","\\\\")))
                FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                if not ((FALSE_bool==0)and(str(ResInfo)=="1")):
                    if "ERROR:" in ResInfo:
                        msg.msg_lower_Left(u"%s错误 %s"%(str(z2_name),str(ResInfo)))#设置状态栏文字信息
                        msg.msg_box(u"错误提示",str(ResInfo))  #错误提示
                    else:
                        msg.msg_lower_Left(u"%s复制文件完成"%(str(z2_name)))#设置状态栏文字信息
                        get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
                        #self.link_file_tableWidget(str( get_name),"0")  #刷新上传内容
                        self.look_file_Thread(get_name=str(get_name),x="0")  #刷新上传内容
                else:
                    msg.msg_lower_Left(u"%s复制名文件错误"%(str(z2_name)))#设置状态栏文字信息
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_time_shell(self):  #修改文件时间
        try:
            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            name1=self.ShowFile_ui.file_tableWidget.item(int(ranges),1).text()  #获取某一格内容
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            self.ley_operate_name=str(get_name)+str(name1)
            self.ley_operate="time"   #操作方法  重命名  修改文件时间  创建文件夹

            ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            self.ShowFile_ui.file_tableWidget.editItem(self.ShowFile_ui.file_tableWidget.item(int(ranges),2))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_folders_shell(self):  #新建文件夹
        try:
            self.ShowFile_ui.file_tableWidget.setRowCount(self.ShowFile_ui.file_tableWidget.rowCount()+1)  #行  len(node)  #加一行
            i=self.ShowFile_ui.file_tableWidget.rowCount()-1 #统计item数目
            #self.ShowFile_ui.file_tableWidget.setCurrentRow(i+1) #设置当前选择行默认为-1
            #print i
            file_ICO='system/file_ico/file_file.ico'
            color=QColor(0, 0, 0)   #黑色1链接成功
            self.tableWidget_add(1,i,title=str("New folder"),color=color,ico=file_ICO)  #名称
            #tableWidget.verticalScrollBar->setValue(row++)scrollToBottom
            #self.ShowFile_ui.file_tableWidget.scrollToBottom.setValue(int(i))
            self.ShowFile_ui.file_tableWidget.scrollToBottom()   #定位到列表最下面
            # ranges=self.ShowFile_ui.file_tableWidget.currentRow()  #当前选中行号
            self.ley_operate="folders"   #创建文件夹
            self.ShowFile_ui.file_tableWidget.editItem(self.ShowFile_ui.file_tableWidget.item(int(i),1))  #可编辑状态
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_open_txt_shell(self):  #新建文件
        try:
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            Edit_file_ui.Edit_file(ID=self.id,data="NewFile",name=str(get_name)+"NewFile.txt")  #编辑这个文件
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_operate_shell_Thread(self,row,column):  #编辑文件操作   重命名  修改文件时间  创建文件夹
        try:
            ##重命名   #修改文件时间   #创建文件夹
            if ((self.ley_operate=="rename")or(self.ley_operate=="time")or(self.ley_operate=="folders")):
                self.work = Worker_Thread(name="uix2",var1=str(row),var2=str(column))
                self.work.Finish2.connect(self.file_operate_shell)
                self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def file_operate_shell(self,row,column):  #编辑文件操作   重命名  修改文件时间  创建文件夹
        try:
            #openPersistentEditor和closePersistentEditor用来控制某一item是否可以编辑
            name1=self.ShowFile_ui.file_tableWidget.item(int(row),int(column)).text()  #获取某一格内容
            get_name=self.ShowFile_ui.ComPath.currentText()  #获取当前内容
            name=get_name+str(name1)
            #print "name1",self.ley_operate_name  #原先内容
            #print "name2",name   #现在内容
            if self.ley_operate=="rename":#重命名
                if self.script=="PHP":
                    psot_data=link_shell.GetPostText(self.script,"Rename_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                          (link_shell.post_php_data(psot_data),base64.b64encode(str(self.ley_operate_name).replace("\\","\\\\")),base64.b64encode(str(name).replace("\\","\\\\")))
                if self.script=="ASP":
                    psot_data=link_shell.GetPostText(self.script,"Rename_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (psot_data,urllib.quote(str(self.ley_operate_name).replace("\\","\\\\")),urllib.quote(str(name)))
                if self.script=="ASPX":
                    psot_data=link_shell.GetPostText(self.script,"Rename_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (psot_data,urllib.quote(str(self.ley_operate_name).replace('\\', '\\\\')),urllib.quote(str(name).replace('\\', '\\\\')))
                FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                if not ((FALSE_bool==0)and(str(ResInfo)=="1")):
                    if "ERROR:" in ResInfo:
                        msg.msg_lower_Left(u"%s错误 %s"%(str(name),str(ResInfo)))#设置状态栏文字信息
                        msg.msg_box(u"错误提示",str(ResInfo))  #错误提示
                    else:
                        msg.msg_lower_Left(u"%s重命名文件完成"%(str(name)))#设置状态栏文字信息
                else:
                    msg.msg_lower_Left(u"%s重命名文件错误"%(str(name)))#设置状态栏文字信息
            if self.ley_operate=="time":#修改文件时间
                if self.script=="PHP":
                    psot_data=link_shell.GetPostText(self.script,"Time_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (link_shell.post_php_data(psot_data),base64.b64encode(str(self.ley_operate_name).replace("\\","\\\\")),base64.b64encode(str(name1)))
                if self.script=="ASP":
                    psot_data=link_shell.GetPostText(self.script,"Time_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (psot_data,urllib.quote(str(self.ley_operate_name).replace("\\","\\\\")),urllib.quote(str(name1)))  #
                if self.script=="ASPX":
                    psot_data=link_shell.GetPostText(self.script,"Time_file")    #
                    psot_data="%s&z1=%s&z2=%s"% \
                              (psot_data,urllib.quote(str(self.ley_operate_name).replace("\\","\\\\")),urllib.quote(str(name1)))  #
                FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                if not ((FALSE_bool==0)and(str(ResInfo)=="1")):
                    if "ERROR:" in ResInfo:
                        msg.msg_lower_Left(u"%s错误 %s"%(str(name),str(ResInfo)))#设置状态栏文字信息
                        msg.msg_box(u"错误提示",str(ResInfo))  #错误提示
                    else:
                        msg.msg_lower_Left(u"%s修改文件时间完成"%(str(name)))#设置状态栏文字信息
                else:
                    msg.msg_lower_Left(u"%s修改文件时间错误"%(str(name)))#设置状态栏文字信息
            if self.ley_operate=="folders":   #创建文件夹
                if self.script=="PHP":
                    psot_data=link_shell.GetPostText(self.script,"Folders_file")    #
                    psot_data="%s&z1=%s"% \
                              (link_shell.post_php_data(psot_data),base64.b64encode(str(name1).replace("\\","\\\\")))
                if self.script=="ASP":
                    psot_data=link_shell.GetPostText(self.script,"Folders_file")    #
                    psot_data="%s&z1=%s"% \
                              (psot_data,urllib.quote(str(name1).replace("\\","\\\\")))  #
                if self.script=="ASPX":
                    psot_data=link_shell.GetPostText(self.script,"Folders_file")    #
                    psot_data="%s&z1=%s"% \
                              (psot_data,urllib.quote(str(name1).replace('\\', '\\\\')))  #
                FALSE_bool,ResInfo=eval_link.Post_eval_php(str(self.id),psot_data) #获取 请求内容
                if not ((FALSE_bool==0)and(str(ResInfo)=="1")):
                    if "ERROR:" in ResInfo:
                        msg.msg_lower_Left(u"%s错误 %s"%(str(name),str(ResInfo)))#设置状态栏文字信息
                        msg.msg_box(u"错误提示",str(ResInfo))  #错误提示
                    else:
                        msg.msg_lower_Left(u"%s创建文件夹完成"%(str(name)))#设置状态栏文字信息
                else:
                    msg.msg_lower_Left(u"%s创建文件夹错误"%(str(name)))#设置状态栏文字信息

            self.ley_operate=""  #操作方法
            self.ley_operate_name=""   #保存原先内容
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    ########################################################


