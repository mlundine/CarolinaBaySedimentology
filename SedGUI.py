from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import sys
import glob
import matplotlib.pyplot as plt
import pandas as pd


global wd
wd = os.getcwd()
global augerLogs
augerLogs = os.path.join(wd,'AugerLogs')

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()


        sizeObject = QDesktopWidget().screenGeometry(-1)
        global screenWidth
        screenWidth = sizeObject.width()
        global screenHeight
        screenHeight = sizeObject.height()
        global bw1
        bw1 = int(screenWidth/15)
        global bw2
        bw2 = int(screenWidth/50)
        global bh1
        bh1 = int(screenHeight/15)
        global bh2
        bh2 = int(screenHeight/20)

        self.setWindowTitle("Carolina Bay Sediment Logs")
        self.home()
    def read_metadata(self,file):
        metadata = pd.read_excel(file)
        keys = metadata['sample'].tolist()
        depthmin = metadata['depthmin'].tolist()
        depthmax = metadata['depthmax'].tolist()
        values = zip(depthmin, depthmax)
        metadata_dict = dict(zip(keys,values))
        return metadata_dict
        
        
    def plotSedandGrainSize(self, siteFolder):
        siteName = os.path.basename(siteFolder)
        metadata = os.path.join(siteFolder, siteName + '_metadata.xlsx')
        metadata = self.read_metadata(metadata)
        print(metadata)
        self.sedImages = []
        self.grainImages = []
        i=0
        height = 0
        width = 0
        for im in glob.glob(siteFolder + '/*.jpeg'):
            imName = os.path.splitext(os.path.basename(im))[0]
            try:
                title = imName + ' ' + str(metadata[imName])
            except:
                titel = imName
            title = QLabel(title)
            label = QLabel()
            pixmap = QPixmap(im)
            scaleFac = 1
            logical1 = int(bw1*7) + (pixmap.width()/scaleFac) >= screenWidth-int(bw1*3)
            logical2 = int(bw1/2) + (pixmap.height()/scaleFac) >= screenHeight-int(bw1/2)
            while (logical1 or logical2):
                scaleFac = scaleFac + 1
                logical1 = int(bw1*7) + (pixmap.width()/scaleFac) >= screenWidth-int(bw1*3)
                logical2 = int(bw1/2) + (pixmap.height()/scaleFac) >= screenHeight-int(bw1/2)
            small_pixmap = pixmap.scaled(int(pixmap.width()/scaleFac), int(pixmap.height()/scaleFac))
            label.setPixmap(small_pixmap)
            label.move(int(bw1*2),i*height)
            label.resize(int(pixmap.width()/scaleFac),int(pixmap.height()/scaleFac))
            height = int(pixmap.height()/scaleFac)+int(bw1/2)
            width = int(pixmap.width()/scaleFac)
            self.vbox.addWidget(title, i, 1)
            i=i+1
            self.vbox.addWidget(label, i, 1)
            i=i+1
            self.sedImages.append(title)
            self.sedImages.append(label)
        mapName = os.path.join(siteFolder, siteName+'_MAP.jpg')
        label = QLabel()
        pixmap = QPixmap(mapName)
        scaleFac = 1
        logical1 = int(bw1*7) + (pixmap.width()/scaleFac) >= screenWidth-int(bw1*3)
        logical2 = int(bw1/2) + (pixmap.height()/scaleFac) >= screenHeight-int(bw1/2)
        while (logical1 or logical2):
            scaleFac = scaleFac + 1
            logical1 = int(bw1*7) + (pixmap.width()/scaleFac) >= screenWidth-int(bw1*3)
            logical2 = int(bw1/2) + (pixmap.height()/scaleFac) >= screenHeight-int(bw1/2)
        small_pixmap = pixmap.scaled(int(pixmap.width()/scaleFac), int(pixmap.height()/scaleFac))
        label.setPixmap(small_pixmap)
        label.move(int(bw1*2),i*height)
        label.resize(int(pixmap.width()/scaleFac),int(pixmap.height()/scaleFac))
        height = int(pixmap.height()/scaleFac)+int(bw1/2)
        width = int(pixmap.width()/scaleFac)
        self.vbox.addWidget(label, i+1, 1)
        self.sedImages.append(label)
        height=0
        j=0
        for im in glob.glob(siteFolder + '/*.png'):
            title = QLabel(os.path.splitext(os.path.basename(im))[0])
            label = QLabel()
            pixmap = QPixmap(im)
            scaleFac = 1
            logical1 = int(bw1*7) + (pixmap.width()/scaleFac) >= screenWidth-int(bw1*3)
            logical2 = int(bw1/2) + (pixmap.height()/scaleFac) >= screenHeight-int(bw1/2)
            while (logical1 or logical2):
                scaleFac = scaleFac + 1
                logical1 = int(bw1*7) + (pixmap.width()/scaleFac) >= screenWidth-int(bw1*3)
                logical2 = int(bw1/2) + (pixmap.height()/scaleFac) >= screenHeight-int(bw1/2)
            small_pixmap = pixmap.scaled(int(pixmap.width()/scaleFac), int(pixmap.height()/scaleFac))
            label.setPixmap(small_pixmap)
            label.move(int(bw1/4)+int(bw1*2)+width,j*height)
            label.resize(int(pixmap.width()/scaleFac),int(pixmap.height()/scaleFac))
            height = int(pixmap.height()/scaleFac)+int(bw1/2)
            self.vbox.addWidget(title, j, 2)
            j=j+1
            self.vbox.addWidget(label, j, 2)
            j=j+1
            self.grainImages.append(title)
            self.grainImages.append(label)
            

    def clearWindow(self):
        for thing in self.sedImages:
            thing.hide()
        for thing in self.grainImages:
            thing.hide()

    
    def home(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QGridLayout()             # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)
        self.grainImages = None
        self.sedImages = None
        


        ##button for mask or box
        siteSelector = QComboBox()
        self.vbox.addWidget(siteSelector, 0, 0)
        subfolders = [ f.path for f in os.scandir(augerLogs) if f.is_dir() ]
        
        
        for folder in subfolders:
            siteSelector.addItem(folder)
        siteSelector.resize(bw1*2,int(bw1/2))
        siteSelector.move(0, 0)

        goToSite = QPushButton("Go to Site")
        goToSite.resize(bw1*2, bw1)
        goToSite.move(0,bw1)

        self.vbox.addWidget(goToSite, 1, 0)

        clearButton = QPushButton("Clear")
        clearButton.resize(bw1*2, bw1)
        clearButton.move(0,bw1*2)

        self.vbox.addWidget(clearButton, 2, 0)

        goToSite.clicked.connect(lambda: self.plotSedandGrainSize(siteSelector.currentText()))
        clearButton.clicked.connect(lambda: self.clearWindow())


                #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
 


## Function outside of the class to run the app   
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

## Calling run to run the app
run()
