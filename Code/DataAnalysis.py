# coding=utf-8
import time
import pandas as pd
import matplotlib.pyplot as plt
import DFFunctions as DFFuncs
import plotAnalysis as plotMethods
import datetime as dt
import seaborn as sns

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

        self.backgroundStartDate = dt.datetime(2013,12,30)
        self.backgroundEndDate = dt.datetime(2014,1,7)

        self.backgroundStartHour = dt.time(4, 0)
        self.backgroundEndHour = dt.time(9, 0)

        self.plotData = plotMethods.plotAnalysis(plotsDir=self.plotsDir, bgStartHour=self.backgroundStartHour, bgEndHour=self.backgroundEndHour)
        self.DFFunc = DFFuncs.DFFunctions(bgStartDate=self.backgroundStartDate, bgEndDate=self.backgroundEndDate, bgStartHour=self.backgroundStartHour, bgEndHour=self.backgroundEndHour)

        self.TOF_CO2_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'TOF_CO2_data_30sec.csv', timeCol=["Time"], timeFormat=["'%m/%d/%Y %H:%M:%S'"])
        self.screening_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'screening_times.csv', timeCol=["scheduled", "begin"], timeFormat=["%d-%m-%Y %H:%M", "%d-%m-%Y %H:%M"])

        self.labels_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels.csv')
        self.buddy_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Buddy.csv')
        self.hobbit_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Hobbit.csv')
        self.machete_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Machete.csv')
        self.mitty_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Mitty.csv')
        self.paranormal_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Paranormal.csv')
        self.tribute_DF = self.DFFunc.getCSVDF(csv=self.dataDir+'labels/Tribute.csv')

        return

###################################################################
###################################################################
    
    def runAnalysis(self):

        self.displayGraph = False

        # colNames = TOF_CO2_DF.columns

        ## Print All column Names
        # for i in range(0,len(colNames)):
        #     print(colNames[i])

        allMovieNames = [
            "Hobbit 2",
            "Buddy",
            "Machete Kills",
            "Walter Mitty",
            "Paranormal Activity",
            "The Hunger Games: Catching Fire"]

        self.labels_DF['scene_label'] = self.labels_DF[' label '] + self.labels_DF[' sub-label ']

        # print(self.labels_DF)

        # for i in range(0,len(allMovieNames)):
        #     print(self.screening_DF[self.screening_DF['movie']==allMovieNames[i]])

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

        # ballet_DF = self.screening_DF[self.screening_DF["movie"]=="Bolshoi: Dornröschen"]
        # print(ballet_DF.head(10))

        # print(self.hobbit_DF.head(10))
        # print(self.hobbit_DF.tail(10))
        # print(self.hobbit_DF.shape)
        # print(self.buddy_DF.shape)
        # print(self.machete_DF.shape)
        # print(self.mitty_DF.shape)
        # print(self.paranormal_DF.shape)
        # print(self.tribute_DF.shape)
        # print(self.labels_DF)
        # print(self.labels_DF.shape)
        labels = self.labels_DF.drop(self.labels_DF.index[-2]).copy()
        # print(labels.shape)

        hobbit_DF = self.DFFunc.getMovieLabels(labels, self.hobbit_DF)
        buddy_DF = self.DFFunc.getMovieLabels(labels, self.buddy_DF)
        machete_DF = self.DFFunc.getMovieLabels(labels, self.machete_DF)
        mitty_DF = self.DFFunc.getMovieLabels(labels, self.mitty_DF)
        paranormal_DF = self.DFFunc.getMovieLabels(labels, self.paranormal_DF)
        tribute_DF = self.DFFunc.getMovieLabels(labels, self.tribute_DF)

        allLabelsDF = [
            hobbit_DF,
            buddy_DF,
            machete_DF,
            mitty_DF,
            paranormal_DF,
            tribute_DF]

        # hobbit_DF = self.hobbit_DF.copy()
        # hobbit_DF['labels'] = labels['scene_label']
        # hobbit_DF = hobbit_DF.set_index('labels')
        # print(hobbitDF.head(10))

        # self.DFFunc.getInputDF(inLabelsDF=hobbit_DF, inScreening_DF=self.screening_DF, inGasDF=self.TOF_CO2_DF)

        goodMovieNames = [
            # "Hobbit 2",
            "Buddy",
            # "Machete Kills",
            "Walter Mitty",
            # "Paranormal Activity",
            "The Hunger Games: Catching Fire"]

        goodLabelsDF = [
            # hobbit_DF,
            buddy_DF,
            # machete_DF,
            mitty_DF,
            # paranormal_DF,
            tribute_DF]

        self.getMovieAnalysisDF(goodMovieNames, goodLabelsDF)

        # movieAvgDF = self.DFFunc.getMovieAvgDF(movieName=goodMovieNames, inLabelsDF=allLabelsDF, inScreening_DF=self.screening_DF, inGasDF=self.TOF_CO2_DF)
        # movieAvgDF.to_csv('../movieAvgDF.csv', sep=';', encoding='utf-8')

        # print(movieAvgDF.head(5))
        # print(movieAvgDF.tail(5))
        
        # hobbit_Avg_DF = movieAvgDF[movieAvgDF['Movie']=='Hobbit 2']

        # print(hobbit_CO2DF_norm.head(5))
        # print(hobbit_Avg_DF.head(5))

        # Print label map
        # ax = sns.heatmap(hobbit_DF, linewidths=0.1, alpha=0.5, interpolation="nearest", cmap='Blues')#), annot=False)#, cbar=True)
        # plt.imshow(hobbit_DF,interpolation="nearest", cmap='Blues')
        # plt.show()

        # print(hobbit_CO2DF_norm.head(10))


        # self.plotMovieGasData(hobbit_Avg_DF, movie='Hobbit 2_Avg', channel='CO2', display=True, normalised=True, average=True)

        # self.plotChannelBackground(display=True)
        # self.plotRawData(display=True)

        self.plotSessionsData(displayGraph=False)

        if self.displayGraph==True:
            plt.show()

        return

###################################################################
###################################################################

    def getMovieAnalysisDF(self, movieNames, labelsDF):

        print(movieNames[0])
        outDF = self.DFFunc.getMovieDF(movieName=movieNames[0], inLabelsDF=labelsDF[0], inScreening_DF=self.screening_DF, inGasDF=self.TOF_CO2_DF)

        print(outDF.head())

        for i in range(1,len(movieNames)):
            print(movieNames[i])

            movieDF = self.DFFunc.getMovieDF(movieName=movieNames[i], inLabelsDF=labelsDF[i], inScreening_DF=self.screening_DF, inGasDF=self.TOF_CO2_DF)

            outDF = outDF.append(movieDF, ignore_index=True)

            del movieDF

        outDF.to_csv('../movieAvgDF.csv', sep=';', encoding='utf-8')

        print(outDF.shape)
        print(outDF[outDF['sessionTime']==dt.datetime.combine(dt.datetime.now().date(),dt.time(hour=0, minute=0, second=0))])
        print(outDF.loc[237:238])

        return

###################################################################
###################################################################

    def plotSessionsData(self, displayGraph=True):

        # Dataframe with each column as the gas channel data for each session of the specified movie and gas channel
        hobbit_CO2DF = self.DFFunc.getMovieDF(movieName='Hobbit 2', inLabelsDF=self.hobbit_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF)
        buddy_CO2DF = self.DFFunc.getMovieDF(movieName='Buddy', inLabelsDF=self.buddy_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF)
        machete_CO2DF = self.DFFunc.getMovieDF(movieName='Machete Kills', inLabelsDF=self.machete_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF)
        mitty_CO2DF = self.DFFunc.getMovieDF(movieName='Walter Mitty', inLabelsDF=self.mitty_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF)
        paranormal_CO2DF = self.DFFunc.getMovieDF(movieName='Paranormal Activity', inLabelsDF=self.paranormal_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF)
        tribute_CO2DF = self.DFFunc.getMovieDF(movieName='The Hunger Games: Catching Fire', inLabelsDF=self.tribute_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF)

        # Normalised for each session ((value-background)/attendence)
        hobbit_CO2DF_norm = self.DFFunc.getMovieDF(movieName='Hobbit 2', inLabelsDF=self.hobbit_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF, normalised=True)
        buddy_CO2DF_norm = self.DFFunc.getMovieDF(movieName='Buddy', inLabelsDF=self.buddy_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF, normalised=True)
        machete_CO2DF_norm = self.DFFunc.getMovieDF(movieName='Machete Kills', inLabelsDF=self.machete_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF, normalised=True)
        mitty_CO2DF_norm = self.DFFunc.getMovieDF(movieName='Walter Mitty', inLabelsDF=self.mitty_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF, normalised=True)
        paranormal_CO2DF_norm = self.DFFunc.getMovieDF(movieName='Paranormal Activity', inLabelsDF=self.paranormal_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF, normalised=True)
        tribute_CO2DF_norm = self.DFFunc.getMovieDF(movieName='The Hunger Games: Catching Fire', inLabelsDF=self.tribute_DF, inScreening_DF=self.screening_DF, channel='CO2', inGasDF=self.TOF_CO2_DF, normalised=True)

        # self.plotMovieGasData(hobbit_CO2DF, movie='Hobbit 2', channel='CO2', columns=self.hobbit_DF.shape[1], display=displayGraph)
        # self.plotMovieGasData(buddy_CO2DF, movie='Buddy', channel='CO2', columns=self.buddy_DF.shape[1], display=displayGraph)
        # self.plotMovieGasData(machete_CO2DF, movie='Machete Kills', channel='CO2', columns=self.machete_DF.shape[1], display=displayGraph)
        # self.plotMovieGasData(mitty_CO2DF, movie='Walter Mitty', channel='CO2', columns=self.mitty_DF.shape[1], display=displayGraph)
        # self.plotMovieGasData(paranormal_CO2DF, movie='Paranormal Activity', channel='CO2', columns=self.paranormal_DF.shape[1], display=displayGraph)
        # self.plotMovieGasData(tribute_CO2DF, movie='The Hunger Games: Catching Fire', channel='CO2', columns=self.tribute_DF.shape[1], display=displayGraph)

        # self.plotMovieGasData(hobbit_CO2DF_norm, movie='Hobbit 2', channel='CO2', columns=self.hobbit_DF.shape[1], display=displayGraph, normalised=True)
        # self.plotMovieGasData(buddy_CO2DF_norm, movie='Buddy', channel='CO2', columns=self.buddy_DF.shape[1], display=displayGraph, normalised=True)
        # self.plotMovieGasData(machete_CO2DF_norm, movie='Machete Kills', channel='CO2', columns=self.machete_DF.shape[1], display=displayGraph, normalised=True)
        # self.plotMovieGasData(mitty_CO2DF_norm, movie='Walter Mitty', channel='CO2', columns=self.mitty_DF.shape[1], display=displayGraph, normalised=True)
        # self.plotMovieGasData(paranormal_CO2DF_norm, movie='Paranormal Activity', channel='CO2', columns=self.paranormal_DF.shape[1], display=displayGraph, normalised=True)
        # self.plotMovieGasData(tribute_CO2DF_norm, movie='The Hunger Games: Catching Fire', channel='CO2', columns=self.tribute_DF.shape[1], display=displayGraph, normalised=True)

        return

###################################################################
###################################################################

    def plotMovieGasData(self, movieGasDF, movie, channel, columns=0, display=False, normalised=False, average=False):

        if normalised==True:
            title = movie+"_"+channel+"_normed"
        else:
            title = movie+"_"+channel

        outputFilename = title+".png"

        if average==True:
            self.plotData.plotMovieGasGraph(movieGasDF, title=title, xlabel="Time", ylabel=channel, channel=channel, outputFileName=outputFilename, tilt=self.tiltBool, xTickRotation=self.rotation, dateFormat='%H:%M:%S')
        else:
            self.plotData.plotMovieSessionGasGraph(movieGasDF, title=title, xlabel="Time", ylabel=channel, numColumns=columns, outputFileName=outputFilename, tilt=self.tiltBool, xTickRotation=self.rotation, dateFormat='%H:%M:%S')

        if display==True:
            self.displayGraph = True

        return

###################################################################
###################################################################

    def plotChannelBackground(self, display=False):

        backgroundDF = self.TOF_CO2_DF[(self.TOF_CO2_DF['Time']>=self.backgroundStartDate) & (self.TOF_CO2_DF['Time']<=self.backgroundEndDate)]

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