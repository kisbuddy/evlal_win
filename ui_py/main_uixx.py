# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1199, 642)
        MainWindow.setSizeIncrement(QtCore.QSize(500, 0))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.gridLayout_2.setMargin(2)
        self.gridLayout_2.setHorizontalSpacing(2)
        self.gridLayout_2.setVerticalSpacing(7)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout_2.addWidget(self.treeWidget, 0, 2, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setMargin(1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1199, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        self.menu_4 = QtGui.QMenu(self.menubar)
        self.menu_4.setObjectName(_fromUtf8("menu_4"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.close = QtGui.QAction(MainWindow)
        self.close.setIconVisibleInMenu(True)
        self.close.setObjectName(_fromUtf8("close"))
        self.action_webshell = QtGui.QAction(MainWindow)
        self.action_webshell.setObjectName(_fromUtf8("action_webshell"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.aboutAction = QtGui.QAction(MainWindow)
        self.aboutAction.setObjectName(_fromUtf8("aboutAction"))
        self.menu.addAction(self.close)
        self.menu_2.addAction(self.action_webshell)
        self.menu_3.addAction(self.action_2)
        self.menu_4.addAction(self.aboutAction)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "XXXXXXX", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.menu.setTitle(_translate("MainWindow", "文件", None))
        self.menu_2.setTitle(_translate("MainWindow", "编辑", None))
        self.menu_3.setTitle(_translate("MainWindow", "设置", None))
        self.menu_4.setTitle(_translate("MainWindow", "帮助", None))
        self.close.setText(_translate("MainWindow", "退出", None))
        self.action_webshell.setText(_translate("MainWindow", "添加webshell", None))
        self.action_2.setText(_translate("MainWindow", "设置参数", None))
        self.aboutAction.setText(_translate("MainWindow", "关于软件", None))

