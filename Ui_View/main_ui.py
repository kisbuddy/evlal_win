#!/usr/local/bin/python
#-*- coding: UTF-8 -*-

from PyQt4 import QtCore, QtGui ,QtNetwork
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import socket
socket.setdefaulttimeout(10)

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import time
import json
import urllib
import base64,os
#from ui import * #UI变量
import ui  #UI变量
from Clicked_Controller import msg #消息提示
from Clicked_Controller import treeWidget_work  #目录操作
from Clicked_Controller import tableWidget_work  #SHELL操作
from Clicked_Controller import ip_query #显示IP地址
from Clicked_Controller import threadpool #线程操作
from Clicked_Controller import log #日志记录
import Action_ui   #关于作者
import tree_insert_update_ui  #添加修改目录
import add_shell_ui  #添加SHELL
import ShowFileManage_ui #调用关键管理
import ShowcmdManage_ui #调用CMD
import ShowEdit_shellManage_ui  #自定义代码
import ShowWebManage_ui  #WEB浏览
import Import_export_ui  #导入导出数据
import ConfigParser  #INI读取数据
#from ui_py import main_uixx

shell_sql = None   #数据库

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

class main_ui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        #加载窗体
        # mame_path=sys.argv[0]
        # print mame_path[len(mame_path)-3:].lower()
        # if mame_path[len(mame_path)-3:].lower()==".py":
        #     print "11111"  #调试状态
        # else:
        #     print "222222"  #发布状态


        self.ui=uic.loadUi("ui/main_ui.ui", self)  #主窗口
        #self.ui = main_uixx.Ui_MainWindow(self)
        ##self.ui.setupUi(self)
        #===========ini===========
        #ui.label = QtGui.QLabel('')  #消息提示
        self.setWindowIcon(QtGui.QIcon("system/main.ico"))  #设置图标
        self.setWindowTitle(u'开山斧 V0.3    目前支持PHP ASP ASPX')  #设置标题
        self.ui.tabWidget.setTabText(0,"shell")  #设置标题
        self.ui.treeWidget.setHeaderLabels(['name','ID','Value'])
        self.ui.treeWidget.setColumnWidth(0,150) #设置宽度  1是列号   2是宽度
        self.ui.treeWidget.setColumnWidth(1,0) #设置宽度  1是列号   2是宽度
        self.ui.treeWidget.setHeaderHidden(True) #取消标题
        try:
            global shell_sql
            shell_sql=ui.UIManager.shell_sql
            #=========================右下角提示#状态栏
            self.createActions() #加载菜单
            self.createTrayIcon() #加载菜单
            self.trayIcon.activated.connect(self.iconActivated)    #点击图标响应
            self.setIcon()  #加载图标
            self.showMessage()  #消息提示

            self.tabWidget.setTabsClosable(True) #允许tab点击关闭
            self.tabWidget.setTabIcon(0, QIcon('system/main.ico'))  #加载ICO图标
            #self.setFixedSize(QSize(500,500)) #窗口部件的最小大小和最大大小
            #=========================右键事件响应   目录
            self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  #右键响应
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  #右键响应
            self.treeWidget.customContextMenuRequested.connect(self.treeWidget_menu)  #右键响应  SHELL
            #=========================右键事件响应   SHELL
            self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  #右键响应
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  #右键响应
            self.tableWidget.customContextMenuRequested.connect(self.tableWidget_menu)  #右键响应  目录
            #========================= 事件响应
            #self.aboutAction.triggered = self.Action_show  #直接覆盖写法
            #self.connect(self.tabwidget, SIGNAL("tabCloseRequested(int)"),self.closeTab)
            self.aboutAction.triggered.connect(self.Action_show)  #关于作者
            #self.treeWidget.itemClicked.connect(self.single_click)  #查看数据  单击
            self.treeWidget.doubleClicked.connect(self.double_click_Thread)  #目录查看数据  双击
            self.tabWidget.tabCloseRequested.connect(self.closeTab_Thread)  #关闭属性页

            self.tableWidget.cellDoubleClicked.connect(self.open_file_shell_Thread)  #双击  SHELL
            #self.tableWidget.verticalHeader().sectionClicked.connect(self.VerSectionClicked)#表头单击信号
            #self.tableWidget.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)#表头单击信号
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    # def VerSectionClicked(self,index):
    #     print "xxxxx",index
    # def HorSectionClicked(self,index):
    #     print "zzzzz",index

    def closeTab_Thread(self): #UI线程操作#关闭属性页
        try:
            id=self.ui.tabWidget.count()-1
            self.work = Worker("uix1",str(id), self)
            self.work.Finish1.connect(self.closeTab)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def open_file_shell_Thread(self): #UI线程操作#双击  SHELL
        try:
            self.work = Worker("uix0", self)
            self.work.Finish.connect(self.open_file_shell)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def double_click_Thread(self): #UI线程操作#目录查看数据  双击
        try:
            self.work = Worker("uix0", self)
            self.work.Finish.connect(self.double_click)
            self.work.start()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def open_file_shell(self):    #,row,column双击  SHELL  文件管理
        try:
            int_model = self.tableWidget.selectionModel()  #获取选中编号
           # model = self.tableWidget.model()#index = model.index(3,1)#data = model.data(index)#print data.toString()
            if len(int_model.selectedRows())==1:
                int_index=int_model.selectedRows()[0].row()#获取行号
                ID=self.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                ShowFileManage_ui.ShowFileManage_ui(ID=ID,form=1)
            elif len(int_model.selectedRows())>=1:
                for index in int_model.selectedRows():       #// 对于被选中的每一行
                    try:
                        #s0= model.data(model.index(int_index,0)).toString()
                        int_index=index.row()#获取行号
                        ID=self.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                        ShowFileManage_ui.ShowFileManage_ui(ID=ID,form=1)
                    except BaseException, e:
                        pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def open_cmd_shell(self):    #cmd管理
        try:
            int_model = self.tableWidget.selectionModel()  #获取选中编号
            if len(int_model.selectedRows())==1:
                int_index=int_model.selectedRows()[0].row()#获取行号
                ID=self.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                ShowcmdManage_ui.ShowcmdManage_ui(ID=ID,form=1)
            elif len(int_model.selectedRows())>=1:
                for index in int_model.selectedRows():       #// 对于被选中的每一行
                    try:
                        int_index=index.row()#获取行号
                        ID=self.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                        ShowcmdManage_ui.ShowcmdManage_ui(ID=ID,form=1)
                    except BaseException, e:
                        pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def open_Edit_shell_shell(self): #自写脚本
        try:
            int_model = self.tableWidget.selectionModel()  #获取选中编号
            if len(int_model.selectedRows())==1:
                int_index=int_model.selectedRows()[0].row()#获取行号
                ID=self.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                ShowEdit_shellManage_ui.ShowEdit_shellManage_ui(ID=ID,form=1)
            elif len(int_model.selectedRows())>=1:
                for index in int_model.selectedRows():       #// 对于被选中的每一行
                    try:
                        int_index=index.row()#获取行号
                        ID=self.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                        ShowEdit_shellManage_ui.ShowEdit_shellManage_ui(ID=ID,form=1)
                    except BaseException, e:
                        pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def web_shell(self):  #WEB浏览软
        try:
            #self.ShowWebManage_ui=ShowWebManage_ui.ShowWebManage_ui()
            int_model = self.tableWidget.selectionModel()  #获取选中编号
            if len(int_model.selectedRows())==1:
                int_index=int_model.selectedRows()[0].row()#获取行号
                web=self.tableWidget.item(int(int_index),2).text()  #获取某一格内容
                name_Title=u"%s"%(ip_query.url_www1(str(web)))
                ShowWebManage_ui.ShowWebManage_ui(Title=name_Title,form=1)
                # if self.ShowWebManage_ui.exec_() == QtGui.QDialog.Accepted:
                #     pass
            elif len(int_model.selectedRows())>=1:
                for index in int_model.selectedRows():       #// 对于被选中的每一行
                    try:
                        int_index=index.row()#获取行号
                        web=self.tableWidget.item(int(int_index),2).text()  #获取某一格内容
                        name_Title=u"%s"%(ip_query.url_www1(str(web)))
                        ShowWebManage_ui.ShowWebManage_ui(Title=name_Title,form=1)
                    except BaseException, e:
                        pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def shell_find(self):  #查找SHELL
        try:
            name_Title=""
            int_model = self.tableWidget.selectionModel()  #获取选中编号
            if len(int_model.selectedRows())==1:
                int_index=int_model.selectedRows()[0].row()#获取行号
                web=self.tableWidget.item(int(int_index),2).text()  #获取某一格内容
                name_Title=u"%s"%(ip_query.url_www1(str(web)))
            text,ok = QtGui.QInputDialog.getText(self,u"查找  当前类别",u"输入你要查找的url     进行匹配",QtGui.QLineEdit.Normal,str(name_Title))
            if ok and text != '':
                tableWidget_work.add_find_shell_tableWidget(str(ui.treeWidget_id),str(text))   #数据进行模糊查询
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def Import_export_ui_show(self,x):  #导入导出数据
        try:
            self.Import_export_ui=Import_export_ui.Import_export_ui()
            json_data,list_data=self.look_type()  #读取分类
            if x==1: #导入数据
                self.Import_export_ui.set_data(type_id_key=str(ui.treeWidget_id),title=u'导入数据',Import_export=1,type_id=json_data)
                #self.Import_export_ui.show()
                if self.Import_export_ui.exec_() == QtGui.QDialog.Accepted:
                    pass
            if x==2: #导出数据
                self.Import_export_ui.set_data(type_id_key=str(ui.treeWidget_id),title=u'导出数据',Import_export=2,type_id=json_data)
                #self.Import_export_ui.show()
                if self.Import_export_ui.exec_() == QtGui.QDialog.Accepted:
                    pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def closeTab(self,tabId):#关闭属性页
        try:
            if int(tabId)>=1:
                self.tabWidget.removeTab(int(tabId))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    ##################################
    def double_click(self):  #查看数据  双击
        try:
            item = self.treeWidget.currentItem()  #获取当前选择类别
            tableWidget_work.add_tableWidget(unicode(item.text(1)))   #查询数据 在添加
            ui.treeWidget_id=unicode(item.text(1))    #记录当前选择目录
            msg.msg_lower_right()  #更新目录数据
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    # def single_click(self):  #查看数据  单击
    #     item = self.treeWidget.currentItem()
    #     print unicode(item.text(0)),unicode(item.text(1))

    def Action_show(self):#关于作者
        try:
            self.Action=Action_ui.Action_ui()#关于作者
            #self.setFocusPolicy(Qt.NoFocus)
            #self.Action.show()
            #self.Action.activateWindow()
            if self.Action.exec_() == QtGui.QDialog.Accepted:
                pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    ##################################
    def closeEvent(self, event):  #退出提示
        import os
        #1. sys.exit(n) 退出程序引发SystemExit异常, 可以捕获异常执行些清理工作. n默认值为0, 表示正常退出. 其他都是非正常退出. 还可以sys.exit("sorry, goodbye!"); 一般主程序中使用此退出.
        #2. os._exit(n), 直接退出, 不抛异常, 不执行相关清理工作. 常用在子进程的退出.
        #3. exit()/quit(), 跑出SystemExit异常. 一般在交互式shell中退出时使用.
        os._exit(1)

        #event.accept()  #接受退出信号，程序退出

        #event->ignore();  //忽略退出信号，程序继续运行
        # if self.trayIcon.isVisible():
        #     QMessageBox.information(self, u"感谢使用开山斧",
        #                             u"<b>(以完善功能为荣，以突破安全防护软件为耻)(向中国菜刀作者致敬)</b>"
        #                             u"如果本软件(开山斧)使用遇到问题或好的建议，请及时与本团队联系，谢谢！ 大家不断的支持是我们开发的动力。"
        #                             u"http://eval.webxscan.com   开山斧QQ交流群：528392695")
            #self.hide()
            #event.ignore()
    ##################################
    ########################################SHELL 右键 操作
    def tableWidget_menu(self,p):  #右键菜单
        try:
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.popMenu = QMenu(self)
            int_model = self.tableWidget.selectionModel()  #获取选中编号
            sum=len(int_model.selectedRows())  #获取数量
            if sum==0:   #如果没有选中  只有添加
                action = QAction(QtGui.QIcon('system\\+.ico'),u'添加数据',self)
                action.triggered.connect(lambda:self.add_shell_show(1))
                self.popMenu.addAction(action)
            if sum>=1:   #如果选中1条  添加  删除  修改
                action = QAction(QtGui.QIcon('system/ShowFileManage.ico'),u'文件管理',self)
                action.triggered.connect(lambda:self.open_file_shell())
                self.popMenu.addAction(action)
                # action = QAction(u'数据库管理',self)
                # self.popMenu.addAction(action)
                action = QAction(QtGui.QIcon('system/ShowcmdManage.ico'),u'虚拟终端',self)
                action.triggered.connect(lambda:self.open_cmd_shell())
                self.popMenu.addAction(action)
                action = QAction(QtGui.QIcon('system/file_Edit.ico'),u'自写脚本',self)
                action.triggered.connect(lambda:self.open_Edit_shell_shell())
                self.popMenu.addAction(action)

                self.popMenu.addSeparator()#添加分隔
                action = QAction(QtGui.QIcon('system\\+.ico'),u'添加数据',self)
                action.triggered.connect(lambda:self.add_shell_show(1))
                self.popMenu.addAction(action)
                action = QAction(QtGui.QIcon('system\\#.ico'),u'修改数据',self)
                action.triggered.connect(lambda:self.add_shell_show(2))
                self.popMenu.addAction(action)
                action = QAction(QtGui.QIcon('system\\-.ico'),u'删除数据',self)
                action.triggered.connect(lambda:self.dll_shell())
                self.popMenu.addAction(action)
                self.popMenu.addSeparator()#添加分隔
                action = QAction(QtGui.QIcon('system\\find.ico'),u'查找',self)
                action.triggered.connect(lambda:self.shell_find())
                self.popMenu.addAction(action)
                self.popMenu.addSeparator()#添加分隔
                action = QAction(QtGui.QIcon('system\\web.ico'),u'浏览网站',self)
                action.triggered.connect(lambda:self.web_shell())
                self.popMenu.addAction(action)
                self.popMenu.addSeparator()#添加分隔
                action = QAction(QtGui.QIcon('system\\shell_cs.ico'),u'批量测试状态',self)
                action.triggered.connect(lambda:tableWidget_work.shell_cs_thread())
                self.popMenu.addAction(action)
                self.popMenu.addSeparator()#添加分隔

                self.name=self.popMenu.addMenu(u'批量导入/导出')
                action = QAction(QtGui.QIcon('system\\Upload_files.ico'),u'批量导入数据',self)
                action.triggered.connect(lambda:self.Import_export_ui_show(1))
                self.name.addAction(action)
                action = QAction(QtGui.QIcon('system\\Download_File.ico'),u'批量导出数据',self)
                action.triggered.connect(lambda:self.Import_export_ui_show(2))
                self.name.addAction(action)
                action = QAction(QtGui.QIcon('system\\Download_File.ico'),u'选择导出数据',self)
                action.triggered.connect(lambda:self.while_export_shell())
                self.name.addAction(action)

            self.popMenu.exec_(self.tableWidget.mapToGlobal(p))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def while_export_shell(self):  #指定导出数据
        try:
            self.Import_export_ui=Import_export_ui.Import_export_ui()
            self.Import_export_ui.while_export_shell()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def dll_shell(self):  #删除SHELL数据
        try:
            int_model = self.tableWidget.selectionModel()  #获取选中编号
            #model = self.tableWidget.model()#index = model.index(3,1)#data = model.data(index)#print data.toString()
            ok=0
            no=0
            for index in int_model.selectedRows():       #// 对于被选中的每一行
                int_index=index.row()#获取行号
                id= self.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                if tableWidget_work.delete_shell(id):
                    ok=ok+1
                else:
                    no=no+1
            msg.msg_lower_Left(u"删除数据  成功%d条  失败%d条"%(ok,no))
            tableWidget_work.add_tableWidget(str(ui.treeWidget_id))   #加载当前列表
            treeWidget_work.reload_tree()  #加载目录
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))


    def look_type(self):  #读取分类
        try:
            json_data={}
            list_data=[]
            sql_data = "select * from type"   # asc 表示升序 , desc表示降序
            shell_sql.conn.commit()# 获取到游标对象
            cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
            cur.execute(sql_data)# 获取所有结果
            res = cur.fetchall()  #从结果中取出所有记录
            for line in res:
                #self.url_data=line[0]
                s0=u"%s"%(urllib.unquote(str(line[0])))
                #s1=u"%s"%(base64.b64decode(str(line[1])).decode('gb18030').encode('utf-8'))
                s1=u"%s"%(base64.decodestring(str(line[1])))
                json_data.setdefault(s0,s1)
                list_data.append(s1)  #添加数据
                #self.add_child_item(self.tree_i, s1,s0)  #添加数据
            cur.close()  #关闭游标
            return json.dumps(json_data),list_data
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def add_shell_show(self,x):#添加SHELL
        try:
            self.add_shell=add_shell_ui.add_shell_ui()#添加shell
            if x==1:  #添加
                if x==1: #添加数据
                    json_data,list_data=self.look_type()  #读取分类
                    self.add_shell.set_data(title=u'添加数据',siteurl=u'http://',type_id=json_data)
                    self.add_shell.show()
                    #self.add_shell.activateWindow()
                    self.add_shell.insert.connect(tableWidget_work.add_shell)  #响应事件
            if x==2:  #修改
                if self.tableWidget.isItemSelected(self.tableWidget.currentItem()):  #判断是否选中一行
                    row=self.tableWidget.currentItem().row()  #当前选中行
                    type_id=self.tableWidget.item(row,0).text()  #获取某一格内容
                    sql_data = "select * from sitetable where ID='%s'"%(str(type_id))   # asc 表示升序 , desc表示降序
                    shell_sql.conn.commit()# 获取到游标对象
                    cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
                    cur.execute(sql_data)# 获取所有结果
                    res = cur.fetchall()  #从结果中取出所有记录
                    res=res[0]
                    cur.close()  #关闭游标
                    json_data,list_data=self.look_type()  #读取分类
                    if str(res[10])=="":
                        remarks=""
                    else:
                        try:
                            remarks=u"%s"%(base64.decodestring(str(res[10]))) #encodestring编码    解码decodestring
                        except BaseException, e:
                            remarks="except"
                    self.add_shell.set_data(title=u'修改数据',siteurl=u'%s'%(str(res[2])),
                                            type_id=json_data,
                                            id_key=str(res[0]),type_id_key=str(res[1]),sitepass_key=str(res[3]),config_key=base64.decodestring(str(res[6])),coding_key=str(res[7]),script_key=str(res[8]),remarks_key=remarks)
                    self.add_shell.show()
                    self.add_shell.update.connect(tableWidget_work.update_shell)  #响应事件
                #pass
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    ########################################
    ########################################目录右键菜单
    def treeWidget_menu(self,p):  #右键菜单
        try:
            item = self.treeWidget.currentItem()
            if len(unicode(item.text(1)))>=1:
                self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.popMenu = QMenu(self)
                action = QAction(QtGui.QIcon('system\\+.ico'),u'添加分类',self)
                action.triggered.connect(lambda:self.tree_insert_update(1))
                self.popMenu.addAction(action)
                action = QAction(QtGui.QIcon('system\\#.ico'),u'修改分类',self)
                action.triggered.connect(lambda:self.tree_insert_update(2))
                self.popMenu.addAction(action)
                action = QAction(QtGui.QIcon('system\\-.ico'),u'删除分类',self)
                action.triggered.connect(lambda:self.tree_insert_delete())
                self.popMenu.addAction(action)

                # action = QAction(u'列表维护',self)
                # #action.triggered.connect(lambda:self.tree_insert_delete())
                # self.popMenu.addAction(action)

                self.popMenu.exec_(self.treeWidget.mapToGlobal(p))
            else:
                self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.popMenu = QMenu(self)
                action = QAction(QtGui.QIcon('system\\+.ico'),u'添加分类',self)
                action.triggered.connect(lambda:self.tree_insert_update(1))
                self.popMenu.addAction(action)
                self.popMenu.exec_(self.treeWidget.mapToGlobal(p))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def tree_insert_delete(self): #删除目录
        try:
            item = self.treeWidget.currentItem()
            #title = unicode(item.text(0))  %(unicode(item.text(0)))
            customMsgBox=QMessageBox(self)
            customMsgBox.setWindowTitle(u"删除目录")
            lockButton=customMsgBox.addButton(u"确定",QMessageBox.ActionRole)
            unlockButton=customMsgBox.addButton(u"取消",QMessageBox.ActionRole)
            customMsgBox.setText(u"删除目录:  %s"%(unicode(item.text(0))))
            customMsgBox.exec_()
            button=customMsgBox.clickedButton()
            if button==lockButton:
                treeWidget_work.add_tree_delete(unicode(item.text(0)),int(unicode(item.text(1))))  #修改目录
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def tree_insert_update(self,i):  #目录操作
        try:
            item = self.treeWidget.currentItem()
            #title = unicode(item.text(0))
            #print unicode(item.text(0)),unicode(item.text(1))
            self.tree_insert_update_ui=tree_insert_update_ui.tree_insert_update_ui()#添加重命名  目录
            if i==1: #添加
                self.tree_insert_update_ui.set_data(title=u"添加分类",name=u"%s"%(unicode(item.text(0))),ID=unicode(item.text(1)),ico_path="ico/google1.ico")
                if not self.tree_insert_update_ui.isVisible():
                    self.tree_insert_update_ui.show()
                    self.tree_insert_update_ui.Data.connect(treeWidget_work.add_tree_insert)  #响应事件
            if i==2: #修改
                ico_path=treeWidget_work.sql_type_ICO(unicode(item.text(1)))
                self.tree_insert_update_ui.set_data(title=u"修改分类",name=u"%s"%(unicode(item.text(0))),ID=unicode(item.text(1)),ico_path=ico_path)
                if not self.tree_insert_update_ui.isVisible():
                    self.tree_insert_update_ui.show()
                    self.tree_insert_update_ui.Data.connect(treeWidget_work.add_tree_update)  #响应事件
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    ########################################目录右键菜单

    ########################################右下角提示#状态栏
    def createActions(self):#加载菜单
        try:
            self.minimizeAction = QAction(u"最小化", self, triggered=self.hide)
            self.maximizeAction = QAction(u"最大化", self,triggered=self.showMaximized)
            self.restoreAction = QAction(u"还原", self,triggered=self.showNormal)
            self.quitAction = QAction(u"退出", self,triggered=QApplication.instance().quit)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def createTrayIcon(self):
        try:
            self.trayIconMenu = QMenu(self)
            self.trayIconMenu.addAction(self.minimizeAction)
            self.trayIconMenu.addAction(self.maximizeAction)
            self.trayIconMenu.addAction(self.restoreAction)
            self.trayIconMenu.addSeparator()
            self.trayIconMenu.addAction(self.quitAction)

            self.trayIcon = QSystemTrayIcon(self)
            self.trayIcon.setContextMenu(self.trayIconMenu)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def setIcon(self):
        try:
            self.trayIcon.setIcon(QtGui.QIcon("system/main.ico"))
            self.trayIcon.setToolTip("China creation axe")
            self.trayIcon.show()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def showMessage(self):
        try:
            icon = QtGui.QSystemTrayIcon.MessageIcon("1")
            self.trayIcon.showMessage(u'欢迎使用开山斧',u'欢迎您使用开山斧，欢迎\n反馈意见和建议\n请加入qq群 528392695', icon,1000)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))

    def iconActivated(self, reason):
        try:
            if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):  #单击图标反应
                self.showNormal()   #还原
                #triggered=self.showNormal
                #print("111111111111111")
                #显示应该在这里
                # elif reason == QSystemTrayIcon.MiddleClick:
                #     print("22222")
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    ########################################右下角提示#状态栏


