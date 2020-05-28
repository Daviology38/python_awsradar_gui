# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:00:55 2019

@author: CoeFamily
"""

import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from math import radians
from compass_bearing import calculate_initial_compass_bearing as cicb

direction = []

for file in os.listdir("H:/Python/snowsquall_excel"):
    
    #open the data file
    df = pd.read_csv("H:/Python/snowsquall_excel/" + file)
    
    #get the date from the file name
    date = file[0:8]
    #Get the index value of each row of <0,0> and put it into a list
    index = df.xcoor.index[df.xcoor == 0].tolist()

    #Get the number of coordinate pairs
    num_pairs = len(df) 
    
    #List to put the directions in between each pair. We will take average
    #of all directions to find the average direction of motion.
    test_list = []
    test_direction = []
    #Loop through the coordinates
    for i in range(num_pairs-1):
        if i+1 in index:
            mean = round(np.mean(test_list),2)
            test_direction.append(mean)
            test_list = []
        elif i in index:
            pass
        else:
            x1 = df.xcoor[i]
            x2 = df.xcoor[i+1]
            y1 = df.ycoor[i]
            y2 = df.ycoor[i+1]
            
            xcoord = (y1,x1)
            ycoord = (y2,x2)
            compass = cicb(xcoord,ycoord)
            test_list.append(compass)
    if not index:
        listing = [date,round(np.mean(test_list),2),1]
        direction.append(listing)
    else:
        listing = [date,round(np.mean(test_direction),2),1]
        direction.append(listing)
    
new_df = pd.DataFrame(direction)
new_df.columns = ['Date', 'Direction','Value']




ax = plt.subplot(111, polar=True)
ax.scatter(x = [radians(x) for x in new_df['Direction'].values], y = new_df['Value'].values)
ax.set_theta_zero_location('N')
ax.set_yticklabels([])
ax.set_theta_direction(-1)

plt.savefig("coords.png")