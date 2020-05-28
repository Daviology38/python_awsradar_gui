# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:48:56 2019

@author: CoeFamily
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout,QGridLayout,QToolButton,
    QAction, QComboBox,QApplication, qApp, QWidget,QLabel,QPushButton)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#list dates in both directories
kenx_dates = os.listdir('radar_data/kenx')
kbox_dates = os.listdir('radar_data/kenx')

#Only take dates that have data for both sites
both = (kenx_dates and kbox_dates)

#Setup the gui program for each date
############################

#Main Window
class Ui(QMainWindow):
    
    def __init__(self, parent = None):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('H:/Python/snowsquall.ui', self) # Load the .ui file
        self.show() # Show the GUI

    def adddates(self,date_list):
        for date in date_list:
            self.Datelist.addItem(date)
        self.Datelist.activated[str].connect(self.onActivated)
        
    def onActivated(self, text):
        global date
        date = text
        date = int(date)
        date = str(date).rstrip()
        self.accept()
#    def initUI(self):               
#
#        #############################################################
#        #get the data
#        
#        #First we to set up the grid layout
#        self._main = QWidget()
#        self.setCentralWidget(self._main)
#        grid = QGridLayout(self._main)
#        
#        #Add in a menu bar
#        self.statusBar()
#        menubar = self.menuBar()
#        
#        #Add stuff to menu bar
#        fileMenu = menubar.addMenu('&File')
#        newAct = QAction('New', self)   
#        saveAct = QAction('Save', self)
#        saveAct.setShortcut("Ctrl+S")
#        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
#        exitAct.setShortcut('Ctrl+Q')
#        exitAct.setStatusTip('Exit application')
#        exitAct.triggered.connect(qApp.quit)
#        
#        #Link the actions to the menu text
#        fileMenu.addAction(newAct)
#        fileMenu.addAction(saveAct)
#        fileMenu.addAction(exitAct)
#        self.clearAct = QAction(QIcon('wedb.png'), 'Clear', self)
#        menubar.addAction(self.clearAct)
#        
#        #############################################################
#        #Add in a dropdown menu (combobox) for the dates
#        self.cb = QComboBox()
#        #Add all dates that we have data for
#        for date in both:
#            self.cb.addItem(date)
#        grid.addWidget(self.cb)
#        self.cb.activated[str].connect(self.onActivated)
#
#        #############################################################
#        #Add in the plot on the right
#        self.canvas = FigureCanvas(fig)
#        self.mplvl.addWidget(self.canvas)
#        self.canvas.draw()
#        sc2 = static2(self._main)
#        grid.addWidget(sc2, 1, 3,1,2)
#        ##############################################################
#        #############################################################
#        #Add in image slider
#
#
#        self.label = QLabel(self)
#        global imagenumber 
#        directory = dirname
#        imagelist = os.listdir(directory)
#        imagelist.sort(key=lambda fname: int(fname.split('.')[0]))
#        pixmap = QPixmap(directory + '/' + imagelist[imagenumber])
#        self.label.setPixmap(pixmap)
#        #self.resize(pixmap.width(), pixmap.height())            
#        grid.addWidget(self.label,1,1,1,2)
#        #self.resize(pixmap.width() + 500, pixmap.height())
#        pybutton = QPushButton('->', self)
#        pybutton.resize(100,32)      
#        pybutton.clicked.connect(self.keyPressEvent)
#        grid.addWidget(pybutton,2,2,1,1)
#        pybutton2 = QPushButton('<-', self)
#        pybutton2.resize(100,32)      
#        pybutton2.clicked.connect(self.keyPressEvent2)
#        grid.addWidget(pybutton2,2,1,1,1)
#        #############################################################
#        #Add in a Toolbar
#        plotradar = QAction(QIcon('exit24.png'), 'Plot View', self)
#        plotradar = QToolButton()
#        plotradar.setText("Plot Cells")
#        plotradar.pressed.connect(self.plotcells)
#        crosssectionAct = QToolButton()
#        crosssectionAct.pressed.connect(self.plotpoints)
#        crosssectionAct.setText("Choose new cell")
#        self.toolbar = self.addToolBar('Plot View')
#        self.toolbar.addWidget(plotradar)
#        self.toolbar.addWidget(crosssectionAct)
#        #############################################################
#        
#        self.setGeometry(200, 300, 1000, 500)
#        self.setWindowTitle('Simple menu')  
#        self.show()
#        
#        
#        
#
#        
#    def onActivated(self, text):
#        global date
#        date = text
#        date = int(date)
#        date = str(date).rstrip()
#        self.accept()
#        
#        
#        
##            testing = len(localfiles.success)
##            #Organize the files to get one for each 3 digit time for each station
##            check = localfiles.success[0].filepath[-6:-5]
##            check2 = localfiles.success[0].filepath[-3:-2]
##            times1 = []
##            times2 = []
##            def remove(duplicate):
##                final_list = []
##                found = set([])
##                for num in duplicate:
##                    lst = []
##                    for element in num:
##                        if element not in found:
##                            found.add(element)
##                            lst.append(element)
##                    final_list.append(lst)
##                return final_list
##            #Check to see if we are using one station or two stations
##            if(check == 'V' and site == 'both'):
##                for i in range(len(localfiles.success)):
##                    time1 = localfiles.success[i].filepath[-13:-10]
##                    times1.append([time1,i])
##                for j in range(len(localfiles2.success)):
##                    time2 = localfiles2.success[j].filepath[-13:-10]
##                    times2.append([time2,j])
##            elif(check2 == 'V' and site =='both'):
##                for i in range(len(localfiles.success)):
##                    time1 = localfiles.success[i].filepath[-10:-7]
##                    times1.append([time1,i])
##                for j in range(len(localfiles2.success)):
##                    time2 = localfiles2.success[j].filepath[-10:-7]
##                    times2.append([time2,j])    
##                #time2 = localfiles2.success[self.j].filepath[-13:-10]
##            elif(check == 'V' and site != 'both'):
##                for i in range(len(localfiles.success)):
##                    time1 = localfiles.success[i].filepath[-13:-10]
##                    times1.append([time1,i])
##            elif(check2 == 'V' and site != 'both'):
##                for i in range(len(localfiles.success)):
##                    time1 = localfiles.success[i].filepath[-10:-7]
##                    times1.append([time1,i])
##            elif((check != 'V' or check2 != 'V') and site != 'both'):
##                for i in range(len(localfiles.success)):
##                    time1 = localfiles.success[i].filepath[-9:-6]
##                    times1.append([time1,i])
##            else:
##                for i in range(len(localfiles.success)):
##                    time1 = localfiles.success[i].filepath[-9:-6]
##                    times1.append([time1,i])
##                for j in range(len(localfiles2.success)):
##                    time2 = localfiles2.success[j].filepath[-9:-6]
##                    times2.append([time2,j])    
##            #Find similar values in the array(s) and remove them
##            if(site == 'both'):
##                temp1 = remove(times1)
##                temp2 = remove(times2)
##            else:
##                temp1 = remove(times1)
##            #Now if there is more than 1 array, organize so both arrays have the same time scales
##            if(site == 'both'):
##                tlist1 = []
##                tlist2 = []
##                for i in range(len(temp1)):
##                    tlist1.append(temp1[i][0])
##                for j in range(len(temp2)):
##                    tlist2.append(temp2[j][0])
##                svalue = set(tlist1) & set(tlist2)
##                index1 = []
##                index2 = []
##                for value in svalue:
##                    try:
##                        ind = tlist1.index(value)    
##                        index1.append(temp1[ind][1])
##                    except:
##                        pass
##                for value in svalue:
##                    try:
##                        ind = tlist2.index(value)    
##                        index2.append(temp2[ind][1])
##                    except:
##                        pass
##                for i in range(len(index1)):
##                    nfile = localfiles.success[index1[i]].filepath
##                    files1.append(nfile)
##                    nfile = localfiles2.success[index2[i]].filepath
##                    files2.append(nfile)
##            else:
##                for i in range(len(temp1)):
##                    try:
##                        nfile = localfiles.success[temp1[i][1]].filepath
##                        print(temp1[i][1])
##                        files1.append(nfile)
##                    except:
##                        pass
##            if(site == 'both'):
##                files1, files2 = (list(t) for t in zip(*sorted(zip(files1, files2))))
##                static(self)
##            else:
##                files1.sort()
##                static(self)
##                
#            
#
#    
#    def keyPressEvent(self):
#        global imagenumber
#        imagenumber=imagenumber+1
#        directory = dirname
#        imagelist = os.listdir(directory)
#        if(imagenumber == len(imagelist)):
#            imagenumber = 0
#        imagelist.sort(key=lambda fname: int(fname.split('.')[0]))
#        pixmap = QPixmap(directory + '/' + imagelist[imagenumber])
#        self.label.setPixmap(pixmap)
#          
#
#        # self.show()  
#
#    def keyPressEvent2(self):
#        global imagenumber
#        imagenumber=imagenumber-1
#        directory = dirname
#        imagelist = os.listdir(directory)
#        if(imagenumber <0):
#            imagenumber = len(imagelist)-1
#        imagelist.sort(key=lambda fname: int(fname.split('.')[0]))
#        pixmap = QPixmap(directory + '/' + imagelist[imagenumber])
#        self.label.setPixmap(pixmap)
#          
#
#        # self.show()  
#            
#    def plotpoints(self):
#        global coordsx
#        global coordsy
#        coordsx.append(0)
#        coordsy.append(0)
#        print(0)
#        global ii
#        global jj    
#        global filetype
#        jj = 0
#        
#        pass
#    
#
#    
#    def plotcells(self):
#        global coordsx
#        global coordsy
#        global date
#        lenx = len(coordsx)
#        figure = plt.figure()
#        self.axes = figure.add_subplot(111)
#        newcoordsx = []
#        newcoordsy = []
#        for i in range(lenx):
#            xcoor = coordsx[i]
#            ycoor = coordsy[i]
#            if( xcoor == 0 and ycoor == 0):
#                #now sort them to make sure they are in order
#                newcoordsx, newcoordsy = (list(t) for t in zip(*sorted(zip(newcoordsx, newcoordsy))))
#                self.axes.plot(newcoordsx,newcoordsy)
#                self.axes.scatter(newcoordsx,newcoordsy,marker='X',color='black')
#                newcoordsx = []
#                newcoordsy = []
#            else:
#                newcoordsx.append(xcoor)
#                newcoordsy.append(ycoor)
#        #now sort them to make sure they are in order
#        newcoordsx, newcoordsy = (list(t) for t in zip(*sorted(zip(newcoordsx, newcoordsy))))
#        self.axes.plot(newcoordsx,newcoordsy)
#        self.axes.scatter(newcoordsx,newcoordsy,marker='X',color='black')
#        print('Plot is Done')
#        df = pd.DataFrame(list(zip(coordsx,coordsy)),columns=['xcoor','ycoor'])
#        df.to_csv(date + '.csv', encoding='utf-8', index=False)
#        figure.savefig(date + '.png')
#        try:
#            shutil.rmtree(templocation)
#        except:
#            pass
#        sys.exit(0)
#            
#
#
################################################################################
#class showimage(QLabel):
#     def __init__(self,imagenumber):
#        super(showimage,self).__init__(parent=None)
#        self.mainLayout = QHBoxLayout()
#        self.setLayout(self.mainLayout)
#        # label = QLabel(self)

###############################################################################
      
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Ui()
    ex.adddates(both)
    sys.exit(app.exec_())    