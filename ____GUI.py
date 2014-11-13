# -*- coding: utf-8 -*-
"""
Created on Sun Apr 08 16:41:23 2012
Updated on Mon Jun 16 20:05:32 2014

@author: Finnegan 
@version: 1.0.2
"""
__version__ = "1.0.2"
import sys
from PyQt4 import QtCore, QtGui
import os.path
import os
from GPS_EM_calibration_v1 import on_go
from GPS_EM_view_data import on_view
from gui.gui_code import Ui_MainWindow
from includes.terminal import OutputWrapper
'''
for line in sys.stdin:
            sys.stout.write(line)
            sys.stdout.flush() 
'''
class cmdForm(QtGui.QMainWindow):
     def __init__(self, parent=None):
                  
        QtGui.QDialog.__init__(self, parent)
        self.cmdui = Ui_MainWindow()
        self.cmdui.setupUi(self)

        stdout = OutputWrapper(self, True)
        stdout.outputWritten.connect(self.handleOutput)
        stderr = OutputWrapper(self, False)
        stderr.outputWritten.connect(self.handleOutput)
        
        QtCore.QObject.connect(self.cmdui.about_pushButton, QtCore.SIGNAL("clicked()"), self.about)
        
        #Calb connections
        QtCore.QObject.connect(self.cmdui.open_data_pushButton, QtCore.SIGNAL("clicked()"), self.data_SourceFile)
        QtCore.QObject.connect(self.cmdui.open_calb_pushButton, QtCore.SIGNAL("clicked()"), self.calb_SourceFile)
        QtCore.QObject.connect(self.cmdui.Output_dir_pushButton, QtCore.SIGNAL("clicked()"), self.OutPutFile)
        QtCore.QObject.connect(self.cmdui.GO_pushButton, QtCore.SIGNAL("clicked()"), self.go_button)
        
        #Raw data connections
        QtCore.QObject.connect(self.cmdui.open_view_pushButton, QtCore.SIGNAL("clicked()"), self.view_SourceFile)
        QtCore.QObject.connect(self.cmdui.Outputv_dir_pushButton, QtCore.SIGNAL("clicked()"), self.OutvPutFile)
        QtCore.QObject.connect(self.cmdui.View_pushButton, QtCore.SIGNAL("clicked()"), self.view_button)
        
        self.cmdui.statusbar.showMessage('Ready')
               
        
     #Progress box set up 
     def handleOutput(self, text, stdout):
        self._err_color = QtCore.Qt.red
        color = self.cmdui.terminal.textColor()
        self.cmdui.terminal.setTextColor(color if stdout else self._err_color)
        self.cmdui.terminal.moveCursor(QtGui.QTextCursor.End)
        self.cmdui.terminal.ensureCursorVisible()
        self.cmdui.terminal.insertPlainText(text)
        self.cmdui.terminal.setTextColor(color)
        
     #Calb file inputs/outputs
     def OutPutFile(self):
        Dir_name = unicode(QtGui.QFileDialog.getExistingDirectory(self,
                "Choose Dir", "",
                QtGui.QFileDialog.ShowDirsOnly))
        print Dir_name
        self.cmdui.output_lineEdit.setText(Dir_name)
        self.Dir_name = Dir_name
        
     def data_SourceFile(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose data file","", "*.dat"))
         self.dataname = filename
         
         self.cmdui.data_lineEdit.setText(filename)
         self.Dir_name = os.path.dirname(self.dataname)
         self.cmdui.output_lineEdit.setText(self.Dir_name)
         
     def calb_SourceFile(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose calibration file","", "*.dat"))
         self.calbname = filename
         
         self.cmdui.calb_lineEdit.setText(filename)
                          
     def go_button(self):
         global status_var
         status_var = ''
         
         if QtCore.QTime.currentTime().second() % 2:
            print('Chugging away...')
         else:
            sys.stderr.write('Chugging...\n')
                          
         x_var = self.cmdui.x_var.text()
         y_var = self.cmdui.y_var.text()
         intsp_x = self.cmdui.x_var.text()
         intsp_y = self.cmdui.y_var.text()
         arcgrdval = self.cmdui.arcgrdval.text()
         buff = self.cmdui.buff.text()
         blank = self.cmdui.blank.text()
         
         shape = self.cmdui.shape.checkState() == 2
         gisgrd = self.cmdui.gisgrd.checkState() == 2
         surf = self.cmdui.surf.checkState() == 2
         geopng = self.cmdui.geopng.checkState() == 2
         topo = self.cmdui.topo.checkState() == 2       
         
         utm = self.cmdui.coordGroup.checkedId() == -2
         wgs = self.cmdui.coordGroup.checkedId() == -4
         print 'FFS:', self.cmdui.coordGroup.checkedId()
         
         calb_interp = self.cmdui.cubic.isChecked == True
         
         linear_interp = self.cmdui.linear
         despike =  self.cmdui.despike.checkState() == 2
         data_match =  self.cmdui.data_match.checkState() == 2
         
         self.cmdui.statusbar.showMessage('Running' + ':' + status_var)
         on_go(self.dataname,self.calbname,self.Dir_name, calb_interp,linear_interp, despike, x_var, y_var, intsp_x, intsp_y, arcgrdval, data_match, buff, shape, gisgrd, surf, geopng, topo, blank, utm, wgs)
         self.cmdui.statusbar.showMessage('Complete', 100)
         QtGui.QMessageBox.information(self,"Output Complete", 'Data output is complete. The files are stored in %s' % self.Dir_name, QtGui.QMessageBox.Ok)
         self.cmdui.statusbar.showMessage('Ready')
         
     
     #Raw data stuff         
     def OutvPutFile(self):
        Dir_name = unicode(QtGui.QFileDialog.getExistingDirectory(self,
                "Choose Dir", "",
                QtGui.QFileDialog.ShowDirsOnly))
        print Dir_name
        self.cmdui.outputv_lineEdit.setText(Dir_name)
        self.Dir_name = Dir_name
        
     def view_SourceFile(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose data file","", "*.dat"))
         self.dataname = filename
         
         self.cmdui.view_lineEdit.setText(filename)
         self.Dir_name = os.path.dirname(self.dataname)
         self.cmdui.outputv_lineEdit.setText(self.Dir_name)
                                   
     def view_button(self):
         global status_var
         status_var = ''
         
         if QtCore.QTime.currentTime().second() % 2:
            print('Chugging away...')
         else:
            sys.stderr.write('Chugging...\n')
          
         data_match = False
         
         x_var = self.cmdui.x_varv.text()
         y_var = self.cmdui.y_varv.text()       
         intsp_x = self.cmdui.x_varv.text()
         intsp_y = self.cmdui.y_varv.text()
         arcgrdval = self.cmdui.arcgrdvalv.text()
         blank = self.cmdui.blankv.text()
         
         shape = self.cmdui.shapev.checkState() == 2
         gisgrd = self.cmdui.gisgrdv.checkState() == 2
         surf = self.cmdui.surfv.checkState() == 2
         geopng = self.cmdui.geopngv.checkState() == 2
         topo = self.cmdui.topov.checkState() == 2       
         
         utm = self.cmdui.coordGroup.checkedId() == -2
         wgs = self.cmdui.coordGroup.checkedId() == -4
         
         despike =  self.cmdui.despikev.checkState() == 2
         self.cmdui.statusbar.showMessage('Running' + ':' + status_var)
         
         on_view(self.dataname,self.Dir_name, despike, intsp_x, intsp_y, arcgrdval, shape, gisgrd, surf, geopng, topo, blank, utm, wgs, x_var, y_var, data_match)
         
         self.cmdui.statusbar.showMessage('Complete', 100)
         QtGui.QMessageBox.information(self,"Output Complete", 'Data output is complete. The files are stored in %s' % self.Dir_name, QtGui.QMessageBox.Ok)
         self.cmdui.statusbar.showMessage('Ready')

     def filename(self):
             return(self.filename)

     def about(self):
         QtGui.QMessageBox.about(self,"About CMD Calibration", ' (c) 2014. Finnegan Pope-Carter, Tom Sparrow, Mary K Saunders. \n \n Version - %s \n \n calibrates CMD Mini-Explorer data collected in GPS continuous mode against a collected calibration line \n \n please direct all feedback/requests to popefinn@gmail.com' % __version__ )
                
                         
     def tick_check(value):
         return value == 2


        

if __name__ == "__main__":
    Bartyapp = QtGui.QApplication(sys.argv)
    BartyApp = cmdForm()
    BartyApp.show()
    sys.exit(Bartyapp.exec_())   
  

