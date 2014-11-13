# -*- coding: utf-8 -*-
def despike(data_coord,data,radius,threshold):
    """
    despikes a given dataset using the equation
    
    Z = (datapoint - mean) / standard deviation
    
    
    Usage:
    
        despike.py <coordinates> <data> <radius> <threshold>
    Parameters
    ---------
    
    coordinates: should be a numpy array of x, y, (z) coordinates
    data:numpy array with the same number of rows as coordinates but as many columns as required
    radius:a numerical value
    threshold: a numerical value
    
    
    returns
    -------
    a numpy array containing coordinates and data
    
    Finnegan Pope-Carter
    """
    
    import numpy as np
    from scipy.spatial import KDTree

#creates a tree from the coordinates to allow tree querys
    data_tree = KDTree(data_coord)

# creates lists of indices of points within 'radius' of point       
    groups = data_tree.query_ball_tree(data_tree,radius, eps=1)
#defines some variables
    row_delete = []
    j=0
    col_cnt = data.shape[1]
#creates list of rows Z is greater than defined threshold
    for row in groups:           
        if row:
            for i in range(col_cnt):
                vars()['temp',i] = np.array(data[row,i])
                mean = np.mean(vars()['temp',i])
                std = np.std(vars()['temp',i])
                #Avoids issues with division by/of 0
                if mean == 0:
                    pass
                if std == 0:
                    pass
                else:
                    z = abs(data[j,i] - mean)/std
                                
                    if z > threshold:
                        row_delete.append(j)
                        break
                        
        j += 1
#combines coordinate and data arrays
    data = np.column_stack((data_coord,data))
#deletes rows defined in previous list
    data = np.delete(data, row_delete, axis=0)
#returns numpy array
    return data