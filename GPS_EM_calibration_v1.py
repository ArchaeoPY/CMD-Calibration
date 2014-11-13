# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 19:01:33 2012

@author: Finnegan Pope-Carter and MKS


Copyright 2014
"""
import sys
import numpy as np
import os
#from invdisttree import Invdisttree
#from includes.qhull import hull_peeling
from includes.despike import despike as spike_removal
from includes.drift_calb import drift_calb
from includes.plot_data import plot_data, plot_corr
from includes.shape_export import raw_shape_out, corr_shape_out
from includes.coords import rawtodd, calbtodd
from PyQt4 import QtGui
import mpl_toolkits.basemap.pyproj as pyproj
import matplotlib.pyplot as plt

def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()

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
          
def on_go(datafile,calbfile,dirname, calb_interp,linear_interp, despike,x_var,y_var, intsp_x, intsp_y, arcgrdval, data_match, buff, shape, gisgrd, surf, geopng, topo, blank, utm, wgs):
    #Variables related to direction of data collection
    #negative_gradient = True
    
    #x_var = (int(x_var))*2 #average measurement spacing 0.5
    #y_var = (int(y_var))*2 #average traverse spacing  0.25   
    #try:
    
    filename = os.path.basename(datafile)
       
    if not os.path.exists(dirname):
        os.makedirs(dirname, mode = 511)
    
    if linear_interp.isChecked():
        csv_path = dirname + '/' + 'Linear' + '/' + 'CSV_output'
    else:
        csv_path = dirname + '/' + 'Cubic' + '/' + 'CSV_output'  
    if not os.path.exists(csv_path):    
        os.makedirs(csv_path, mode = 511)
        print 'CSV folder created'
        flusher()
    
    output_name = csv_path + '/' + filename[0:-4] + '_calibrated.csv'
    
    if shape:
        if linear_interp.isChecked():
            raw_shape_path = dirname + '/' + 'Linear' + '/' + 'shapefiles'
        else: raw_shape_path = dirname + '/' + 'Cubic' + '/' + 'shapefiles'
        if not os.path.exists(raw_shape_path):
            os.makedirs(raw_shape_path, mode = 511)
            print "\n"'Shapefile folder created'
            flusher()
    else: raw_shape_path = False
    
    if topo:
        if linear_interp.isChecked():
            topo_path = dirname + '/' + 'Linear' + '/' + 'topo'
        else: topo_path = dirname + '/' + 'Cubic' + '/' + 'topo'
        if not os.path.exists(topo_path):
            os.makedirs(topo_path, mode = 511) 
            print "\n"'Topo folder created'
            flusher()
    else: topo_path = False
    
    if geopng:
        if linear_interp.isChecked():
            raw_img_path = dirname + '/' + 'Linear' + '/' + 'raw_images'
        else: raw_img_path = dirname + '/' + 'Cubic' + '/' + 'raw_images'
        if not os.path.exists(raw_img_path):
            os.makedirs(raw_img_path, mode = 511)
            print "\n"'Raw image folder created'
            flusher()
    else: raw_img_path = False
        
    if geopng:   
        if linear_interp.isChecked():   
            corr_img_path = dirname + '/' + 'Linear' + '/' + 'corr_images'
        else: corr_img_path = dirname + '/' + 'Cubic' + '/' + 'corr_images'
        if not os.path.exists(corr_img_path):
            os.makedirs(corr_img_path, mode = 511)
            print "\n"'Calibrated image folder created'
            flusher()
    else: corr_img_path = False 
    
    if gisgrd:          
        if linear_interp.isChecked():
            raw_gis_path = dirname + '/' + 'Linear' + '/' + 'raw_gis_grids'
        else: raw_gis_path = dirname + '/' + 'Cubic' + '/' + 'raw_gis_grids'
        if not os.path.exists(raw_gis_path):
            os.makedirs(raw_gis_path, mode = 511)
            print "\n"'Raw GIS grid folder created'
            flusher()
    else: raw_gis_path = False
            
    if gisgrd:         
        if linear_interp.isChecked():
            corr_gis_path = dirname + '/' + 'Linear' + '/' + 'corr_gis_grids'
        else: corr_gis_path = dirname + '/' + 'Cubic' + '/' + 'corr_gis_grids'
        if not os.path.exists(corr_gis_path):
            os.makedirs(corr_gis_path, mode = 511)
            print "\n"'Calibrated GIS grid folder created'
            flusher()
    else: corr_gis_path = False 
            
    if surf:
        if linear_interp.isChecked():
            raw_surf_path = dirname + '/' + 'Linear' + '/' + 'raw_surfer_grids'
        else: raw_surf_path = dirname + '/' + 'Cubic' + '/' + 'raw_surfer_grids'
        if not os.path.exists(raw_surf_path):
            os.makedirs(raw_surf_path, mode = 511)  
            print "\n"'Raw surfer grid folder created'
            flusher()
    else: raw_surf_path = False       
        
    if surf:
        if linear_interp.isChecked():
            corr_surf_path = dirname + '/' + 'Linear' + '/' + 'corr_surfer_grids'
        else: corr_surf_path = dirname + '/' + 'Cubic' + '/' + 'corr_surfer_grids'
        if not os.path.exists(corr_surf_path):
            os.makedirs(corr_surf_path, mode = 511) 
        print "\n"'Calibrated surfer grid folder created'
        flusher()
    else: corr_surf_path = False 
    

    #loads data from datafile into data array    
    if utm:
        data = np.loadtxt(datafile, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
    elif wgs:
        data = np.loadtxt(datafile, dtype = object, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
        data = rawtodd(data)
    else:
        data = np.loadtxt(datafile, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
    

    #Convert data to OS for use in GIS
    osgb36=pyproj.Proj("+init=EPSG:27700")
    UTM30N=pyproj.Proj("+init=EPSG:32630")
    wgs84=pyproj.Proj("+init=EPSG:4326")
    
    n_data = data[:,0]
    e_data = data[:,1]
        
    if utm:
        data_coord = np.array(pyproj.transform(UTM30N, osgb36, e_data, n_data)).T
        data = np.column_stack((data_coord, data[:,2:9]))
        print "\n"'UTM data loaded'
        flusher()
    elif wgs:
        data_coord = np.array(pyproj.transform(wgs84, osgb36, e_data, n_data)).T
        data = np.column_stack((data_coord, data[:,2:9]))         
        print "\n"'WGS84 data loaded'
        flusher()       
    else:   
        data = data
        data_coord = data[:,0:2]
        print "\n"'OS Data loaded'
        flusher()
         
 
    if not despike:
        print "\n" 'Data not despiked'
        flusher()
        if shape:        
            raw_shape_out(data, dirname, filename, raw_shape_path)
            print "\n"'Shapes created' 
            flusher()
        plot_data(filename, data, x_var, y_var, intsp_x, intsp_y, dirname, arcgrdval, data_match, geopng, gisgrd, surf, topo, blank, raw_img_path, raw_gis_path, topo_path, raw_surf_path)        
    
    output_orig = csv_path + '/' + filename[0:-4] + '_OS_transform.csv'
    outputOS = open(output_orig, 'w')
    np.savetxt(outputOS, data, fmt = '%8.3f', delimiter = ',', header = 'Eastings, Northings,Altitude,C1,I1,C2,I2,C3,I3', comments = '')
    print "\n" 'OS transformed raw data CSV exported'
    flusher()
    
    #loads data from calibration file into array
    if utm:
        calb = np.loadtxt(calbfile, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
    elif wgs:
        calb = np.loadtxt(calbfile, dtype = object, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
        calb = calbtodd(calb)       
    else:
        calb = np.loadtxt(calbfile, skiprows=1, usecols =(0,1,2,3,4,5,6,7,8))
    
        
    #Convert calibration to OS for use in GIS
    n_calb = calb[:,0]
    e_calb = calb[:,1]
    
    if utm:
        calb_coord = np.array(pyproj.transform(UTM30N, osgb36, e_calb, n_calb)).T 
        calb = np.column_stack((calb_coord, calb[:,2:9]))
        print "\n"'UTM calibration loaded'
        flusher()
    elif wgs:
        calb_coord = np.array(pyproj.transform(wgs84, osgb36, e_calb, n_calb)).T 
        calb = np.column_stack((calb_coord, calb[:,2:9]))
        print "\n"'WGS84 calibration loaded'
        flusher()        
    else:
        calb = calb
        calb_coord = calb[:,0:2]
        print 'calb coord', calb_coord
        print "\n"'OS calibration loaded'
        flusher()
        
    set_status_var('loaded into arrays')
    print 'loaded into arrays'
    flusher()
    
    #initiates spike removal for calibration and data arrays
    if despike:
        print "\n" 'Despiking data'
        flusher()
        data = spike_removal(data[:,0:3],data[:,3:9], 2, 2)
        calb = spike_removal(calb[:,0:3],calb[:,3:9], 3, 2)
        print "\n"'Despike completed'
        flusher()
        if shape:
            raw_shape_out(data, dirname, filename, raw_shape_path)
            print "\n"'Shapes created'
            flusher()
        plot_data(filename, data, x_var, y_var, intsp_x, intsp_y, dirname, arcgrdval, data_match, geopng, gisgrd, surf, topo, blank, raw_img_path, raw_gis_path, topo_path, raw_surf_path)        
    
    #produces arrays containing only coordinates
    data_coord = np.array(data[:,0:3])
    calb_coord = np.array(calb[:,0:3])
    
    #Corrects data against drift calibration file 
    out_array = drift_calb(data_coord,data,calb_coord,calb,calb_interp,buff,csv_path)
    print "\n"'Calibration completed'
    flusher()
    
    output = open(output_name, 'w')
    
    header = 'Eastings, Northings,Altitude,C1,I1,C2,I2,C3,I3'
    print>>output, header
           
    if shape:
        print "\n"'Shapes created'
        flusher()
        corr_shape_out(out_array, dirname, filename, raw_shape_path)
          
    np.savetxt(output, out_array, fmt = '%8.3f', delimiter=',')
    print "\n"'OS transformed calibrated data saved'
    flusher()
     
    topo = False   
    plot_corr(out_array, filename, x_var, y_var, intsp_x, intsp_y, dirname, arcgrdval, geopng, gisgrd, surf, topo, blank, corr_img_path, corr_gis_path, topo_path, corr_surf_path)        
    
    #The last thing that happens!
    plt.show()   

    
    ##########
    #Is any of the following doing anything???       
    '''
           
    mean = np.mean(out_array,axis=0)
    print 'mean', mean        
    out_array[:,3:9] = np.subtract(out_array[:,3:9],mean[3:9])
                    
    #I don't want to peform convex hull peeling 
    out_array = hull_peeling(out_array,85.0)        
    
    
    #Begin Periodic Filtering
    #periodic_filter(out_array[:,3:9])
      
    #begin calculation of initial vector
    x_gradients = np.subtract(out_array[1:-1,0],out_array[0:-2,0])
    y_gradients = np.subtract(out_array[1:-1,1],out_array[0:-2,1])
    print len(x_gradients), len(y_gradients)
    #old_err_state = np.seterr(divide='ignore')
    for i in x_gradients:
        if i <> 0:
            return x_gradients
    for i in y_gradients:
        if i <> 0:
            return y_gradients 
 
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
    
    '''