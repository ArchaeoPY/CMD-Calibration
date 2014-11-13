# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 19:01:33 2012

@author: Finnegan Pope-Carter and MKS


Copyright 2014
"""
import sys
import numpy as np
import os
from includes.despike import despike as spike_removal
from includes.plot_data import plot_data
from includes.shape_export import raw_shape_out
from includes.coords import rawtodd
from PyQt4 import QtGui
import mpl_toolkits.basemap.pyproj as pyproj
import matplotlib.pyplot as plt


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

def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()
      
def on_view(datafile, dirname, despike, x_var, y_var, intsp_x, intsp_y, arcgrdval, shape, gisgrd, surf, geopng, topo, blank, utm, wgs):
     
    data_match = False
    
    filename = os.path.basename(datafile)
       
    if not os.path.exists(dirname):
        os.makedirs(dirname, mode = 511)
        
    dirname = dirname + '/' + 'raw_data'
    
    csv_path = dirname + '/' + 'CSV_output'         
    if not os.path.exists(csv_path):    
        os.makedirs(csv_path, mode = 511)
        print "\n"'CSV folder created'
        flusher()
    
    if shape:
        raw_shape_path = dirname + '/' + 'shapefiles'        
        if not os.path.exists(raw_shape_path):
            os.makedirs(raw_shape_path, mode = 511)
            print "\n"'Shapefile folder created'
            flusher()
    else: raw_shape_path = False
    
    if topo:
        topo_path = dirname + '/' + 'topo'
        if not os.path.exists(topo_path):
            os.makedirs(topo_path, mode = 511)    
            print "\n"'Topo folder created'
            flusher()
    else: topo_path = False
    
    if geopng:
        raw_img_path = dirname + '/' + 'raw_images'
        if not os.path.exists(raw_img_path):
            os.makedirs(raw_img_path, mode = 511)
            print "\n"'Image folder created'
            flusher()
    else: raw_img_path = False
        
    if gisgrd:          
        raw_gis_path = dirname + '/' + 'raw_gis_grids'
        if not os.path.exists(raw_gis_path):
            os.makedirs(raw_gis_path, mode = 511)
            print "\n"'GIS grid folder created'
            flusher()
    else: raw_gis_path = False
            
    if surf:
        raw_surf_path = dirname + '/' + 'raw_surfer_grids'
        if not os.path.exists(raw_surf_path):
            os.makedirs(raw_surf_path, mode = 511)  
            print "\n"'Surfer grid folder created'
            flusher()
    else: raw_surf_path = False
    
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
        data_coord = data[:,0:1]
        print "\n"'OS Data loaded'
        flusher()
        
    set_status_var('loaded into arrays')
    print 'loaded into arrays'
    flusher()         
 
    if not despike:
        print "\n" 'Data not despiked'
        flusher()
        if shape:        
            raw_shape_out(data, dirname, filename, raw_shape_path)
            print "\n"'Shapes created' 
            flusher()
        plot_data(data, x_var, y_var, intsp_x, intsp_y, filename, dirname, arcgrdval, data_match, geopng, gisgrd, surf, topo, blank, raw_img_path, raw_gis_path, topo_path, raw_surf_path)        
    
    output_orig = csv_path + '/' + filename[0:-4] + '_OS_transform.csv'
    outputOS = open(output_orig, 'w')
    np.savetxt(outputOS, data, fmt = '%8.3f', delimiter = ',', header = 'Eastings, Northings,Altitude,C1,I1,C2,I2,C3,I3', comments = '')
    print "\n" 'OS transformed raw data CSV exported'
    flusher()  
    
    #initiates spike removal for calibration and data arrays
    if despike:
        print "\n" 'Despiking data'
        flusher()
        data = spike_removal(data[:,0:2],data[:,3:9], 2, 2)
        print "\n"'Despike completed'
        flusher()
        if shape:
            raw_shape_out(data, dirname, filename, raw_shape_path)
            print "\n"'Shapes created'
            flusher()
        plot_data(filename, data, x_var, y_var, intsp_x, intsp_y, dirname, arcgrdval, data_match, geopng, gisgrd, surf, topo, blank, raw_img_path, raw_gis_path, topo_path, raw_surf_path)        
    
    #The last thing that happens!
    plt.show()   