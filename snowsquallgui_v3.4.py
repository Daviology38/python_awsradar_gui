# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 17:00:30 2019

@author: CoeFamily
"""


import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow,QInputDialog, QMessageBox, QAbstractItemView, QListWidget, QHBoxLayout,QLineEdit, QCheckBox,QGridLayout,QGroupBox, QToolButton,
    QAction, QFileDialog, QDialog, QComboBox, QListWidgetItem, QTreeView, QListView, QFileSystemModel, QApplication, qApp, QWidget,QVBoxLayout,QLabel,QPushButton,QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDir, QRect,QTimer, Qt
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
import os

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
global dirname
global imagenumber
global jj
global filedir
global filedir2
global filetype
global select
global usrdir
jj = 0
ii = 0
imagenumber = 0
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
        #Change to location of the snowsqualldatesv5.txt file
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
class choosetype(QDialog):
     def __init__(self, parent=None):
        super(choosetype, self).__init__(parent)
        self.setWindowTitle("Choose Type")
        self.layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem('Local')
        self.cb.addItem('Download')
        #self.listWidget.itemClicked.connect(self.printItemText)
        self.layout.addWidget(self.cb)
        self.setLayout(self.layout)
        self.cb.activated[str].connect(self.onActivated)
       
     def onActivated(self, text):
        global filetype
        filetype = text
        filetype = str(filetype).rstrip()
        self.accept()    
################################################################################
class yesno(QDialog):
     def __init__(self, parent=None):
        super(yesno, self).__init__(parent)
        self.setWindowTitle("Are You Using More Than One Site?")
        self.layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem('Yes')
        self.cb.addItem('No')
        #self.listWidget.itemClicked.connect(self.printItemText)
        self.layout.addWidget(self.cb)
        self.setLayout(self.layout)
        self.cb.activated[str].connect(self.onActivated)
       
     def onActivated(self, text):
        global select
        select = text
        select = str(select).rstrip()
        self.accept()    
################################################################################
class choosefiles(QDialog):
     def __init__(self, parent=None):
        super(choosefiles, self).__init__(parent)
        global filedir
        filedir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.accept()          

################################################################################
class choosefiles2(QDialog):
     def __init__(self, parent=None):
        super(choosefiles2, self).__init__(parent)
        global filedir2
        filedir2 = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
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

############################

#Main Window
class Example(QMainWindow):
    
    def __init__(self, parent = None):
        super(Example,self).__init__()
        self.title = 'Radar Analysis'
        self.left = 30
        self.top = 30
        self.width = 640
        self.height = 480
        self.dialog = choosetype(self)
        som = self.dialog.exec()
        if som == QDialog.Accepted:
            
            global filetype

            if (filetype == 'Local'):      
                global filedir
                global usrdir
                filedir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
                self.dialog8 = yesno(self)
                som3 = self.dialog8.exec()
                global select
                if(select == 'Yes'):
                    global filedir2
                    filedir2 = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
                text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter date (mmddyyyy):')
                if ok:
                    global usrdir
                    usrdir = str(text)
                self.dialog9 = RadarSite(self)
                if self.dialog9.exec_():
                    self.initUI2()
            else:
                self.dialog2 = Test(self)
                self.dialog3 = Timeteststart(self)
                self.dialog4 = Timetestend(self)
                self.dialog5 = RadarSite(self)
                if self.dialog2.exec_():
                    if self.dialog3.exec_():
                        if self.dialog4.exec_():
                            if self.dialog5.exec_():
                                self.initUI()

    def initUI2(self):               
        print('Here')
        #############################################################
        #get the data
        global date
        global starttime
        global endtime
        global filedir
        global filedir2
        global site
        global files1
        global files2
        global dirname
        global usrdir
        try:
            os.mkdir(usrdir)
        except:
            pass
        dirname = usrdir
        filenames = os.listdir(filedir)
        date = usrdir
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
        if(check == 'V' and site == 'both'):
            filenames2 = os.listdir(filedir2)
            for i in range(len(filenames)):
                time1 = filenames[i][-13:-10]
                times1.append([time1,i])
            for j in range(len(filenames2)):
                time2 = filenames2[j][-13:-10]
                times2.append([time2,j])
            #time2 = localfiles2.success[self.j].filepath[-13:-10]
        elif(check == 'V' and site != 'both'):
            for i in range(len(filenames)):
                time1 = filenames[i][-13:-10]
                times1.append([time1,i])
        elif(check != 'V' and site == 'both'):
            filenames2 = os.listdir(filedir2)
            for i in range(len(filenames)):
                time1 = filenames[i][-6:-3]
                times1.append([time1,i])
            for j in range(len(filenames2)):
                time2 = filenames2[-6:-3]
                times2.append([time2,j])
        else:
            for i in range(len(filenames)):
                time1 = filenames[i][-6:-3]
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
            for i in range(len(index1)):
                nfile = filenames[index1[i]]
                files1.append(nfile)
                nfile = filenames2[index2[i]]
                files2.append(nfile)
        else:
            tlist1 = []
            for i in range(len(temp1)):
                tlist1.append(temp1[i][0])
            svalue = set(tlist1)
            index1 = []
            index2 = []
            for value in svalue:
                try:
                    ind = tlist1.index(value)    
                    index1.append(temp1[ind][1])
                except:
                    pass
            print(index1)
            for i in range(len(index1)):
                nfile = filenames[index1[i]]
                files1.append(nfile)
        if(site == 'both'):
            files1, files2 = (list(t) for t in zip(*sorted(zip(files1, files2))))
            static12(self)
        else:
            files1.sort()
            static12(self)
            
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
        #Add in a grid layout
        self._main = QWidget()
        self.setCentralWidget(self._main)
        grid = QGridLayout(self._main)
        #############################################################
        #Add in the second plot
        sc2 = static22(self._main)
        grid.addWidget(sc2, 1, 3,1,2)
        ##############################################################
        #############################################################
        #Add in image slider


        self.label = QLabel(self)
        global imagenumber 
        directory = dirname
        imagelist = os.listdir(directory)
        imagelist.sort(key=lambda fname: int(fname.split('.')[0]))
        pixmap = QPixmap(directory + '/' + imagelist[imagenumber])
        self.label.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())            
        grid.addWidget(self.label,1,1,1,2)
        #self.resize(pixmap.width() + 500, pixmap.height())
        pybutton = QPushButton('->', self)
        pybutton.resize(100,32)      
        pybutton.clicked.connect(self.keyPressEvent)
        grid.addWidget(pybutton,2,2,1,1)
        pybutton2 = QPushButton('<-', self)
        pybutton2.resize(100,32)      
        pybutton2.clicked.connect(self.keyPressEvent2)
        grid.addWidget(pybutton2,2,1,1,1)
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
        
        self.setGeometry(200, 300, 1000, 500)
        self.setWindowTitle('Simple menu')  
        self.show()

    
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
            global dirname
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
            try:
                os.mkdir(year+month+dayst)
            except:
                pass
            dirname = year + month + dayst
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
            #If the try for the files says there are NoneType files found, then we skip
            except TypeError:
                QMessageBox.about(self,"Warning", "Type Error, try new date!")
                sys.exit(0)
            testing = len(localfiles.success)
            #Organize the files to get one for each 3 digit time for each station
            check = localfiles.success[0].filepath[-6:-5]
            check2 = localfiles.success[0].filepath[-3:-2]
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
            elif(check2 == 'V' and site =='both'):
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-10:-7]
                    times1.append([time1,i])
                for j in range(len(localfiles2.success)):
                    time2 = localfiles2.success[j].filepath[-10:-7]
                    times2.append([time2,j])    
                #time2 = localfiles2.success[self.j].filepath[-13:-10]
            elif(check == 'V' and site != 'both'):
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-13:-10]
                    times1.append([time1,i])
            elif(check2 == 'V' and site != 'both'):
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-10:-7]
                    times1.append([time1,i])
            else:
                for i in range(len(localfiles.success)):
                    time1 = localfiles.success[i].filepath[-9:-6]
                    times1.append([time1,i])
                for j in range(len(localfiles2.success)):
                    time2 = localfiles2.success[j].filepath[-9:-6]
                    times2.append([time2,j])    
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
                for i in range(len(index1)):
                    nfile = localfiles.success[index1[i]].filepath
                    files1.append(nfile)
                    nfile = localfiles2.success[index2[i]].filepath
                    files2.append(nfile)
            else:
                for i in range(len(temp1)):
                    try:
                        nfile = localfiles.success[temp1[i][1]].filepath
                        print(temp1[i][1])
                        files1.append(nfile)
                    except:
                        pass
            if(site == 'both'):
                files1, files2 = (list(t) for t in zip(*sorted(zip(files1, files2))))
                static(self)
            else:
                files1.sort()
                static(self)
                
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
            #Add in a grid layout
            self._main = QWidget()
            self.setCentralWidget(self._main)
            grid = QGridLayout(self._main)
            #############################################################
            #Add in the second plot
            sc2 = static2(self._main)
            grid.addWidget(sc2, 1, 3,1,2)
            ##############################################################
            #############################################################
            #Add in image slider


            self.label = QLabel(self)
            global imagenumber 
            directory = dirname
            imagelist = os.listdir(directory)
            imagelist.sort(key=lambda fname: int(fname.split('.')[0]))
            pixmap = QPixmap(directory + '/' + imagelist[imagenumber])
            self.label.setPixmap(pixmap)
            #self.resize(pixmap.width(), pixmap.height())            
            grid.addWidget(self.label,1,1,1,2)
            #self.resize(pixmap.width() + 500, pixmap.height())
            pybutton = QPushButton('->', self)
            pybutton.resize(100,32)      
            pybutton.clicked.connect(self.keyPressEvent)
            grid.addWidget(pybutton,2,2,1,1)
            pybutton2 = QPushButton('<-', self)
            pybutton2.resize(100,32)      
            pybutton2.clicked.connect(self.keyPressEvent2)
            grid.addWidget(pybutton2,2,1,1,1)
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
            
            self.setGeometry(200, 300, 1000, 500)
            self.setWindowTitle('Simple menu')  
            self.show()
        else:
            QMessageBox.about(self,"Warning", "No Date has been selected. Please click Select date first!")
   
    
    def keyPressEvent(self):
        global imagenumber
        imagenumber=imagenumber+1
        directory = dirname
        imagelist = os.listdir(directory)
        if(imagenumber == len(imagelist)):
            imagenumber = 0
        imagelist.sort(key=lambda fname: int(fname.split('.')[0]))
        pixmap = QPixmap(directory + '/' + imagelist[imagenumber])
        self.label.setPixmap(pixmap)
          

        # self.show()  

    def keyPressEvent2(self):
        global imagenumber
        imagenumber=imagenumber-1
        directory = dirname
        imagelist = os.listdir(directory)
        if(imagenumber <0):
            imagenumber = len(imagelist)-1
        imagelist.sort(key=lambda fname: int(fname.split('.')[0]))
        pixmap = QPixmap(directory + '/' + imagelist[imagenumber])
        self.label.setPixmap(pixmap)
          

        # self.show()  
            
    def plotpoints(self):
        global coordsx
        global coordsy
        coordsx.append(0)
        coordsy.append(0)
        print(0)
        global ii
        global jj        
        jj = 0
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
        try:
            shutil.rmtree(templocation)
        except:
            pass
        sys.exit(0)
            


###############################################################################
class showimage(QLabel):
     def __init__(self,imagenumber):
        super(showimage,self).__init__(parent=None)
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        # label = QLabel(self)
        
            
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



        self.canvas=FigureCanvas.__init__(self, figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.figure.suptitle('Radar Returns')
        self.compute_initial_figure()
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
            self.draw()
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
     
    def onclick(self):
        pass
    
    def compute_initial_figure(self):
               #select the radar site
        global localfiles
        global localfiles2
        global files1
        global files2
        global site
        global ii
        global dirname
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

        if(site != 'both'):
            index = len(files1)
        else:
            index = len(files1)
        while ii < index:
            if(site != 'both'):
        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location(site)
                #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
                lon0 = loc[1] ; lat0 = loc[0]
                #lon1 = loc2[1]; lat1 = loc2[0]
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[ii][-6:-5]
                check2 = files1[ii][-3:-2]
                if(check == 'V'):
                    timme = files1[ii][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[ii][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-10:-7]
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
                    #p2 = m.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,axii=ax,latlon=True)
                    p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                    #add the colorbar axes and create the colorbar based on the settings above
                    name =  str(ii) + '.png'
                    self.figure.savefig(dirname + '/' + name)
                    self.draw()
                    ii = ii + 1
                except ValueError:
                    ii = ii + 1
                    pass
                except:
                    ii = ii + 1
                    pass
            else:
                        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
                loc2 = pyart.io.nexrad_common.get_nexrad_location('KENX')
                lon0 = loc[1] ; lat0 = loc[0]
                lon1 = loc2[1]; lat1 = loc2[0]
                self.axes.clear()
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[ii][-6:-5]
                check2 = files1[ii][-3:-2]
                if(check == 'V'):
                    timme = files1[ii][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[ii][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-10:-7]
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
                    p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                    #add the colorbar axes and create the colorbar based on the settings above
                    name = str(ii) + '.png'
                    self.figure.savefig(dirname + '/' + name)
                    self.draw()
                    ii = ii + 1
                except ValueError:
                    ii = ii + 1
                    print('Value')
                    pass
                except:
                    print('other')
                    ii = ii + 1
                    pass
        
            
class static2(mycanvas):
    def __init__(self, parent=None):
        mycanvas.__init__(self)
        global jj
        self.j = 0
    def compute_initial_figure(self):
               #select the radar site
        global localfiles
        global localfiles2
        global files1
        global files2
        global site
        global jj
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
            self.draw()
        except ValueError:
            pass

    def onclick(self,event):
        global jj
        global files1
        global files2
        if(jj != 0):
            ix, iy = event.xdata, event.ydata
            #ix,iy = crs.LambertConformal.transform_point(ix,iy,crs.PlateCarree)
            print ('x = %f, y = %f'%(
                ix, iy))
        
            global coordsx
            global coordsy
            global testing
            coordsx.append(ix)
            coordsy.append(iy)

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
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-9:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-9:-6]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(files1[jj])
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
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
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-9:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-9:-6]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(files1[jj])
                    radar2 = pyart.io.read_nexrad_archive(files2[jj])
               
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
        else:
            global localfiles
            global localfiles2
            #site = 'KBOX'
            #site2 = 'KENX'
            if(site != 'both'):
        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location(site)
                #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
                lon0 = loc[1] ; lat0 = loc[0]
                #lon1 = loc2[1]; lat1 = loc2[0]
                self.axes.clear()
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-9:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-9:-6]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(files1[jj])
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
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
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-9:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-9:-6]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(files1[jj])
                    radar2 = pyart.io.read_nexrad_archive(files2[jj])
               
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
            

###############################################################################
###############################################################################
class mycanvas2(FigureCanvas):
    def __init__(self, parent=None):
        figure = matplotlib.figure.Figure()
        self.axes = figure.add_subplot(111,projection=crs.PlateCarree())
        self.axes.set_extent([-78, -68, 40, 45], crs.PlateCarree())
        #ax = plt.axes(projection=crs.PlateCarree())
        #states = NaturalEarthFeature(category = 'cultural', scale = '50m', facecolor = 'none',name = 'admin_1_states_provinces_shp')
        #self.axes.add_feature(states,linewidth=1.,edgecolor="black")
        #self.axes.coastlines('50m',linewidth=0.8)
        self.axes.gridlines(color="black", linestyle="dotted")



        self.canvas=FigureCanvas.__init__(self, figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.figure.suptitle('Radar Returns')
        self.compute_initial_figure()
                       #select the radar site

    def compute_initial_figure(self):
               #select the radar site
        global localfiles
        global localfiles2
        global files1
        global files2
        global site
        global ii
        global filedir
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
            radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[0])
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
class static12(mycanvas2):
    def __init__(self, parent=None):
        mycanvas2.__init__(self)
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
        global filedir
        global filedir2
        global dirname
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
            radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[0])
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

        if(site != 'both'):
            index = len(files1)
        else:
            index = len(files1)
        while ii < index:
            if(site != 'both'):
        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location(site)
                #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
                lon0 = loc[1] ; lat0 = loc[0]
                #lon1 = loc2[1]; lat1 = loc2[0]
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[ii][-6:-5]
                check2 = files1[ii][-3:-2]
                if(check == 'V'):
                    timme = files1[ii][-6:-1]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-6:-3]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[ii][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-10:-7]
                else:
                    timme = files1[ii][-6:]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-6:-3]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[ii])
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
                    #p2 = m.pcolormesh(glons2,glats2,refl2,norm=norm,cmap=cmap,axii=ax,latlon=True)
                    p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    #self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                    #add the colorbar axes and create the colorbar based on the settings above
                    name =  str(ii) + '.png'
                    self.figure.savefig(dirname + '/' + name)
                    self.draw()
                    ii = ii + 1
                except ValueError:
                    ii = ii + 1
                    pass
                except:
                    ii = ii + 1
                    pass
            else:
                        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location('KBOX')
                loc2 = pyart.io.nexrad_common.get_nexrad_location('KENX')
                lon0 = loc[1] ; lat0 = loc[0]
                lon1 = loc2[1]; lat1 = loc2[0]
                self.axes.clear()
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[ii][-6:-5]
                check2 = files1[ii][-3:-2]
                if(check == 'V'):
                    timme = files1[ii][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[ii][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-10:-7]
                else:
                    timme = files1[ii][-6:]
                    timelabel = timme[0:6]
                    time1 = files1[ii][-6:-3]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[ii])
                    radar2 = pyart.io.read_nexrad_archive(filedir2 + '/' + files2[ii])
               
                    #set up the plotting grid for the data
                    display = pyart.graph.RadarMapDisplay(radar)
                    display2 = pyart.graph.RadarMapDisplay(radar2)
                    x,y = display._get_x_y(0,True,None)
                    x2,y2 = display2._get_x_y(0,True,None)
                    self.axes.set_extent([-78, -68, 40, 45], crs.Geodetic())
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
                    p1 = self.axes.pcolormesh(glons,glats,refl,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.axes.pcolormesh(glons2,glats2,refl2,norm=self.norm,cmap=cmap,transform=crs.PlateCarree())
                    self.figure.suptitle('Time = ' + timelabel[0:2] + ':' + timelabel[2:4] + ':' + timelabel[4:6] + ' z')
                    #add the colorbar axes and create the colorbar based on the settings above
                    name = str(ii) + '.png'
                    self.figure.savefig(dirname + '/' + name)
                    self.draw()
                    ii = ii + 1
                except ValueError:
                    ii = ii + 1
                    print('Value')
                    pass
                except:
                    print('other')
                    ii = ii + 1
                    pass
    def onclick(self,event):
        pass               
                    
            
class static22(mycanvas2):
    def __init__(self, parent=None):
        mycanvas2.__init__(self)
        global jj
        self.j = 0
    def compute_initial_figure(self):
               #select the radar site
        global localfiles
        global localfiles2
        global files1
        global files2
        global site
        global jj
        global filedir
        global filedir2
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
            radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[0])
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
        global jj
        global files1
        global files2
        if(jj != 0):
            ix, iy = event.xdata, event.ydata
            #ix,iy = crs.LambertConformal.transform_point(ix,iy,crs.PlateCarree)
            print ('x = %f, y = %f'%(
                ix, iy))
        
            global coordsx
            global coordsy
            global testing
            coordsx.append(ix)
            coordsy.append(iy)
            global files1
            global files2
            global dirname
            global localfiles
            global localfiles2
            global site
            global filedir
            global filedir2
            #site = 'KBOX'
            #site2 = 'KENX'
            if(site != 'both'):
        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location(site)
                #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
                lon0 = loc[1] ; lat0 = loc[0]
                #lon1 = loc2[1]; lat1 = loc2[0]
                self.axes.clear()
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-6:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-6:-3]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[jj])
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
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
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-6:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-6:-3]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[jj])
                    radar2 = pyart.io.read_nexrad_archive(filedir2 + '/' + files2[jj])
               
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
        else:
            global dirname
            global localfiles
            global localfiles2
            #site = 'KBOX'
            #site2 = 'KENX'
            if(site != 'both'):
        
                #get the radar location (this is used to set up the basemap and plotting grid)
                loc = pyart.io.nexrad_common.get_nexrad_location(site)
                #loc2 = pyart.io.nexrad_common.get_nexrad_location(site2)
                lon0 = loc[1] ; lat0 = loc[0]
                #lon1 = loc2[1]; lat1 = loc2[0]
                self.axes.clear()
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-6:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-6:-3]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[jj])
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
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
                jj = jj + 1
                self.j = self.j + 1
                if(jj == len(files1)):
                    jj = jj - 1
                #if(self.j == len(localfiles2.success)):
                    #self.j = self.j - 1
                check = files1[jj][-6:-5]
                check2 = files1[jj][-3:-2]
                if(check == 'V'):
                    timme = files1[jj][-13:-7]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-13:-10]
                    #time2 = localfiles2.success[self.j].filepath[-13:-10]
                elif(check2 == 'V'):
                    timme = files1[jj][-10:-4]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-10:-7]
                else:
                    timme = files1[jj][-6:]
                    timelabel = timme[0:6]
                    time1 = files1[jj][-6:-3]
                    #time2 = localfiles2.success[self.j].filepath[-9:-6]
                try:
                    radar = pyart.io.read_nexrad_archive(filedir + '/' + files1[jj])
                    radar2 = pyart.io.read_nexrad_archive(filedir2 + '/' + files2[jj])
               
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
                    if(jj == len(files1)-1):
                        jj = 0
                except ValueError:
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
                except:
        
                    if(jj == len(files1)-1):
                        jj = 0
                    pass
            

###############################################################################

###############################################################################
      
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())