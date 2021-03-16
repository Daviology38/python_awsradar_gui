# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:45:58 2019

@author: CoeFamily
"""


import os

# suppress deprecation warnings
import warnings

warnings.simplefilter("ignore", category=DeprecationWarning)
import nexradaws
from datetime import datetime
import numpy as np

# Holds the dates
content = []

# Holds the missing files
missing = []

# Open the file with the dates and add each one to the content array
with open("H:/Python/snowsqualldatesv5.txt") as f:
    for line in f:
        line = line.rstrip()
        content.append(line)

# Check if a folder exists to save the data to and create if not
if not os.path.exists("radar_data"):
    os.makedirs("radar_data")

# Check if the folders for each site exist and create if not
if not os.path.exists("radar_data/kbox"):
    os.makedirs("radar_data/kbox")

if not os.path.exists("radar_data/kenx"):
    os.makedirs("radar_data/kenx")

# For each date grab all available radar data, create a folder for it in the approraite folder, and download it
for date in content:
    # Split the date into month, day and year
    index = content.index(date)
    year = content[index][0:4]
    month = content[index][4:6]
    day = content[index][6:8]

    # Set the start and end hours to get full days worth of data
    hourstart = 0
    hourend = 23

    # Check to see if the folder for the date exists in both KENX and KBOX, if not, make it
    if not os.path.exists("radar_data/kbox/" + date):
        os.makedirs("radar_data/kbox/" + date)

    if not os.path.exists("radar_data/kenx/" + date):
        os.makedirs("radar_data/kenx/" + date)

    # Open an interface to get the radar data
    conn = nexradaws.NexradAwsInterface()

    # Put the radar sites here
    radarid = "KBOX"
    radarid2 = "KENX"

    # Create datetime objects for the start time and end time that we want the radar data
    start = datetime(int(year), int(month), int(day), int(hourstart), 0)
    end = datetime(int(year), int(month), int(day), int(hourend), 59)

    # Put the paths to the directories we want the data to go into in variables
    dirname = "radar_data/kbox/" + date
    dirname2 = "radar_data/kenx/" + date

    # See if the files exist on the server and if so, download them
    # If not, add the date and site to the missing array
    try:
        radarid = "KBOX"
        scans = conn.get_avail_scans_in_range(start, end, radarid)
        localfiles = conn.download(scans[0:], dirname)
    except:
        missing.append(date + "-- KBOX")

    try:
        radarid2 = "KENX"
        scans2 = conn.get_avail_scans_in_range(start, end, radarid2)
        localfiles2 = conn.download(scans2[0:], dirname2)
    except:
        missing.append(date + "-- KENX")

# Delete all empty folders
for folder in os.listdir("radar_data/kbox/"):
    if not os.listdir(folder):
        os.rmdir(folder)
for folder in os.listdir("radar_data/kenx/"):
    if not os.listdir(folder):
        os.rmdir(folder)

np.savetxt("radar_data/missingdates.txt", missing)
