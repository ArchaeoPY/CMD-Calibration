# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 21:11:44 2014

@author: Mary Kathleen Saunders

Exports grid files for use in Surfer
"""
import numpy as np
import os
import sys

def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()
    
def raw_surf_out(dirname, filename, data, i, min_x, max_x, min_y, max_y, grid, raw_surf_path):  
    
    print 'Exporting raw Surfer grids: column', -2+i
    flusher()
    
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
               
    output_name = raw_surf_path + '/' + filename[0:-4] + '_' + ext + '.grd'
    output = open(output_name, 'w')
    
    ncols = len(grid[0,:])
    nrows = len(grid)  
    min_z = np.amin(data[:,i])
    max_z = np.amin(data[:,i])
    
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
    
    
def corr_surf_out(dirname, filename, out_array, i, min_x, max_x, min_y, max_y, grid, corr_surf_path):  
    
    print 'Exporting calibrated Surfer grids: column', -2+i
    flusher()
    
    if -2+i == 1:
        ext = 'corr_c1'
    elif -2+i == 2:
        ext = 'corr_i1'
    elif -2+i == 3:
        ext = 'corr_c2'
    elif -2+i == 4:
        ext = 'corr_i2'
    elif -2+i == 5:
        ext = 'corr_c3'
    else:
        ext = 'corr_i3'
        
    output_name = corr_surf_path + '/' + filename[0:-4] + '_' + ext + '.grd'
    output = open(output_name, 'w')
    
    ncols = len(grid[0,:])
    nrows = len(grid)  
    min_z = np.amin(out_array[:,i])
    max_z = np.amin(out_array[:,i])
    
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
