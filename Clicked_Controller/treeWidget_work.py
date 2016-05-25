#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#目录操作
from PyQt4.QtCore import *
from ctypes import *
from PyQt4.QtGui import *
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
import urllib
import base64


#from ui import * #UI变量
from Ui_View import ui  #UI变量
from Clicked_Controller import log #日志记录
import msg #消息提示
import tableWidget_work  #SHELL操作

main_ui = None
shell_sql = None

#目录操作
def add_tree_insert(name,x,ico_path):  #添加目录
    try:
        #item = self.ui.treeWidget.currentItem()    #获取当前选择
        sql_data="insert into type(name,createtime,ico_path) VALUES('%s','%s','%s')"%(str(base64.encodestring(str(name))),str(time.time()),str(base64.encodestring(str(ico_path))))
        if shell_sql.mysqlite3_insert(sql_data):
            reload_tree()  #加载目录
            msg.msg_lower_Left(u"加载目录:%s 成功"%(str(name)))  #右下角提示
        else:
            msg.msg_lower_Left(u"加载目录:%s 失败"%(str(name)))  #右下角提示
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def add_tree_update(name,x,ico_path):  #修改目录
    try:
        sql_data="update type set name='%s',createtime='%s',ico_path='%s' where ID='%s'"%(str(base64.encodestring(str(name))),str(time.time()),str(base64.encodestring(str(ico_path))),str(x))
        if shell_sql.mysqlite3_update(sql_data):
            reload_tree()  #加载目录
            tableWidget_work.add_tableWidget(str(ui.treeWidget_id))   #加载当前列表
            msg.msg_lower_Left(u"修改目录:%s 成功"%(str(name)))  #右下角提示
        else:
            msg.msg_lower_Left(u"修改目录:%s 失败"%(str(name)))  #右下角提示
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def add_tree_delete(name,x):  #删除目录
    try:
        if str(x)==u"0":
            msg.msg_box(u"目录操作提示",u"不能删除默认目录/只能修改名称！")
        else:
            sql_data="update  sitetable set type_id='0' where type_id='%s'"%(str(x))
            if shell_sql.mysqlite3_update(sql_data):
                sql_data="delete from type where ID='%s'"%(str(x))
                if shell_sql.mysqlite3_delete(sql_data):
                    reload_tree()  #加载目录
                    msg.msg_lower_Left(u"删除目录:%s 成功"%(str(name)))  #右下角提示
                    tableWidget_work.add_tableWidget("0")   #查询数据 在添加##########################################
                else:
                    msg.msg_lower_Left(u"删除目录:%s 失败"%(str(name)))  #右下角提示
            else:
                msg.msg_lower_Left(u"SHELL目录转移失败"%(str(name)))  #右下角提示
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
#############
def reload_tree():  #加载目录
    try:
        global main_ui
        global shell_sql
        main_ui=ui.UIManager.get_ui('main_ui')
        shell_sql=ui.UIManager.shell_sql
        main_ui.treeWidget.clear()  #清空
        tree_i = add_top_item(u'站点类别','system/main.ico')
        tree_i.setExpanded(True)
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
            s2="%s"%(base64.decodestring(str(line[2])))
            tx=cx_sitetable_type_id(s0)  #查询type_id数量
            add_child_item(tree_i, s1,s0,tx,s2)  #添加数据
        cur.close()  #关闭游标
        ###########
        # sql_data = "select type_id from sitetable"   # asc 表示升序 , desc表示降序
        # cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        # cur.execute(sql_data)# 获取所有结果
        # res2 = cur.fetchall()  #从结果中取出所有记录
        # msg.msg_lower_right(u"分类(%d)数据(%d)"%(len(res),len(res2)))  #右下角提示
        msg.msg_lower_right()  #右下角提示
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def cx_sitetable_type_id(id):  #查询type_id数量
    try:
        # 你的代码
        sql_data = "select type_id from sitetable WHERE type_id ='%s'"%(str(id))   # asc 表示升序 , desc表示降序
        #self.shell_sql.conn.commit()# 获取到游标对象
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        return len(res)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return 0

def sql_type_ICO(id):   #查询指定ID  ICO
    try:
        # 你的代码
        sql_data = "select ico_path from type where ID='%s'"%(str(id))   # asc 表示升序 , desc表示降序
        shell_sql.conn.commit()# 获取到游标对象
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        s2="%s"%(base64.decodestring(str(res[0][0])))
        return s2
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return ""

import os
def if_file_path(file):  #判断文件是否存在
    try:
        if os.path.isfile(str(file)):
            return 1
        else:
            return 0
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return 0

def add_child_item(item, title,id,tx,ico):  #添加子项
    try:
        subitem = QTreeWidgetItem()
        try:  # 你的代码
            if if_file_path(str(ico)): #文件存在则添加
                subitem.setIcon(0,QtGui.QIcon(str(ico)))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            pass
        subitem.setText(0, title)
        subitem.setText(1, id)
        subitem.setText(2, "(%s)"%(str(tx)))
        item.addChild(subitem)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def add_child_item1(item, title,ico):  #添加子项
    try:
        subitem = QTreeWidgetItem()
        try:  # 你的代码
            subitem.setIcon(0,QtGui.QIcon(str(ico)))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
        subitem.setText(0, title)
        item.addChild(subitem)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def add_top_item(title,ico):  #添加目录
    try:
        item = QTreeWidgetItem()
        try:  # 你的代码
            item.setIcon(0,QtGui.QIcon(str(ico)))
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
        item.setText(0, title)
        main_ui.treeWidget.addTopLevelItem(item)
        return item
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def del_take_Top(y):  #去除节点
    try:
        main_ui.treeWidget.takeTopLevelItem(y)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

