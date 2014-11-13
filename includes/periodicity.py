# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 13:07:41 2012

@author: fpopecar
"""
import matplotlib.pyplot as plt
#def periodic_filter(coords,data):
x = [0,1,2,3,4]
y = [10,11,12,13,14]
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x,y)

# set processing to continue when window closed
def onclose(event):
    fig.canvas.stop_event_loop()
fig.canvas.mpl_connect('close_event', onclose)

fig.show() # this call does not block on my system
fig.canvas.start_event_loop_default() # block here until window closed

a,b = fedit([('start','0'),('stop','100')], title="Periodic Filter Range")
# continue with further processing, perhaps using result from callbacks