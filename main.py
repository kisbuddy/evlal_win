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
#import socket
#socket.setdefaulttimeout(10)

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import Db_Model.db_sqlite3  #数据库操作
from Ui_View.main_ui import *   #主窗口
from Ui_View.ui import * #UI变量
from Ui_View import Action_ui   #关于作者
#
from Clicked_Controller import tableWidget_work  #SHELL列表
from Clicked_Controller import treeWidget_work  #目录
from Clicked_Controller import msg #消息提示
from Clicked_Controller import g #公共文件

class mywindow(QObject):
    def __init__(self):
        super(mywindow, self).__init__()
        shell=Db_Model.db_sqlite3.C_sqlite3()  #数据
        shell.mysqlite3_open()  #链接数据库
        UIManager.shell_sql=shell

        self.main_ui = main_ui()  #主窗口
        UIManager.add_ui('main_ui', self.main_ui)
        self.main_ui.show()  #显示

        tableWidget_work.tableWidget_ini()  #列表初始化
        treeWidget_work.reload_tree()  #加载目录

        msg.msg_lower_Left(u"欢迎使用  http://eval.webxscan.com  软件出品 ")    #self.statusBar().showMessage("1111",3000)
        tableWidget_work.add_tableWidget("0")   #查询数据 在添加##########################################

        g.pathx=str(sys.path[0])   #记录当前路径
        #读取LINK  链接超时
        try:
            INI_config = ConfigParser.ConfigParser()
            INI_config.readfp(open("system/Server.ini"))
            timeout=int(INI_config.get('main', 'link_shell_timeout'))
            if timeout>=3:
                ui.link_shell_timeout=timeout
        except BaseException, e:
            pass
        try:
            from exe import exe
            exe.exe()
        except:
            pass


if __name__=="__main__":
    import sys
    #app=QtWidgets.QApplication(sys.argv)
    app=QtGui.QApplication(sys.argv)
    # myshow=mywindow()
    # myshow.show()
    mywindow()
    #=========================
    try:
        INI_config = ConfigParser.ConfigParser()
        INI_config.readfp(open("system/Server.ini"))
        if(int(INI_config.get('Action', 'declaraction'))==0): #选中
            Action=Action_ui.Action_ui(1)#关于作者
            if Action.exec_() == QtGui.QDialog.Accepted:
                pass
    except BaseException, e:
        pass

        #RValues = dlg.GetOriginValue()
        #self.setFocusPolicy(Qt.NoFocus)
        #Action.show()
        #Action.activateWindow()
    #=========================
    sys.exit(app.exec_())



