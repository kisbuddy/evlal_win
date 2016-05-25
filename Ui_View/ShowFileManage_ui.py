#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#文件操作
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
from Clicked_Controller import ip_query #ip数据库
from Clicked_Controller import link_shell  #链接SHELL等操作
from Clicked_Controller import eval_link  #链接SHELL
from Clicked_Controller import ShowFileManage_class  #文件管理事件响应
from Clicked_Controller import threadpool #线程操作
from Clicked_Controller import msg #消息提示
from Clicked_Controller import log #日志记录

import link_except_ui   #错误异常处理

class Worker(QThread):
    Finish = pyqtSignal() #basestring
    Finish1 = pyqtSignal(basestring) #
    def __init__(self,name,x1=None,parent=None):
        super(Worker,self).__init__(parent)
        self.name=name
        self.x1=x1
        #print "xxx",self.name
    def run(self):
        try:
            if self.name=="uix0":   #无参数
                self.Finish.emit()
                #self.treeWidget.doubleClicked.connect(self.double_click)  #目录查看数据  双击
            if self.name=="uix1":   #1个无参数
                self.Finish1.emit(self.x1)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            #print(str(e))

class ShowFileManage_ui(QWidget):
    def __init__(self,**kwargs):
        super(ShowFileManage_ui, self).__init__()
        #uic.loadUi("ui/file.ui", self)
        try:
            self.main_ui=UIManager.get_ui('main_ui') #主程序UI
            self.shell_sql=UIManager.shell_sql
            self.ShowFile_ui = uic.loadUi("ui/ShowFileManage.ui", self)#动态加标签
            self.ShowFileManage_data=ShowFileManage_class.ShowFileManage_class(self.ShowFile_ui,'%s'%(kwargs['ID'])) #事件处理
            #self.Upload_files=[] #上传文件
            #self.Download_File=[] #下载文件
            ###########################################
            self.ComPath.setMouseTracking(False)
            self.ComPath.setAcceptDrops(False)
            self.ComPath.setEditable(True)
            self.ComPath.setMaxVisibleItems(15)#设置下拉最大选项数为15
            self.ComPath.installEventFilter(self)#在窗体上为self.edit安装过滤器

            #self.ShowFile_ui.file_treeWidget.setHeaderLabels(['path','system_path'])
            #self.ShowFile_ui.file_treeWidget.setColumnWidth(0,150) #设置宽度  1是列号   2是宽度
            #self.ShowFile_ui.file_treeWidget.setColumnWidth(1,0) #设置宽度  1是列号   2是宽度
            #self.ShowFile_ui.file_treeWidget.setHeaderHidden(True) #取消标题

            self.file_treeWidget.setColumnCount(1)
            self.file_treeWidget.setHeaderLabels([_fromUtf8(u"文件管理")])
            self.file_treeWidget.setColumnWidth(0, 700)#设置列宽

            self.file_tableWidget.setColumnCount(5)     #列
            self.file_tableWidget.setRowCount(0)  #行  len(node)
            self.file_tableWidget.setHorizontalHeaderLabels([u'name',u'名称',u'时间',u'大小',u'属性'])
            self.file_tableWidget.setColumnWidth(0,0)  #设置表格的各列的宽度值
            self.file_tableWidget.setColumnWidth(1,320)  #设置表格的各列的宽度值
            self.file_tableWidget.setColumnWidth(2,170)  #设置表格的各列的宽度值
            self.file_tableWidget.setColumnWidth(3,100)  #设置表格的各列的宽度值
            self.file_tableWidget.setColumnWidth(4,160)  #设置表格的各列的宽度值

            for i in range(0):  #调整行高度  len(node)
                self.file_tableWidget.setRowHeight(i, 23)
            self.file_tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)  #设置表格的单元为只读属性，即不能编辑
            self.file_tableWidget.setSelectionBehavior(QTableWidget.SelectRows) #点击选择是选择行//设置选中时为整行选中
            self.file_tableWidget.setSelectionMode(QTableWidget.SingleSelection)  #禁止多行选择
            self.file_tableWidget.setAlternatingRowColors(True)  #还是只可以选择单行（单列）
            self.file_tableWidget.verticalHeader().hide() #隐藏行头
            self.file_tableWidget.setAlternatingRowColors(True)#隔行换色
            #self.file_tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)#不可编辑
            self.setAcceptDrops(True)   #拖拽接收文件
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
            #if "url" in kwargs:  #名称
            name_Title=u"%s"%(ip_query.url_www(str(self.siteurl)))  #_fromUtf8("文件管理-" + str(QTableName))
            #else:
            #    name_Title=u"null"
            self.main_ui.tabWidget.addTab(self.ShowFile_ui,QIcon('system/ShowFileManage.ico'),name_Title)
            #self.main_ui.tabWidget.setTabIcon(self.tabWidget.count()-1, QIcon('system/asp.ico'))
            if "form" in kwargs:  #名称
                if int(kwargs['form']):
                    self.main_ui.tabWidget.setCurrentIndex(self.main_ui.tabWidget.count()-1)#显示当前页

            msg.msg_lower_Left(u"正在连接 %s 请等待...."%(str(self.siteurl)))#设置状态栏文字信息
            self.ini_run_Thread() #类初始化线程
            ###########################################
            #=========================右键事件响应   SHELL
            self.file_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  #右键响应
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  #右键响应
            self.file_tableWidget.customContextMenuRequested.connect(self.file_tableWidget_menu)  #右键响应
            ###########################################
            #事件响应
            self.file_treeWidget.itemClicked.connect(self.ShowFileManage_data.GetTreeRoot)#双击  目录   #xxxxx有参数无法线程等待解决
            #self.file_tableWidget.dragEnterEvent.connect(self.dragEnterEventxxx) #拖拽接收文件
            self.look_Button.clicked.connect(self.ShowFileManage_data.look_file_Thread)    #读取文件
            self.file_tableWidget.cellDoubleClicked.connect(self.ShowFileManage_data.open_file_Thread)  #双击  文件
            #self.lineEditAdr = QtGui.QLineEdit(self)
            self.file_tableWidget.cellChanged.connect(self.ShowFileManage_data.file_operate_shell_Thread)  #编辑事件
            ###########################################
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    ########################################
    def ini_run_Thread(self): #类初始化线程
        try:
            self.work = Worker("uix0", self)
            self.work.Finish.connect(self.ini_run)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def ini_run(self):  #初始化
        try:
            if self.script=="ASP":
                psot_data=link_shell.GetPostText(self.script,"WebRoot")    #获取代码
            if self.script=="PHP":
                psot_data=link_shell.GetPostText(self.script,"WebRoot")    #获取代码
                psot_data=link_shell.post_php_data(psot_data)  #转换代码
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
                db_shell.SELECT_shell_link(str(self.id),1) #更新链接状态  0链接失败 1链接成功  2还未测试
                db_shell.SELECT_shell_updatetime(str(self.id),str(self.siteurl))  #更新shell时间  updatetime     修改时间   最后一次访问时间
                self.ShowFileManage_data.link_shell_file_Thread(Info) #链接SHELL显示文件
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def eventFilter(self, source, event):  #事件监听
        try:
            #PyQt4.QtCore.QEvent.KeyPress
            #PyQt4.QtCore.QEvent.KeyRelease
            if event.type()==QtCore.QEvent.KeyPress:   #检测键盘事件
                if event.key()==QtCore.Qt.Key_Return:  #判断回车
                    #回车是16777220
                    self.ShowFileManage_data.look_file_Thread()    #读取文件
            return QtGui.QWidget.eventFilter(self, source, event)#将事件交给上层对话框
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    ########################################文件 右键 操作
    def file_tableWidget_menu(self,p):  #右键菜单
        try:
            # action = QAction(u'删除数据',self)
            # self.popMenu.addAction(action)
            self.popMenu = QtGui.QMenu()
            action = QAction(QtGui.QIcon('system\\file_Refresh.ico'),u'刷新',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_Refresh_shell())
            self.popMenu.addAction(action)
            self.popMenu.addSeparator()#添加分隔
            action = QtGui.QAction(QtGui.QIcon('system\Upload_files.ico'),u'上传文件',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_Upload_shell())
            self.popMenu.addAction(action)
            action = QtGui.QAction(QtGui.QIcon('system\Download_File.ico'),u'下载文件',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_Download_shell_Thread())
            self.popMenu.addAction(action)

            self.popMenu.addSeparator()#添加分隔
            action = QtGui.QAction(QtGui.QIcon('system\\file_Edit.ico'),u'编辑',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_edit_shell_Thread())
            self.popMenu.addAction(action)
            action = QtGui.QAction(QtGui.QIcon('system\\file_delete.ico'),u'删除',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_delete_shell_Thread())
            self.popMenu.addAction(action)
            action = QtGui.QAction(QtGui.QIcon(''),u'重命名',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_rename_shell())
            self.popMenu.addAction(action)
            action = QtGui.QAction(QtGui.QIcon('system\\Copy_file.ico'),u'复制',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_copy_shell())
            self.popMenu.addAction(action)
            action = QtGui.QAction(QtGui.QIcon('system\\Copy_file.ico'),u'粘贴',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_paste_shell_Thread())
            self.popMenu.addAction(action)

            self.popMenu.addSeparator()#添加分隔
            action = QtGui.QAction(QtGui.QIcon('system\\time_file.ico'),u'修改文件(夹)时间',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_time_shell())
            self.popMenu.addAction(action)

            #action = QtGui.QAction(QtGui.QIcon(''),u'新建',self)
            self.name=self.popMenu.addMenu(u'新建')
            action = QtGui.QAction(QtGui.QIcon('system\ShowFileManage.ico'),u'文件夹',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_folders_shell())
            self.name.addAction(action)
            action = QtGui.QAction(QtGui.QIcon('system\\file_Edit.ico'),u'文件',self)
            action.triggered.connect(lambda:self.ShowFileManage_data.file_open_txt_shell())
            self.name.addAction(action)

            #self.popMenu.addAction(action)
            self.popMenu.exec_(self.file_tableWidget.mapToGlobal(p))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    ###########################################
    def dragEnterEvent(self, event):   #拖拽接收文件
        try:
            self.Upload_files=[] #上传文件
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
                if event.mimeData().hasUrls():
                    #遍历输出拖动进来的所有文件路径
                    for url in event.mimeData().urls():
                        file=str(url.toLocalFile()).decode('UTF-8').encode('GBK').replace("/", "\\")
                        name=file[file.rfind("\\")+1:]#从尾部查找字符串
                        if name.rfind("."):  #判断是否是文件
                            file="%s%s|%s|%s"%(str(self.ComPath.currentText()),str(name),str(file),str(name))  #获取当前内容
                            self.Upload_files.append(file)  #添加数据
            if len(self.Upload_files):
                try:
                    t_h_Thread = threadpool.ThreadPool(1)   #创建多线程  线程池
                    t_h_Thread.push(self.ShowFileManage_data.thread_Upload_files,self.Upload_files) #"Upload_files"
                    t_h_Thread.wait_for_idel(1)
                except BaseException, e:
                    log.logging.debug("except:%s"%(str(e)))
                    pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            #print("dragEnterEvent except",str(e))
            # 有数据   就开启一个线程单独  进行上传操纵
            # 单独写个  函数
            # 在菜单栏里  更新上传状态






