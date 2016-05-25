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
import socket
socket.setdefaulttimeout(10)
import threading
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#label = None  #消息提示
treeWidget_id  = 0  #当前目录ID
tabWidget_close_lock = threading.Lock()   #属性页锁
link_shell_timeout=5 #链接SHELL 超时
#thread.allocate()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class UIManager(QObject):
    widget = {}  #ui
    shell_sql=None  #数据库
    #label = None  #消息提示
    @classmethod
    def add_ui(cls, key, widget):
        cls.widget[key] = widget
    @classmethod
    def get_ui(cls, key):
        return cls.widget[key]



##############################################
import os
#以下是常用操作
def open_file(file):  #读取文件
    try:
        # 你的代码
        if not os.path.exists(file):
            return "file null"
        f=open(file ,'rb')
        f.seek(0,0)
        byte = f.read()
        f.close()
        return byte
    except BaseException, e:
        return "null"

def open_file_hex(file):  #按照16进制读取文件
    try:
        # 你的代码
        if not os.path.exists(file):
            return "file null"
        f=open(file ,'rb')
        f.seek(0,0)
        hexstr=""
        while True:
            byte = f.read(1)
            if byte == '':
                break
            else:
                #加密.encode('hex')  data.decode('hex')  解密
                hexstr =hexstr+"%s" %(byte.encode('hex'))
                #hexstr =  "%s" % byte.encode('hex')
                #decnum = int(hexstr, 16)
                #print byte, hexstr, decnum
        f.close()
        return hexstr
    except BaseException, e:
        return "null"


if __name__ == '__main__':
    htex_data=open_file_hex('123.txt')  #按照16进制读取文件
    print htex_data
