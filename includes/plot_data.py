# -*- coding: utf-8 -*-
"""
Created on Tue Jul 01 14:57:30 2014

@author: Mary Kathleen Saunders
"""

import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np
from collections import OrderedDict
from raw_export import gis_raw_out
from corr_export import gis_corr_out
from surfer_out import raw_surf_out, corr_surf_out 
from includes.topo_tastic import topo_out
import os
from scipy.spatial import cKDTree as KDTree
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import matplotlib
#from PyQt4 import QtCore

matplotlib.rcParams.update({'font.size': 8})

def flusher():
    with open('log.txt', 'w') as f:
        sys.stdout.flush()
        sys.stderr.flush()
        f.flush()

def plot_data(filename, data, x_var, y_var, intsp_x, intsp_y, dirname, arcgrdval, data_match, geopng, gisgrd, surf, topo, blank, raw_img_path, raw_gis_path, topo_path, raw_surf_path):        
    
    print "\n"'Starting plot_data' "\n"
    flusher()     
    #Regrid and plot data
    min_x = np.amin(data[:,0])
    max_x = np.amax(data[:,0])
    min_y = np.amin(data[:,1])
    max_y = np.amax(data[:,1])
    rng_x = max_x - min_x
    rng_y = max_y - min_y
    
    #Determine the existing data spacing
    x_values = data[:,0]
    x_values = x_values.tolist()
    x_values = list(set(x_values))
    
    spac_x = rng_x/(len(x_values) - 1)
    print 'x spacing', spac_x
    flusher()
    
    y_values = data[:,1]
    y_values = y_values.tolist()
    y_values = list(set(y_values))
    
    spac_y = rng_y/(len(y_values) - 1)
    print 'y spacing', spac_y
    flusher()
    
    #Takes user input values
    intsp_x = float(intsp_x)
    intsp_y = float(intsp_y)    
    step_x = 1/intsp_x
    step_y = 1/intsp_y
    
    #Determine grid parameters for make grid       
    cxpnts = rng_x/intsp_x 
    cxpnts = '%ij' %(cxpnts)
    cxpnts = complex(cxpnts)
    
    cypnts = rng_y/intsp_y
    cypnts = '%ij' %(cypnts)
    cypnts = complex(cypnts)
    
        
    #Determine grid spacing for matplotlib gridding    
    noxpnts = ((step_x) * (rng_x)) + 1
    noypnts = ((step_y) * (rng_y)) + 1
    
    xi = np.linspace(min_x, max_x, noxpnts)
    yi = np.linspace(min_y, max_y, noypnts)
    
    blank = float(blank)   
    print blank
    flusher()
    
    if gisgrd or surf or topo:
        #Takes user input value
        arcgrdval = float(arcgrdval)
        step = 1/arcgrdval
    
        #Determine arcgis grid spacing    
        no_arcxpnts = ((step) * (rng_x)) + 1
        no_arcypnts = ((step) * (rng_y)) + 1
        
        xi2 = np.linspace(min_x, max_x, no_arcxpnts)
        yi2 = np.linspace(min_y, max_y, no_arcypnts)
        
        #Determine grid parameters for make grid 
        arccxpnts = rng_x/arcgrdval 
        arccxpnts = '%ij'%(arccxpnts)
        arccxpnts = complex(arccxpnts)
    
        arccypnts = rng_y/arcgrdval
        arccypnts = '%ij' %(arccypnts)
        arccypnts = complex(arccypnts)
        
    if topo:        
        topo_out(data, filename, topo_path, arcgrdval, intsp_x, intsp_y, arccxpnts, arccypnts, min_x, max_x, min_y, max_y, rng_x, rng_y, xi2, yi2, blank)
            
    colrng = range(len(data[0,:]))
            
    i = 0
    for i in colrng:
        if i > 2:
                x = data[:,0]
                y = data[:,1] 
                z = data[:,i]
                
                newxyz = OrderedDict()
                for point in zip(x, y, z):
                    newxyz.setdefault(point[:2], point)
                newxyz = newxyz.values()
                newxyz = np.array(newxyz)
            
                x = newxyz[:,0]
                y = newxyz[:,1]
                z = newxyz[:,2]
                
                #Zero mean data set
                if data_match:                
                    mean_z = np.mean(z)
                    z = z - mean_z 
                
                #Grid data for display  
                print "\n"'Gridding raw data: column', -2+i
                flusher()
                grid = griddata(x, y, z, xi, yi, interp = 'nn')
                
                #Make a grid of x,y values
                a, b = np.mgrid[min_x:max_x:cxpnts, min_y:max_y:cypnts]

                tree = KDTree(np.c_[x, y])
                dist, _ = tree.query(np.c_[a.ravel(), b.ravel()], k=1)
                dist = dist.reshape(a.shape).T
                
                grid[dist > blank] = np.nan 
                print 'Blanked grid: column', -2+i
                flusher()
                                
                #Export each data set as an image 
                if geopng:
                    print 'Saving raw image: column', -2+i
                    flusher()
                                           
                
                    if intsp_x <= intsp_y:
                        x_m_pxl = intsp_x
                    else:
                        x_m_pxl = intsp_y                    
                    
                    y_m_pxl = -(x_m_pxl)
                    x_tlc = min_x + (intsp_x/2)
                    y_tlc = max_y + (intsp_y/2)
                    rot = 0.00000000000
                    
                    if intsp_x <= intsp_y:
                        xPix = noxpnts
                        yPix = (intsp_y/intsp_x)*noypnts
                    else:
                        yPix = noypnts 
                        xPix = (intsp_x/intsp_y)*noxpnts
                    
                    xSize = rng_x/50 #relating real size to image size
                    ySize = (xSize/xPix)*yPix
                    dpi = xPix/xSize
                                    
                    expimg = plt.figure(0, dpi = dpi, figsize = (xSize, ySize))
                    plt.imshow(grid, cmap=plt.cm.jet, vmin = np.percentile(z, 15), vmax = np.percentile(z, 85), extent = (min_x, max_x, min_y, max_y), interpolation = 'none', origin = 'lower')
                    a = plt.gca()
                    a.set_xticks([]); a.set_yticks([])
                    a.set_axis_off()
                    a.patch.set_alpha(0)
                    plt.tight_layout(rect=[0, 0, 1, 1], pad = 0, h_pad = 0)
                    
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
                        
                    dpi = expimg.get_dpi()
                    size = expimg.get_size_inches()
                    print "DPI: %f" % dpi
                    print "Size in inches: %f x %f" % (size[0], size[1])
                    print "Pixels: %i x %i" % (dpi * size[0], dpi * size[1])
                    flusher()
                    
                    
                    plt.gcf().savefig(raw_img_path + '/' + filename[0:-4] + '_' + ext + '.png', dpi  = dpi, transparent = True)
                    plt.close()
                                
                    #Set up correct file format for world file
                    template = """{x_m_pxl}
{rot}
{rot}
{y_m_pxl}
{x_tlc}
{y_tlc}"""    
        
                    context = {
                     "x_m_pxl":x_m_pxl, 
                     "rot":rot,
                     "rot":rot,
                     "y_m_pxl":y_m_pxl,
                     "x_tlc":x_tlc,
                     "y_tlc":y_tlc
                     } 
                  
                    world_txt = template.format(**context)                
                    world_name = raw_img_path + '/' + filename[0:-4] + '_' + ext + '.pgw'
                    world = open(world_name, 'w')
                    world.write(world_txt)          
                    
                    proj_img = raw_img_path + '/' + filename[0:-4] + '_' + ext + '.png.aux.xml'
                    projimg = open(proj_img, 'w')
                    
                    projimg.write("""<PAMDataset>
<SRS>PROJCS[&quot;British_National_Grid&quot;,GEOGCS[&quot;GCS_OSGB_1936&quot;,DATUM[&quot;OSGB_1936&quot;,SPHEROID[&quot;Airy_1830&quot;,6377563.396,299.3249646]],PRIMEM[&quot;Greenwich&quot;,0.0],UNIT[&quot;Degree&quot;,0.0174532925199433]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;False_Easting&quot;,400000.0],PARAMETER[&quot;False_Northing&quot;,-100000.0],PARAMETER[&quot;Central_Meridian&quot;,-2.0],PARAMETER[&quot;Scale_Factor&quot;,0.9996012717],PARAMETER[&quot;Latitude_Of_Origin&quot;,49.0],UNIT[&quot;Meter&quot;,1.0]]</SRS>
<Metadata domain="IMAGE_STRUCTURE">
<MDI key="INTERLEAVE">PIXEL</MDI>
</Metadata>
</PAMDataset>""")
                    projimg.close()
                
                #save each file as an .asc GIS grid file
                if gisgrd:                    
                    gis_raw_out(filename, raw_img_path, raw_gis_path, arcgrdval,colrng, i, x, y, z, xi2, yi2, min_x, max_x, min_y, max_y, arccxpnts, arccypnts, blank)
    
                #Save each file as a Sufer grid file
                if surf:                    
                    raw_surf_out(dirname, filename, data, i, min_x, max_x, min_y, max_y, grid, raw_surf_path)  
        
                #Plot all 6 raw plots on one figure                
                print 'Plotting raw data: column', -2+i,"\n"  
                flusher()
                
                
                plt.figure(1)
                pic = plt.subplot(2,3,-2+i)
                im = plt.imshow(grid, cmap=plt.cm.jet, vmin = np.percentile(z, 15), vmax = np.percentile(z, 85), extent = (min_x, max_x, min_y, max_y), interpolation = 'none', origin = 'lower')
                                
                plt.xlabel('Metres')
                plt.ylabel('Metres')
                plt.tick_params(direction = 'out')
                plt.subplots_adjust(wspace = 0.4, hspace = 0.3, left = 0.04, right = 0.96, top = 0.95, bottom = 0.07) 
                ax = plt.gca()
                divider = make_axes_locatable(ax)       
                cax = divider.append_axes("right", size="5%", pad=0.05)
                cb = plt.colorbar(im, cax)                  
                
                if -2+i == 1:
                    cb.set_label('S/m')
                    pic.set_title('Raw C1')
                elif -2+i == 2:
                    cb.set_label('mS/m')
                    pic.set_title('Raw I1')   
                elif -2+i == 3:
                    cb.set_label('S/m')
                    pic.set_title('Raw C2')
                elif -2+i == 4:
                    cb.set_label('mS/m')
                    pic.set_title('Raw I2')    
                elif -2+i == 5:
                    cb.set_label('S/m')
                    pic.set_title('Raw C3')
                else:
                    cb.set_label('mS/m')
                    pic.set_title('Raw I3')
                    
    i += 1
    
    plt.gcf().canvas.set_window_title('Raw data')
    
def plot_corr(out_array, filename, x_var, y_var, intsp_x, intsp_y, dirname, arcgrdval, geopng, gisgrd, surf, topo, blank, corr_img_path, corr_gis_path, topo_path, corr_surf_path):        
    
    print "\n"'Starting plot_corr' "\n"
    flusher()
    
    #Regrid and plot data
    min_x = np.amin(out_array[:,0])
    max_x = np.amax(out_array[:,0])
    min_y = np.amin(out_array[:,1])
    max_y = np.amax(out_array[:,1])
    rng_x = max_x - min_x
    rng_y = max_y - min_y
    
    #Determine the existing data spacing
    x_values = out_array[:,0]
    x_values = x_values.tolist()
    x_values = list(set(x_values))
    
    y_values = out_array[:,1]
    y_values = y_values.tolist()
    y_values = list(set(y_values))

    #Takes user input values
    intsp_x = float(intsp_x)
    intsp_y = float(intsp_y)
    step_x = 1/intsp_x
    step_y = 1/intsp_y
    
    #Determine grid parameters for make grid       
    cxpnts = rng_x/intsp_x 
    cxpnts = '%ij'%(cxpnts)
    cxpnts = complex(cxpnts)
    
    cypnts = rng_y/intsp_y
    cypnts = '%ij' %(cypnts)
    cypnts = complex(cypnts)
    
    #Make a grid of x,y values
    a, b = np.mgrid[min_x:max_x:cxpnts, min_y:max_y:cypnts]
    
    #Determine grid spacing for matplotlib gridding    
    noxpnts = ((step_x) * (rng_x)) + 1
    noypnts = ((step_y) * (rng_y)) + 1
    
    xi = np.linspace(min_x, max_x, noxpnts)
    yi = np.linspace(min_y, max_y, noypnts)
    
    blank = float(blank)   
        
    if gisgrd or surf:    
        #Takes user input value
        arcgrdval = float(arcgrdval)
        step = 1/arcgrdval
    
        #Determine arcgis grid spacing    
        no_arcxpnts = ((step) * (rng_x)) + 1
        no_arcypnts = ((step) * (rng_y)) + 1
        
        xi2 = np.linspace(min_x, max_x, no_arcxpnts)
        yi2 = np.linspace(min_y, max_y, no_arcypnts) 
        
        #Determine grid parameters for make grid 
        arccxpnts = rng_x/arcgrdval 
        arccxpnts = '%ij'%(arccxpnts)
        arccxpnts = complex(arccxpnts)
        
        arccypnts = rng_y/arcgrdval
        arccypnts = '%ij' %(arccypnts)
        arccypnts = complex(arccypnts)     
    
    if topo:  
        data = out_array
        topo_out(data, filename, topo_path, arcgrdval, intsp_x, intsp_y, arccxpnts, arccypnts, min_x, max_x, min_y, max_y, rng_x, rng_y, xi2, yi2, blank)
      
    colrng = range(len(out_array[0,:]))     
    
    i = 0
    for i in colrng:
        if i > 2:
                x = out_array[:,0]
                y = out_array[:,1] 
                z = out_array[:,i]
                
                newxyz = OrderedDict()
                for point in zip(x, y, z):
                    newxyz.setdefault(point[:2], point)
                newxyz = newxyz.values()
                newxyz = np.array(newxyz)
            
                x = newxyz[:,0]
                y = newxyz[:,1]
                z = newxyz[:,2]
                
                #Grid data for display  
                print "\n"'Gridding calibrated data: column', -2+i
                flusher()
                grid = griddata(x, y, z, xi, yi, interp = 'nn')
                
                
                #Make a grid of x,y values
                a, b = np.mgrid[min_x:max_x:cxpnts, min_y:max_y:cypnts]

                tree = KDTree(np.c_[x, y])
                dist, _ = tree.query(np.c_[a.ravel(), b.ravel()], k=1)
                dist = dist.reshape(a.shape).T
                                    
                grid[dist > blank] = np.nan     
                print 'Blanked grid: column', -2+i
                flusher()
                
                
                #Export each data set as an image 
                if geopng:
                    print 'Saving calibrated image: column', -2+i
                    flusher()
                    
                    
                    if intsp_x <= intsp_y:
                        x_m_pxl = intsp_x
                    else:
                        x_m_pxl = intsp_y                    
                    
                    y_m_pxl = -(x_m_pxl)
                    x_tlc = min_x + (intsp_x/2)
                    y_tlc = max_y + (intsp_y/2)
                    rot = 0.00000000000
                    
                    if intsp_x <= intsp_y:
                        xPix = noxpnts
                        yPix = (intsp_y/intsp_x)*noypnts
                    else:
                        yPix = noypnts 
                        xPix = (intsp_x/intsp_y)*noxpnts
                    
                    xSize = rng_x/50 #relating real size to image size
                    ySize = (xSize/xPix)*yPix
                    dpi = xPix/xSize
                                    
                    expimg = plt.figure(0, dpi = dpi, figsize = (xSize, ySize))
                    plt.imshow(grid, cmap=plt.cm.jet, vmin = np.percentile(z, 15), vmax = np.percentile(z, 85), extent = (min_x, max_x, min_y, max_y), interpolation = 'none', origin = 'lower')
                    a = plt.gca()
                    a.set_xticks([]); a.set_yticks([])
                    a.set_axis_off()
                    a.patch.set_alpha(0)
                    plt.tight_layout(rect=[0, 0, 1, 1], pad = 0, h_pad = 0)
                    
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
                        
                    dpi = expimg.get_dpi()
                    size = expimg.get_size_inches()
                    print "DPI: %f" % dpi
                    print "Size in inches: %f x %f" % (size[0], size[1])
                    print "Pixels: %i x %i" % (dpi * size[0], dpi * size[1])
                    flusher()
                    
                    
                    plt.gcf().savefig(corr_img_path + '/' + filename[0:-4] + '_' + ext + '.png', dpi  = dpi, transparent = True)
                    plt.close()
                                
                    #Set up correct file format for world file
                    template = """{x_m_pxl}
{rot}
{rot}
{y_m_pxl}
{x_tlc}
{y_tlc}"""    
        
                    context = {
                     "x_m_pxl":x_m_pxl, 
                     "rot":rot,
                     "rot":rot,
                     "y_m_pxl":y_m_pxl,
                     "x_tlc":x_tlc,
                     "y_tlc":y_tlc
                     } 
                  
                    world_txt = template.format(**context)                
                    world_name = corr_img_path + '/' + filename[0:-4] + '_' + ext + '.pgw'
                    world = open(world_name, 'w')
                    world.write(world_txt) 
                    
                    proj_img = corr_img_path + '/' + filename[0:-4] + '_' + ext + '.png.aux.xml'
                    projimg = open(proj_img, 'w') 
                    
                    projimg.write("""<PAMDataset>
<SRS>PROJCS[&quot;British_National_Grid&quot;,GEOGCS[&quot;GCS_OSGB_1936&quot;,DATUM[&quot;OSGB_1936&quot;,SPHEROID[&quot;Airy_1830&quot;,6377563.396,299.3249646]],PRIMEM[&quot;Greenwich&quot;,0.0],UNIT[&quot;Degree&quot;,0.0174532925199433]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;False_Easting&quot;,400000.0],PARAMETER[&quot;False_Northing&quot;,-100000.0],PARAMETER[&quot;Central_Meridian&quot;,-2.0],PARAMETER[&quot;Scale_Factor&quot;,0.9996012717],PARAMETER[&quot;Latitude_Of_Origin&quot;,49.0],UNIT[&quot;Meter&quot;,1.0]]</SRS>
<Metadata domain="IMAGE_STRUCTURE">
<MDI key="INTERLEAVE">PIXEL</MDI>
</Metadata>
</PAMDataset>""")
                    projimg.close()
                
                #save each file as a asc file
                if gisgrd:
                    gis_corr_out(filename, corr_gis_path, corr_img_path, arcgrdval,colrng, i, x, y, z, xi2, yi2, min_x, max_x, min_y, max_y, arccxpnts, arccypnts, blank)  
    
                #save each file as a Surfer grid file
                if surf:
                    corr_surf_out(dirname, filename, out_array, i, min_x, max_x, min_y, max_y, grid, corr_surf_path)
                
                #Plot all 6 raw plots                
                print 'Plotting calibrated data: column', -2+i,"\n"  
                flusher()
                
                
                plt.figure(2)                
                pic = plt.subplot(2,3,-2+i)
                im = plt.imshow(grid, cmap=plt.cm.jet, vmin = np.percentile(z, 15), vmax = np.percentile(z, 85), extent = (min_x, max_x, min_y, max_y), interpolation = 'none', origin = 'lower')
                                
                plt.xlabel('Metres')
                plt.ylabel('Metres')
                plt.tick_params(direction = 'out')
                plt.subplots_adjust(wspace = 0.4, hspace = 0.3, left = 0.04, right = 0.96, top = 0.95, bottom = 0.07) 
                ax = plt.gca()
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="5%", pad=0.05)
                cb = plt.colorbar(im, cax)                    
                
                if -2+i == 1:
                    cb.set_label('S/m')
                    pic.set_title('Calibrated C1')
                elif -2+i == 2:
                    cb.set_label('mS/m')
                    pic.set_title('Calibrated I1')   
                elif -2+i == 3:
                    cb.set_label('S/m')
                    pic.set_title('Calibrated C2')
                elif -2+i == 4:
                    cb.set_label('mS/m')
                    pic.set_title('Calibrated I2')    
                elif -2+i == 5:
                    cb.set_label('S/m')
                    pic.set_title('Calibrated C3')
                else:
                    cb.set_label('mS/m')
                    pic.set_title('Calibrated I3')
                
    
    i += 1
    
    plt.gcf().canvas.set_window_title('Corrected data')
   