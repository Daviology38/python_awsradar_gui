# python_awsradar_gui
This project uses the nexrad aws api and py-ART libraries incorporated into a pyqt-5 gui to pull radar data from selected stations (in this case KBOX or KENX) for selected dates for snow squall cases from 1999-2018 across the Northeast U.S. 

# How to use GUI Option
## Choosing the Data
The gui initializes with a choice for date, start time, end time, and radar site (in that order). Some dates are missing radar files from some of the radar sites, so if the 'both' option is chosen, only times available at both radar sites within the time range chosen will be used.

# Running the Program
Once the choices are made, the program downloads the files to a temporary directory (which will be deleted upon program completion). These files are sorted by time and then we remove duplicate times so we have one file per site per 10 minute time frame. This allows us to choose corresponding files when using the 'both' option.

# Tracking Squalls
Once these files are downloaded, they are plotted using matplotlib and cartopy. The left graph presents an animation which runs through each of the files. The right image goes frame by frame, initializing as blank. Both graphs are clickable and the corrdinates which are clicked are retained in an array. On the right graph the first frame is shown to start (except for when using local files, the first frame of the animation is shown on a click event which is not registered as a coordinate), with subsequent animations shown on each mouse-click. This enables us to feature track each of the squalls. 

Once the squall has been sufficiently tracked (coordinates through mouse-click) then the 'choose new cell' or 'plot data' option can be chosen. If the 'choose new cell' option is chosen, then the right graph will restart from the first frame and a <0,0> coordinate pair is added to the array. Once all the squalls have been tracked, the 'plot data' button can be clicked. This creates a plot (which is saved locally) of each set of coordinates showing a line tracking the movement of the squall. The coordinates are split by the <0,0> pair if multiple cells are tracked. The coordinates are sorted before plotting to make a linear plot (which would not be the case if points were added for one cell after running through the initial plots). The coordinates are saved to a .csv file with cells separated by a <0,0> line added in at the end of each set of coordinates.

# Non-GUI Version
In the non-gui folder, there is a second version of this program that is more resource efficient compared to the gui version. This folder consists of the programs, which must be run in a specific order:

1. download_radar_data.py
2. make_snowsquall_avi.py
3. tracking_test.py

## Download_radar_data.py
This program contains a 4 letter station ID from which to grab the radar data. The program is set for KBOX. The dates and times are pulled from separate text file. The radar data is downloaded for the whole range of the date (00z-23z where possible) from the Amazon S3 radar bucket. If the whole day is not available, then the available times for that date are downloaded instead. These files are put into folders with structure (StationID/date/file)

## Make_Snowsquall_Avi
This program takes the downloaded radar data for each data and creates a .avi file from the radar sequences. The dates and times are loaded from an excel file into a dataframe. This time is the start time and the program runs for 4 hours after the start time (or until the end of the day). These files are saved to the root directory and can be moved to new folders.

## Tracking_test.py
This is no test, this is the real deal. This program uses the openCV python extension to dynamically track the squalls. Each .avi file is loaded into the program from the directory specified by the user. Then the video appears on the screen and loops continuously through. The user needs to press the 's' key to initiate the tracking program. The user draws a box around the feature which they would like to track. NOTE: Make sure the box is specifically around the feature as if it is too big or too small the program will get confused if there are multiple features near it. Then the user presses 'enter/return' and the video loops through each frame with the box tracking the selected feature. The user can also press the 's' key again to track multiple features at the same time. The boxes dissapear once the feature is either not present for 2 frames of animation or on a restart of the loop. The 'q' key can then be pressed to move to the next image.

Once the program has run, it will spit out a .csv file containing the date and the average direction of motion of the tracked cells. The motion is computed in the program by taking the averge cartesian direction of motion for each tracked feature, transforming them to a compass direction, and then taking the average direction for the motion.
