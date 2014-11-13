# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 13:29:54 2012

@author: fpopecar
"""
import numpy as np
from scipy.spatial import KDTree
from scipy import interpolate
import sys

def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()
        
def drift_calb(data_coord,data,calb_coord,calb,interp_method,buff, csv_path):
    """
    Takes four Numpy Arrays
    1 - Data Corrdinates in X, Y, (Z)
    2 - Data
    3 - Calibration line coordinates in X, Y, (Z) - Must be the same format as data coordinates
    4 - Calibration Data - must be the same format as Data
    """
    print "\n"'Calibration started'
    flusher()
    #produces tree of data and calibration coordinates
    dt_tree = KDTree(data_coord)
    cl_tree = KDTree(calb_coord)
    
    print 'trees created'
    flusher()
    
    #creates an array containing indexes of calibration point within specified distance of each measured data point
    buff =  float(buff)
    coords = dt_tree.query_ball_tree(cl_tree, buff)
    #print coords
    print len(coords), 'matching coordinates'"\n"
    flusher()
    temp = int(len(coords))
    
    #creates empty array the same size as data array
    calb_array = np.empty((temp,9))
    
    #produces temp blank lists 
    for i in range(3,9):
        vars()['temp',i]=[]
        
    xp = []
    j=0
    
    #creates list of calibration data
    for row in coords:
        if row:
            xp.append(j)
            for i in range(3,9):
                temp_calb = 0
                for k in range(len(row)):
                    temp_calb += calb[row[k],i]
                tempdata = data[(j),(i)]  - temp_calb/len(row)
                vars()['temp',i].append(tempdata)
                
        j += 1
        
    Northings = data[:,0]
    Eastings = data[:,1]
    Altitude = data[:,2]
    
    calb_array = np.column_stack((Northings,Eastings,Altitude))
         
    #Creates list of interpolated calibration data using chosen method
    for i in range(3,9):
        if interp_method:
            s = interpolate.UnivariateSpline(xp,vars()['temp',i],k=3)
            vars()['c'+str(i)] = s(range(j))
        else:
            vars()['c' + str(i)] = np.interp(range(j),xp,vars()['temp',i])
        
        calb_array = np.column_stack((calb_array,vars()['c'+str(i)]))
    #prints the calibration curves to csv files to check for erroneous results.
        np.savetxt(csv_path + '/' + 'c'+str(i)+'.csv', vars()['c'+str(i)], delimiter=',')
        
    out_array = np.subtract(data,calb_array)
    
    out_array[:,0:3] = data_coord
    
    return out_array