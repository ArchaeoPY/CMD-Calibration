# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 17:19:15 2014

@author: Mary Kathleen Saunders
"""

import numpy as np
import os
from matplotlib.mlab import griddata
from scipy.spatial import cKDTree as KDTree
import sys


def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()

def gis_raw_out(filename, raw_img_path, raw_gis_path, arcgrdval,colrng, i, x, y, z, xi2, yi2, min_x, max_x, min_y, max_y, arccxpnts, arccypnts, blank):  
    
    print 'Exporting raw GIS grid: column', -2+i
    flusher()   
    #Grid data    
    arcgrid = griddata(x, y, z, xi2, yi2, interp = 'nn')
    
    #Make a grid of x,y values
    a, b = np.mgrid[min_x:max_x:arccxpnts, min_y:max_y:arccypnts]

    tree = KDTree(np.c_[x, y])
    dist, _ = tree.query(np.c_[a.ravel(), b.ravel()], k=1)
    dist = dist.reshape(a.shape).T
    
    arcgrid[dist > blank] = np.nan 

    #Set grd export parameters 
    
    if -2+i == 1:
        ext = 'raw_c1'
    elif -2+i == 2:
        ext = 'raw_i1'
    elif -2+i == 3:
        ext = 'raw_c2'
    elif -2+i == 4:
        ext = 'raw_i2'
    elif -2+i == 5:
        ext = 'raw_c3'
    else:
        ext = 'raw_i3'
        
    output_name = raw_gis_path + '/' + filename[0:-4] + '_' + ext + '.asc'
    output = open(output_name, 'w')
    
    proj_name = raw_gis_path + '/' + filename[0:-4] + '_' + ext + '.prj'
    proj = open(proj_name, 'w')
    
    ncols = len(arcgrid[0,:])
    nrows = len(arcgrid)
    xllcorner = min_x
    yllcorner = min_y
    cellsize = arcgrdval
    nodata_value = '2047.5'   
  
    #Iternate through rows, bottom to top to get correct orientation
    R = 0
    
    row = arcgrid[R,:]    
    expt_data = ()
    for row in arcgrid[::-1]:
        row_copy = np.copy(row)
        expt_data = np.append(expt_data, row_copy)

    R += 1
    
    #Set no data value and transpose data
    expt_data[np.isnan(expt_data)] = 2047.5
    expt_data = expt_data,

    #Set up correct file format
    template = """ncols {ncols}
nrows {nrows}
xllcorner {xllcorner}
yllcorner {yllcorner}
cellsize {cellsize}
nodata_value {nodata_value}"""    
    
    context = {
     "ncols":ncols, 
     "nrows":nrows,
     "xllcorner":xllcorner,
     "yllcorner":yllcorner,
     "cellsize":cellsize,
     "nodata_value":nodata_value
     } 
  
    header = template.format(**context)
    print>> output,header
    
    np.savetxt(output, expt_data, fmt = '%-f', delimiter=' ')
    
    proj.write('PROJCS["British_National_Grid",GEOGCS["GCS_OSGB_1936",DATUM["D_OSGB_1936",SPHEROID["Airy_1830",6377563.396,299.3249646]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",400000.0],PARAMETER["False_Northing",-100000.0],PARAMETER["Central_Meridian",-2.0],PARAMETER["Scale_Factor",0.9996012717],PARAMETER["Latitude_Of_Origin",49.0],UNIT["Meter",1.0]]')
    proj.close()
