#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
# coding=gbk
#导入导出数据

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
import ui
from Db_Model import db_shell #常用数据库操作
from Clicked_Controller import link_shell  #链接SHELL等操作
from Clicked_Controller import eval_link  #链接SHELL
from Clicked_Controller import ShowFileManage_class  #文件管理事件响应
from Clicked_Controller import threadpool #线程操作
from Clicked_Controller import treeWidget_work #目录操作
from Clicked_Controller import tableWidget_work  #SHELL操作
from Clicked_Controller import g #公共文件
from Clicked_Controller import msg #消息提示
from Clicked_Controller import log #日志记录
import link_except_ui   #错误异常处理
import json
import time
from os.path import isfile


#class Import_export_ui(QWidget):
class Import_export_ui(QDialog):
    #def __init__(self,**kwargs):
    #    super(Import_export_ui, self).__init__()
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        #uic.loadUi("ui/file.ui", self)
        self.main_ui=UIManager.get_ui('main_ui') #主程序UI
        self.shell_sql=UIManager.shell_sql
        self.ShowFile_ui = uic.loadUi("ui/Import_export.ui", self)#动态加标签
        self.setWindowIcon(QtGui.QIcon("system/main.ico"))  #设置图标
        flags = 0  #设置禁止最大化
        flags|= Qt.WindowMinimizeButtonHint  #设置禁止最大化
        self.setWindowFlags(flags)  #设置禁止最大化
        #禁止最大化按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        #禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())
        try:
            self.path_Edit.setEnabled(0)  #给改成禁用
            #self.textEdit.setEnabled(0)  #给改成禁用
            self.radioButton_1.setChecked(True)
            self.Import_export=0  #操作方式
            self.radio_id="|"  #分割符号
            self.list_data=[]

            self.log_edit_shell(self.radio_id)  #注释
            self.path_Edit.setText(_fromUtf8(str("file Utf-8")))  #设置当前内容
            self.link_Button.setEnabled(0)  #给改成禁用
            ###################################################
            self.path_Button.clicked.connect(self.open_path_Button)    #读取文件
            self.link_Button.clicked.connect(self.open_link_Button)    #导入

            self.radioButton_1.clicked.connect(self.radioButton_id)    #
            self.radioButton_2.clicked.connect(self.radioButton_id)    #
            self.radioButton_3.clicked.connect(self.radioButton_id)    #
            self.radioButton_4.clicked.connect(self.radioButton_id)    #
            self.radioButton_5.clicked.connect(self.radioButton_id)    #
            ###################################################
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def log_edit_shell(self,x):  #注释
        try:
            data="http://eval.webxscan.com/xx.php%swebxscan"%(str(x))
            self.shell_label.setText(data)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def radioButton_id(self): #判断选择
        try:
            if (self.radioButton_1.isChecked()):
                self.radio_id="|"
                self.log_edit_shell(self.radio_id)  #注释
            if (self.radioButton_2.isChecked()):
                self.radio_id=","
                self.log_edit_shell(self.radio_id)  #注释
            if (self.radioButton_3.isChecked()):
                self.radio_id="*"
                self.log_edit_shell(self.radio_id)  #注释
            if (self.radioButton_4.isChecked()):
                self.radio_id="\t"
                self.log_edit_shell(self.radio_id)  #注释
            if (self.radioButton_5.isChecked()):
                self.radio_id="5"
                #self.textEdit.setEnabled(1)  #给改成禁用
                self.log_edit_shell(self.radio_id)  #注释
            #print self.radio_id
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def set_data(self,**kwargs):  #远程参数
        try:
            if "title" in kwargs:  #标题
                self.setWindowTitle(u'%s'%(kwargs['title']))
            if "Import_export" in kwargs:  #操作方式
                self.Import_export=int(kwargs['Import_export'])

            if "type_id" in kwargs:  #类别
                self.type_id.addItem(QtGui.QIcon('system/main.ico'),_fromUtf8(str("站点类别")))
                #self.type_id.addItems(kwargs['type_id'])
                self.json_data=json.loads(kwargs['type_id'])
                for colour in self.json_data:
                    #print "xxxx",colour
                    self.type_ICO=treeWidget_work.sql_type_ICO(str(colour))
                    self.type_id.addItem(QtGui.QIcon(str(self.type_ICO)),_fromUtf8(str(self.json_data.get(str(colour)))))
                    self.list_data.append(colour)
                #self.type_id.setCurrentIndex(int(1))
            if "type_id_key" in kwargs:  #类别
                self.insert_update=False   #0是True添加    1是False  修改
                x= self.list_data.index(u'%s'%(kwargs['type_id_key']))
                # if self.type_id.currentIndex()>=int(x): #返回Item数目
                #     print self.type_id.currentIndex(),"bbbbb",x
                try:
                    # 你的代码
                    self.type_id.setCurrentIndex(int(x)+1)
                except BaseException, e:
                    pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def open_path_Button(self):
        try:
            if self.Import_export==1:  #导入
                self.window = QtGui.QMainWindow()
                files = QtGui.QFileDialog.getOpenFileName(self.window,
                                                           u"选取文件"
                                                           #g.cur_file_dir()
                                                           u"%s\\"%(g.cur_file_dir()))
                                                            #"All Files (*);;Text Files (*.txt)"设置文件扩展名过滤,注意用双分号间隔
                if len(files):
                    self.link_Button.setEnabled(1)  #给改成禁用
                    self.path_Edit.setText(_fromUtf8(str(files)))  #设置当前内容
            if self.Import_export==2:  #导出
                self.window = QtGui.QMainWindow()
                files= QFileDialog.getSaveFileName(self.window,
                                               u"文件保存",
                                               u"%s\\"%(g.cur_file_dir()))
                if len(files):
                    self.link_Button.setEnabled(1)  #给改成禁用
                    self.path_Edit.setText(_fromUtf8(str(files)))  #设置当前内容
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def open_link_Button(self):
        try:
            file_path=self.path_Edit.text()  #获取文件路径
            if str(file_path)=="file Utf-8":
                QtGui.QMessageBox.information(self, _fromUtf8(u"操作提示"),  _fromUtf8(u"请注意 请选择文件保存路径！"))#弹出对话框
                return
            if self.Import_export==1:  #导入
                if isfile(file_path):
                    try:
                        open_file = file(str(file_path), 'r')
                    except IOError, e:
                        msg.msg_box(u"操作提示",u"打开文件错误 %s"%(str(e)))
                        #msg.msg_box(u"操作提示",u"请注意 文件格式请选择另存为 UTF-8 模式！")
                        return
                    if self.radio_id=="5":
                        if self.textEdit.text()=="":  #获取文件路径
                            msg.msg_box(u"操作提示",u"请注意 自定义格式不能为空！")
                            return
                        self.radio_id==str(self.textEdit.text())
                    self.add_shell(open_file,str(self.radio_id))  #添加数据
            if self.Import_export==2:  #导出
                if self.radio_id=="5":
                    if self.textEdit.text()=="":  #获取文件路径
                        msg.msg_box(u"操作提示",u"请注意 自定义格式不能为空！")
                        return
                    self.radio_id==str(self.textEdit.text())
                self.Dexport(file_path)  #导出数据
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def Dexport(self,open_file): #导出数据
        try:
            #self.main_ui
            type_id_id=self.type_id.currentIndex()
            type_id=self.list_data[type_id_id-1]  #获取ID
            sql_data = "select * from sitetable WHERE type_id='%s' order by `updatetime` desc"%(str(type_id))   # asc 表示升序 , desc表示降序
            self.shell_sql.conn.commit()# 获取到游标对象
            cur = self.shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
            cur.execute(sql_data)# 获取所有结果
            res = cur.fetchall()  #从结果中取出所有记录
            cur.close()  #关闭游标
            data=""
            for line in res:
                url_pass="%s%s%s"%(str(line[2]),str(self.radio_id),str(line[3]))
                data+=url_pass+"\r\n"

            if self.TXT_file2(open_file,data):
                msg.msg_lower_Left(u"导出SHELL %s 成功"%(str(open_file)))#设置状态栏文字信息
                msg.msg_box(u"导出SHELL",u"导出SHELL %s 成功"%(str(open_file)))
            else:
                msg.msg_lower_Left(u"导出SHELL %s 失败"%(str(open_file)))#设置状态栏文字信息
                msg.msg_box(u"导出SHELL",u"导出SHELL %s 失败"%(str(open_file)))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def TXT_file2(self,file_nem,data):  #写入文本 中文
        try:
            #file_nem=time.strftime('%Y.%m.%d')   #file_nem+".txt"
            file_object = open(file_nem,'a')
            file_object.write(data.encode("utf-8")) #成功
            file_object.writelines("\n")
            file_object.close()
            return 1
        except Exception,e:
            print u"写入TXT失败",file_nem,data,e
            log.logging.debug("except:%s"%(str(e)))
            return 0

    def GetExt(self,siteurl): #判断编码方式
        #siteurl=self.siteurl.toPlainText()
        try:
            siteurl=siteurl.upper()
            if (".PHP" in str(siteurl)):
                return "1" #php
            if (".ASP" in str(siteurl)):
                return "2" #.ASP
            if ("ASPX" in str(siteurl)):
                return "3" #ASPX
            else:
                return "0" #脚本类型
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            return "0" #脚本类型

    def add_shell(self,open_file,split):#添加数据
        try:
            i_ok=0
            i_no=0
            for xxx_line in open_file.readlines():
                try:
                    data=xxx_line.strip().lstrip()
                    line = data.split(str(split))
                    type_id_id=self.type_id.currentIndex()
                    type_id=self.list_data[type_id_id-1]
                    script=self.GetExt(str(line[0])) #判断文件编码
                    sql_data="insert into sitetable(type_id,siteurl,sitepass,link,config,remarks,script,coding,createtime) " \
                             "VALUES(%s,'%s','%s','%s','%s','%s','%s','%s','%s')" \
                             %(str(type_id),str(line[0]),str(line[1]),"2","","",script,"65001",str(time.time()))
                    if self.shell_sql.mysqlite3_insert(sql_data):
                        i_ok+=1
                    else:
                        i_no+=1
                except BaseException, e:
                    log.logging.debug("except:%s"%(str(e)))
            msg.msg_lower_Left(u"添加数据成功%s条  失败%s条"%(str(i_ok),str(i_no)))#设置状态栏文字信息
            msg.msg_box(u"提示",u"添加数据成功%s条  失败%s条"%(str(i_ok),str(i_no)))
            #tableWidget_work.add_tableWidget(str(ui.treeWidget_id))   #加载当前列表
            tableWidget_work.reload_tree()  #加载目录
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def while_export_shell(self):  #选择导出
        try:
            data=""
            self.window = QtGui.QMainWindow()
            files= QFileDialog.getSaveFileName(self.window,
                                               u"文件保存",
                                               u"%s\\"%(g.cur_file_dir()),
                                               "Text Files (*.txt)")
            if len(files):
                int_model = self.main_ui.tableWidget.selectionModel()  #获取选中编号
                if len(int_model.selectedRows())>=1:
                    for index in int_model.selectedRows():       #// 对于被选中的每一行
                        try:
                            int_index=index.row()#获取行号
                            ID=self.main_ui.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                            #print ID
                            self.id_shell_list=db_shell.id_sitetable_shell(str(ID))  #通过ID查询SHELL的状态
                            #self.id=str(self.id_shell_list[0])         #自动编号
                            #self.type_id=str(self.id_shell_list[1])    #      类别
                            self.siteurl=str(self.id_shell_list[2])    #    网址
                            self.sitepass=str(self.id_shell_list[3])   #    密码
                            data+="%s|%s\r\n"%(str(self.siteurl),str(self.sitepass))
                        except BaseException, e:
                            pass
                    if self.TXT_file2(files,data):
                        msg.msg_lower_Left(u"导出SHELL %s 成功"%(str(files)))#设置状态栏文字信息
                        msg.msg_box(u"导出SHELL",u"导出SHELL %s 成功"%(str(files)))
                    else:
                        msg.msg_lower_Left(u"导出SHELL %s 失败"%(str(files)))#设置状态栏文字信息
                        msg.msg_box(u"导出SHELL",u"导出SHELL %s 失败"%(str(files)))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
