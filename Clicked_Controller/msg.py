#!/usr/local/bin/python
#-*- coding: UTF-8 -*-


from PyQt4 import QtCore, QtGui ,QtNetwork
from PyQt4.QtCore import *
from ctypes import *
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import urllib
import time
import base64

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from Ui_View import ui #UI变量
from Clicked_Controller import log #日志记录
from datetime import datetime, date
#label = None  #消息提示
#import ui
import time
lower_right_data=""
def msg_lower_Left(data):  #左下角提示
    try:
        main_ui=ui.UIManager.get_ui('main_ui')
        #statusBar()  的一些机制可能无法适应多线程情况   导致程序崩溃
        #main_ui.statusBar().showMessage(u"%s TIME:%s"%(data,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))    #self.statusBar().showMessage("1111",3000)
        main_ui.statusbar_label.setText(u"%s TIME:%s"%(data,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        pass

def msg_box(time,name):  #弹出对话框
    window = QtGui.QMainWindow()
    QtGui.QMessageBox.information(window, _fromUtf8(u"%s"%(str(time))),_fromUtf8(u"%s"%(str(name))))#弹出对话框

def msg_time(): #更新提示时间

    try:
        main_ui=ui.UIManager.get_ui('main_ui')

        day_cn = [u'一', u'二', u'三', u'四',u'五', u'六', u'日']
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime(u"%Y-%m-%d", timeArray)
        dayOfWeek = datetime.now().weekday()
        main_ui.time_right.setText(u'星期'+day_cn[dayOfWeek] + u' ' + otherStyleTime)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        pass

def msg_lower_right():  #右下角提示
    try:
        #label = QtGui.QLabel('')  #消息提示
        # label=ui.label
        # main_ui=ui.UIManager.get_ui('main_ui')
        # label.setText(u"%s"%(data))
        # main_ui.statusBar().addWidget(label)
        # main_ui.statusBar().addPermanentWidget(label)
        # global lower_right_data
        # if len(data)>3:
        #     lower_right_data=data
        # else:
        #     data=lower_right_data
        main_ui=ui.UIManager.get_ui('main_ui')
        shell_sql=ui.UIManager.shell_sql
        ###################
        data=reload_tree(shell_sql) #加载目录  数据
        ###################
        id=ui.treeWidget_id
        s1=u"%s"%(base64.decodestring(str(type_id_name(shell_sql,id))))
        main_ui.msg_lower_right.setText(u"<center>--%s%s</center>"%(s1,data))
        msg_time()#更新提示时间
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def reload_tree(shell_sql): #加载目录  数据
    try:
        sql_data = "select * from type"   # asc 表示升序 , desc表示降序
        shell_sql.conn.commit()# 获取到游标对象
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        #######
        sql_data = "select type_id from sitetable"   # asc 表示升序 , desc表示降序
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res2 = cur.fetchall()  #从结果中取出所有记录
        return u"--%d--%d"%(len(res),len(res2))  #右下角提示分类-%d数据-%d
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return "except"

def type_id_name(shell_sql,id):  #右下角提示
    try:
        sql_data = "select * from type where ID='%s'"%(str(id))   # asc 表示升序 , desc表示降序
        shell_sql.conn.commit()# 获取到游标对象
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        res=res[0]
        return str(res[1])
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return "except"

def msg_box(name,data):  #消息提示
    window = QtGui.QMainWindow()
    QtGui.QMessageBox.information(window, _fromUtf8(u"%s"%(name)),  _fromUtf8(u"%s"%(data)))#弹出对话框



