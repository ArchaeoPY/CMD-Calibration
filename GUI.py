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
from GPS_EM_combine_calb import on_comb
from gui.gui_code import Ui_MainWindow
import matplotlib.pyplot as plt

def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()

class cmdForm(QtGui.QMainWindow):
     def __init__(self, parent=None):
                  
        QtGui.QDialog.__init__(self, parent)
        self.cmdui = Ui_MainWindow()
        self.cmdui.setupUi(self)
      
        #Calb connections
        QtCore.QObject.connect(self.cmdui.open_data_pushButton, QtCore.SIGNAL("clicked()"), self.data_SourceFile)
        QtCore.QObject.connect(self.cmdui.open_calb_pushButton, QtCore.SIGNAL("clicked()"), self.calb_SourceFile)
        QtCore.QObject.connect(self.cmdui.Output_dir_pushButton, QtCore.SIGNAL("clicked()"), self.OutPutFile)
        QtCore.QObject.connect(self.cmdui.GO_pushButton, QtCore.SIGNAL("clicked()"), self.go_button)
        
        #Raw data connections
        QtCore.QObject.connect(self.cmdui.open_view_pushButton, QtCore.SIGNAL("clicked()"), self.view_SourceFile)
        QtCore.QObject.connect(self.cmdui.Outputv_dir_pushButton, QtCore.SIGNAL("clicked()"), self.OutvPutFile)
        QtCore.QObject.connect(self.cmdui.View_pushButton, QtCore.SIGNAL("clicked()"), self.view_button)
        
        #Calb data connections
        QtCore.QObject.connect(self.cmdui.open_calb1_pushButton, QtCore.SIGNAL("clicked()"), self.calb_SourceFileone)
        QtCore.QObject.connect(self.cmdui.open_calb2_pushButton, QtCore.SIGNAL("clicked()"), self.calb_SourceFiletwo)
        QtCore.QObject.connect(self.cmdui.open_calb3_pushButton, QtCore.SIGNAL("clicked()"), self.calb_SourceFilethree)
        QtCore.QObject.connect(self.cmdui.open_calb4_pushButton, QtCore.SIGNAL("clicked()"), self.calb_SourceFilefour)
        QtCore.QObject.connect(self.cmdui.open_calb5_pushButton, QtCore.SIGNAL("clicked()"), self.calb_SourceFilefive)
        QtCore.QObject.connect(self.cmdui.Outputc_dir_pushButton, QtCore.SIGNAL("clicked()"), self.OutcPutFile)
        QtCore.QObject.connect(self.cmdui.combine_pushButton, QtCore.SIGNAL("clicked()"), self.comb_button)
        
        
        #About button
        QtCore.QObject.connect(self.cmdui.about_pushButton, QtCore.SIGNAL("clicked()"), self.about)
        #Status bar
     
        self.cmdui.statusbar.showMessage('Ready')    
        
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
         
         plt.close('all') 
                     
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
         wgs = self.cmdui.coordGroup.checkedId() == -3
         
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
        flusher()
        
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
         
         plt.close('all') 
                                        
         x_var = self.cmdui.vx_var.text()
         y_var = self.cmdui.vy_var.text()       
         intsp_x = self.cmdui.vx_var.text()
         intsp_y = float(self.cmdui.vy_var.text())
         arcgrdval = self.cmdui.varcgrdval.text()
         blank = self.cmdui.vblank.text()
         
         shape = self.cmdui.vshape.checkState() == 2
         gisgrd = self.cmdui.vgisgrd.checkState() == 2
         surf = self.cmdui.vsurf.checkState() == 2
         geopng = self.cmdui.vgeopng.checkState() == 2
         topo = self.cmdui.vtopo.checkState() == 2       
         
         utm = self.cmdui.vcoordGroup.checkedId() == -2
         wgs = self.cmdui.vcoordGroup.checkedId() == -3
         
         despike =  self.cmdui.vdespike.checkState() == 2
         self.cmdui.statusbar.showMessage('Running' + ':' + status_var)
         
         on_view(self.dataname,self.Dir_name, despike, x_var, y_var, intsp_x, intsp_y, arcgrdval, shape, gisgrd, surf, geopng, topo, blank, utm, wgs)
         
         self.cmdui.statusbar.showMessage('Complete', 100)
         QtGui.QMessageBox.information(self,"Output Complete", 'Data output is complete. The files are stored in %s' % self.Dir_name, QtGui.QMessageBox.Ok)
         self.cmdui.statusbar.showMessage('Ready')

     #Calb combine stuff         
     def OutcPutFile(self):
        Dir_name = unicode(QtGui.QFileDialog.getExistingDirectory(self,
                "Choose Dir", "",
                QtGui.QFileDialog.ShowDirsOnly))
        print Dir_name
        self.cmdui.Outputc_lineEdit.setText(Dir_name)
        self.Dir_name = Dir_name
        
     def calb_SourceFileone(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose data file","", "*.csv"))
         self.datafile = filename
         
         self.cmdui.calb1_lineEdit.setText(filename)
         self.Dir_name = os.path.dirname(self.datafile)
         self.cmdui.Outputc_lineEdit.setText(self.Dir_name)
         
     def calb_SourceFiletwo(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose calibration file","", "*.csv"))
         self.calbtwoname = filename
         
         self.cmdui.calb2_lineEdit.setText(self.calbtwoname)
         
     def calb_SourceFilethree(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose calibration file","", "*.csv"))
         self.calbthreename = filename    
         
         self.cmdui.calb3_lineEdit.setText(self.calbthreename)
         
     def calb_SourceFilefour(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose calibration file","", "*.csv"))
         self.calbfourname = filename    
         
         self.cmdui.calb4_lineEdit.setText(self.calbfourname)
         
     def calb_SourceFilefive(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose calibration file","", "*.csv"))
         self.calbfivename = filename    
         
         self.cmdui.calb5_lineEdit.setText(self.calbfivename)
                                   
     def comb_button(self):
         global status_var
         status_var = ''
         
         plt.close('all') 
         
         self.calbtwoname = self.cmdui.calb2_lineEdit.text()
         self.calbthreename = self.cmdui.calb3_lineEdit.text()
         self.calbfourname = self.cmdui.calb4_lineEdit.text()
         self.calbfivename = self.cmdui.calb5_lineEdit.text()
         
         x_var = self.cmdui.cx_var.text()
         y_var = self.cmdui.cy_var.text()       
         intsp_x = self.cmdui.cx_var.text()
         intsp_y = float(self.cmdui.cy_var.text())
         arcgrdval = self.cmdui.carcgrdval.text()
         blank = self.cmdui.cblank.text()
         
         shape = self.cmdui.cshape.checkState() == 2
         gisgrd = self.cmdui.cgisgrd.checkState() == 2
         surf = self.cmdui.csurf.checkState() == 2
         geopng = self.cmdui.cgeopng.checkState() == 2
         topo = self.cmdui.ctopo.checkState() == 2       
       
         self.cmdui.statusbar.showMessage('Running' + ':' + status_var)
         
         on_comb(self.datafile, self.calbtwoname, self.calbthreename, self.calbfourname, self.calbfivename, self.Dir_name, x_var, y_var, intsp_x, intsp_y, arcgrdval, shape, gisgrd, surf, geopng, topo, blank)
         
         self.cmdui.statusbar.showMessage('Complete', 100)
         QtGui.QMessageBox.information(self,"Output Complete", 'Data output is complete. The files are stored in %s' % self.Dir_name, QtGui.QMessageBox.Ok)
         self.cmdui.statusbar.showMessage('Ready')

     #General stuff
     def filename(self):
             return(self.filename)

     def about(self):
         QtGui.QMessageBox.about(self,"About CMD Calibration", ' (c) 2014. Finnegan Pope-Carter, Tom Sparrow, Mary K Saunders. \n \n Version - %s \n \n calibrates CMD Mini-Explorer data collected in GPS continuous mode against a collected calibration line \n and outputs a variety of formats \n\n please direct all feedback/requests to popefinn@gmail.com' % __version__ )
                
                         
     def tick_check(value):
         return value == 2
         

                 

if __name__ == "__main__":
    CMDapp = QtGui.QApplication(sys.argv)
    CMDApp = cmdForm()
    CMDApp.show()
    sys.exit(CMDapp.exec_())   


