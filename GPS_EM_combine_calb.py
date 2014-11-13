# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 19:01:33 2012

@author: MKS and FP-C


Copyright 2014
"""
import sys
import numpy as np
import os
from includes.plot_data import plot_corr
from includes.shape_export import corr_shape_out
from PyQt4 import QtGui
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
    
def on_comb(datafile,calbtwoname,calbthreename, calbfourname, calbfivename, dirname, x_var, y_var, intsp_x, intsp_y, arcgrdval, shape, gisgrd, surf, geopng, topo, blank):      
        
        calbtwoname = str(calbtwoname)
        calbthreename = str(calbthreename)
        calbfourname = str(calbfourname)
        calbfivename = str(calbfivename)        
        
        fileone = os.path.basename(datafile)
        if calbtwoname <> '':
            filetwo = os.path.basename(calbtwoname)
        if calbthreename <> '':
            filethree = os.path.basename(calbthreename)
        if calbfourname <> '':
            filefour = os.path.basename(calbfourname)
        if calbfivename <> '':
            filefive = os.path.basename(calbfivename)
        
        if calbfivename <> '':
            filename = fileone[0:-28] + '_' + filetwo[0:-28] + '_' + filethree[0:-28] + '_' + filefour[0:-28] + '_' + filefive[0:-28] + '.csv'                
        elif calbfourname <> '':
            filename = fileone[0:-28] + '_' + filetwo[0:-28] + '_' + filethree[0:-28] + '_' + filefour[0:-28] + '.csv'                   
        elif calbthreename <> '':
            filename = fileone[0:-28] + '_' + filetwo[0:-28] + '_' + filethree[0:-28] + '.csv'
        elif calbtwoname <> '': 
            filename = fileone[0:-28] + '_' + filetwo[0:-28] + '.csv'
        else:
            filename = fileone[0:-28] + '.csv'
           
        if not os.path.exists(dirname):
            os.makedirs(dirname, mode = 511)
        
        csv_path = dirname + '/' + 'Combined' + '/' + 'CSV_output'
        if not os.path.exists(csv_path):    
            os.makedirs(csv_path, mode = 511)
            print 'CSV folder created'
        flusher()
        
        output_name = csv_path + '/' + filename[0:-4] + '_OS_calibrated.csv'
        
        if shape:
            raw_shape_path = dirname + '/' + 'Combined' + '/' + 'shapefiles'
            if not os.path.exists(raw_shape_path):
                os.makedirs(raw_shape_path, mode = 511)
                print "\n"'Shapefile folder created'
                flusher()
        else: raw_shape_path = False

        if topo:
            topo_path = dirname + '/' + 'Combined' + '/' + 'topo'
            if not os.path.exists(topo_path):
                os.makedirs(topo_path, mode = 511) 
                print "\n"'Topo folder created'
                flusher()
        else: topo_path = False

        if geopng:   
            corr_img_path = dirname + '/' + 'Combined' + '/' + 'corr_images'
            if not os.path.exists(corr_img_path):
                os.makedirs(corr_img_path, mode = 511)
                print "\n"'Image folder created'
                flusher()
        else: corr_img_path = False 
        
        if gisgrd:         
            corr_gis_path = dirname + '/' + 'Combined' + '/' + 'corr_gis_grids'
            if not os.path.exists(corr_gis_path):
                os.makedirs(corr_gis_path, mode = 511)
                print "\n"'GIS grid folder created'
                flusher()
        else: corr_gis_path = False 
                
        if surf:
            corr_surf_path = dirname + '/' + 'Combined' + '/' + 'corr_surfer_grids'
            if not os.path.exists(corr_surf_path):
                os.makedirs(corr_surf_path, mode = 511)   
                print "\n"'Surfer grid folder created'
                flusher()
        else: corr_surf_path = False 
        
        #loads data from datafile into data array    
        fileone = np.loadtxt(datafile, skiprows=1, delimiter = ',', usecols =(0,1,2,3,4,5,6,7,8))
        print "\n"'File one loaded'"\n"
        flusher()    
        
        if not calbtwoname == '':
            filetwo = np.loadtxt(calbtwoname, skiprows=1, delimiter = ',', usecols =(0,1,2,3,4,5,6,7,8))
            print 'File two loaded'"\n" 
            flusher()  
        else:
            print 'No second file'"\n"
            flusher()
        
        if not calbthreename == '':
            filethree = np.loadtxt(calbthreename, skiprows=1, delimiter = ',', usecols =(0,1,2,3,4,5,6,7,8))
            print 'File three loaded'"\n"
            flusher()
        else:
            print 'No third file'"\n"
            flusher()
            
        if not calbfourname == '':
            filefour = np.loadtxt(calbfourname, skiprows=1, delimiter = ',', usecols =(0,1,2,3,4,5,6,7,8))
            print 'File four loaded'"\n"
            flusher()
        else:
            print 'No fourth file'"\n"
            flusher()    
            
        if not calbfivename == '':
            filefive = np.loadtxt(calbfivename, skiprows=1, delimiter = ',', usecols =(0,1,2,3,4,5,6,7,8))
            print 'File five loaded'"\n"
            flusher()
        else:
            print 'No fifth file'"\n"
            flusher()
            
        if calbfivename <> '':
            out_array = np.vstack((fileone, filetwo, filethree, filefour, filefive))
        elif calbfourname <> '':
            out_array = np.vstack((fileone, filetwo, filethree, filefour))
        elif calbthreename <> '':
            out_array = np.vstack((fileone, filetwo, filethree))
        elif calbtwoname <> '':    
            out_array = np.vstack((fileone, filetwo))
        else:
            out_array = fileone
        print 'Files combined'"\n"
        flusher() 
    
        output = open(output_name, 'w')
        
        header = 'Eastings, Northings,Altitude,C1,I1,C2,I2,C3,I3'
        print>>output, header
               
        if shape:
            print 'Shapes created'"\n"
            flusher()
            corr_shape_out(out_array, dirname, filename, raw_shape_path)
              
        np.savetxt(output, out_array, fmt = '%8.3f', delimiter=',')
        print 'OS transformed calibrated data saved'"\n"
        flusher()
        
        plot_corr(out_array, filename, x_var, y_var, intsp_x, intsp_y, dirname, arcgrdval, geopng, gisgrd, surf, topo, blank, corr_img_path, corr_gis_path, topo_path, corr_surf_path)       
    
        #The last thing that happens!
        plt.show()   
