# coding=utf-8
# import matplotlib
# import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta, time, date
import progressbar

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

    def getMovieDF(self, movieName, inLabelsDF, inScreening_DF, inGasDF, channel="", normalised=False, trimmed=False):

        ## This function creates a dataframe that contains the values of the specified gas channel for all sessions of the specified movie

        labelsDF = inLabelsDF.copy()
        screening_DF = inScreening_DF.copy()
        gasDF = inGasDF.copy()

        del inLabelsDF
        del inScreening_DF
        del inGasDF

        # Acquire the number of columns from the labels dataframe for determining the time length of the movie
        numColumns = labelsDF.shape[1]
        num30SecBlocks = numColumns+90

        # Create time column of values from start of movie session
        sessionStart = time(hour=0, minute=0, second=0)
        sessionTime = [None]*num30SecBlocks

        for i in range(0, num30SecBlocks):
            sessionTime[i] = datetime.combine(datetime.now().date(),sessionStart) + i*timedelta(seconds=30)

        # Create output dataframe with time from start of each session
        outDF = pd.DataFrame({'sessionTime': pd.Series(sessionTime)})

        # Get data for the specified gas channel
        movieDF = screening_DF[screening_DF['movie'] == movieName]

        movieDF = self.getCleanMovieSessions(inDF=movieDF, movieName=movieName)

        # Resets the index for joining data
        movieDF = movieDF.reset_index()

        if len(channel)<1:

            channels = list(gasDF.columns)

            background = [None] * len(channels)

            labelsDF_T = self.getSessionLabels(labelsDF)

            for j in range(1,len(channels)):
                
                # Get background count of channel
                if (normalised==True):
                    background[j] = self.getChannelBackground(channels[j], gasDF)
                else:
                    background[j] = 0
                    
            widgets=[
                ' [', progressbar.Timer(), '] ',
                progressbar.Bar(),
                ' (', progressbar.ETA(), ') ',
            ]

            bar = progressbar.ProgressBar(widgets=widgets)

            # Loop throught the list of session starting times
            for i in bar(range(0, movieDF.shape[0])):

                # Acquire start time of movie session
                start = movieDF['begin'][i]

                # Acquire start time of movie session
                scheduled = movieDF['scheduled'][i]

                # Determine end time of the movie session by assuming each column is 30s
                if trimmed==True:
                    end = start + numColumns*timedelta(seconds=30)
                else:
                    end = scheduled + num30SecBlocks*timedelta(seconds=30)

                # Get data from gas channel and reset index
                session = gasDF[(gasDF['Time']>=start) & (gasDF['Time']<=end)].reset_index()

                sessionDF = pd.DataFrame({'sessionTime': pd.Series(sessionTime), 'Movie': movieName})
                session_normedDF = pd.DataFrame({'sessionTime': pd.Series(sessionTime), 'Movie': movieName})
                session_normedDF['sessionStart'] = start

                # Get atttendence
                if (normalised==True):
                    attendence = (movieDF['filled %'][i]*movieDF['capacity'][i])/100.0
                else:
                    attendence = 1.0

                # Only add to the output dataframe if the dataframe if not empty
                if session.shape[0] < 1:
                    continue;
                elif (normalised==True):
                    for j in range(1,len(channels)):
                        sessionDF[channels[j]] = session[channels[j]].apply(lambda x: (x-background[j])/attendence)
                else:
                    for j in range(1,len(channels)):
                        sessionDF[channels[j]] = session[channels[j]]

                for j in range(1,len(channels)):
                    total = sessionDF[channels[j]].sum()
                    session_normedDF[channels[j]] = sessionDF[channels[j]]/total

                session_normedDF['labels'] = labelsDF_T['labels']
                session_normedDF['label_Names'] = labelsDF_T['label_Names']

                if i==0:
                    outDF = session_normedDF
                else:
                    outDF = outDF.append(session_normedDF, ignore_index=True)

                del session_normedDF
            
        else:

            # Get background count of channel
            if (normalised==True):
                background = self.getChannelBackground(channel, gasDF)
            else:
                background = 0
                attendence = 1.0

            # Loop throught the list of session starting times
            for i in range(0, movieDF.shape[0]):

                # Acquire start time of movie session
                start = movieDF['begin'][i]

                # Acquire start time of movie session
                scheduled = movieDF['scheduled'][i]

                # Determine end time of the movie session by assuming each column is 30s
                if trimmed==True:
                    end = start + numColumns*timedelta(seconds=30)
                else:
                    end = scheduled + num30SecBlocks*timedelta(seconds=30)

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

    def getCleanMovieSessions(self, inDF, movieName):

        cleanedDF = inDF.copy()

        del inDF

        # Remove problematic sessions
        tributeSessions = [datetime.strptime('2013-12-30 13:15', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-06 13:50:00', '%Y-%m-%d %H:%M:%S'),
            datetime.strptime('2014-01-08 13:45:00', '%Y-%m-%d %H:%M:%S')]

        if movieName == 'The Hunger Games: Catching Fire':
            cleanedDF = cleanedDF[~cleanedDF['begin'].isin(tributeSessions)]

        buddySessions = [
            datetime.strptime('2013-12-25 12:10', '%Y-%m-%d %H:%M'),
            datetime.strptime('2013-12-25 23:10', '%Y-%m-%d %H:%M'),
            datetime.strptime('2013-12-26 22:25', '%Y-%m-%d %H:%M'),
            datetime.strptime('2013-12-27 22:25', '%Y-%m-%d %H:%M'),
            datetime.strptime('2013-12-29 22:25', '%Y-%m-%d %H:%M'),
            datetime.strptime('2013-12-30 22:25', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-01 22:25', '%Y-%m-%d %H:%M')
            ]

        if movieName == 'Buddy':
            cleanedDF = cleanedDF[~cleanedDF['begin'].isin(buddySessions)]

        walterMittySessions = [
            datetime.strptime('2013-12-19 20:00', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-02 23:15', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-03 23:15', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-04 20:15', '%Y-%m-%d %H:%M'), # This is a weird session
            datetime.strptime('2014-01-04 23:15', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-05 23:15', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-06 23:15', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-07 23:15', '%Y-%m-%d %H:%M'),
            datetime.strptime('2014-01-08 23:15', '%Y-%m-%d %H:%M')
            ]

        if movieName == 'Walter Mitty':
            cleanedDF = cleanedDF[~cleanedDF['begin'].isin(walterMittySessions)]

        # Apply time shift correction

        buddyCorrections_dict = {
            datetime.strptime('2013-12-25 14:50', '%Y-%m-%d %H:%M'):40,
            datetime.strptime('2013-12-25 17:35', '%Y-%m-%d %H:%M'):42,
            datetime.strptime('2013-12-25 20:20', '%Y-%m-%d %H:%M'):40,
            datetime.strptime('2013-12-26 19:30', '%Y-%m-%d %H:%M'):68,
            datetime.strptime('2013-12-27 19:30', '%Y-%m-%d %H:%M'):70,
            datetime.strptime('2013-12-28 22:25', '%Y-%m-%d %H:%M'):10,
            datetime.strptime('2013-12-28 19:30', '%Y-%m-%d %H:%M'):72,
            datetime.strptime('2013-12-29 19:30', '%Y-%m-%d %H:%M'):68,
            datetime.strptime('2013-12-30 19:30', '%Y-%m-%d %H:%M'):68,
            datetime.strptime('2014-01-01 19:30', '%Y-%m-%d %H:%M'):67
        }

        if movieName == 'Buddy':
            cleanedDF = self.getSyncMovieDF(inDF=cleanedDF, delayDict=buddyCorrections_dict)

        tributeCorrections_dict = {
            datetime.strptime('2013-12-26 13:15', '%Y-%m-%d %H:%M'):52,
            datetime.strptime('2013-12-27 13:15', '%Y-%m-%d %H:%M'):57,
            datetime.strptime('2013-12-28 13:15', '%Y-%m-%d %H:%M'):55,
            datetime.strptime('2013-12-29 13:15', '%Y-%m-%d %H:%M'):58,
            datetime.strptime('2013-12-31 13:15', '%Y-%m-%d %H:%M'):54,
            datetime.strptime('2014-01-02 13:45', '%Y-%m-%d %H:%M'):44,
            datetime.strptime('2014-01-03 13:45', '%Y-%m-%d %H:%M'):42,
            datetime.strptime('2014-01-04 13:45', '%Y-%m-%d %H:%M'):44,
            datetime.strptime('2014-01-05 13:45', '%Y-%m-%d %H:%M'):40,
            datetime.strptime('2014-01-07 13:45', '%Y-%m-%d %H:%M'):12
        }

        if movieName == 'The Hunger Games: Catching Fire':
            cleanedDF = self.getSyncMovieDF(inDF=cleanedDF, delayDict=tributeCorrections_dict)

        walterMittyCorrections_dict = {
            datetime.strptime('2014-01-01 16:25', '%Y-%m-%d %H:%M'):47,
            datetime.strptime('2014-01-02 17:15', '%Y-%m-%d %H:%M'):35,
            datetime.strptime('2014-01-02 20:15', '%Y-%m-%d %H:%M'):39,
            datetime.strptime('2014-01-03 17:15', '%Y-%m-%d %H:%M'):36,
            datetime.strptime('2014-01-03 20:15', '%Y-%m-%d %H:%M'):39,
            datetime.strptime('2014-01-04 17:15', '%Y-%m-%d %H:%M'):34,
            datetime.strptime('2014-01-05 17:15', '%Y-%m-%d %H:%M'):34,
            datetime.strptime('2014-01-05 20:15', '%Y-%m-%d %H:%M'):39,
            datetime.strptime('2014-01-06 17:15', '%Y-%m-%d %H:%M'):35,
            datetime.strptime('2014-01-06 20:15', '%Y-%m-%d %H:%M'):39,
            datetime.strptime('2014-01-07 17:15', '%Y-%m-%d %H:%M'):37,
            datetime.strptime('2014-01-07 20:15', '%Y-%m-%d %H:%M'):41,
            datetime.strptime('2014-01-08 17:15', '%Y-%m-%d %H:%M'):37,
            datetime.strptime('2014-01-08 20:15', '%Y-%m-%d %H:%M'):37
        }

        if movieName == 'Walter Mitty':
            cleanedDF = self.getSyncMovieDF(inDF=cleanedDF, delayDict=walterMittyCorrections_dict)

        macheteKillsCorrections_dict = {
            datetime.strptime('2013-12-23 19:35', '%Y-%m-%d %H:%M'):65
        }

        if movieName == 'Machete Kills':
            cleanedDF = self.getSyncMovieDF(inDF=cleanedDF, delayDict=macheteKillsCorrections_dict)

        return cleanedDF

###################################################################
###################################################################

    def getSyncMovieDF(self, inDF, delayDict):

        outDF = inDF.copy()

        del inDF

        allDates = list(delayDict.keys())
        for i in range(0, len(allDates)):
            index = int(outDF[outDF['begin']==allDates[i]].index[0])
            delay = delayDict[allDates[i]]
            adjusted = outDF.at[index, 'begin']+delay*timedelta(seconds=30)
            outDF.at[index, 'begin'] = adjusted

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

        widgets=[
            ' [', progressbar.Timer(), '] ',
            progressbar.Bar(),
            ' (', progressbar.ETA(), ') ',
        ]

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

            bar = progressbar.ProgressBar(widgets=widgets)

            for j in bar(range(1,20)):
            # for j in bar(range(1,len(colNames))):
                channelName = colNames[j]
                # print(movieName[i] + ': ' + channelName + ' (' + str(j) + '/' + str(len(colNames)) + '), Movie (' + str(i) + '/' + str(len(movieName)) + ')')
            
                movieDF = self.getMovieDF(movieName=movieName[i], inLabelsDF=labelsDF, inScreening_DF=screening_DF, channel=channelName, inGasDF=gasDF, normalised=True, trimmed=True)
                # numSessions = movieDF.shape[1]-1
                movieDF['sum'] = movieDF.apply(self.sumRowWithNan, axis=1)
                movieDF['nonNaN'] = movieDF.apply(self.getRowNonNaNNum, axis=1)
                movieDF['Average'] = movieDF['sum']/movieDF['nonNaN']

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

    def getRowNonNaNNum(self, row):

        row_matrix = row.values

        num = 0

        for i in range(0, len(row_matrix)):
            if isinstance(row_matrix[i], float) and math.isnan(row_matrix[i])==False:
                num = num + 1

        return num

###################################################################
###################################################################