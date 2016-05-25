#!/usr/local/bin/python
#-*- coding: UTF-8 -*-

from PyQt4 import QtCore, QtGui ,QtNetwork
# from PyQt4.QtCore import *
# from ctypes import *
# from PyQt4 import uic
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
#from PyQt4.QtWidgets import *
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

#import Db_Model.Csqlite3  #数据库操作
from Db_Model import db_sqlite3
import time,base64,hashlib

class db_ui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        #加载窗体
        self.ui=uic.loadUi("ui/db_ui.ui", self)  #主窗口
        self.setWindowTitle(u'链接数据操作   代码管理器')  #设置标题
        self.setWindowIcon(QtGui.QIcon("system/main.ico"))  #设置图标
        self.shell=db_sqlite3.C_sqlite3()  #数据
        self.shell.mysqlite3_open()  #链接数据库
#        self.ui.setupUi(self)
        #http://www.cnblogs.com/caomingongli/archive/2011/09/19/2181842.html    这个不错   PyQt之自定义无边框窗口遮盖任务栏显示问题
        flags = 0  #设置禁止最大化
        flags|= Qt.WindowMinimizeButtonHint  #设置禁止最大化
        self.setWindowFlags(flags)  #设置禁止最大化
        #######################################################
        self.update_pushButton.setEnabled(0)  #给改成禁用

        self.script.addItem(QtGui.QIcon('system/script.ico'),_fromUtf8(str("脚本类型")))
        self.script.addItem(QtGui.QIcon('system/php.ico'),_fromUtf8(str("PHP(Eval)")))
        self.script.addItem(QtGui.QIcon('system/asp.ico'),_fromUtf8(str("ASP(Eval)")))
        self.script.addItem(QtGui.QIcon('system/aspx.ico'),_fromUtf8(str("ASPX(Eval)")))
        self.script.addItem(_fromUtf8(str("Customize")))
        self.script.setCurrentIndex(0)

        self.tableWidget.setColumnCount(3)     #列
        self.tableWidget.setRowCount(0)  #行  len(node)
        self.tableWidget.setHorizontalHeaderLabels([u'关键字',u'备注',u'时间'])
        #self.ui.tableWidget.setModel(self.model)
        #self.tableView.resizeColumnsToContents()   #由内容调整列
        self.tableWidget.setColumnWidth(0,90)  #设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(1,100)  #设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(2,150)  #设置表格的各列的宽度值

        for i in range(0):  #调整行高度  len(node)
            self.tableWidget.setRowHeight(i, 23)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)  #设置表格的单元为只读属性，即不能编辑
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows) #点击选择是选择行//设置选中时为整行选中
        #self.tableView.setSelectionMode(QTableWidget.SingleSelection)  #禁止多行选择
        self.tableWidget.setAlternatingRowColors(True)  #还是只可以选择单行（单列）
        self.tableWidget.verticalHeader().hide() #隐藏行头

        self.form=""   #FORM表名
        self.name_data='关键字'
        self.name_feil_md5=[]  #MD5
        self.remarks_data='备注'
        self.remarks_feil_md5=[]  #MD5
        self.data_data='代码'
        self.data_feil_md5=[]  #MD5
        self.name_textEdit.setText(u'%s'%(self.name_data))
        self.remarks_textEdit.setText(u'%s'%(self.remarks_data))
        self.data_textEdit.setText(u'%s'%(self.data_data))
        #######################################################
        self.script.currentIndexChanged.connect(self.currentIndex)  #查询当前选择
        self.tableWidget.cellDoubleClicked.connect(self.open_eval)  #双击
        self.data_textEdit.textChanged.connect(self.GetExt)  #代码
        self.name_textEdit.textChanged.connect(self.GetExt)  #关键字
        self.remarks_textEdit.textChanged.connect(self.GetExt)  #备注
        self.insert_pushButton.clicked.connect(self.insert_data)  #添加
        self.update_pushButton.clicked.connect(self.update_data)  #修改
        self.delete_pushButton.clicked.connect(self.delete_data)  #删除
        #######################################################

    def insert_data(self):  #添加数据
        name_textEdit=unicode(QtCore.QString(self.name_textEdit.toPlainText())) #名称
        remarks_textEdit=unicode(QtCore.QString(self.remarks_textEdit.toPlainText())) #备注
        data_textEdit=unicode(QtCore.QString(self.data_textEdit.toPlainText())) #代码
        #config=base64.encodestring(str(config)) #encodestring编码    解码decodestring
        sql="insert into %s(TYPE,data,remarks,createtime) VALUES('%s','%s','%s','%s')"%\
            (str(self.form),str(name_textEdit),base64.encodestring(str(data_textEdit)),base64.encodestring(str(remarks_textEdit)),str(time.time()))
        if self.shell.mysqlite3_insert(sql):
            QtGui.QMessageBox.information(self, _fromUtf8(u"操作提示"),  _fromUtf8(u"添加数据成功"))#弹出对话框
            self.open_sql(str(self.form))
        else:
            QtGui.QMessageBox.information(self, _fromUtf8(u"操作提示"),  _fromUtf8(u"添加数据失败"))#弹出对话框

    def update_data(self):  #修改数据
        name_textEdit=unicode(QtCore.QString(self.name_textEdit.toPlainText())) #名称
        remarks_textEdit=unicode(QtCore.QString(self.remarks_textEdit.toPlainText())) #备注
        data_textEdit=unicode(QtCore.QString(self.data_textEdit.toPlainText())) #代码
        sql="update %s set data='%s',remarks='%s',createtime='%s' where TYPE='%s'"% \
            (str(self.form),base64.encodestring(str(data_textEdit)),base64.encodestring(str(remarks_textEdit)),str(time.time()),str(name_textEdit))
        if self.shell.mysqlite3_update(sql):
            QtGui.QMessageBox.information(self, _fromUtf8(u"操作提示"),  _fromUtf8(u"修改数据成功"))#弹出对话框
            self.open_sql(str(self.form))
        else:
            QtGui.QMessageBox.information(self, _fromUtf8(u"操作提示"),  _fromUtf8(u"修改数据失败"))#弹出对话框

    def delete_data(self):  #删除数据
        name_textEdit=unicode(QtCore.QString(self.name_textEdit.toPlainText())) #名称
        sql="delete from %s where TYPE='%s'"% \
            (str(self.form),str(name_textEdit))
        if self.shell.mysqlite3_delete(sql):
            QtGui.QMessageBox.information(self, _fromUtf8(u"操作提示"),  _fromUtf8(u"删除数据成功"))#弹出对话框
            self.open_sql(str(self.form))
        else:
            QtGui.QMessageBox.information(self, _fromUtf8(u"操作提示"),  _fromUtf8(u"删除数据失败"))#弹出对话框

    def GetExt(self):
        # self.name_feil_md5=[]  #MD5
        # self.remarks_feil_md5=[]  #MD5
        # self.data_feil_md5=[]  #MD5
        try:
            name_textEdit=unicode(QtCore.QString(self.name_textEdit.toPlainText())) #名称
            feil_md5_name = self.getfilemd5(name_textEdit)
            remarks_textEdit=unicode(QtCore.QString(self.remarks_textEdit.toPlainText())) #备注
            feil_md5_remarks = self.getfilemd5(remarks_textEdit)
            data_textEdit=unicode(QtCore.QString(self.data_textEdit.toPlainText())) #代码
            feil_md5_data = self.getfilemd5(data_textEdit)
            #if (int(feil_md5_data[0]==int(self.data_feil_md5[0]))and(int(feil_md5_remarks[0])==int(self.remarks_feil_md5[0]))and(int(feil_md5_name[0]))==int(self.name_feil_md5[0])):
            if (str(feil_md5_data[1]).lower()==str(self.data_feil_md5[1]).lower())or(str(feil_md5_remarks[1]).lower()==str(self.remarks_feil_md5[1]).lower())or(str(feil_md5_name[1]).lower()==str(self.name_feil_md5[1]).lower()):
                self.update_pushButton.setEnabled(1)  #给改成禁用
        except BaseException, e:
            pass

    def getfilemd5(self, filedata):
        if not filedata:
            return [0, ""]
        bres = 0
        strmd5 = ""
        try:
            md5 = hashlib.md5()
            md5.update(filedata)
            strmd5 = md5.hexdigest()
            bres = 1
        except:
            pass
        return [bres, strmd5]

    def open_eval(self,row,column):   #获取代码
        ID=self.tableWidget.item(int(row),0).text()  #获取某一格内容
        sql_data = "select * from %s where TYPE='%s'"%(self.form,str(ID))   # asc 表示升序 , desc表示降序
        self.shell.conn.commit()# 获取到游标对象
        cur = self.shell.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        res=res[0]
        cur.close()  #关闭游标
        if not str(res[0])=="None":
            self.name_textEdit.setText(u'%s'%(res[0]))  #名称
            self.name_data=u'%s'%(res[0])
            self.name_feil_md5 = self.getfilemd5(self.name_data)
        else:
            self.name_feil_md5 = self.getfilemd5("")
        #config=base64.encodestring(str(config)) #encodestring编码    解码decodestring
        if not str(res[1])=="None":
            s1=u"%s"%(base64.decodestring(str(res[1])))#代码
            self.data_textEdit.setText(u'%s'%(s1))  #代码
            self.data_data=u'%s'%(s1)
            self.data_feil_md5 = self.getfilemd5(self.data_data)
        else:
            self.data_feil_md5 = self.getfilemd5("")

        if not str(res[2])=="None":
            s2=u"%s"%(base64.decodestring(str(res[2])))#备注
            self.remarks_textEdit.setText(u'%s'%(s2))  #备注
            self.remarks_data=u'%s'%(s2)
            self.remarks_feil_md5 = self.getfilemd5(self.remarks_data)
        else:
            self.remarks_feil_md5 = self.getfilemd5("")

    def currentIndex(self,id):
        if int(id)==1:
            self.form="PHP"
            self.open_sql("PHP")
        if int(id)==2:
            self.form="ASP"
            self.open_sql("ASP")
        if int(id)==3:
            self.form="ASPX"
            self.open_sql("ASPX")
        if int(id)==4:
            self.form="Customize"
            self.open_sql("Customize")

    def open_sql(self,name):
        sql_data = "select * from %s"%(name)   # asc 表示升序 , desc表示降序
        self.shell.conn.commit()# 获取到游标对象
        cur = self.shell.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        i=0
        self.tableWidget.setRowCount(len(res))  #行  len(node)
        for line in res:
            s1=u"%s"%(str(line[0]))
            self.tableWidget_add(0,i,s1)
            #config=base64.encodestring(str(config)) #encodestring编码    解码decodestring
            if not str(line[2])=="None":
                s2=u"%s"%(base64.decodestring(str(line[2])))
                self.tableWidget_add(1,i,s2)
            x = time.localtime(round(float(str(line[3]))))
            createtime=time.strftime('%Y/%m/%d %H:%M:%S',x)
            s3=u"%s"%(str(createtime))
            self.tableWidget_add(2,i,s3)
            i=i+1
        cur.close()  #关闭游标

        #添加数据
    def tableWidget_add(self,x, y,title):
        #main_ui.tableWidget.setRowCount(main_ui.tableWidget.rowCount()+1)  #行  len(node)  #加一行
        item = QTableWidgetItem()
        item.setText(title)
        self.tableWidget.setItem(y, x, item)

if __name__=="__main__":
    import sys
    #app=QtWidgets.QApplication(sys.argv)
    app=QtGui.QApplication(sys.argv)
    myshow=db_ui()
    myshow.show()
    #db_ui()
    sys.exit(app.exec_())


