# coding=utf-8
# import matplotlib
# import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta, time, date

###################################################################
###################################################################
###################################################################
###################################################################

class DFFunctions():

###################################################################
###################################################################

    def __init__(self, bgStartDate, bgEndDate, bgStartHour, bgEndHour):
        
        self.backgroundStartDate = bgStartDate
        self.backgroundEndDate = bgEndDate
        self.backgroundStartHour = bgStartHour
        self.backgroundEndHour = bgEndHour

        return
        
###################################################################
###################################################################

    def getCSVDF(self, csv, skiprow=0, timeCol=[], timeFormat=[]):

        ## This function loads the csv files into dataframes, and converts the values in the respective time columns into datetime formats

        ## lists timeCol and timeFormat must have the same length

        outDF = pd.read_csv(csv, skiprows=skiprow)
        if len(timeCol) > 0:
            for i in range(0,len(timeCol)):

                ## Converts the string in specified column with time data to datetime object
                outDF[timeCol[i]] = pd.to_datetime(outDF[timeCol[i]],format=timeFormat[i])
        
        return outDF

###################################################################
###################################################################

    def getMovieDF(self, movieName, inLabelsDF, inScreening_DF, channel, inGasDF, normalised=False):

        ## This function creates a dataframe that contains the values of the specified gas channel for all sessions of the specified movie

        labelsDF = inLabelsDF.copy()
        screening_DF = inScreening_DF.copy()
        gasDF = inGasDF.copy()

        del inLabelsDF
        del inScreening_DF
        del inGasDF

        # Acquire the number of columns from the labels dataframe for determining the time length of the movie
        numColumns = labelsDF.shape[1]

        # Create time column of values from start of movie session
        sessionStart = time(hour=0, minute=0, second=0)
        sessionTime = [None]*numColumns

        for i in range(0, numColumns):
            sessionTime[i] = datetime.combine(datetime.now().date(),sessionStart) + i*timedelta(seconds=30)

        # Create output dataframe with time from start of each session
        outDF = pd.DataFrame({'sessionTime': pd.Series(sessionTime)})

        # Get data for the specified gas channel
        movieDF = screening_DF[screening_DF['movie'] == movieName]

        # Resets the index for joining data
        movieDF = movieDF.reset_index()

        # Get background count of channel
        if (normalised==True):
            background = self.getChannelBackground(channel, gasDF)
        else:
            background = 0
            attendence = 1.0

        # Loop throught the list of session starting times
        for i in range(0, movieDF.shape[0]):

            # Acquire start time of movie session
            start = movieDF['scheduled'][i]

            # Determine end time of the movie session by assuming each column is 30s
            end = start + numColumns*timedelta(seconds=30)

            # Get data from gas channel and reset index
            session = gasDF[(gasDF['Time']>=start) & (gasDF['Time']<=end)].reset_index()

            # Get atttendence
            if (normalised==True):
                attendence = (movieDF['filled %'][i]*movieDF['capacity'][i])/100.0

            # Only add to the output dataframe if the dataframe if not empty
            if session.shape[0] < 1:
                continue;
            elif (normalised==True):
                outDF[str(start)] = session[channel].apply(lambda x: (x-background)/attendence)
            else:
                outDF[str(start)] = session[channel]

        return outDF

###################################################################
###################################################################

    def getChannelBackground(self, channel, gasDF):

        ## This function extracts the background counts of specified gas channel from the time periods between sessions

        inDF = gasDF
        inDF['Hours'] = inDF['Time'].apply(lambda x: x.time())
        backgroundDF = inDF[(inDF['Time']>=self.backgroundStartDate) & (inDF['Time']<=self.backgroundEndDate) & (inDF['Hours']>=self.backgroundStartHour) & (inDF['Hours']<=self.backgroundEndHour)]
        
        return backgroundDF[channel].mean()

###################################################################
###################################################################

    def getMovieAvgDF(self, movieName, inLabelsDF, inScreening_DF, inGasDF):

        # labelsDF = inLabelsDF.copy()
        screening_DF = inScreening_DF.copy()
        gasDF = inGasDF.copy()

        # del inLabelsDF
        del inScreening_DF
        del inGasDF

        # self.getSessionLabels(inLabelsDF[1])

        # Create time column of values from start of movie session
        sessionStart = time(hour=0, minute=0, second=0)

        colNames = list(gasDF.columns)

        for i in range(0,len(movieName)):

            labelsDF = inLabelsDF[i].copy()

            labelsDF_T = self.getSessionLabels(inLabelsDF[i])

            # Acquire the number of columns from the labels dataframe for determining the time length of the movie
            numColumns = labelsDF.shape[1]

            # Create time column of values from start of movie session
            # sessionStart = time(hour=0, minute=0, second=0)
            sessionTime = [None]*numColumns

            for k in range(0, numColumns):
                sessionTime[k] = datetime.combine(datetime.now().date(),sessionStart) + k*timedelta(seconds=30)

            singleMovieDF = pd.DataFrame({'sessionTime': pd.Series(sessionTime), 'Movie':movieName[i]})
            print(movieName[i])
            for j in range(1,10):
            # for j in range(1,len(colNames)):
                channelName = colNames[j]
                print(channelName)
            
                movieDF = self.getMovieDF(movieName=movieName[i], inLabelsDF=labelsDF, inScreening_DF=screening_DF, channel=channelName, inGasDF=gasDF, normalised=True)
                numSessions = movieDF.shape[1]-1
                movieDF['Average'] = movieDF.apply(self.sumRowWithNan, axis=1)/(numSessions)

                singleMovieDF[channelName] = movieDF['Average']
                del movieDF

            del labelsDF

            singleMovieDF['labels'] = labelsDF_T['labels']
            singleMovieDF['label_Names'] = labelsDF_T['label_Names']

            del labelsDF_T

            if i==0:
                outDF = singleMovieDF
            else:
                outDF = outDF.append(singleMovieDF, ignore_index=True)

            del singleMovieDF

        return outDF

###################################################################
###################################################################

    def getSessionLabels(self, inLabelsDF):

        labelsDF = inLabelsDF.copy()

        del inLabelsDF

        labelsDF_transposed = labelsDF.T # or df1.transpose()

        columnNames = list(labelsDF_transposed.columns)

        del labelsDF

        labelsDF_transposed['vec'] = labelsDF_transposed.apply(self.getListFromRow, axis=1)
        labelsDF_transposed['label_Names'] = labelsDF_transposed['vec'].apply(lambda x: self.getLabelListFromRow(x, columnNames))

        labelsDF_transposed = labelsDF_transposed.reset_index()

        outDF = pd.DataFrame({'labels':labelsDF_transposed['vec'], 'label_Names':labelsDF_transposed['label_Names']})

        del labelsDF_transposed

        return outDF

###################################################################
###################################################################

    def getLabelListFromRow(self, vec, colNames):

        out_vec = []

        for i in range(0, len(vec)):
            if vec[i]==1:
                out_vec.append(str(colNames[i]).strip())

        if len(out_vec)<1:
            out_vec.append('Not labelled')

        return out_vec

###################################################################
###################################################################

    def getListFromRow(self, row):

        row_matrix = row.values

        vec = []

        for i in range(0,len(row_matrix)):
            vec.append(row_matrix[i])

        del row_matrix

        return vec

###################################################################
###################################################################

    def getInputDF(self, inLabelsDF, inScreening_DF, inGasDF, normalised=False):

        labelsDF = inLabelsDF.copy()
        screening_DF = inScreening_DF.copy()
        gasDF = inGasDF.copy()

        del inLabelsDF
        del inScreening_DF
        del inGasDF

        gasDF['Total'] = gasDF.apply(self.sumRowWithNan, axis=1)

        print(gasDF.head(2))

        return

###################################################################
###################################################################

    def getMovieLabels(self, labels, originalMovieDF):

        movieDF = originalMovieDF.copy()
        movieDF['labels'] = labels['scene_label']
        movieDF = movieDF.set_index('labels')

        return movieDF

###################################################################
###################################################################

    def sumRowWithNan(self, row):

        row_matrix = row.values

        sum = 0

        for i in range(0, len(row_matrix)):
            if isinstance(row_matrix[i], float) and math.isnan(row_matrix[i])==False:
                sum = sum + row_matrix[i]

        return sum

###################################################################
###################################################################