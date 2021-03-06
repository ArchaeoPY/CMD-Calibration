# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 14:27:10 2014

@author: mainly from https://gist.github.com/rbonvall/9982648 and Finn
"""

from PyQt4 import QtGui, QtCore
from cmdUI_code import Ui_TestUI
 
def p(x):
    print x
 
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
                  
        QtGui.QDialog.__init__(self, parent)
        self.cmdui = Ui_TestUI()
        self.cmdui.setupUi(self)
 
        print 'Connecting process'
        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)
        self.process.started.connect(lambda: p('Started!'))
        self.process.finished.connect(lambda: p('Finished!'))
 
        print 'Starting process'
        self.process.start('python', ['GUI.py'])
 
    def append(self, text):
        cursor = self.cmdui.terminal.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.cmdui.terminal.ensureCursorVisible()
 
    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput())
        print text.strip()
        self.append(text)
 
    def stderrReady(self):
        text = str(self.process.readAllStandardError())
        print text.strip()
        self.append(text)
 
 
def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()