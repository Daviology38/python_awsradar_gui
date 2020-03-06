#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:41:51 2019

@author: mariofire
"""

#This program will take the downloaded radar files and make plots of each one
#Depending on if there is data for both stations or not.
#First a check will be done for each date to see if files are contained for both stations.
#If these exist, then the times will be matched as close as possible and plotted together. 
#If multiple times exist near each other, then the closest matches will be put together.
#The plots will then be saved to their respective date folders to be used by the gui.

#os.environ['PROJ_LIB'] = '/PATH_TO_ANANCONDA_ENV/share/proj/'
import os
import matplotlib
import cartopy.crs as ccrs
import pyart
from mpl_toolkits.basemap import Basemap
import numpy as np

#list dates in both directories
kenx_dates = os.listdir('radar_data/kenx')
kbox_dates = os.listdir('radar_data/kbox')

#Only take dates that have data for both sites to start
both = (kenx_dates and kbox_dates)

for name in both:
    if len(os.listdir('radar_data/kenx/'+name) ) == 0:
        print("Directory is empty")
    elif len(os.listdir('radar_data/kbox/'+name) ) == 0:
        print("Directory is empty")
    else:    
        print("Directory is not empty")
        files1 = []
        files2 = []
        filenames = os.listdir('radar_data/kenx/'+name)
        filenames2 = os.listdir('radar_data/kbox/'+name)
        #Check to see if the folder for the date exists in both KENX and KBOX, if not, make it
        if not os.path.exists('radar_data/'+ name):
            os.makedirs('radar_data/'+name)
        dirname = 'radar_data/'+name
        date = name
        testing = len(filenames)
        #Organize the files to get one for each 3 digit time for each station
        check = filenames[0][-6:-5]
        times1 = []
        times2 = []
        def remove(duplicate):
            final_list = []
            found = set([])
            for num in duplicate:
                lst = []
                for element in num:
                    if element not in found:
                        found.add(element)
                        lst.append(element)
                final_list.append(lst)
            return final_list
        #Check to see if we are using one station or two stations
        if(check == 'V'):
            for i in range(len(filenames)):
                time1 = filenames[i][-13:-10]
                times1.append([time1,i])
            for j in range(len(filenames2)):
                time2 = filenames2[j][-13:-10]
                times2.append([time2,j])
        else:
            for i in range(len(filenames)):
                time1 = filenames[i][-6:-3]
                times1.append([time1,i])
            for j in range(len(filenames2)):
                time2 = filenames2[-6:-3]
                times2.append([time2,j])
        #Find similar values in the array(s) and remove them
        temp1 = remove(times1)
        temp2 = remove(times2)
        #Now if there is more than 1 array, organize so both arrays have the same time scales
        tlist1 = []
        tlist2 = []
        for i in range(len(temp1)):
            tlist1.append(temp1[i][0])
        for j in range(len(temp2)):
            tlist2.append(temp2[j][0])
        svalue = set(tlist1) & set(tlist2)
        index1 = []
        index2 = []
        for value in svalue:
            try:
                ind = tlist1.index(value)    
                index1.append(temp1[ind][1])
            except:
                pass
        for value in svalue:
            try:
                ind = tlist2.index(value)    
                index2.append(temp2[ind][1])
            except:
                pass
        for i in range(len(index1)):
            nfile = filenames[index1[i]]
            files1.append(nfile)
            nfile = filenames2[index2[i]]
            files2.append(nfile)
    
    
        files1, files2 = (list(t) for t in zip(*sorted(zip(files1, files2))))
        
        figure = matplotlib.figure.Figure()
        axes = figure.add_subplot(111,projection=ccrs.PlateCarree())
        axes.set_extent([-78, -68, 40, 45], ccrs.PlateCarree())
    
        axes.gridlines(color="black", linestyle="dotted")
        figure.suptitle('Radar Returns')
        #get the radar location (this is used to set up the basemap and plotting grid)
        loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
        loc2 = pyart.io.nexrad_common.get_nexrad_location('KENX')
        lon0 = loc[1] ; lat0 = loc[0]
        lon1 = loc2[1]; lat1 = loc2[0]
                
        #use boto to connect to the AWS nexrad holdings directory
        #ax = self.figure.add_subplot(111)
                        #set up a basemap with a lambert conformal projection centered 
        # on the radar location, extending 1 degree in the meridional direction
        # and 1.5 degrees in the longitudinal in each direction away from the 
        # center point.
        m = Basemap(projection='lcc',lon_0=-73,lat_0=42.5,
                  llcrnrlat=40,llcrnrlon=-78,
                  urcrnrlat=45,urcrnrlon=-68,resolution='l')
        
        index = len(files1)
        ii = 0
        while ii < index:
    
            loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
            loc2 = pyart.io.nexrad_common.get_nexrad_location('KENX')
            lon0 = loc[1] ; lat0 = loc[0]
            lon1 = loc2[1]; lat1 = loc2[0]
            axes.clear()
        
            check = files1[ii][-6:-5]
            check2 = files1[ii][-3:-2]
            if(check == 'V'):
                timme = files1[ii][-13:-7]
                timelabel = timme[0:6]
                time1 = files1[ii][-13:-10]
            elif(check2 == 'V'):
                timme = files1[ii][-10:-4]
                timelabel = timme[0:6]
                time1 = files1[ii][-10:-7]
            else:
                timme = files1[ii][-6:]
                timelabel = timme[0:6]
                time1 = files1[ii][-6:-3]
            try:
                radar = pyart.io.read_nexrad_archive('radar_data/kbox/'+name+'/' + files1[ii])
                radar2 = pyart.io.read_nexrad_archive('radar_data/kenx/'+name+'/' + files2[ii])
           
                #set up the plotting grid for the data
                display = pyart.graph.RadarMapDisplay(radar)
                display2 = pyart.graph.RadarMapDisplay(radar2)
                x,y = display._get_x_y(0,True,None)
                x2,y2 = display2._get_x_y(0,True,None)
                axes.set_extent([-78, -68, 40, 45], ccrs.Geodetic())
                axes.gridlines(color="black", linestyle="dotted")
        
                
                #get the plotting grid into lat/lon coordinates
                x0,y0 = m(lon0,lat0)
                x1,y1 = m(lon1,lat1)
                glons,glats = m((x0+x*1000.), (y0+y*1000.),inverse=True)
                glons2,glats2 = m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                #read in the lowest scan angle reflectivity field in the NEXRAD file 
                refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                del radar
                del radar2
                cmap = 'pyart_NWSRef'
                levs = np.linspace(0,80,41,endpoint=True)
                norm = matplotlib.colors.BoundaryNorm(levs,256)
                #create a colormesh of the reflectivity using with the plot settings defined above
                p1 = axes.pcolormesh(glons,glats,refl,norm=norm,cmap=cmap,transform=ccrs.PlateCarree())
                axes.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,transform=ccrs.PlateCarree())
                figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                #add the colorbar axes and create the colorbar based on the settings above
                name2 = str(ii) + '.png'
                figure.savefig(dirname + name2)
                figure.canvas.draw_idle()
                ii = ii + 1
            except ValueError:
                ii = ii + 1
                print('Value')
                pass
            except:
                print('other')
                ii = ii + 1
                pass
