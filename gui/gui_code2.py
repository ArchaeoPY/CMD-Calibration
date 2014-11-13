# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Oct 22 16:11:35 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(870, 599)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.MayaviQWidget = QtGui.QWidget(self.centralwidget)
        self.MayaviQWidget.setGeometry(QtCore.QRect(9, 9, 731, 551))
        self.MayaviQWidget.setObjectName(_fromUtf8("MayaviQWidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 870, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuProcess = QtGui.QMenu(self.menubar)
        self.menuProcess.setTitle(QtGui.QApplication.translate("MainWindow", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProcess.setObjectName(_fromUtf8("menuProcess"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar)
        self.actionCubic_Drift_Correct = QtGui.QAction(MainWindow)
        self.actionCubic_Drift_Correct.setText(QtGui.QApplication.translate("MainWindow", "Cubic Drift Correct", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCubic_Drift_Correct.setObjectName(_fromUtf8("actionCubic_Drift_Correct"))
        self.actionPeriodic_Filter = QtGui.QAction(MainWindow)
        self.actionPeriodic_Filter.setText(QtGui.QApplication.translate("MainWindow", "Periodic Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPeriodic_Filter.setObjectName(_fromUtf8("actionPeriodic_Filter"))
        self.actionDeSpike = QtGui.QAction(MainWindow)
        self.actionDeSpike.setText(QtGui.QApplication.translate("MainWindow", "DeSpike", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeSpike.setObjectName(_fromUtf8("actionDeSpike"))
        self.actionLinear_Drift_Correct = QtGui.QAction(MainWindow)
        self.actionLinear_Drift_Correct.setText(QtGui.QApplication.translate("MainWindow", "Linear Drift Correct", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLinear_Drift_Correct.setObjectName(_fromUtf8("actionLinear_Drift_Correct"))
        self.actionNormalise_Vector = QtGui.QAction(MainWindow)
        self.actionNormalise_Vector.setText(QtGui.QApplication.translate("MainWindow", "Normalise Vector", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNormalise_Vector.setObjectName(_fromUtf8("actionNormalise_Vector"))
        self.actionOpen_Calibration_File = QtGui.QAction(MainWindow)
        self.actionOpen_Calibration_File.setText(QtGui.QApplication.translate("MainWindow", "Open Calibration File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Calibration_File.setObjectName(_fromUtf8("actionOpen_Calibration_File"))
        self.actionInterpolate = QtGui.QAction(MainWindow)
        self.actionInterpolate.setText(QtGui.QApplication.translate("MainWindow", "Interpolate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInterpolate.setObjectName(_fromUtf8("actionInterpolate"))
        self.actionOpen_File = QtGui.QAction(MainWindow)
        self.actionOpen_File.setText(QtGui.QApplication.translate("MainWindow", "Open File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_File.setObjectName(_fromUtf8("actionOpen_File"))
        self.actionModify_Output_Location = QtGui.QAction(MainWindow)
        self.actionModify_Output_Location.setText(QtGui.QApplication.translate("MainWindow", "Modify Output Location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionModify_Output_Location.setObjectName(_fromUtf8("actionModify_Output_Location"))
        self.actionPrint = QtGui.QAction(MainWindow)
        self.actionPrint.setText(QtGui.QApplication.translate("MainWindow", "Print", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionModify_Output_Location)
        self.menuFile.addAction(self.actionPrint)
        self.menuHelp.addAction(self.actionAbout)
        self.menuProcess.addAction(self.actionLinear_Drift_Correct)
        self.menuProcess.addAction(self.actionCubic_Drift_Correct)
        self.menuProcess.addAction(self.actionDeSpike)
        self.menuProcess.addAction(self.actionNormalise_Vector)
        self.menuProcess.addAction(self.actionPeriodic_Filter)
        self.menuProcess.addAction(self.actionInterpolate)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProcess.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionOpen_Calibration_File)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDeSpike)
        self.toolBar.addAction(self.actionCubic_Drift_Correct)
        self.toolBar.addAction(self.actionLinear_Drift_Correct)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPeriodic_Filter)
        self.toolBar.addAction(self.actionNormalise_Vector)
        self.toolBar.addAction(self.actionInterpolate)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

