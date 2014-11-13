# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 20:12:16 2014

@author: Mary Kathleen Saunders
"""
from collections import OrderedDict
from matplotlib.mlab import griddata
import numpy as np
import os
from scipy.spatial import cKDTree as KDTree
import sys

def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()

def topo_out(data, filename, topo_path, arcgrdval, intsp_x, intsp_y, arccxpnts, arccypnts, min_x, max_x, min_y, max_y, rng_x, rng_y, xi2, yi2, blank):
    
    #Values to grid
    x = data[:,0]
    y = data[:,1] 
    z = data[:,2]
    
    newxyz = OrderedDict()
    for point in zip(x, y, z):
        newxyz.setdefault(point[:2], point)
    newxyz = newxyz.values()
    newxyz = np.array(newxyz)

    x = newxyz[:,0]
    y = newxyz[:,1]
    z = newxyz[:,2]
    
    #Export arcgis grid
    print "\n"'Exporting topo data ArcGIS grid'
    flusher()
    
    topogrid = griddata(x, y, z, xi2, yi2, interp = 'nn')
    
    #Make a grid of x,y values
    a, b = np.mgrid[min_x:max_x:arccxpnts, min_y:max_y:arccypnts]

    tree = KDTree(np.c_[x, y])
    dist, _ = tree.query(np.c_[a.ravel(), b.ravel()], k=1)
    dist = dist.reshape(a.shape).T
                            
    topogrid[dist > blank] = np.nan  
    
    #Set grd export parameters       
    output_name = topo_path + '/' + filename[0:-4] + '_' + 'topo' + '.asc'
    output = open(output_name, 'w')
    
    proj_name = topo_path + '/' + filename[0:-4] + '_' + 'topo' + '.prj'
    proj = open(proj_name, 'w')

    ncols = len(topogrid[0,:])
    nrows = len(topogrid)
    xllcorner = min_x
    yllcorner = min_y
    cellsize = arcgrdval
    nodata_value = '2047.5'   
  
    #Iternate through rows, bottom to top to get correct orientation
    R = 0
    
    row = topogrid[R,:]    
    expt_data = ()
    for row in topogrid[::-1]:
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

    #Export surfer grid
    print 'Exporting topo data Surfer grid'
    flusher()
        
    output_name = topo_path + '/' + filename[0:-4] + '_' + 'topo' + '.grd'
    output = open(output_name, 'w')
    
    #Takes user input values
    intsp_x = float(intsp_x)
    intsp_y = float(intsp_y)
    step_x = 1/intsp_x
    step_y = 1/intsp_y
    
    #Determine grid spacing    
    noxpnts = ((step_x) * (rng_x)) + 1
    noypnts = ((step_y) * (rng_y)) + 1

    xi = np.linspace(min_x, max_x, noxpnts)
    yi = np.linspace(min_y, max_y, noypnts)   
    
    #Determine grid parameters for make grid       
    cxpnts = rng_x/intsp_x 
    cxpnts = '%ij' %(cxpnts)
    cxpnts = complex(cxpnts)
    
    cypnts = rng_y/intsp_y
    cypnts = '%ij' %(cypnts)
    cypnts = complex(cypnts)
    
    grid = griddata(x, y, z, xi, yi, interp = 'nn')
    
    #Make a grid of x,y values
    a, b = np.mgrid[min_x:max_x:cxpnts, min_y:max_y:cypnts]

    tree = KDTree(np.c_[x, y])
    dist, _ = tree.query(np.c_[a.ravel(), b.ravel()], k=1)
    dist = dist.reshape(a.shape).T
    
    grid[dist > blank] = np.nan 
        
    ncols = len(grid[0,:])
    nrows = len(grid)  
    min_z = np.amin(data[:,2])
    max_z = np.amin(data[:,2])
    
    #Iternate through rows, bottom to top to get correct orientation
    R = 0
    
    row = grid[R,:]    
    expt_data = ()
    for row in grid:
        row_copy = np.copy(row)
        expt_data = np.append(expt_data, row_copy)

    R += 1
    
    #Set no data value and transpose data
    expt_data[np.isnan(expt_data)] = 1.70141E+38
    expt_data = expt_data,

    #Set up correct file format

    template = """DSAA
{ncols} {nrows}
{min_x} {max_x}
{min_y} {max_y}
{min_z} {max_z}"""    
    
    context = {
     "ncols":ncols, "nrows":nrows,
     "min_x":min_x, "max_x":max_x,
     "min_y":min_y, "max_y":max_y,
     "min_z":min_z, "max_z":max_z
     } 
  
    header = template.format(**context)
    print>> output,header
    
    np.savetxt(output, expt_data, fmt = '%-f', delimiter='\t')  
