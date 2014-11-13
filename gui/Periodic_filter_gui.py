# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'periodic_filter_dialog.ui'
#
# Created: Fri Oct 19 21:42:52 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Period_Filter_Dialog(object):
    def setupUi(self, Period_Filter_Dialog):
        Period_Filter_Dialog.setObjectName(_fromUtf8("Period_Filter_Dialog"))
        Period_Filter_Dialog.resize(486, 390)
        Period_Filter_Dialog.setWindowTitle(QtGui.QApplication.translate("Period_Filter_Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBox = QtGui.QDialogButtonBox(Period_Filter_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 350, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.Period_Filter_Plot = MatplotlibWidget(Period_Filter_Dialog)
        self.Period_Filter_Plot.setGeometry(QtCore.QRect(0, 0, 491, 300))
        self.Period_Filter_Plot.setObjectName(_fromUtf8("Period_Filter_Plot"))
        self.Filter_start = QtGui.QLineEdit(Period_Filter_Dialog)
        self.Filter_start.setGeometry(QtCore.QRect(20, 340, 71, 20))
        self.Filter_start.setObjectName(_fromUtf8("Filter_start"))
        self.Filter_end = QtGui.QLineEdit(Period_Filter_Dialog)
        self.Filter_end.setGeometry(QtCore.QRect(100, 340, 81, 20))
        self.Filter_end.setObjectName(_fromUtf8("Filter_end"))
        self.label = QtGui.QLabel(Period_Filter_Dialog)
        self.label.setGeometry(QtCore.QRect(60, 320, 81, 16))
        self.label.setText(QtGui.QApplication.translate("Period_Filter_Dialog", "Filtering Range", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Period_Filter_Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Period_Filter_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Period_Filter_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Period_Filter_Dialog)

    def retranslateUi(self, Period_Filter_Dialog):
        pass

from matplotlibwidget import MatplotlibWidget
