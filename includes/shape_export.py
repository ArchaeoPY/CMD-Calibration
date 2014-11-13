# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 14:01:05 2014

@author: Mary K Saunders

Script from http://pygis.blogspot.co.uk/2012_10_01_archive.html
"""

import shapefile
import numpy as np
import os

def  raw_shape_out(data, dirname, filename, raw_shape_path):       
     
    #Set up blank lists for data
    x = data[:,0]
    np.array(x).tolist()
    y = data[:,1]
    np.array(y).tolist()
    z = data[:,2]
    np.array(z).tolist()
    
    c1 = data[:,3]
    np.array(c1).tolist()
    i1 = data[:,4]
    np.array(i1).tolist()
    c2 = data[:,5]
    np.array(c2).tolist()
    i2 = data[:,6]
    np.array(i2).tolist()
    c3 = data[:,7]
    np.array(c3).tolist()
    i3 = data[:,8]
    np.array(i3).tolist()
     
    #Set up shapefile writer and create empty fields
    w = shapefile.Writer(shapefile.POINTZ)
    w.autoBalance = 1 #ensures gemoetry and attributes match
    w.field('X','F',20,5)
    w.field('Y','F',20,5) #float - needed for coordinates
    w.field('Z','F',20,5)
    w.field('c1','F',20,5)
    w.field('i1','F',20,5) 
    w.field('c2','F',20,5)
    w.field('i2','F',20,5)
    w.field('c3','F',20,5) 
    w.field('i3','F',20,5)
    
    #loop through the data and write the shapefile
    for j,k in enumerate(x):
        w.point(k, y[j], z[j]) #write the geometry
        w.record(k, y[j], z[j], c1[j], i1[j], c2[j], i2[j], c3[j], i3[j]) #write the attributes
    
    #Save shapefile
    w.save(raw_shape_path + '/' + filename[0:-4] + '_' + 'raw' + '.prj')
    
    #Save projection file
    proj_name = raw_shape_path + '/' + filename[0:-4] + '_' + 'raw' + '.prj'
    proj = open(proj_name, 'w')    
    
    proj.write('PROJCS["British_National_Grid",GEOGCS["GCS_OSGB_1936",DATUM["D_OSGB_1936",SPHEROID["Airy_1830",6377563.396,299.3249646]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",400000.0],PARAMETER["False_Northing",-100000.0],PARAMETER["Central_Meridian",-2.0],PARAMETER["Scale_Factor",0.9996012717],PARAMETER["Latitude_Of_Origin",49.0],UNIT["Meter",1.0]]')
    proj.close()
   
def  corr_shape_out(out_array, dirname, filename, raw_shape_path):

    #Set up blank lists for data
    x = out_array[:,0]
    np.array(x).tolist()
    y = out_array[:,1]
    np.array(y).tolist()
    z = out_array[:,2]
    np.array(z).tolist()
    
    c1 = out_array[:,3]
    np.array(c1).tolist()
    i1 = out_array[:,4]
    np.array(i1).tolist()
    c2 = out_array[:,5]
    np.array(c2).tolist()
    i2 = out_array[:,6]
    np.array(i2).tolist()
    c3 = out_array[:,7]
    np.array(c3).tolist()
    i3 = out_array[:,8]
    np.array(i3).tolist()
     
    #Set up shapefile writer and create empty fields
    w = shapefile.Writer(shapefile.POINTZ)
    w.autoBalance = 1 #ensures gemoetry and attributes match
    w.field('X','F',20,5)
    w.field('Y','F',20,5) #float - needed for coordinates
    w.field('Z','F',20,5)
    w.field('c1','F',20,5)
    w.field('i1','F',20,5) 
    w.field('c2','F',20,5)
    w.field('i2','F',20,5)
    w.field('c3','F',20,5) 
    w.field('i3','F',20,5)
    
    #loop through the data and write the shapefile
    for j,k in enumerate(x):
        w.point(k, y[j], z[j]) #write the geometry
        w.record(k, y[j], z[j], c1[j], i1[j], c2[j], i2[j], c3[j], i3[j]) #write the attributes
    
    #Save shapefile
    w.save(raw_shape_path + '/' + filename[0:-4] + '_' + 'corr' + '.prj')
    
    #Save projection file
    proj_name = raw_shape_path + '/' + filename[0:-4] + '_' + 'corr' + '.prj'
    proj = open(proj_name, 'w')    
    
    proj.write('PROJCS["British_National_Grid",GEOGCS["GCS_OSGB_1936",DATUM["D_OSGB_1936",SPHEROID["Airy_1830",6377563.396,299.3249646]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",400000.0],PARAMETER["False_Northing",-100000.0],PARAMETER["Central_Meridian",-2.0],PARAMETER["Scale_Factor",0.9996012717],PARAMETER["Latitude_Of_Origin",49.0],UNIT["Meter",1.0]]')
    proj.close()   