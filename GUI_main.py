# -*- coding: utf-8 -*-
"""
Created on Sun Apr 08 16:41:23 2012

@author: Finnegan
@version: 1.0.0
"""
__version__ = "1.0.1"

# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ['ETS_TOOLKIT'] = 'qt4'

import sys
import numpy as np

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
from pyface.qt import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)

import os.path


from gui.gui_code2 import Ui_MainWindow
from gui.Periodic_filter_gui import Ui_Period_Filter_Dialog
#matplotlib stuff
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
#mayavi stuff
from enthought.traits.api import HasTraits, Range, Instance, \
                    on_trait_change
from enthought.traits.ui.api import View, Item, HGroup
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.tools.mlab_scene_model import \
                    MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene


################################################################################
class Visualization(HasTraits):
    meridional = Range(1, 30,  6)
    transverse = Range(0, 30, 11)
    data = np.random.rand(3,6819)
    scene      = Instance(MlabSceneModel, ())

    def __init__(self):
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self)
        x, y, z = Visualization.data
#        self.plot = self.scene.mlab.points3d(x, y, z)

    @on_trait_change('meridional,transverse')
    def update_plot(self):
        self.data = GPS_MainWindow.data
        self.data= np.rot90(self.data)
        print self.data.shape
        x, y, z, c1,i1,c2,i2,c3,i3 = self.data
        self.plot = self.scene.mlab.points3d(x,y,c2)


    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                    height=500, width=600, show_label=False),
                HGroup(
                        '_', 'meridional', 'transverse',
                    ),
                )



        
class PF_DLG(QtGui.QDialog, Ui_Period_Filter_Dialog):
    var1 = np.random.rand(500)
    var2 = np.random.rand(500)
    
    data = np.column_stack((var1,var2))
    
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.CreatePlot()
        self.on_draw()
        str1 = unicode(self.Filter_start.text())
        str2 = unicode(self.Filter_end.text())
        
        print str1, str2
    
    def CreatePlot(self):
        self.Dialog = QtGui.QWidget()       
        
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.Dialog)
        
        self.axes = self.fig.add_subplot(111)
        
    def getValues(self):
        return True
        
    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = unicode(QtGui.QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)
            
    def on_draw(self):
        a = unicode(self.Filter_start.text())
        b = unicode(self.Filter_end.text())
        
        var1 = np.random.rand(500)
        var2 = np.random.rand(500)
        data = np.column_stack((var1,var2))
        
        print a, b
        txt_data = np.column_stack((a,b))
        
        data_fft = np.fft.rfft(data[:,0])
        data_fft = abs(data_fft)
        data_fft = np.log10(data_fft)
        print data_fft

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()        
 #        self.axes.grid(self.grid_cb.isChecked())
        
        self.axes.plot(data_fft)
        
        self.canvas.draw()
        
        if len(txt_data) == 2:
            print 'filtering using', txt_data
            a,b = int(txt_data(0)), int(txt_data(1))
            col_cnt = data.shape(1)
            for i in range(col_cnt):
                temp = np.fft.rfft(data[:,i], axis=0)
                temp[a:b] = 0
                temp[-a:-b] = 0
                global out_array
                data[:,i] = np.fft.irfft(temp, n=len(data[:,i]), axis=0)
                np.savetxt('filtered.csv', data, delimiter=',')
                


class GPS_MainWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        
        QtGui.QWidget.__init__(self, parent)
        self.visualization = Visualization()
        self.ui = self.visualization.edit_traits().control
#        
        
        QtGui.QDialog.__init__(self, parent)
        self.cmdui = Ui_MainWindow()
        self.cmdui.setupUi(self)
        self.ConnectActions()
        self.cmdui.statusbar.showMessage('Ready')
        self.setCentralWidget(self.ui)

            
            
    def ConnectActions(self):
#==============================================================================
#         Connects action buttons within GUI to functions
#==============================================================================
        self.cmdui.actionOpen_File.triggered.connect(self.data_SourceFile)
        self.cmdui.actionOpen_Calibration_File.triggered.connect(self.calb_SourceFile)
        self.cmdui.actionModify_Output_Location.triggered.connect(self.OutPutFile)
        self.cmdui.actionDeSpike.triggered.connect(self.Despike)
        self.cmdui.actionLinear_Drift_Correct.triggered.connect(self.Linear_Drift)
        self.cmdui.actionCubic_Drift_Correct.triggered.connect(self.Cubic_Drift)
        self.cmdui.actionPeriodic_Filter.triggered.connect(self.Periodic_Filter)
        self.cmdui.actionNormalise_Vector.triggered.connect(self.Normalise_Vector)
        self.cmdui.actionInterpolate.triggered.connect(self.Interpolate)
        
        self.cmdui.actionAbout.triggered.connect(self.about)
        self.cmdui.actionPrint.triggered.connect(self.Print_Image)
    
    def Despike(self):
        despike = True
        
    def plot_data(self):
        plot_data = True
        
    def Linear_Drift(self):
        Linear_Drift = True
        
    def Cubic_Drift(self):
        Cubic_Drift = True
    
    def Periodic_Filter(self):
        dlg = PF_DLG()
        if dlg.exec_():
            values = dlg.getValues()

        
    def Normalise_Vector(self):
        Normalise_Vector = True
        
    def Interpolate(self):
        Interpolate = True
        
    def Print_Image(self):
        Print = True
        
    def OutPutFile(self):
        
        Dir_name = unicode(QtGui.QFileDialog.getExistingDirectory(self,
                "Choose Dir", "",
                QtGui.QFileDialog.ShowDirsOnly))
        self.Dir_name = Dir_name
        
    def data_SourceFile(self):
        filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
           "Choose data file","", "*"))
        self.dataname = filename
        self.Dir_name = os.path.dirname(self.dataname)
        GPS_MainWindow.data = np.loadtxt(self.dataname, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
        
        print GPS_MainWindow.data[0,:]
        
        return GPS_MainWindow.data

        
    def calb_SourceFile(self):
         filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "Choose calibration file","", "*.dat"))
         self.calbname = filename

         
    def filename(self):
         return(self.filename)
         

    def about(self):
         QtGui.QMessageBox.about(self,"About CMD Calibration", ' (c) 2012. Finnegan Pope-Carter, Tom Sparrow. \n \n Version - %s \n \n calibrates CMD Mini-Explorer data collected in GPS continuous mode against a collected calibration line \n \n please direct all feedback/requests to popefinn@gmail.com' % __version__ )
                
                         
    def tick_check(value):
         return value == 2
         
    
        

if __name__ == "__main__":
    Gps_app = QtGui.QApplication(sys.argv)
    BartyApp = GPS_MainWindow()
    BartyApp.show()
    QtGui.qApp.exec_()
    sys.exit(Gps_app.exec_())


