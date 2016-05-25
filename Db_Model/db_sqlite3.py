#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#数据库连接
################################################
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import sqlite3
import threading
from Clicked_Controller import log #日志记录
import thread
import ConfigParser  #INI读取数据
import os

class C_sqlite3():
    def __init__(self):
        self.db="system/shell.db" #self.cur_file_dir()+

    def mysqlite3_open(self):
        try:
            #self.conn = sqlite3.connect(self.db)
            self.conn = sqlite3.connect(self.db,check_same_thread = False)
            self.conn.isolation_level = None #这个就是事务隔离级别，默认是需要自己commit才能修改数据库，置为None则自动每次修改都提交,否则为""
            #OperationalError: Could not decode to UTF-8 column 'name' with text '国内其他' 解决方法如下
            self.conn.text_factory = str #注意在连接后添加此语句即可

        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            print u"连接数据库:",self.db,u"登录服务器失败###"

    def mysqlite3_close(self):  #关闭数据库
        try:
            self.conn.close()
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            print u"关闭数据异常"
            return 0

#    def mysqlite3_select(self):  #查询数据
#        try:
#            self.conn.commit()# 获取到游标对象
#            cur = self.conn.cursor()# 用游标来查询就可以获取到结果
#            cur.execute("select * from TCP_port")# 获取所有结果
#            res = cur.fetchall()  #从结果中取出所有记录
#            for line in res:
#                for f in line:
#                    print f,
#                print
#            print '-'*60
#            cur.close()  #关闭游标
#        except:
#            print u"查询数据异常"
#
#    def mysqlite3_insert(self,data):  #添加数据
#        try:
#            return self.conn.execute(data)
#        except:
#            print u"添加数据异常"

    def mysqlite3_select(self,data):  #查询数据
        try:
           # print data
            self.conn.commit()# 获取到游标对象
            cur = self.conn.cursor()# 用游标来查询就可以获取到结果
            cur.execute(data)# 获取所有结果
            res = cur.fetchall()  #从结果中取出所有记录
            for line in res:
                self.url_data=line[0]
            cur.close()  #关闭游标
            return self.url_data
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            print "查询数据异常"
            return "null123456"

    def mysqlite3_insert(self,data):  #添加数据
        try:
            self.conn.execute(data)
            return 1
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            #print(str(e))
            #print u"添加数据异常",data
            return 0

    def mysqlite3_update(self,data):  #修改数据
        try:
            self.conn.execute(data)
            return 1
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            #print u"修改数据异常"
            return 0

    def mysqlite3_delete(self,data):  #删除数据
        try:
            self.conn.execute(data)
            return 1
        except BaseException, e:
            log.logging.debug("except:%s"%(str(e)))
            #print "删除数据异常"
            return 0

if __name__=='__main__':
    new=C_sqlite3()
    new.mysqlite3_open()
    print new.mysqlite3_insert("insert into www(url,time) VALUES('111','222')")

#    mysql_handle.__init__('localhost','root','316118740','urldata')
#    mysql.mysql_open()  #连接数据库
#    TH_OPURL=CS_openurl()
#    TH_OPURL.start()
#    threads = []  #线程
#    nthreads=5
#    for i in range(nthreads):  #nthreads=10  创建10个线程
#        threads.append(C_sqlite3(i))
#
#    for thread in threads:   #不理解这是什么意思    是结束线程吗
#        thread.start()  #start就是开始线程

