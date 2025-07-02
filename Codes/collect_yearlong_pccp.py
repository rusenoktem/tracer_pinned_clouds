#Written by Rusen Oktem,  rusenoktem@berkeley.edu
#Collect cloud point heights from TRACER PCCP data and plot seasonal histograms

import numpy as np
import numpy.ma as ma
import pandas as pd
import glob
import sys
import os
import math
import time
import matplotlib.pyplot as plt
from matplotlib import cm
from netCDF4 import Dataset
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap


#Initialize variables
c_N = 19
cspace = np.vstack([np.ones((1, 4)), cm.jet(np.linspace(0, 1, c_N))])  # Generate color space
cmap = LinearSegmentedColormap.from_list("custom_cmap",cspace)

#time bins
tbins = np.arange(0, 25, 1)
lt = len(tbins)
#height bins
zbins = np.arange(0, 12100, 100)
lz = len(zbins)-1

def read_nc_file(fname):
    tz_hist = np.zeros((lz, lt))
    tcnt = np.zeros(lt)
    
    with Dataset(fname, 'r') as nc_file:
        # Read 'time' variable first, this will also tell the size of time steps
        timeoff = nc_file.variables['time'][:]
        Nt = len(timeoff)
        #get the fillvalue, there are lots of fillvalues in this dataset, it is best to skip them
        fill_value = getattr(nc_file.variables["z_relative"], "_FillValue", None)

        for ii in range(1,Nt,1):
            ti = timeoff[ii] #time in seconds            
            z_slice = nc_file.variables['z_relative'][ii][:][:] # cloud point heights
            z_t = z_slice.flatten()
            ind =  np.argwhere(z_t != fill_value) #discard fillvalues
            if len(ind) > 0: #if there exists data in this time step
                # Calculate histogram
                hist, bin_edges = np.histogram(z_t[ind], bins=zbins)
                ti_q = math.floor(ti/3600)
                tz_hist[:,ti_q] = tz_hist[:,ti_q] + hist 
                tcnt[ti_q] = tcnt[ti_q] + 1

    return tz_hist, tcnt


def plot_seasonal_histograms(tz,time_step):
    
    tz1 = np.sum(tz[10:13,:,:],0)
    tz2 = np.sum(tz[1:4,:,:],0)
    tz3 = np.sum(tz[4:7,:,:],0)
    tz4 = np.sum(tz[7:10,:,:],0)

    np.savetxt('array1.txt', tz1, fmt='%d')  # Use fmt='%d' for integer format
    np.savetxt('array2.txt', tz2, fmt='%d')
    np.savetxt('array3.txt', tz3, fmt='%d')
    np.savetxt('array4.txt', tz4, fmt='%d')
    np.savetxt('arraytime.txt', time_step, fmt='%d')
    
    fig = plt.figure(figsize=(8,6))
    #fig.suptitle('PCCP data from file '+inFileName +' at '+curTimeStr + ' UTC')
    
    plt.subplot(2, 2, 1)
    plot_single_panel(tz1,plt,1) 
    plt.ylabel('height [km]')
    
    
    plt.subplot(2, 2, 2)
    plot_single_panel(tz2,plt,1) 

    plt.subplot(2, 2, 3)
    plot_single_panel(tz3,plt,1) 
    plt.xlabel('local time')
    plt.ylabel('height [km]')
    
    plt.subplot(2, 2, 4)
    plot_single_panel(tz4,plt,1) 
    plt.xlabel('local time')

    
    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_single_panel(tz,plt,cb):

    I, J = np.where(tz > 0)
    tzf = tz.flatten()
    ii = np.where(tzf>0)
    sct = plt.scatter(tbins[J] , zbins[I] / 1e3, s=41, c=np.round(tzf[ii] * c_N / np.max(tzf)).astype(int), marker='s',cmap=cmap)

    if (cb):
        # Add colorbar
        cbar = plt.colorbar(sct, orientation='horizontal')
        cbar.set_label('count')  # Label for the colorbar
        cbar.set_ticks([0, 10 ,18])  # Set specific tick positions on the colorbar
        cbar.set_ticklabels([f'{int(t*max(tzf))}' for t in [0,0.5,0.9 ]]) 
        #cbar = fig.colorbar(cax, ax=ax, orientation='horizontal')
        
    plt.title('2D Histogram ')
    

def main():
    #get list of nc files under pccp folder
    flist = glob.glob('/data/datastream/hou/houpccpS5.c1/*202204*.nc')
    N = len(flist)  # Number of files
    
    #initialize  hist array for 12 months - 1..12, 0 will not be used
    tz_year = np.zeros((13,lz, lt))
    time_stp = np.zeros((13,lt))
    
    # Loop through each file and read the required data
    for j in range(0,N,1):
        fname = flist[j]
        print(fname)
        month = int(fname[-14:-12])
        tz_hist, tcnt = read_nc_file(fname) 
        tz_year[month] = tz_year[month]+ tz_hist
        time_stp[month,] = time_stp[month,] + tcnt
    print(time_stp)
    #display seasonal histograms    
    plot_seasonal_histograms(tz_year,time_stp)
