# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 14:28:18 2014

@author: mary
"""
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TestUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        #MainWindow.resize(374, 600)
        MainWindow.setGeometry(800, 50, 374, 655)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CMD Progress Window", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setWindowIcon(QtGui.QIcon('./includes/icon.PNG')) 
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        #Bottom of window
        #Progress reporter
        self.termgrp = QtGui.QGroupBox(self.centralwidget)
        self.termgrp.setGeometry(QtCore.QRect(5, 5, 360, 630))
        self.termgrp.setTitle(QtGui.QApplication.translate("MainWindow", "Program progress", None, QtGui.QApplication.UnicodeUTF8))
        self.termgrp.setCheckable(False)
        self.termgrp.setObjectName(_fromUtf8("termgrp"))        
        self.terminal = QtGui.QTextEdit(self.termgrp)
        self.terminal.setGeometry(QtCore.QRect(10, 15, 340, 605))     
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 374, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
                