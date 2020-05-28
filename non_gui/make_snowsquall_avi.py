import pandas as pd
import os
import pyart
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import cv2
import glob
import matplotlib
import cartopy.crs as ccrs
import natsort


#Input the dates and times into a dictionary
file_path = 'C:/Users/CoeFamily/Downloads/snowsquall_datesandtimes.xlsx'
df = pd.read_excel(file_path, encoding='utf-16')
df = df.set_index(df.Dates).drop('Dates',axis=1)
dt = df.to_dict()
#This leaves a dictionary of dictionaries, so we take the Times one with the dates as keys and times as values
dt = dt['Times']
ii = 0
count = 0
#Now loop over each date for a 2 hour time period (unless it starts at 23z, then go till end of time period)
for file in os.listdir("C:/Users/CoeFamily/radar_data/kbox"):
        #Get list of the radar files in the directory
        names = os.listdir('C:/Users/CoeFamily/radar_data/kbox/'+file)
        date = names[0][4:12]
        tstart = dt[int(date)]
        if (tstart >= 22):
            tend = 23
        else:
            tend = tstart + 2
        for name in names:
            #Need to check which location we are at
            location = name[0:4]
            date = name[4:12]
            time = name[13:15]

            if(tstart<=int(time)<=tend):
                try:
                    #Get the number of grid points for our refl field here
                    radar = pyart.io.read_nexrad_archive('C:/Users/CoeFamily/radar_data/kbox/'+file+'/' + name)
                    refl = np.squeeze(radar.get_field(sweep=0, field_name='reflectivity'))

                    #Need to check which location we are at
                    location = name[0:4]
                    date = name[4:12]
                    time = name[13:15]

                    #get the radar location (this is used to set up the basemap and plotting grid)
                    if(location == 'KENX'):
                        loc = pyart.io.nexrad_common.get_nexrad_location('KENX')
                    else:
                        loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
                    lon0 = loc[1]
                    lat0 = loc[0]
                    m = Basemap(projection='lcc', lon_0=-73, lat_0=42.5,
                                     llcrnrlat=40, llcrnrlon=-78,
                                     urcrnrlat=45, urcrnrlon=-68, resolution='l')
                    # set up the plotting grid for the data
                    display = pyart.graph.RadarMapDisplay(radar)
                    x, y = display._get_x_y(0, True, None)
                    x0,y0 = m(lon0,lat0)
                    glons,glats = m((x0+x*1000.), (y0+y*1000.),inverse=True)
                    refl[refl<15] = np.nan
                    refl[refl>35] = np.nan
                    figure = plt.figure(figsize=(12,10))
                    axes = figure.add_subplot(111, projection=ccrs.PlateCarree())
                    axes.set_extent([-78, -68, 40, 45], ccrs.PlateCarree())
                    axes.gridlines(color="black", linestyle="dotted")
                    cmap = 'pyart_NWSRef'
                    levs = np.linspace(0, 80, 41, endpoint=True)
                    norm = matplotlib.colors.BoundaryNorm(levs, 256)
                    # create a colormesh of the reflectivity using with the plot settings defined above
                    p1 = axes.pcolormesh(glons, glats, refl, norm=norm, cmap=cmap, transform=ccrs.PlateCarree())
                    # add the colorbar axes and create the colorbar based on the settings above
                    name2 = str(ii) + '.png'
                    figure.savefig(name2)
                    ii = ii + 1
                    plt.close()
                except:
                    pass
        img_array = []
        filenames = natsort.natsorted(glob.glob('C:/Users/CoeFamily/Documents/python_awsradar_gui-master/*.png'))
        for filename in filenames:
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

        out = cv2.VideoWriter(date+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), .5, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        for filename in filenames:
            os.remove(filename)