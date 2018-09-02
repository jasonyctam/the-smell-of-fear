# coding=utf-8
import time
import pandas as pd
import matplotlib.pyplot as plt
import DFFunctions as DFFuncs
import plotAnalysis as plotMethods
import datetime as dt

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

        # colNames = self.TOF_CO2_DF.columns

        ## Print All column Names
        # for i in range(0,len(colNames)):
        #     print(colNames[i])

        self.screening_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'screening_times.csv', timeCol=["scheduled", "begin"], timeFormat=["%d-%m-%Y %H:%M", "%d-%m-%Y %H:%M"])

        self.labels_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels.csv')
        self.labels_DF['scene_label'] = self.labels_DF[' label '] + self.labels_DF[' sub-label ']

        self.buddy_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Buddy.csv')
        self.hobbit_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Hobbit.csv')
        self.machete_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Machete.csv')
        self.mitty_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Mitty.csv')
        self.paranormal_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Paranormal.csv')
        self.tribute_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Tribute.csv')

        # Was going to use this, may be useful later
        nameDict =	{
            "Hobbit 2": self.hobbit_DF,
            "Buddy": self.buddy_DF,
            "Machete Kills": self.machete_DF,
            "Walter Mitty": self.mitty_DF,
            "Paranormal Activity": self.paranormal_DF,
            "The Hunger Games: Catching Fire": self.tribute_DF
        }

        # Was going to use this, may be useful later
        # movieLengthDict =	{
        #     "Hobbit 2" : 161,
        #     "Carrie" : 100,
        #     "Wolkig 2" : 95,
        #     "Suck Me Shakespeer" : 119,
        #     "Dinosaurier" : 88,
        #     "Walter Mitty" : 114,
        #     "Counselor" : 117,
        #     "Belle & Sebastian" : 104,
        #     "Bolshoi: Dornröschen" : 
        #     "Machete Kills" : 107,
        #     "Buddy" : 94,
        #     "The Hunger Games: Catching Fire" : 146,
        #     "Journey to the Christmas Star" : 80,
        #     "Medicus" : 150,
        #     "The Little Ghost" : 92,
        #     "Little Ghost" : 92,
        #     "The Starving Games" : 83,
        #     "Paranormal Activity" : 88,
        #     "Bele & Sebastian" : 104
        # }

        ballet_DF = self.screening_DF[self.screening_DF["movie"]=="Bolshoi: Dornröschen"]
        print(ballet_DF.head(10))

        hobbit_CO2DF = self.DFFunc.getMovieDF('Hobbit 2', self.hobbit_DF, self.screening_DF, 'CO2', self.TOF_CO2_DF)

        print(self.DFFunc.getChannelBackground('CO2', self.TOF_CO2_DF))

        # self.plotMovieGasData(hobbit_CO2DF, movie='Hobbit 2', channel='CO2', display=True)
        self.plotChannelBackground(display=True)
        # self.plotRawData(display=True)

        if self.displayGraph==True:
            plt.show()

        return

###################################################################
###################################################################

    def plotMovieGasData(self, movieGasDF, movie, channel, display=False):

        self.plotData.plotMovieGasGraph(movieGasDF, title=channel, xlabel="Time", ylabel=channel, outputFileName=movie+"_"+channel+".png", tilt=self.tiltBool, xTickRotation=self.rotation, dateFormat='%H:%M:%S')

        if display==True:
            self.displayGraph = True

        return

###################################################################
###################################################################

    def plotChannelBackground(self, display=False):

        backgroundDF = self.TOF_CO2_DF[(self.TOF_CO2_DF['Time']>=dt.datetime(2013,12,30)) & (self.TOF_CO2_DF['Time']<=dt.datetime(2014,1,7))]

        self.plotData.plotBackgroundGraph(backgroundDF, channel="CO2", title="CO2", xlabel="Time", ylabel="CO2", legendLabel1="CO2", outputFileName="bg_CO2.png", tilt=self.tiltBool, xTickRotation=self.rotation, dateFormat='%m-%d %H:%M:%S')

        if display==True:
            self.displayGraph = True

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