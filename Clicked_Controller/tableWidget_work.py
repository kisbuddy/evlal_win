#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#shell编辑
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

import msg #消息提示
import treeWidget_work  #目录列表
from Clicked_Controller import threadpool #线程操作
from Db_Model import db_shell #常用数据库操作
from Clicked_Controller import link_shell  #链接SHELL等操作
from Clicked_Controller import eval_link  #链接SHELL
from Clicked_Controller import ip_query #ip数据库
from Clicked_Controller import log #日志记录
from Clicked_Controller import g #公共文件
#from ui import * #UI变量
from Ui_View import ui #UI变量
import os

main_ui = None
shell_sql = None

#shell编辑
def add_shell(siteurl,sitepass,config,remarks,type_id,script,coding):  #添加数据
    try:
        global treeWidget_id  #当前选择ID
        # siteurl #URL
        # sitepass  #密码
        # config   #配置
        # remarks  备注
        # type_id #类别
        # script  #脚本类型  asp   php
        # coding   #编码方式
        config=base64.encodestring(str(config)) #encodestring编码    解码decodestring
        remarks=base64.encodestring(u"%s"%(remarks)) #encodestring编码    解码decodestring
        # sql_data="insert into sitetable(type_id,siteurl,sitepass,config,remarks,script,coding,createtime) " \
        #          "VALUES((select ID from type where name='%s'),'%s','%s','%s','%s','%s','%s','%s')"\
        #          %(base64.encodestring(str(type_id)),siteurl,sitepass,config,remarks,script,coding,str(time.time()))
        sql_data="insert into sitetable(type_id,siteurl,sitepass,link,config,remarks,script,coding,createtime) " \
                 "VALUES(%s,'%s','%s','%s','%s','%s','%s','%s','%s')" \
                 %(str(type_id),siteurl,sitepass,"2",config,remarks,script,coding,str(time.time()))
        if shell_sql.mysqlite3_insert(sql_data):
            #加载目录之前先加载SHELL列表
            add_tableWidget(str(ui.treeWidget_id))   #加载当前列表
            treeWidget_work.reload_tree()  #加载目录
            msg.msg_lower_Left(u"添加SHELL  url:%s   成功"%(str(siteurl)))  #右下角提示
            main_ui.tableWidget.scrollToBottom()   #定位到列表最下面
        else:
            msg.msg_lower_Left(u"添加SHELL  url:%s   失败"%(str(siteurl)))  #右下角提示
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def update_shell(id,siteurl,sitepass,config,remarks,type_id,script,coding):  #修改数据
    try:
        #print id,siteurl,sitepass,config,remarks,type_id,script,coding
        config=base64.encodestring(str(config)) #encodestring编码    解码decodestring
        remarks=base64.encodestring(u"%s"%(remarks)) #encodestring编码    解码decodestring
        sql_data="update sitetable set siteurl='%s',sitepass='%s',config='%s',remarks='%s',type_id='%s',script='%s',coding='%s' where ID='%s'"% \
                 (siteurl,sitepass,config,remarks,str(type_id),script,coding,str(id))
        if shell_sql.mysqlite3_update(sql_data):
            #加载目录之前先加载SHELL列表
            add_tableWidget(str(ui.treeWidget_id))   #加载当前列表
            treeWidget_work.reload_tree()  #加载目录
            msg.msg_lower_Left(u"修改SHELL  url:%s   成功"%(str(siteurl)))  #右下角提示
        else:
            msg.msg_lower_Left(u"修改SHELL  url:%s   失败"%(str(siteurl)))  #右下角提示
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def delete_shell(type_id):   #删除数据
    try:
        sql_data="delete from sitetable where ID='%s'"%(str(type_id))
        return shell_sql.mysqlite3_delete(sql_data)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
##################################
def add_tableWidget(id):   #查询数据 在添加
    try:
        sql_data = "select * from sitetable WHERE type_id='%s' order by `updatetime` desc"%(str(id))   # asc 表示升序 , desc表示降序
        shell_sql.conn.commit()# 获取到游标对象
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        cur.close()  #关闭游标
        add_list_tableWidget(res)# 添加数据
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def add_find_shell_tableWidget(id,url):  #模糊查询SHELL
    try:
        sql_data = "select * from sitetable WHERE(type_id='%s' and siteurl like '%s') order by `updatetime` desc"%(str(id),"%"+str(url)+"%")   # asc 表示升序 , desc表示降序
        shell_sql.conn.commit()# 获取到游标对象
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        cur.close()  #关闭游标
        add_list_tableWidget(res)# 添加数据
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))


def add_list_tableWidget(res): #数组添加SHELL
    try:
        main_ui.tableWidget.clearContents()  #清空
        i=0
        main_ui.tableWidget.setRowCount(len(res))  #行  len(node)

        for line in res:
            #LINK 颜色提亮
            if int(line[4])==0:
                color=QColor(255, 0, 0)   #红色0链接失败
            elif int(line[4])==1:
                color=QColor(0, 0, 0)   #黑色1链接成功
            elif int(line[4])==2:
                color=QColor(128, 128, 128)   #灰色2还未测试
            else:
                color=QColor(184, 134, 11)   #金黄菊 变量为空
            #引入链接类型
            #list_script=["PHP(Eval)","ASP(Eval)","ASPX(Eval)","Customize"]
            if int(line[8])==1:
                ASP_PHP_NET_ico='system/php.ico'
            elif int(line[8])==2:
                ASP_PHP_NET_ico='system/asp.ico'
            elif int(line[8])==3:
                ASP_PHP_NET_ico='system/aspx.ico'
            elif int(line[8])==4:
                ASP_PHP_NET_ico='system/customize.ico'
            else:
                ASP_PHP_NET_ico='system/customize.ico'
            #LINK  0链接失败 1链接成功  2还未测试   颜色提亮
            if int(line[4])==0:
                LINK_ICO='system/link_0.ico'
            elif int(line[4])==1:
                LINK_ICO='system/link_1.ico'
            elif int(line[4])==2:
                LINK_ICO='system/link_2.ico'
            else:
                LINK_ICO='system/link_3.ico'
            tableWidget_add(0,i,title=str(line[0]),color=color)  #自动编号
            tableWidget_add(1,i,ico=ASP_PHP_NET_ico)  #类型
            tableWidget_add(2,i,title=str(line[2]),color=color,ico=LINK_ICO)  #网址

            if GetData(str(line[5]))=='':
                ip=""
            else:
                ip="%s/%s"%(ip_query.geoip2_ip_Physical_information(str(line[5])),str(line[5]))
            country=ip_query.geoip2_ip_country(str(line[5]))
            country_country_ico="system/country_ico/%s.ico"%(country)
            if not if_file_path(country_country_ico):
                country_country_ico="system/country_ico/except.ico"
                ip="%s-%s"%(str(country),ip)
            if not if_file_path(country_country_ico):
                country_country_ico=""
            if len(ip)<=5:
                tableWidget_add(3,i,title=str(ip),color=color)  #ip地址
            else:
                tableWidget_add(3,i,title=str(ip),color=color,ico=country_country_ico)  #ip地址

            if str(line[10])=="":
                remarks=""
            else:
                try:
                    remarks=u"%s"%(base64.decodestring(str(line[10]))) #encodestring编码    解码decodestring
                except BaseException, e:
                    remarks="except"
            if line[13]:  #操作系统
                os_ico="system/os_ico/%s.ico"%(str(line[13]))
                tableWidget_add(4,i,title=str(remarks),color=color,ico=os_ico)  #备注
            else:
                tableWidget_add(4,i,title=str(remarks),color=color)  #备注
            if line[11]:
                x = time.localtime(round(float(str(line[11]))))
                createtime=time.strftime('%Y/%m/%d %H:%M:%S',x)
            else:
                createtime=""
            tableWidget_add(5,i,title=str(createtime),color=color)  #添加时间
            if line[12]:
                x = time.localtime(round(float(str(line[12]))))
                createtime=time.strftime('%Y/%m/%d %H:%M:%S',x)
            else:
                createtime=""
            tableWidget_add(6,i,title=str(createtime),color=color)  #修改时间
            i=i+1
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def if_file_path(file):  #判断文件是否存在
    try:
        if os.path.isfile(str(file)):
            return 1
        else:
            return 0
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return 0

import Queue
import thread
list_ID = Queue.Queue()
I_OK=0
I_NO=0
I_G=0 #
shell_on_off=0

def shell_cs_thread():  #线程
    try:
        global I_OK,I_NO,list_ID,I_G,shell_on_off
        #list_ID=[]
        int_model = main_ui.tableWidget.selectionModel()  #获取选中编号
        if len(int_model.selectedRows())==1:
            msg.msg_box(u"操作提示",u"请选择>=2条数据测试！")
            return
        for index in int_model.selectedRows():       #// 对于被选中的每一行
            try:
                int_index=index.row()#获取行号
                ID=main_ui.tableWidget.item(int(int_index),0).text()  #获取某一格内容
                #list_ID.append(str(ID))  #添加数据
                list_ID.put(str(ID), 0.1)
            except BaseException, e:
                print str(e)
                log.logging.debug("except:%s"%(str(e)))
        try:
            # t_h_Thread = threadpool.ThreadPool(1)   #创建多线程  线程池
            # #t_h_Thread.push(shell_cs,list_ID) #"Upload_files"
            # t_h_Thread.push(shell_cs,"") #"Upload_files"
            # t_h_Thread.wait_for_idel(1)
            #threads = []  # 线程
            if list_ID.qsize() >= 300:
                x=10
            elif list_ID.qsize() >= 100:
                x=5
            elif list_ID.qsize() >= 50:
                x=3
            elif list_ID.qsize() <= 10:
                x=2
            else:
                x=1

            I_G=list_ID.qsize()  #共多少条数据
            shell_on_off=0
            I_OK=0
            I_NO=0
            data=u"正在开启%s 个线程测试中 %s条数据需要测试  请等待"%(str(x),str(list_ID.qsize()))#设置状态栏文字信息
            msg.msg_lower_Left(data)#设置状态栏文字信息
            for i in range(x):  # nthreads=10  创建10个线程
                #thread.start_new_thread(shell_cs,(str(i+1),))  #
                ###############################
                # work = Worker_Thread(name="uix0",var1=str(i+1))
                # work.Finish2.connect(shell_cs)
                # work.start()
                ###############################
                t_h_Thread = threadpool.ThreadPool(1)   #创建多线程  线程池
                #t_h_Thread.push(shell_cs,list_ID) #"Upload_files"
                t_h_Thread.push(shell_cs,str(i+1)) #"Upload_files"
                t_h_Thread.wait_for_idel(1)
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

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


def shell_cs(x_ID):  #SHELL测试
    try:
        global I_OK,I_NO,list_ID,I_G,shell_on_off
        #for i in range(0, len(list_ID)):
        #id=list_ID[i]
        while True:
            try:
                id = list_ID.get(0.5)
                if not id:
                    break #跳出
                if list_ID.empty():   #判断队列是否为空
                    break #跳出
                id_shell_list=db_shell.id_sitetable_shell(str(id))  #通过ID查询SHELL的状态
                #siteurl=str(id_shell_list[2])    #    网址
                script=str(id_shell_list[8])      #   asp   php
                # if script=="PHP":
                #     psot_data=link_shell.post_php_data(str("@ini_set(\"display_errors\",\"0\");@set_time_limit(0);@set_magic_quotes_runtime(0);echo(\"->|\");echo(\"webxscan\");echo(\"|<-\");die();"))
                # elif script=="ASP":
                #     psot_data="=execute(\"response.clear:response.write(\"\"webxscan\"\"):response.end\")"
                # else:
                #     psot_data="=Response.Clear();Response.Write(\"webxscan\");"
                if script=="PHP":
                    psot_data=link_shell.GetPostText(script,"WebRoot")    #获取代码
                    psot_data=link_shell.post_php_data(psot_data)  #转换代码
                if script=="ASP":
                    psot_data=link_shell.GetPostText(script,"WebRoot")    #获取代码
                if script=="ASPX":
                    psot_data=link_shell.GetPostText(script,"WebRoot")    #获取代码
                FALSE_bool,Info=eval_link.Post_eval_php(str(id),psot_data) #获取 请求内容
                if FALSE_bool==0:
                    I_NO+=1
                    db_shell.SELECT_shell_link(str(id),0) #更新链接状态  0链接失败 1链接成功  2还未测试
                    sql_data="update sitetable set os='%s' where ID='%s'"%(str(""),str(id))
                else:
                    I_OK+=1
                    db_shell.SELECT_shell_link(str(id),1) #更新链接状态  0链接失败 1链接成功  2还未测试
                    OS_data=g.if_os(Info)
                    if OS_data=="":  #操作系统
                        #空
                        sql_data="update sitetable set os='%s' where ID='%s'"%(str("except"),str(id))
                    else:
                        #判断到操作系统
                        sql_data="update sitetable set os='%s' where ID='%s'"%(str(OS_data),str(id))
                if shell_sql.mysqlite3_update(sql_data):
                    pass
                    #msg.msg_lower_right(u"修改目录:%s 成功"%(str(name)))  #右下角提示
                else:
                    pass

                    # if(Info.find("webxscan") >= 0):
                    #     I_OK+=1
                    #     db_shell.SELECT_shell_link(str(id),1) #更新链接状态  0链接失败 1链接成功  2还未测试
                    #     db_shell.SELECT_shell_updatetime(str(id),str(siteurl))
                    # else:
                    #     I_NO+=1
                    #     db_shell.SELECT_shell_link(str(id),0) #更新链接状态  0链接失败 1链接成功  2还未测试
                if shell_on_off==0:
                    data=u"Thread:%d  shell测试   成功:%d  失败:%d  还有%d条需要测试  共计%d条"%(int(x_ID),int(I_OK),int(I_NO),int(I_G)-(int(I_OK)+int(I_NO)),int(I_G))#设置状态栏文字信息
                    #print data
                    msg.msg_lower_Left(data)#设置状态栏文字信息
            except BaseException, e:
                pass
        if shell_on_off==0:
            data=u"shell测试完成   成功:%d  失败:%d  共计%d条"%(int(I_OK),int(I_NO),int(I_G))#设置状态栏文字信息
            #print data
            msg.msg_lower_Left(data)#设置状态栏文字信息
            shell_on_off=1
            add_tableWidget(str(ui.treeWidget_id))   #加载当前列表
        #time.sleep(2000)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def GetData(Data):#该函数用于防止数据为空时显示None
    try:
        EndData=_fromUtf8(str(Data))
        if EndData=="None":
            EndData=""
        return (EndData)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
#添加数据
def tableWidget_add(x, y,**kwargs):
    try:
        #main_ui.tableWidget.setRowCount(main_ui.tableWidget.rowCount()+1)  #行  len(node)  #加一行
        item = QTableWidgetItem()
        if "ico" in kwargs:  #ICO 图标
            if if_file_path(str(kwargs['ico'])): #文件存在则添加
                item.setIcon(QtGui.QIcon(u'%s'%(kwargs['ico'])))
        if(("title" in kwargs) and (not GetData(kwargs['title'])=='')):  #内容
            item.setText(u'%s'%(kwargs['title']))
        if "color" in kwargs:  #颜色
            item.setTextColor(kwargs['color']) #字体变色
        if not(x==1 or x==2):
            item.setTextAlignment(Qt.AlignCenter)#设置字体居中
        main_ui.tableWidget.setItem(y, x, item)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
##################################
#列表操作
def tableWidget_ini():
    try:
        global main_ui
        global shell_sql
        main_ui=ui.UIManager.get_ui('main_ui')
        shell_sql=ui.UIManager.shell_sql
        main_ui.tableWidget.setColumnCount(7)     #列
        main_ui.tableWidget.setRowCount(0)  #行  len(node)
        main_ui.tableWidget.setHorizontalHeaderLabels([u'ID',u'-',u'网址',u'IP/物理位置',u'备注',u'insert',u'update'])
        #self.ui.tableWidget.setModel(self.model)
        #self.tableView.resizeColumnsToContents()   #由内容调整列
        main_ui.tableWidget.setColumnWidth(0,0)  #设置表格的各列的宽度值
        main_ui.tableWidget.setColumnWidth(1,28)  #设置表格的各列的宽度值
        main_ui.tableWidget.setColumnWidth(2,300)  #设置表格的各列的宽度值
        main_ui.tableWidget.setColumnWidth(3,255)  #设置表格的各列的宽度值
        main_ui.tableWidget.setColumnWidth(4,90)  #设置表格的各列的宽度值
        main_ui.tableWidget.setColumnWidth(5,165)  #设置表格的各列的宽度值
        main_ui.tableWidget.setColumnWidth(6,165)  #设置表格的各列的宽度值

        for i in range(0):  #调整行高度  len(node)
            main_ui.tableWidget.setRowHeight(i, 23)
        main_ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)  #设置表格的单元为只读属性，即不能编辑
        main_ui.tableWidget.setSelectionBehavior(QTableWidget.SelectRows) #点击选择是选择行//设置选中时为整行选中
        #main_ui.tableWidget.setSelectionMode(QTableWidget.SingleSelection)  #禁止多行选择
        main_ui.tableWidget.setAlternatingRowColors(True)  #还是只可以选择单行（单列）
        main_ui.tableWidget.verticalHeader().hide() #隐藏行头
        ##################################
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))