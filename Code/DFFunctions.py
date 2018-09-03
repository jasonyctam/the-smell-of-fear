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

    def getMovieDF(self, movieName, labelsDF, screening_DF, channel, gasDF, normalised=False):

        ## This function creates a dataframe that contains the values of the specified gas channel for all sessions of the specified movie

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