# coding=utf-8
import time
import pandas as pd
import matplotlib.pyplot as plt
import DFFunctions as DFFuncs
import plotAnalysis as plotMethods

###################################################################
###################################################################
###################################################################
###################################################################

class DataAnalysis():

###################################################################
###################################################################

    def __init__(self, dataDir, plotsDir):

        self.dataDir = dataDir
        self.plotsDir = plotsDir

        self.figWidth = 15
        self.figHeight = 8
        self.linewidth = 2

        self.tiltBool = True
        self.rotation = 30

        self.plotData = plotMethods.plotAnalysis(self.plotsDir)
        self.DFFunc = DFFuncs.DFFunctions()

        return

###################################################################
###################################################################
    
    def runAnalysis(self):

        self.displayGraph = False

        self.TOF_CO2_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'TOF_CO2_data_30sec.csv', timeCol=["Time"], timeFormat=["'%m/%d/%Y %H:%M:%S'"])

        print(self.TOF_CO2_DF.head())
        print(self.TOF_CO2_DF['Time'].dtype)

        colNames = self.TOF_CO2_DF.columns

        ## Print All column Names
        # for i in range(0,len(colNames)):
        #     print(colNames[i])

        self.screening_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'screening_times.csv', timeCol=["scheduled", "begin"], timeFormat=["%d-%m-%Y %H:%M", "%d-%m-%Y %H:%M"])
        print(self.screening_DF.head())

        self.labels_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels.csv')
        print(self.labels_DF.head())

        self.buddy_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Buddy.csv')
        self.hobbit_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Hobbit.csv')
        self.machete_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Machete.csv')
        self.mitty_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Mitty.csv')
        self.paranormal_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Paranormal.csv')
        self.tribute_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Tribute.csv')

        self.plotRawData(display=True)

        if self.displayGraph==True:
            plt.show()

        return

###################################################################
###################################################################

    def plotRawData(self, display=False):

        self.plotData.plotGraph(self.TOF_CO2_DF['Time'], self.TOF_CO2_DF['CO2'], title="CO2", xlabel="Time", ylabel="CO2", legendLabel1="CO2", outputFileName="CO2.png", tilt=self.tiltBool, xTickRotation=self.rotation, dateFormat='%Y-%m-%d')

        if display==True:
            self.displayGraph = True

        return

###################################################################
###################################################################

if __name__ == "__main__":

    startTime = time.time()
    
    dataDir = '../Data/'
    plotsDir = '../Plots/'
        
    Analysis_Object = DataAnalysis(dataDir, plotsDir)
    
    Analysis_Object.runAnalysis()
    
    endTime = time.time()
    
    print ("Time elapsed: " + repr(endTime-startTime))