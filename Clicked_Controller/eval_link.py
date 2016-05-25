#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
import re
import httplib
import gzip
import StringIO
import urllib
import urllib2
import requests
from Db_Model import db_shell #常用数据库操作
from Clicked_Controller import log #日志记录
from Ui_View import ui #UI变量
from PyQt4 import QtCore, QtGui ,QtNetwork
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

# def Post_eval_php(SiteUrl,PASS,params): #执行一句话
#     values = {PASS:params}#得密码post内容
#     pdata = urllib.unquote(urllib.urlencode(values))#先编码后再解码，要不就出错了不编码=/?
#     #pdata = urllib.quote(str(tdata), "=")#不编码=/?
#     #QtGui.QMessageBox.information(self.centralWidget, _fromUtf8("操作提示"),  _fromUtf8(urllib.quote(str(pdata), "=?")))#弹出对话框
#     req = urllib2.Request(str(SiteUrl), pdata)#强制转换为str
#     try:
#         response = urllib2.urlopen(req, timeout=12)
#     except urllib2.HTTPError as e:
#         if hasattr(e, 'code'):
#             data=u"HTTP link Error Status %s\n%s"%(str(e.code),str(e.info()))
#             return 0,str(data)
#             #sys.exit()#假如Http请求报错则退出程序
#     except urllib2.URLError as e:
#         if hasattr(e,"reason"):
#             data=u"无法解析服务器名称或地址\nurl:%s\n%s\n"%(str(SiteUrl),str(e.reason))
#             return 0,str(data)
#     if str(response.getcode())=="200":
#         one_page = response.read()
#         the_page=one_page
#         real_page=GetRealTxt("->|", "|<-", str(the_page))
#         print real_page,one_page
#         if str(real_page)=="False":
#             data=u"HTTP /1.1 %sOK\n%s\n%s"%(str(response.getcode()),str(response.info()),str(response.read()))
#             return 0,str(data)
#         else:
#             return 1,str(real_page)
#     else:
#         #链接错误判断下应该   返回数据
#         pass

def Post_eval_php(ID,params):  #POST 提交内容
    try:
        id_shell_list=db_shell.id_sitetable_shell('%s'%(str(ID)))  #通过ID查询SHELL的状态
        #id=str(id_shell_list[0])         #自动编号
        #type_id=str(self.id_shell_list[1])    #      类别
        url=str(id_shell_list[2])    #    网址
        PASS=str(id_shell_list[3])   #    密码
        #ip=str(id_shell_list[4])         #    ip地址
        #config=str(id_shell_list[5])     #    配置
        coding=str(id_shell_list[6])     #  编码方式
        #script=str(id_shell_list[7])      #   asp   php
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        #values = {SitePass:Data}#得密码post内容
        values = PASS  + params#上面的方式会进行自动URL编码所以用这种方式+ "="
        #req = requests.post(str(url), values, headers=headers, timeout=10)#强制转换为str
        req = requests.post(str(url), values, headers=headers, timeout=int(ui.link_shell_timeout))#强制转换为str
        if str(req.status_code)!="200":
            data=u"%s\n%s"%(str(req.status_code),str(req.headers))
            return 0,str(data)
        else:
            if coding=="65001":
                req.encoding = 'UTF-8'
            elif coding=="936":
                req.encoding = 'GB2312'
            elif coding=="950":
                req.encoding = 'BIG5'
            elif coding=="949":
                req.encoding = 'Euc-KR'
            elif coding=="20932":
                req.encoding = 'Euc-JP'
            elif coding=="932":
                req.encoding = 'Shift_JIS'
            elif coding=="1251":
                req.encoding = 'Windows-1251'
            elif coding=="874":
                req.encoding = 'Windows-874'
            elif coding=="1252":
                req.encoding = 'ISO-8859-1'
            else:
                req.encoding = 'GB2312'

            one_page = req.text

            real_page=GetRealTxt("->|", "|<-", str(one_page))
            if str(real_page)=="False":
                data=u"HTTP /1.1 OK\n%s\n%s"%(str(req.headers),str(req.text))
                return 0,str(data)
            else:
                return 1,str(real_page)
    except BaseException, e:
        #log.logging.debug("except:%s"%(str(e)))
        return 0,str("LINK SHELL error:"+str(e))

# def Post_eval_php(ID,params): #URL地址 ，密码   只支持PHP  url,PASS,params
#     try:
#         id_shell_list=db_shell.id_sitetable_shell('%s'%(str(ID)))  #通过ID查询SHELL的状态
#         #id=str(id_shell_list[0])         #自动编号
#         #type_id=str(self.id_shell_list[1])    #      类别
#         url=str(id_shell_list[2])    #    网址
#         PASS=str(id_shell_list[3])   #    密码
#         #ip=str(id_shell_list[4])         #    ip地址
#         #config=str(id_shell_list[5])     #    配置
#         #coding=str(id_shell_list[6])     #  编码方式
#         #script=str(id_shell_list[7])      #   asp   php
#         #print params
#         #构造HTTP头
#         pattern = re.compile('http:*')
#         match = pattern.search(url)
#         if(match):
#             ztarget = url.replace("http://","").split('/')[0]
#             headers={"Host": ztarget, \
#                      "User-Agent": "Mozilla/5.0", \
#                      "Content-Type": "application/x-www-form-urlencoded", \
#                      "Referer": "http://"+ztarget
#                      }
#         else:
#             #print "please enter an address....For example: [url]http://www.xxx.com/1.asp[/url]"
#             return 0,"headers except"
#             #测试  链接
#         #values = {PASS:params}#得密码post内容
#         # data = urllib.unquote(urllib.urlencode(values))#先编码后再解码，要不就出错了……
#         # req = urllib2.Request(str(url), data)#强制转换为str
#         # response = urllib2.urlopen(req)
#         # the_page = response.read()
#         try:
#             conn = httplib.HTTPConnection(ztarget,timeout=20)
#             params = PASS+params
#             #print params
#             url_plg = url.replace("http://","")
#             url_plg=url_plg[url_plg.index("/"):len(url_plg)]
#             conn.request(method="POST",url=url_plg,body=params,headers=headers)
#             response = conn.getresponse()
#             if ('content-encoding', 'gzip') in response.getheaders():
#                 compressedstream = StringIO.StringIO(response.read())
#                 gzipper = gzip.GzipFile(fileobj=compressedstream)
#                 the_page = gzipper.read()
#             else:
#                 the_page = response.read()
#                 #return data
#             real_page=GetRealTxt("->|", "|<-", str(the_page))
#             #print real_page
#             if str(real_page)=="False":
#                 data=u"HTTP /1.1 %sOK\n%s\n%s"%(str(response.getcode()),str(response.info()),str(response.read()))
#                 return 0,str(data)
#             else:
#                 Info = the_page[the_page.find('->|')+3:the_page.find('|<-')]#截取->||<-之间的字符
#                 return 1,Info
#         except Exception,e:
#             #print e
#             return 0,str(e)
#             #return str(e)
#
#     except Exception,e:
#         #print e
#         return 0,str(e)

def GetRealTxt(start_str, end, html):#取两个字符串之间的值
    try:
        if str(html)=="":
            return("False")
        else:
            start = html.find(start_str)
            if start >= 0:
                start += len(start_str)
                end = html.rfind(end, start)  #从尾部查找
                if end >= 0:
                    return html[start:end].strip()
                else:
                    return ("False")
            else:
                return ("False")
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))




