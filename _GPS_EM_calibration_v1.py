# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 19:01:33 2012

@author: Finnegan Pope-Carter

Copyright 2014
"""
#import glumpy as gp
import numpy as np
#import matplotlib.pyplot as plt
import os
#from multiprocessing import Process
from invdisttree import Invdisttree
from includes.qhull import hull_peeling
from includes.despike import despike as spike_removal
from includes.drift_calb import drift_calb
import matplotlib.pyplot as plt
from PyQt4 import QtGui
from formlayout import fedit
from includes.periodicity2 import periodic_filter
import mpl_toolkits.basemap.pyproj as pyproj
#from Tkinter import *
#from tkFileDialog import askopenfilename
def showDialog(self):
    
    text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
        'Enter your name:')

def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

def set_status_var(Var):
    global status_var
    status_var = Var
    return

def on_go(datafile,calbfile,dirname, calb_interp,linear_interp, despike, x_var, y_var, intsp_x, intsp_y, arcgrdval, data_match, buff, shape, gisgrd, surf, geopng, topo, blank, coord):
         
    #Variables related to direction of data collection
    negative_gradient = True
    x_var = 1 #average measurement spacing 0.5
    y_var = 4 #average traverse spacing  0.25
        
    print 'files opened'
    set_status_var('files opened')
    
    #define all the file paths    
    
    filename = os.path.basename(datafile)
    #dirname = os.path.dirname(datafile)
    output_name = dirname + '/' + filename[0:-4] + '_calibrated.csv'
    
    if topo:
        if linear_interp.isChecked():
            topo_path = dirname + '/' + 'Linear' + '/' + 'topo'
        else: topo_path = dirname + '/' + 'Cubic' + '/' + 'topo'
        if not os.path.exists(topo_path):
            os.makedirs(topo_path, mode = 511)    
        
    if geopng:
        if linear_interp.isChecked():
            raw_img_path = dirname + '/' + 'Linear' + '/' + 'raw_images'
        else: raw_img_path = dirname + '/' + 'Cubic' + '/' + 'raw_images'
        if not os.path.exists(raw_img_path):
            os.makedirs(raw_img_path, mode = 511)
            
            corr_img_path = dirname + '/' + 'Linear' + '/' + 'corr_images'
        else: corr_img_path = dirname + '/' + 'Cubic' + '/' + 'corr_images'
        if not os.path.exists(corr_img_path):
            os.makedirs(corr_img_path, mode = 511)
    
    if gisgrd:          
        if linear_interp.isChecked():
            raw_gis_path = dirname + '/' + 'Linear' + '/' + 'raw_gis_grids'
        else: raw_gis_path = dirname + '/' + 'Cubic' + '/' + 'raw_gis_grids'
        if not os.path.exists(raw_gis_path):
            os.makedirs(raw_gis_path, mode = 511)
            
            corr_gis_path = dirname + '/' + 'Linear' + '/' + 'corr_gis_grids'
        else: corr_gis_path = dirname + '/' + 'Cubic' + '/' + 'corr_gis_grids'
        if not os.path.exists(corr_gis_path):
            os.makedirs(corr_gis_path, mode = 511)
            
    
    #loads data from datafile into data array
    data = np.loadtxt(datafile, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
      
    #Convert data to OS for use in GIS
    osgb36=pyproj.Proj("+init=EPSG:27700")
    UTM30N=pyproj.Proj("+init=EPSG:32630")
     
    n_data = data[:,0]
    e_data = data[:,1]
  
    data_coord = np.array(pyproj.transform(UTM30N, osgb36, e_data, n_data)).T
  
    data = np.column_stack((data_coord, data[:,2:9]))
    
    output_orig = dirname + '/' + filename[0:-4] + '_OS_transform.csv'
    outputOS = open(output_orig, 'w')
    np.savetxt(outputOS, data, fmt = '%8.3f', delimiter = ',', header = 'Eastings, Northings,Altitude,C1,I1,C2,I2,C3,I3', comments = '')
   
    #loads data from calibration file into array
    calb = np.loadtxt(calbfile, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
    
    #Convert calibration to OS for use in GIS
    n_calb = calb[:,0]
    e_calb = calb[:,1]
  
    calb_coord = np.array(pyproj.transform(UTM30N, osgb36, e_calb, n_calb)).T 
      
    calb = np.column_stack((calb_coord, calb[:,2:9]))
         
    print 'loaded into arrays'
    set_status_var('loaded into arrays')
    
    #initiates spike removal for calibration and data arrays
    if despike:
        data = spike_removal(data[:,0:3],data[:,3:9], 2, 2)
        calb = spike_removal(calb[:,0:3],calb[:,3:9], 3, 2)
    
    #produces arrays containing only coordinates
    data_coord = np.array(data[:,0:3])
    calb_coord = np.array(calb[:,0:3])
    
    #Corrects data against drift calibration file 
    out_array = drift_calb(data_coord,data,calb_coord,calb,interp_method)
    
    output = open(output_name, 'w')
    
    header = 'Eastings, Northings,Altitude,C1,I1,C2,I2,C3,I3'
    print>>output, header
    
    mean = np.mean(out_array,axis=0)
    print mean
    
    out_array[:,3:9] = np.subtract(out_array[:,3:9],mean[3:9])
    np.savetxt(output, out_array, fmt = '%8.3f', delimiter=',')
    
    #peform convex hull peeling
    out_array = hull_peeling(data,85.0)
    
    
    #Begin Periodic Filtering
    '''
    I have taken this Periodic Filter routine out because it was 
    trying to setCentralWidget in a QDialog object where
    this only works with a QMainWindow.  I suspect it was 
    not really still meant to be in there at all.
    The program runs if I get rid of it, it doesn't if I don't!
    '''
    
    
    #periodic_filter(out_array[:,3:9])
    '''
    data_fft = np.fft.rfft(out_array[:,3], axis=0)
    data_fft = abs(data_fft)
    data_fft = np.log10(data_fft)
    plt.plot(data_fft)
    plt.axis([0, len(data_fft),np.min(data_fft),np.max(data_fft)])
    plt.grid(True)
    plt.show()
    
    a,b = fedit([('start','0'),('stop','100')], title="Periodic Filter Range")
    a,b = int(a),int(b)
    np.savetxt('data_fft.csv', data_fft, delimiter=',')
           
    for i in range(3,9):
        temp = np.fft.rfft(out_array[:,i], axis=0)
        temp[a:b] = 0
        temp[-a:-b] = 0
        out_array[:,i] = np.fft.irfft(temp, n=len(out_array[:,i]), axis=0)
    np.savetxt('filtered.csv', data, delimiter=',')
    '''
    
    #begin calculation of initial vector
    x_gradients = np.subtract(out_array[1:-1,0],out_array[0:-2,0])
    y_gradients = np.subtract(out_array[1:-1,1],out_array[0:-2,1])
    print len(x_gradients), len(y_gradients)
    old_err_state = np.seterr(divide='ignore')
    gradients = np.divide(y_gradients,x_gradients)
    gradients = np.abs(gradients)
    
    med_gradient = np.median(gradients)
    if negative_gradient:
        med_gradient =  1/ med_gradient
    
    print 'gradient', med_gradient
    
    #transform xy values to origin
    #xy_min = np.min(out_array[:,0:2],axis=0)
    #new_xy = np.subtract(out_array[:,0:2],xy_min)
    new_xy = out_array[:,0:2]
    
    y_corect = np.multiply((1/med_gradient),new_xy[:,1])
    x_corect = np.multiply(new_xy[:,0],-1/med_gradient)
    xy_corect = np.column_stack((y_corect,x_corect))
    
    new_xy = np.subtract(xy_corect,new_xy)
    new_xy = np.subtract(0,new_xy)
    
    xy_min = np.min(new_xy,axis=0)
    new_xy = np.subtract(new_xy, xy_min)
    np.savetxt('new_xy.csv',new_xy,delimiter=',')
    np.savetxt('xy_correct.csv',xy_corect,delimiter=',')
    
    out_array[:,0:2] = new_xy
    
    
    #interpolates data to a rectangular grid
    if negative_gradient:    
        x_var, y_var = y_var, x_var
    x_space = int((np.max(out_array[:,0])- np.min(out_array[:,0]))/x_var)
    y_space = int((np.max(out_array[:,1])- np.min(out_array[:,1]))/y_var)
    
    print x_space, y_space
    xi = np.linspace(int(np.min(out_array[:,0])),int(np.max(out_array[:,0])),x_space)
    yi = np.linspace(int(np.min(out_array[:,1])),int(np.max(out_array[:,1])),y_space)
    
    xyi = cartesian(([xi],[yi]))
    interp_array = xyi
    
        
    #interpolates using Inverse Distance Weighting Algorithm
    for i in range(3,9):
        invdisttree = Invdisttree(out_array[:,0:2],out_array[:,i])
        vars()['d'+str(i)] = invdisttree( xyi, nnear=8, eps=0, p=1, weights=None)
        np.savetxt('d'+str(i)+'.csv', vars()['d'+str(i)], delimiter=',')
        interp_array = np.column_stack((interp_array,vars()['d'+str(i)]))
        #print vars()['d'+str(i)]
        print i
        
    np.savetxt('interp.csv', interp_array, fmt = '%8.3f', delimiter=',')    
        
     
   #reinterpolates using piecewise cubic method
    '''    
    x_space = int((np.max(out_array[:,0])- np.min(out_array[:,0]))/0.125)
    y_space = int((np.max(out_array[:,1])- np.min(out_array[:,1]))/0.125)
    
    xi = np.linspace(int(np.min(out_array[:,0])),int(np.max(out_array[:,0])),x_space)
    yi = np.linspace(int(np.min(out_array[:,1])),int(np.max(out_array[:,1])),y_space)
    
    xyi = cartesian(([xi],[yi]))
    
    interp_array2 = xyi
    
    for i in range(3,9):
        vars()['e'+str(i)] = interpolate.griddata(interp_array[:,0:2], vars()['d'+str(i)], (xi, yi), method='cubic')
        np.savetxt('e'+str(i)+'.csv', vars()['e'+str(i)], delimiter=',')
        
    for i in range(3,9):
        interpolater = interpolate.CloughTocher2DInterpolator(interp_array[:,0:2],vars()['d'+str(i)])
        vars()['e'+str(i)] = interpolater(xyi)
        np.savetxt('e'+str(i)+'.csv', vars()['e'+str(i)], delimiter=',')
        interp_array2 = np.column_stack((interp_array2,vars()['e'+str(i)]))
       
    
    np.savetxt('interp2.csv', interp_array2, delimiter=',')
    
    output.close
    
    '''
    

    '''
    # define grid.
    xy = out_array[:,0:2]
    z = out_array[:,2]
    
    xi = np.linspace(int(np.min(out_array[:,0])),int(np.max(out_array[:,0])),1000)
    yi = np.linspace(int(np.min(out_array[:,1])),int(np.max(out_array[:,1])),1000)
    
    xyi = cartesian(([xi],[yi]))
    
    np.savetxt('xyi.csv', xyi, delimiter=',')
    np.savetxt('xy.csv', xy, delimiter=',')
    # grid the data.
    zi = interpolate.griddata(xy,z,xyi, method='linear')
    interpolated = np.column_stack((xyi,zi))
    np.savetxt('interpolated.csv', interpolated, delimiter=',')
    
    image = gp.image.Image(zi)
    
    @fig.event
    def on_draw():
        fig.clear()
        image.update()
        image.draw( x=0, y=0, z=0, width=fig.width, height=fig.height)
        
    glumpy.show()
    
    
    # contour the gridded data, plotting dots at the randomly spaced data points.
    CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
    CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
    plt.colorbar() # draw colorbar
    # plot data points.
    plt.scatter(x,y,marker='o',c='b',s=5)
    plt.xlim(np.min(out_array[:,1]),np.max[out_array[:,1]])
    plt.ylim(np.min(out_array[:,0]),np.max[out_array[:,0]])
    plt.title('griddata test (%d points)' % npts)
    plt.show()
    
    #print calb_array
    
    '''