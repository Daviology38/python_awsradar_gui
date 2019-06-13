# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 17:00:30 2019

@author: CoeFamily
"""


import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QAbstractItemView, QListWidget, QHBoxLayout,QLineEdit, QCheckBox,QGridLayout,QGroupBox, QToolButton,
    QAction, QFileDialog, QDialog, QComboBox, QListWidgetItem, QTreeView, QListView, QFileSystemModel, QApplication, qApp, QWidget,QVBoxLayout,QLabel,QPushButton,QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir, QRect,QTimer 
import matplotlib.figure
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pyart
import tempfile
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation, ArtistAnimation
#suppress deprecation warnings
import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)
import six
import nexradaws
import gc
from datetime import datetime

date = ''
content = []
timess = []
counter = 1
counter2 = 0
counter1 = 0
global starttime
global localfiles
global localfiles2
global files1
global files2
global templocation
global temp_dir
global testing
global overallcoords
global endtime
global site
global ii 
ii = 0
files1 = []
files2 = []
with open('H:/Python/snowsqualldatesv5.txt') as f:
    for line in f:
        line = line.rstrip()
        content.append(line)
with open('H:/Python/timessnowsquallsv5.txt') as f:
    for line in f:
        line = line.rstrip()
        timess.append(line)
coordsx = []
coordsy = []
################################################################################
class Test(QDialog):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        self.setWindowTitle("Choose date")
        self.layout = QHBoxLayout()
        self.cb = QComboBox()
        with open('H:/Python/snowsqualldatesv5.txt','r') as movieDir:
            for movie in movieDir:
                self.cb.addItem(movie)
        #self.listWidget.itemClicked.connect(self.printItemText)
        self.layout.addWidget(self.cb)
        self.setLayout(self.layout)
        self.cb.activated[str].connect(self.onActivated)
        
    def onActivated(self, text):
        global date
        date = text
        date = int(date)
        date = str(date).rstrip()
        self.accept()
###############################################################################
class Timeteststart(QDialog):
    def __init__(self, parent=None):
        super(Timeteststart, self).__init__(parent)
        self.setWindowTitle("Choose start time")
        self.layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem('0')
        self.cb.addItem('1')
        self.cb.addItem('2')
        self.cb.addItem('3')
        self.cb.addItem('4')
        self.cb.addItem('5')
        self.cb.addItem('6')
        self.cb.addItem('7')
        self.cb.addItem('8')
        self.cb.addItem('9')
        self.cb.addItem('10')
        self.cb.addItem('11')
        self.cb.addItem('12')
        self.cb.addItem('13')
        self.cb.addItem('14')
        self.cb.addItem('15')
        self.cb.addItem('16')
        self.cb.addItem('17')
        self.cb.addItem('18')
        self.cb.addItem('19')
        self.cb.addItem('20')
        self.cb.addItem('21')
        self.cb.addItem('22')
        self.cb.addItem('23')
        #self.listWidget.itemClicked.connect(self.printItemText)
        self.layout.addWidget(self.cb)
        self.setLayout(self.layout)
        self.cb.activated[str].connect(self.onActivated)
        
    def onActivated(self, text):
        global starttime
        starttime = text
        starttime = str(starttime).rstrip()
        self.accept()        
################################################################################
class Timetestend(QDialog):
    def __init__(self, parent=None):
        super(Timetestend, self).__init__(parent)
        self.setWindowTitle("Choose end time")
        self.layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem('0')
        self.cb.addItem('1')
        self.cb.addItem('2')
        self.cb.addItem('3')
        self.cb.addItem('4')
        self.cb.addItem('5')
        self.cb.addItem('6')
        self.cb.addItem('7')
        self.cb.addItem('8')
        self.cb.addItem('9')
        self.cb.addItem('10')
        self.cb.addItem('11')
        self.cb.addItem('12')
        self.cb.addItem('13')
        self.cb.addItem('14')
        self.cb.addItem('15')
        self.cb.addItem('16')
        self.cb.addItem('17')
        self.cb.addItem('18')
        self.cb.addItem('19')
        self.cb.addItem('20')
        self.cb.addItem('21')
        self.cb.addItem('22')
        self.cb.addItem('23')
        #self.listWidget.itemClicked.connect(self.printItemText)
        self.layout.addWidget(self.cb)
        self.setLayout(self.layout)
        self.cb.activated[str].connect(self.onActivated)
        
    def onActivated(self, text):
        global endtime
        endtime = text
        endtime = str(endtime).rstrip()
        self.accept()   
################################################################################
class RadarSite(QDialog):
    def __init__(self, parent=None):
        super(RadarSite, self).__init__(parent)
        self.setWindowTitle("Choose Radar Site")
        self.layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem('KENX')
        self.cb.addItem('KBOX')
        self.cb.addItem('both')
        #self.listWidget.itemClicked.connect(self.printItemText)
        self.layout.addWidget(self.cb)
        self.setLayout(self.layout)
        self.cb.activated[str].connect(self.onActivated)
        
    def onActivated(self, text):
        global site
        site = text
        site = str(site).rstrip()
        self.accept()   
##Window for Cross Section Gui
#class XSectiongui(QMainWindow):
#    
#    def __init__(self, parent = None):
#        super(XSectiongui, self).__init__()
#        #iinitUI()
  

############################

#Main Window
class Example(QMainWindow):
    
    def __init__(self, parent = None):
        super(Example,self).__init__()
        self.dialog2 = Test(self)
        self.dialog3 = Timeteststart(self)
        self.dialog4 = Timetestend(self)
        self.dialog5 = RadarSite(self)
        if self.dialog2.exec_():
            if self.dialog3.exec_():
                if self.dialog4.exec_():
                    if self.dialog5.exec_():
                        self.initUI()
  
        
    def initUI(self):               

        #############################################################
        #get the data
        global date
        global starttime
        global endtime
        if( date != ''):
            global content
            global timess
            global localfiles
            global localfiles2
            global templocation
            global testing
            global site
            global files1
            global files2
            files1 = []
            files2 = []
            index = content.index(date)
            year = content[index][0:4]
            month = content[index][4:6]
            day = content[index][6:8]
            hourstart = int(starttime)
            hourend = int(endtime)
            
            #Open a temp directory to house the radar files and then delete when done plotting
            temp_dir = tempfile.mkdtemp()
            templocation = temp_dir
            self.conn = nexradaws.NexradAwsInterface()
            #Put radar site here
            self.radarid = site
            #self.radarid2 = 'KENX'
            #Put the times you want the radar for here (yyyy,mm,dd,hh,mm)
            dayst = day
            dayend = day
            self.start = datetime(int(year),int(month),int(dayst),int(hourstart),0)
            self.end = datetime(int(year),int(month),int(dayend),int(hourend),59)
            #See if the files exist on the server and if so, do this
            try:
                if(site == 'both'):
                    self.radarid = 'KBOX'
                    self.radarid2 = 'KENX'
                    self.scans = self.conn.get_avail_scans_in_range(self.start, self.end, self.radarid)
                    self.scans2 = self.conn.get_avail_scans_in_range(self.start, self.end, self.radarid2)
                    localfiles = self.conn.download(self.scans[0:],templocation)
                    localfiles2 = self.conn.download(self.scans2[0:],templocation)
                else:
                    self.scans = self.conn.get_avail_scans_in_range(self.start, self.end, self.radarid)
                    #self.scans2 = self.conn.get_avail_scans_in_range(self.start, self.end, self.radarid2)
                    localfiles = self.conn.download(self.scans[0:],templocation)
                    #localfiles2 = self.conn.download(self.scans2[0:],templocation)
                    #See if the files aren't empty and do this
                try:
                    print(localfiles)
                except IndexError:
                    QMessageBox.about(self, "Warning", "Index Error, ran out of data!")
                    sys.exit(0)
            #If the try for the files says there are NoneType files found, then we skip
            except TypeError:
                QMessageBox.about(self,"Warning", "Type Error, try new date!")
                sys.exit(0)
            testing = len(localfiles.success)
            #Organize the files to get one for each 3 digit time for each station
            check = localfiles.success[0].filepath[-6:-5]
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
            if(check == 'V' and site == 'both'):
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-13:-10]
                    times1.append([time1,i])
                for j in range(len(localfiles2.success)):
                    time2 = localfiles2.success[j].filepath[-13:-10]
                    times2.append([time2,j])
                #time2 = localfiles2.success[self.j].filepath[-13:-10]
            elif(check == 'V' and site != 'both'):
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-13:-10]
                    times1.append([time1,i])
            elif(check != 'V' and site == 'both'):
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-9:-6]
                    times1.append([time1,i])
                for j in range(len(localfiles2.success)):
                    time2 = localfiles2.success[j].filepath[-9:-6]
                    times2.append([time2,j])
            else:
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-9:-6]
                    times1.append([time1,i])
            #Find similar values in the array(s) and remove them
            if(site == 'both'):
                temp1 = remove(times1)
                temp2 = remove(times2)
            else:
                temp1 = remove(times1)
            #Now if there is more than 1 array, organize so both arrays have the same time scales
            if(site == 'both'):
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
                print(index1)
                print(index2)
                for i in range(len(index1)):
                    nfile = localfiles.success[index1[i]].filepath
                    files1.append(nfile)
                    nfile = localfiles2.success[index2[i]].filepath
                    files2.append(nfile)
            else:
                for i in range(len(temp1)):
                    nfile = localfiles.success[temp1[i][1]].filepath
                    files1.append(nfile)
            if(site == 'both'):
                files1, files2 = (list(t) for t in zip(*sorted(zip(files1, files2))))
            else:
                files1.sort()
                
            #Add in a menu bar
            self.statusBar()
            menubar = self.menuBar()
            fileMenu = menubar.addMenu('&File')
            newAct = QAction('New', self)   
            saveAct = QAction('Save', self)
            saveAct.setShortcut("Ctrl+S")
            #openFile = QAction(QIcon('open.png'), 'Open', self)
            #openFile.setShortcut('Ctrl+O')
            #openFile.setStatusTip('Open new File')
            #openFile.triggered.connect(self.opendatafile)       
            exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
            exitAct.setShortcut('Ctrl+Q')
            exitAct.setStatusTip('Exit application')
            exitAct.triggered.connect(qApp.quit)
            fileMenu.addAction(newAct)
            #fileMenu.addAction(openFile)
            fileMenu.addAction(saveAct)
            fileMenu.addAction(exitAct)
            self.clearAct = QAction(QIcon('wedb.png'), 'Clear', self)
            #self.clearAct.triggered.connect(self.clearpic)
            menubar.addAction(self.clearAct)

            ##############################################################
            #Add in a grid layout
            self._main = QWidget()
            self.setCentralWidget(self._main)
            grid = QGridLayout(self._main)
            ############################################################
            #Add in the first plot
            sc1 = animated(self._main)
            grid.addWidget(sc1, 1, 1)
            #############################################################
            #Add in the second plot
            sc2 = static(self._main)
            grid.addWidget(sc2, 1, 2)
            #############################################################
            #Add in a Toolbar
            plotradar = QAction(QIcon('exit24.png'), 'Plot View', self)
            plotradar = QToolButton()
            plotradar.setText("Plot Cells")
            plotradar.pressed.connect(self.plotcells)
            crosssectionAct = QToolButton()
            crosssectionAct.pressed.connect(self.plotpoints)
            crosssectionAct.setText("Choose new cell")
            self.toolbar = self.addToolBar('Plot View')
            self.toolbar.addWidget(plotradar)
            self.toolbar.addWidget(crosssectionAct)
            #############################################################
            
            self.setGeometry(500, 500, 500, 500)
            self.setWindowTitle('Simple menu')  
            self.show()
        else:
            QMessageBox.about(self,"Warning", "No Date has been selected. Please click Select date first!")

            
    def plotpoints(self):
        global coordsx
        global coordsy
        coordsx.append(0)
        coordsy.append(0)
        print(0)
        global ii
        ii = 0
        pass
    
    def plotcells(self):
        global coordsx
        global coordsy
        global date
        lenx = len(coordsx)
        figure = plt.figure()
        self.axes = figure.add_subplot(111)
        newcoordsx = []
        newcoordsy = []
        for i in range(lenx):
            xcoor = coordsx[i]
            ycoor = coordsy[i]
            if( xcoor == 0 and ycoor == 0):
                xcoor.pop(0)
                ycoor.pop(0)
                #now sort them to make sure they are in order
                newcoordsx, newcoordsy = (list(t) for t in zip(*sorted(zip(newcoordsx, newcoordsy))))
                self.axes.plot(newcoordsx,newcoordsy)
                self.axes.scatter(newcoordsx,newcoordsy,marker='X',color='black')
                newcoordsx = []
                newcoordsy = []
            else:
                newcoordsx.append(xcoor)
                newcoordsy.append(ycoor)
        #now sort them to make sure they are in order
        newcoordsx, newcoordsy = (list(t) for t in zip(*sorted(zip(newcoordsx, newcoordsy))))
        self.axes.plot(newcoordsx,newcoordsy)
        self.axes.scatter(newcoordsx,newcoordsy,marker='X',color='black')
        print('Plot is Done')
        figure.savefig(date + '.png')
        shutil.rmtree(templocation)
        sys.exit(0)
            
        

###############################################################################

            
###############################################################################
class mycanvas(FigureCanvas):
    def __init__(self, parent=None):
        figure = matplotlib.figure.Figure()
        self.axes = figure.add_subplot(111,projection=crs.PlateCarree())
        self.axes.set_extent([-78, -68, 40, 45], crs.PlateCarree())
        #ax = plt.axes(projection=crs.PlateCarree())
        #states = NaturalEarthFeature(category = 'cultural', scale = '50m', facecolor = 'none',name = 'admin_1_states_provinces_shp')
        #self.axes.add_feature(states,linewidth=1.,edgecolor="black")
        #self.axes.coastlines('50m',linewidth=0.8)
        self.axes.gridlines(color="black", linestyle="dotted")

        self.compute_initial_figure()

        self.canvas=FigureCanvas.__init__(self, figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.figure.suptitle('Radar Returns')
                       #select the radar site

    def compute_initial_figure(self):
               #select the radar site
        global localfiles
        global localfiles2
        global files1
        global files2
        global site
        global ii
        #site = 'KBOX'
        #site2 = 'KENX'
        if(site != 'both'):            
            #get the radar location (this is used to set up the basemap and plotting grid)
            loc = pyart.io.nexrad_common.get_nexrad_location(site)
            #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
            lon0 = loc[1] ; lat0 = loc[0]
            #lon1 = loc2[1]; lat1 = loc2[0]
            #use boto to connect to the AWS nexrad holdings directory
            #ax = self.figure.add_subplot(111)
                            #set up a basemap with a lambert conformal projection centered 
            # on the radar location, extending 1 degree in the meridional direction
            # and 1.5 degrees in the longitudinal in each direction away from the 
            # center point.
        else:
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
        self.m = Basemap(projection='lcc',lon_0=-73,lat_0=42.5,
                  llcrnrlat=40,llcrnrlon=-78,
                  urcrnrlat=45,urcrnrlon=-68,resolution='l')
        
        #add geographic boundaries and lat/lon labels
        #self.m.drawparallels(np.arange(20,70,0.5),labels=[1,0,0,0],fontsize=12,
                        #color='k',ax=ax,linewidth=0.001)
        #self.m.drawmeridians(np.arange(-150,-50,1),labels=[0,0,1,0],fontsize=12,
                       #color='k',ax=ax,linewidth=0.001)
        #m.drawcounties(linewidth=0.5,color='gray',ax=ax)
        #self.m.drawstates(linewidth=1.5,color='k',ax=ax)
        #self.m.drawcoastlines(linewidth=1.5,color='k',ax=ax)
        #Use Nasa Blue marble Earth for background if you want
        #m.bluemarble()
        #m.shadedrelief()
        #mark the radar location with a black dot
        #m.scatter(lon0,lat0,marker='o',s=20,color='k',ax=ax,latlon=True)
        #m.scatter(lon1,lat1,marker='o',s=20,color='k',ax=ax,latlon=True)
        #normalize the colormap based on the levels provided above                    
        #Take the first file that we gathered to plot (filenames are stored in the dictionary localfiles.success)
        try:
            radar = pyart.io.read_nexrad_archive(files1)
            #radar2 = pyart.io.read_nexrad_archive(localfiles2.success[0].filepath)
   
            #set up the plotting grid for the data
            display = pyart.graph.RadarMapDisplay(radar)
            #display2 = pyart.graph.RadarMapDisplay(radar2)
            x,y = display._get_x_y(0,True,None)
            #x2,y2 = display2._get_x_y(0,True,None)
    
            
            #get the plotting grid into lat/lon coordinates
            x0,y0 = self.m(lon0,lat0)
            #x1,y1 = self.m(lon1,lat1)
            glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
            #glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
            #read in the lowest scan angle reflectivity field in the NEXRAD file 
            refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
            #refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
            del radar
            #del radar2
            #set up the plotting parameters (NWSReflectivity colormap, contour levels,
            # and colorbar tick labels)
            cmap = 'pyart_NWSRef'
            levs = np.linspace(0,80,41,endpoint=True)
            ticks = np.linspace(0,80,9,endpoint=True)
            label = 'Radar Reflectivity Factor ($\mathsf{dBZ}$)'
            #define the plot axis to the be axis defined above
            self.norm = mpl.colors.BoundaryNorm(levs,256)
            #create a colormesh of the reflectivity using with the plot settings defined above
            p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
            #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
            #add the colorbar axes and create the colorbar based on the settings above
            #cax = figure.add_axes([0.075,0.075,0.85,0.025])
            #cbar = plt.colorbar(p1,ticks=ticks,norm=self.norm,cax=cax,orientation='horizontal')
            #cbar.set_label(label,fontsize=12)
            #cbar.ax.tick_params(labelsize=11)
            #display the figurefrom matplotlib.animation import FuncAnimation
                #If the try for files says there aren't any files found, then we skip
        except ValueError:
            pass
###############################################################################
#Plot on the right will display frame by frame
#Plot on the right will display a running gif image
class static(mycanvas):
    def __init__(self, parent=None):
        mycanvas.__init__(self)
        global ii
        self.j = 0
    def compute_initial_figure(self):
               #select the radar site
        global localfiles
        global localfiles2
        global files1
        global files2
        global site
        global ii
        #site = 'KBOX'
        #site2 = 'KENX'
        if(site != 'both'):
            
            #get the radar location (this is used to set up the basemap and plotting grid)
            loc = pyart.io.nexrad_common.get_nexrad_location(site)
            #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
            lon0 = loc[1] ; lat0 = loc[0]
            #lon1 = loc2[1]; lat1 = loc2[0]
        else:
                        
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
        self.m = Basemap(projection='lcc',lon_0=-73,lat_0=42.5,
                  llcrnrlat=40,llcrnrlon=-78,
                  urcrnrlat=45,urcrnrlon=-68,resolution='l')
        
        #add geographic boundaries and lat/lon labels
        #self.m.drawparallels(np.arange(20,70,0.5),labels=[1,0,0,0],fontsize=12,
                        #color='k',ax=ax,linewidth=0.001)
        #self.m.drawmeridians(np.arange(-150,-50,1),labels=[0,0,1,0],fontsize=12,
                       #color='k',ax=ax,linewidth=0.001)
        #m.drawcounties(linewidth=0.5,color='gray',ax=ax)
        #self.m.drawstates(linewidth=1.5,color='k',ax=ax)
        #self.m.drawcoastlines(linewidth=1.5,color='k',ax=ax)
        #Use Nasa Blue marble Earth for background if you want
        #m.bluemarble()
        #m.shadedrelief()
        #mark the radar location with a black dot
        #m.scatter(lon0,lat0,marker='o',s=20,color='k',ax=ax,latlon=True)
        #m.scatter(lon1,lat1,marker='o',s=20,color='k',ax=ax,latlon=True)
        #normalize the colormap based on the levels provided above                    
        #Take the first file that we gathered to plot (filenames are stored in the dictionary localfiles.success)
        try:
            radar = pyart.io.read_nexrad_archive(localfiles.success[0].filepath)
            #radar2 = pyart.io.read_nexrad_archive(localfiles2.success[0].filepath)
   
            #set up the plotting grid for the data
            display = pyart.graph.RadarMapDisplay(radar)
            #display2 = pyart.graph.RadarMapDisplay(radar2)
            x,y = display._get_x_y(0,True,None)
            #x2,y2 = display2._get_x_y(0,True,None)
    
            
            #get the plotting grid into lat/lon coordinates
            x0,y0 = self.m(lon0,lat0)
            #x1,y1 = self.m(lon1,lat1)
            glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
            #glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
            #read in the lowest scan angle reflectivity field in the NEXRAD file 
            refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
            #refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
            del radar
            #del radar2
            #set up the plotting parameters (NWSReflectivity colormap, contour levels,
            # and colorbar tick labels)
            cmap = 'pyart_NWSRef'
            levs = np.linspace(0,80,41,endpoint=True)
            ticks = np.linspace(0,80,9,endpoint=True)
            label = 'Radar Reflectivity Factor ($\mathsf{dBZ}$)'
            #define the plot axis to the be axis defined above
            self.norm = mpl.colors.BoundaryNorm(levs,256)
            #create a colormesh of the reflectivity using with the plot settings defined above
            p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
            #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
            #add the colorbar axes and create the colorbar based on the settings above
            #cax = figure.add_axes([0.075,0.075,0.85,0.025])
            #cbar = plt.colorbar(p1,ticks=ticks,norm=self.norm,cax=cax,orientation='horizontal')
            #cbar.set_label(label,fontsize=12)
            #cbar.ax.tick_params(labelsize=11)
            #display the figurefrom matplotlib.animation import FuncAnimation
                #If the try for files says there aren't any files found, then we skip
        except ValueError:
            pass

    def onclick(self,event):
        global ii
        global files1
        global files2
        if(ii != 0):
            ix, iy = event.xdata, event.ydata
            #ix,iy = crs.LambertConformal.transform_point(ix,iy,crs.PlateCarree)
            print ('x = %f, y = %f'%(
                ix, iy))
        
            global coordsx
            global coordsy
            global testing
            coordsx.append(ix)
            coordsy.append(iy)
            #if(counter == testing):
            #    QMessageBox.about(self, "Warning", "No more data available to plot")
            #    shutil.rmtree(templocation)
            global localfiles
            global localfiles2
            global site
            #site = 'KBOX'
            #site2 = 'KENX'
            if(site != 'both'):
        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location(site)
                #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
                lon0 = loc[1] ; lat0 = loc[0]
                #lon1 = loc2[1]; lat1 = loc2[0]
                self.axes.clear()
                ii = ii + 1
                self.j = self.j + 1
                if(ii == len(files1)):
                    ii = ii - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[ii][-6:-5]
                if(check == 'V'):
                    timme = files1[ii][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                else:
                    timme = files1[ii][-9:]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-9:-6]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(files1[ii])
                    #radar2 = pyart.io.read_nexrad_archive(localfiles2.success[self.j].filepath)
               
                    #set up the plotting grid for the data
                    display = pyart.graph.RadarMapDisplay(radar)
                    #display2 = pyart.graph.RadarMapDisplay(radar2)
                    x,y = display._get_x_y(0,True,None)
                    #x2,y2 = display2._get_x_y(0,True,None)
                    self.axes.set_extent([-78, -68, 40, 45], crs.Geodetic())
                    #ax = plt.axes(projection=crs.PlateCarree())
                    #states = NaturalEarthFeature(category = 'cultural', scale = '50m', facecolor = 'none',name = 'admin_1_states_provinces_shp')
                    #self.axes.add_feature(states,linewidth=1.,edgecolor="black")
                    #self.axes.coastlines('50m',linewidth=0.8)
                    self.axes.gridlines(color="black", linestyle="dotted")
            
                    
                    #get the plotting grid into lat/lon coordinates
                    x0,y0 = self.m(lon0,lat0)
                    #x1,y1 = self.m(lon1,lat1)
                    glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
                    #glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                    #read in the lowest scan angle reflectivity field in the NEXRAD file 
                    refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                    #refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                    del radar
                    #del radar2
                    cmap = 'pyart_NWSRef'
                    #create a colormesh of the reflectivity using with the plot settings defined above
                    #p1 = m.pcolormesh(glons,glats,refl,norm=norm,cmap=cmap,ax=ax,latlon=True)
                    #p2 = m.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,ax=ax,latlon=True)
                    p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                    #add the colorbar axes and create the colorbar based on the settings above
                    self.draw()
                    if(ii == len(files1)):
                        ii = 0
                except ValueError:
                    if(ii == len(files1)):
                        ii = 0
                    pass
                except:
        
                    if(ii == len(files1)):
                        ii = 0
                    pass
            else:
                        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
                loc2 = pyart.io.nexrad_common.get_nexrad_location('KENX')
                lon0 = loc[1] ; lat0 = loc[0]
                #lon1 = loc2[1]; lat1 = loc2[0]
                self.axes.clear()
                ii = ii + 1
                self.j = self.j + 1
                if(ii == len(localfiles.success)):
                    ii = ii - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = localfiles.success[ii].filepath[-6:-5]
                if(check == 'V'):
                    timme = localfiles.success[ii].filepath[-13:-7]
                    timelabel = timme[0:6]
                    time1 = localfiles.success[ii].filepath[-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                else:
                    timme = localfiles.success[ii].filepath[-9:]
                    timelabel = timme[0:6]
                    time1 = localfiles.success[ii].filepath[-9:-6]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(localfiles.success[ii].filepath)
                    #radar2 = pyart.io.read_nexrad_archive(localfiles2.success[self.j].filepath)
               
                    #set up the plotting grid for the data
                    display = pyart.graph.RadarMapDisplay(radar)
                    #display2 = pyart.graph.RadarMapDisplay(radar2)
                    x,y = display._get_x_y(0,True,None)
                    #x2,y2 = display2._get_x_y(0,True,None)
                    self.axes.set_extent([-78, -68, 40, 45], crs.Geodetic())
                    #ax = plt.axes(projection=crs.PlateCarree())
                    #states = NaturalEarthFeature(category = 'cultural', scale = '50m', facecolor = 'none',name = 'admin_1_states_provinces_shp')
                    #self.axes.add_feature(states,linewidth=1.,edgecolor="black")
                    #self.axes.coastlines('50m',linewidth=0.8)
                    self.axes.gridlines(color="black", linestyle="dotted")
            
                    
                    #get the plotting grid into lat/lon coordinates
                    x0,y0 = self.m(lon0,lat0)
                    #x1,y1 = self.m(lon1,lat1)
                    glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
                    #glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                    #read in the lowest scan angle reflectivity field in the NEXRAD file 
                    refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                    #refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                    del radar
                    #del radar2
                    cmap = 'pyart_NWSRef'
                    #create a colormesh of the reflectivity using with the plot settings defined above
                    #p1 = m.pcolormesh(glons,glats,refl,norm=norm,cmap=cmap,ax=ax,latlon=True)
                    #p2 = m.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,ax=ax,latlon=True)
                    p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                    #add the colorbar axes and create the colorbar based on the settings above
                    self.draw()
                    if(ii == len(localfiles.success)):
                        ii = 0
                except ValueError:
                    if(ii == len(localfiles.success)):
                        ii = 0
                    pass
                except:
        
                    if(ii == len(localfiles.success)):
                        ii = 0
                    pass
        else:
            #site = 'KBOX'
            #site2 = 'KENX'
    
            #get the radar location (this is used to set up the basemap and plotting grid)
            loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
            loc2 = pyart.io.nexrad_common.get_nexrad_location('KENX')
            lon0 = loc[1] ; lat0 = loc[0]
            lon1 = loc2[1]; lat1 = loc2[0]
            self.axes.clear()
            ii = ii + 1
            self.j = self.j + 1
            if(ii == len(localfiles.success)):
                ii = ii - 1
            #if(self.j == len(localfiles2.success)):
                #self.j = self.j - 1
            check = files1[ii][-6:-5]
            if(check == 'V'):
                timme = files1[ii][-13:-7]
                timelabel = timme[0:6]
                time1 = files1[ii][-13:-10]
                #time2 = localfiles2.success[self.j].filepath[-13:-10]
            else:
                timme = files1[ii][-9:]
                timelabel = timme[0:6]
                time1 = files1[ii][-9:-6]
                #time2 = localfiles2.success[self.j].filepath[-9:-6]
            try:
                radar = pyart.io.read_nexrad_archive(files1[ii])
                radar2 = pyart.io.read_nexrad_archive(files2[ii])
           
                #set up the plotting grid for the data
                display = pyart.graph.RadarMapDisplay(radar)
                display2 = pyart.graph.RadarMapDisplay(radar2)
                x,y = display._get_x_y(0,True,None)
                x2,y2 = display2._get_x_y(0,True,None)
                self.axes.set_extent([-78, -68, 40, 45], crs.Geodetic())
                #ax = plt.axes(projection=crs.PlateCarree())
                #states = NaturalEarthFeature(category = 'cultural', scale = '50m', facecolor = 'none',name = 'admin_1_states_provinces_shp')
                #self.axes.add_feature(states,linewidth=1.,edgecolor="black")
                #self.axes.coastlines('50m',linewidth=0.8)
                self.axes.gridlines(color="black", linestyle="dotted")
        
                
                #get the plotting grid into lat/lon coordinates
                x0,y0 = self.m(lon0,lat0)
                x1,y1 = self.m(lon1,lat1)
                glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
                glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                #read in the lowest scan angle reflectivity field in the NEXRAD file 
                refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                del radar
                del radar2
                cmap = 'pyart_NWSRef'
                #create a colormesh of the reflectivity using with the plot settings defined above
                #p1 = m.pcolormesh(glons,glats,refl,norm=norm,cmap=cmap,ax=ax,latlon=True)
                #p2 = m.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,ax=ax,latlon=True)
                p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                #add the colorbar axes and create the colorbar based on the settings above
                self.draw()
                if(ii == len(files1[ii])):
                    ii = 0
            except ValueError:
                if(ii == len(files1[ii])):
                    ii = 0
                pass
            except:
    
                if(ii == len(files1[ii])):
                    ii = 0
                pass
            

###############################################################################
#Plot on the right which displays the frame by frame image.       
class animated(mycanvas):

    def __init__(self,*args):
        mycanvas.__init__(self,*args)
        #super().__init__(self)
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
               #select the radar site
        global localfiles
        global localfiles2
        global site
        global files1
        global files2
        #site = 'KBOX'
        #site2 = 'KENX'
        if(site != 'both'):
            #get the radar location (this is used to set up the basemap and plotting grid)
            loc = pyart.io.nexrad_common.get_nexrad_location(site)
            #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
            lon0 = loc[1] ; lat0 = loc[0]
            #lon1 = loc2[1]; lat1 = loc2[0]
            #use boto to connect to the AWS nexrad holdings directory
            #ax = self.figure.add_subplot(111)
                            #set up a basemap with a lambert conformal projection centered 
            # on the radar location, extending 1 degree in the meridional direction
            # and 1.5 degrees in the longitudinal in each direction away from the 
            # center point.
            self.m = Basemap(projection='lcc',lon_0=-73,lat_0=42.5,
                      llcrnrlat=40,llcrnrlon=-78,
                      urcrnrlat=45,urcrnrlon=-68,resolution='l')
            
            #add geographic boundaries and lat/lon labels
            #self.m.drawparallels(np.arange(20,70,0.5),labels=[1,0,0,0],fontsize=12,
                            #color='k',ax=ax,linewidth=0.001)
            #self.m.drawmeridians(np.arange(-150,-50,1),labels=[0,0,1,0],fontsize=12,
                           #color='k',ax=ax,linewidth=0.001)
            #m.drawcounties(linewidth=0.5,color='gray',ax=ax)
            #self.m.drawstates(linewidth=1.5,color='k',ax=ax)
            #self.m.drawcoastlines(linewidth=1.5,color='k',ax=ax)
            #Use Nasa Blue marble Earth for background if you want
            #m.bluemarble()
            #m.shadedrelief()
            #mark the radar location with a black dot
            #m.scatter(lon0,lat0,marker='o',s=20,color='k',ax=ax,latlon=True)
            #m.scatter(lon1,lat1,marker='o',s=20,color='k',ax=ax,latlon=True)
            #normalize the colormap based on the levels provided above                    
            #Take the first file that we gathered to plot (filenames are stored in the dictionary localfiles.success)
            try:
                radar = pyart.io.read_nexrad_archive(files1[0])
                #radar2 = pyart.io.read_nexrad_archive(localfiles2.success[0].filepath)
       
                #set up the plotting grid for the data
                display = pyart.graph.RadarMapDisplay(radar)
                #display2 = pyart.graph.RadarMapDisplay(radar2)
                x,y = display._get_x_y(0,True,None)
                #x2,y2 = display2._get_x_y(0,True,None)
        
                
                #get the plotting grid into lat/lon coordinates
                x0,y0 = self.m(lon0,lat0)
                #x1,y1 = self.m(lon1,lat1)
                glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
                #glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                #read in the lowest scan angle reflectivity field in the NEXRAD file 
                refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                #refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                del radar
                #del radar2
                #set up the plotting parameters (NWSReflectivity colormap, contour levels,
                # and colorbar tick labels)
                cmap = 'pyart_NWSRef'
                levs = np.linspace(0,80,41,endpoint=True)
                ticks = np.linspace(0,80,9,endpoint=True)
                label = 'Radar Reflectivity Factor ($\mathsf{dBZ}$)'
                #define the plot axis to the be axis defined above
                self.norm = mpl.colors.BoundaryNorm(levs,256)
                #create a colormesh of the reflectivity using with the plot settings defined above
                p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
                #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
                #add the colorbar axes and create the colorbar based on the settings above
                #cax = figure.add_axes([0.075,0.075,0.85,0.025])
                #cbar = plt.colorbar(p1,ticks=ticks,norm=self.norm,cax=cax,orientation='horizontal')
                #cbar.set_label(label,fontsize=12)
                #cbar.ax.tick_params(labelsize=11)
                #display the figurefrom matplotlib.animation import FuncAnimation
                    #If the try for files says there aren't any files found, then we skip
            except ValueError:
                pass
        else:
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
            self.m = Basemap(projection='lcc',lon_0=-73,lat_0=42.5,
                      llcrnrlat=40,llcrnrlon=-78,
                      urcrnrlat=45,urcrnrlon=-68,resolution='l')
            
            #add geographic boundaries and lat/lon labels
            #self.m.drawparallels(np.arange(20,70,0.5),labels=[1,0,0,0],fontsize=12,
                            #color='k',ax=ax,linewidth=0.001)
            #self.m.drawmeridians(np.arange(-150,-50,1),labels=[0,0,1,0],fontsize=12,
                           #color='k',ax=ax,linewidth=0.001)
            #m.drawcounties(linewidth=0.5,color='gray',ax=ax)
            #self.m.drawstates(linewidth=1.5,color='k',ax=ax)
            #self.m.drawcoastlines(linewidth=1.5,color='k',ax=ax)
            #Use Nasa Blue marble Earth for background if you want
            #m.bluemarble()
            #m.shadedrelief()
            #mark the radar location with a black dot
            #m.scatter(lon0,lat0,marker='o',s=20,color='k',ax=ax,latlon=True)
            #m.scatter(lon1,lat1,marker='o',s=20,color='k',ax=ax,latlon=True)
            #normalize the colormap based on the levels provided above                    
            #Take the first file that we gathered to plot (filenames are stored in the dictionary localfiles.success)
            try:
                radar = pyart.io.read_nexrad_archive(files1[0])
                radar2 = pyart.io.read_nexrad_archive(files2[0])
       
                #set up the plotting grid for the data
                display = pyart.graph.RadarMapDisplay(radar)
                display2 = pyart.graph.RadarMapDisplay(radar2)
                x,y = display._get_x_y(0,True,None)
                x2,y2 = display2._get_x_y(0,True,None)
        
                
                #get the plotting grid into lat/lon coordinates
                x0,y0 = self.m(lon0,lat0)
                x1,y1 = self.m(lon1,lat1)
                glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
                glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                #read in the lowest scan angle reflectivity field in the NEXRAD file 
                refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                del radar
                del radar2
                #set up the plotting parameters (NWSReflectivity colormap, contour levels,
                # and colorbar tick labels)
                cmap = 'pyart_NWSRef'
                levs = np.linspace(0,80,41,endpoint=True)
                ticks = np.linspace(0,80,9,endpoint=True)
                label = 'Radar Reflectivity Factor ($\mathsf{dBZ}$)'
                #define the plot axis to the be axis defined above
                self.norm = mpl.colors.BoundaryNorm(levs,256)
                #create a colormesh of the reflectivity using with the plot settings defined above
                p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
                self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.LambertConformal())
                #add the colorbar axes and create the colorbar based on the settings above
                #cax = figure.add_axes([0.075,0.075,0.85,0.025])
                #cbar = plt.colorbar(p1,ticks=ticks,norm=self.norm,cax=cax,orientation='horizontal')
                #cbar.set_label(label,fontsize=12)
                #cbar.ax.tick_params(labelsize=11)
                #display the figurefrom matplotlib.animation import FuncAnimation
                    #If the try for files says there aren't any files found, then we skip
            except ValueError:
                pass
    def onclick(self,event):
        ix, iy = event.xdata, event.ydata
        #ix,iy = crs.LambertConformal.transform_point(ix,iy,crs.PlateCarree)
        print ('x = %f, y = %f'%(
            ix, iy))
    
        global coordsx
        global coordsy
        global testing
        coordsx.append(ix)
        coordsy.append(iy)
        #if(counter == testing):
        #    QMessageBox.about(self, "Warning", "No more data available to plot")
        #    shutil.rmtree(templocation)
    def update_figure(self):
        global counter2
        global counter1
        global localfiles
        global localfiles2
        global files1
        global files2
        global site
        #site = 'KBOX'
        #site2 = 'KENX'
        if(site != 'both'):
            #get the radar location (this is used to set up the basemap and plotting grid)
            loc = pyart.io.nexrad_common.get_nexrad_location(site)
            #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
            lon0 = loc[1] ; lat0 = loc[0]
            #lon1 = loc2[1]; lat1 = loc2[0]
            self.axes.clear()
            i = counter2
            #j = counter1
            if(counter2 == len(localfiles.success)):
                i = i - 1
            #if(counter1 == len(localfiles2.success)):
                #j = j - 1
            check = localfiles.success[i].filepath[-6:-5]
            if(check == 'V'):
                timme = localfiles.success[i].filepath[-13:-7]
                timelabel = timme[0:6]
                time1 = localfiles.success[i].filepath[-13:-10]
                #time2 = localfiles2.success[j].filepath[-13:-10]
            else:
                timme = localfiles.success[i].filepath[-9:]
                timelabel = timme[0:6]
                time1 = localfiles.success[i].filepath[-9:-6]
                #time2 = localfiles2.success[j].filepath[-9:-6]
            try:
                radar = pyart.io.read_nexrad_archive(localfiles.success[i].filepath)
                #radar2 = pyart.io.read_nexrad_archive(localfiles2.success[j].filepath)
           
                #set up the plotting grid for the data
                display = pyart.graph.RadarMapDisplay(radar)
                #display2 = pyart.graph.RadarMapDisplay(radar2)
                x,y = display._get_x_y(0,True,None)
                #x2,y2 = display2._get_x_y(0,True,None)
                self.axes.set_extent([-78, -68, 40, 45], crs.Geodetic())
                #ax = plt.axes(projection=crs.PlateCarree())
                #states = NaturalEarthFeature(category = 'cultural', scale = '50m', facecolor = 'none',name = 'admin_1_states_provinces_shp')
                #self.axes.add_feature(states,linewidth=1.,edgecolor="black")
                #self.axes.coastlines('50m',linewidth=0.8)
                self.axes.gridlines(color="black", linestyle="dotted")
        
                
                #get the plotting grid into lat/lon coordinates
                x0,y0 = self.m(lon0,lat0)
                #x1,y1 = self.m(lon1,lat1)
                glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
                #glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                #read in the lowest scan angle reflectivity field in the NEXRAD file 
                refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                #refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                del radar
                #del radar2
                cmap = 'pyart_NWSRef'
                #create a colormesh of the reflectivity using with the plot settings defined above
                #p1 = m.pcolormesh(glons,glats,refl,norm=norm,cmap=cmap,ax=ax,latlon=True)
                #p2 = m.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,ax=ax,latlon=True)
                p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                #self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                #add the colorbar axes and create the colorbar based on the settings above
                self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                counter2 = counter2 + 1
                counter1 = counter1 + 1
                self.draw()
                if(counter2 == len(localfiles.success)):
                    counter2 = 0
                    counter1 = 0
            except ValueError:
                counter2 = counter2 + 1
                counter1 = counter1 + 1
                if(counter2 == len(localfiles.success)):
                    counter2 = 0
                    counter1 = 0
                pass
            except:
                counter2 = counter2 + 1
                counter1 = counter1 + 1
                if(counter2 == len(localfiles.success)):
                    counter2 = 0
                    counter1 = 0
                pass
        else:
                       #get the radar location (this is used to set up the basemap and plotting grid)
            loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
            loc2 = pyart.io.nexrad_common.get_nexrad_location('KENX')
            lon0 = loc[1] ; lat0 = loc[0]
            lon1 = loc2[1]; lat1 = loc2[0]
            self.axes.clear()
            i = counter2
            #j = counter1
            if(counter2 == len(files1)):
                i = i - 1
            #if(counter1 == len(localfiles2.success)):
                #j = j - 1
            check = files1[i][-6:-5]
            if(check == 'V'):
                timme = files1[i][-13:-7]
                timelabel = timme[0:6]
                time1 = files1[i][-13:-10]
                #time2 = localfiles2.success[j].filepath[-13:-10]
            else:
                timme = files1[i][-9:]
                timelabel = timme[0:6]
                time1 = files1[i][-9:-6]
                #time2 = localfiles2.success[j].filepath[-9:-6]
            try:
                radar = pyart.io.read_nexrad_archive(files1[i])
                radar2 = pyart.io.read_nexrad_archive(files2[i])
           
                #set up the plotting grid for the data
                display = pyart.graph.RadarMapDisplay(radar)
                display2 = pyart.graph.RadarMapDisplay(radar2)
                x,y = display._get_x_y(0,True,None)
                x2,y2 = display2._get_x_y(0,True,None)
                self.axes.set_extent([-78, -68, 40, 45], crs.Geodetic())
                #ax = plt.axes(projection=crs.PlateCarree())
                #states = NaturalEarthFeature(category = 'cultural', scale = '50m', facecolor = 'none',name = 'admin_1_states_provinces_shp')
                #self.axes.add_feature(states,linewidth=1.,edgecolor="black")
                #self.axes.coastlines('50m',linewidth=0.8)
                self.axes.gridlines(color="black", linestyle="dotted")
        
                
                #get the plotting grid into lat/lon coordinates
                x0,y0 = self.m(lon0,lat0)
                x1,y1 = self.m(lon1,lat1)
                glons,glats = self.m((x0+x*1000.), (y0+y*1000.),inverse=True)
                glons2,glats2 = self.m((x1+x2*1000.), (y1+y2*1000.),inverse=True)
                #read in the lowest scan angle reflectivity field in the NEXRAD file 
                refl = np.squeeze(radar.get_field(sweep=0,field_name='reflectivity'))
                refl2 = np.squeeze(radar2.get_field(sweep=0,field_name='reflectivity'))
                del radar
                del radar2
                cmap = 'pyart_NWSRef'
                #create a colormesh of the reflectivity using with the plot settings defined above
                #p1 = m.pcolormesh(glons,glats,refl,norm=norm,cmap=cmap,ax=ax,latlon=True)
                #p2 = m.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,ax=ax,latlon=True)
                p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                #self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                #add the colorbar axes and create the colorbar based on the settings above
                self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                counter2 = counter2 + 1
                counter1 = counter1 + 1
                self.draw()
                if(counter2 == len(files1)):
                    counter2 = 0
                    counter1 = 0
            except ValueError:
                counter2 = counter2 + 1
                counter1 = counter1 + 1
                if(counter2 == len(files1)):
                    counter2 = 0
                    counter1 = 0
                pass
            except:
                counter2 = counter2 + 1
                counter1 = counter1 + 1
                if(counter2 == len(files1)):
                    counter2 = 0
                    counter1 = 0
                pass
###############################################################################

###############################################################################
      
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())