# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 20:29:46 2014

@author: mary
"""
import numpy as np


def rawtodd(data):
   
    xi = np.array(data[:,0])
    
    error_pos = []
    
    for i,x in enumerate(xi):
        if len(x) < 6:
            error_pos.append(i)
            
    data = np.delete(data, error_pos, axis=0)
    
    xi = data[:,0]
    yi = data[:,1]
    
    height = [float(item) for item in data[:,2]]
    c1 = [float(item) for item in data[:,3]]
    i1 = [float(item) for item in data[:,4]]
    c2 = [float(item) for item in data[:,5]]
    i2 = [float(item) for item in data[:,6]]
    c3 = [float(item) for item in data[:,7]]
    i3 = [float(item) for item in data[:,8]]
    
    data = np.column_stack((height, c1, i1, c2, i2, c3, i3))
    
    degx = [float(item[0:2]) for item in xi]
    degy = [float(item[0:3]) for item in yi]
    
    mnsx = [float(item[3:-1])/60 for item in xi]
    mnsy = [float(item[3:-1])/60 for item in yi]
    
    xi = np.add(degx, mnsx)
    xi = np.array(xi).T
    yi = -abs(np.add(degy, mnsy))
    yi = np.array(yi).T

    data = np.column_stack((xi, yi, data))
    
    return data

  
def calbtodd(calb):

    xi = np.array(calb[:,0])
    
    error_pos = []
    
    for i,x in enumerate(xi):
        if len(x) < 6:
            error_pos.append(i)
            
    calb = np.delete(calb, error_pos, axis=0)
    
    xi = calb[:,0]
    yi = calb[:,1]
    
    height = [float(item) for item in calb[:,2]]
    c1 = [float(item) for item in calb[:,3]]
    i1 = [float(item) for item in calb[:,4]]
    c2 = [float(item) for item in calb[:,5]]
    i2 = [float(item) for item in calb[:,6]]
    c3 = [float(item) for item in calb[:,7]]
    i3 = [float(item) for item in calb[:,8]]
    
    calb = np.column_stack((height, c1, i1, c2, i2, c3, i3))
    
    degx = [float(item[0:2]) for item in xi]
    degy = [float(item[0:3]) for item in yi]
    
    mnsx = [float(item[3:-1])/60 for item in xi]
    mnsy = [float(item[3:-1])/60 for item in yi]
    
    xi = np.add(degx, mnsx)
    xi = np.array(xi).T
    yi = -abs(np.add(degy, mnsy))
    yi = np.array(yi).T
    
    calb = np.column_stack((xi, yi, calb))
    
    return calb