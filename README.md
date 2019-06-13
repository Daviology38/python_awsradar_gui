# python_awsradar_gui
This project uses the nexrad aws api and py-ART libraries incorporated into a pyqt-5 gui to pull radar data from selected stations (in this case KBOX or KENX) for selected dates for snow squall cases from 1999-2018 across the Northeast U.S. 

The gui initializes with a choice for date, start time, end time, and radar site (in that order). Some dates are missing radar files from some of the radar sites, so if the 'both' option is chosen, only times available at both radar sites within the time range chosen will be used.

Once the choices are made, the program downloads the files to a temporary directory (which will be deleted upon program completion). These files are sorted by time and then we remove duplicate times so we have one file per site per 10 minute time frame. This allows us to choose corresponding files when using the 'both' option.

Once these files are downloaded, they are plotted using matplotlib and cartopy. The left graph presents an animation which runs through each of the files. The right image goes frame by frame, initializing as blank. Both graphs are clickable and the corrdinates which are clicked are retained in an array. On click of the right graph, the first frame of the animation is shown, with subsequent animations shown on each mouse-click. This enables us to feature track each of the squalls. 

Once the squall has been sufficiently tracked (coordinates through mouse-click) then the 'choose new cell' or 'plot data' option can be chosen. If the 'choose new cell' option is chosen, then the right graph will restart from the first frame and a <0,0> coordinate pair is added to the array. Once all the squalls have been tracked, the 'plot data' button can be clicked. This creates a plot (which is saved locally) of each set of coordinates showing a line tracking the movement of the squall. The coordinates are split by the <0,0> pair if multiple cells are tracked. The coordinates are sorted before plotting to make a linear plot (which would not be the case if points were added for one cell after running through the initial plots). 