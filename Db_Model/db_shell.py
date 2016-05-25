#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
import time
from Ui_View import ui #UI变量
from Clicked_Controller import g #公用文件
from Clicked_Controller import ip_query #显示IP地址
from Clicked_Controller import log #日志记录
#main_ui = None
shell_sql = None

def id_sitetable_shell(ID):  #通过ID查询SHELL的状态
    try:
        #global main_ui
        global shell_sql
        #main_ui=ui.UIManager.get_ui('main_ui')
        shell_sql=ui.UIManager.shell_sql
        sql_data = "select * from sitetable where ID='%s'"%(str(ID))   # asc 表示升序 , desc表示降序
        shell_sql.conn.commit()# 获取到游标对象
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        res = cur.fetchall()  #从结果中取出所有记录
        res=res[0]
        cur.close()  #关闭游标
        list_res=[]   #返回内容
        id=str(res[0])         #自动编号
        list_res.append(id) #添加数据

        type_id=str(res[1])    #      类别
        list_res.append(type_id) #添加数据

        siteurl=str(res[2])    #    网址
        list_res.append(siteurl) #添加数据

        sitepass=str(res[3])   #    密码
        list_res.append(sitepass) #添加数据

        ip=str(res[4])         #链接状态
        list_res.append(ip) #添加数据

        ip=str(res[5])         #    ip地址
        list_res.append(ip) #添加数据

        config=str(res[6])     #    配置
        list_res.append(config) #添加数据

        coding=str(res[7])     #  编码方式
        list_res.append(coding) #添加数据

        script=g.id_webx(str(res[8]))      #   asp   php
        list_res.append(script) #添加数据
        return list_res
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return []

def SELECT_shell_updatetime(id,url):   #更新shell时间  updatetime     修改时间   最后一次访问时间
    try:
        global shell_sql
        #main_ui=UIManager.get_ui('main_ui')
        shell_sql=ui.UIManager.shell_sql
        url_ip=ip_query.www_ping_ip(ip_query.url_www(str(url)))  #获取URL ip
        sql_data="update sitetable set updatetime='%s',ip='%s' where ID='%s'"%(str(time.time()),str(url_ip),str(id))
        if shell_sql.mysqlite3_update(sql_data):
            pass
            #msg.msg_lower_right(u"修改目录:%s 成功"%(str(name)))  #右下角提示
        else:
            pass
            #msg.msg_lower_right(u"修改目录:%s 失败"%(str(name)))  #右下角提示
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def SELECT_shell_link(id,link):   #更新链接状态
    try:
        #LINK  0链接失败 1链接成功  2还未测试
        global shell_sql
        #main_ui=UIManager.get_ui('main_ui')
        shell_sql=ui.UIManager.shell_sql
        sql_data="update sitetable set link='%s',updatetime='%s' where ID='%s'"%(str(link),str(time.time()),str(id))
        if shell_sql.mysqlite3_update(sql_data):
            pass
            #msg.msg_lower_right(u"修改目录:%s 成功"%(str(name)))  #右下角提示
        else:
            pass
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))