# coding=utf-8

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import time, timedelta

###################################################################
###################################################################
###################################################################
###################################################################

class plotAnalysis():

###################################################################
###################################################################

    def __init__(self, bgStartHour, bgEndHour, plotsDir=""):

        sns.set_style("darkgrid")
        colors = ["windows blue", "amber", "greenish", "orange", "sky blue", "greyish", "salmon", "faded green", "lavender", "denim blue", "medium green"]
        # colors = ["windows blue", "aquamarine", "amber", "lightblue", "lavender"]
        custom_palette = sns.xkcd_palette(colors)
        sns.set_palette(custom_palette)
        self.outDir = plotsDir
        
        self.figWidth = 15
        self.figHeight = 8
        self.linewidth = 2

        self.backgroundStartHour = bgStartHour
        self.backgroundEndHour = bgEndHour
        
        return
        
###################################################################
###################################################################

    def plotMovieSessionGasGraph(self, inDF, title="", xlabel="", ylabel="", numColumns=0, outputFileName="", xLabelSize=25, tilt=False, xTickRotation=0, dateFormat='%H:%M:%S'):
        
        fig, ax = plt.subplots(figsize=(self.figWidth, self.figHeight))
            
        hfmt = matplotlib.dates.DateFormatter(dateFormat)
        ax.xaxis.set_major_formatter(hfmt)
        
        ax.set_title(title, fontsize=xLabelSize)
        ax.set_xlabel(xlabel, fontsize=xLabelSize)
        ax.set_ylabel(ylabel, fontsize=xLabelSize)
        
        columns = list(inDF)

        inDF[columns[0]] = pd.to_datetime(inDF[columns[0]])

        top_lim = 0

        for i in range(1, len(columns)):
            ax.plot(inDF[columns[0]],inDF[columns[i]], label=columns[i], lw=self.linewidth)
            if inDF[columns[i]].max() > top_lim:
                top_lim = inDF[columns[i]].max()

        ax.legend(loc='upper left', prop={'size': xLabelSize-14}, shadow=True, frameon=True)
        ax.tick_params(axis='both', which='major', labelsize=xLabelSize)
        ax.set_ylim(bottom = 0, top=top_lim*1.5)

        sessionEndTime = inDF[columns[0]].min() + numColumns*timedelta(seconds=30)

        # print('inDF[columns[0]]: ' + str(inDF[columns[0]].min()))
        # print('sessionEndTime: ' + str(sessionEndTime))

        ax.fill_betweenx(ax.get_ylim(), inDF[columns[0]].min(), sessionEndTime, alpha=.1, zorder=-1)

        if tilt:
            fig.autofmt_xdate(rotation=xTickRotation)
            
        if len(outputFileName) > 0:
            plt.savefig(self.outDir+outputFileName)

        return

###################################################################
###################################################################

    def plotMovieGasGraph(self, inDF, title="", xlabel="", ylabel="", outputFileName="", channel="", xLabelSize=25, tilt=False, xTickRotation=0, dateFormat='%H:%M:%S'):
        
        inDF = inDF.dropna()

        print(inDF.tail(10))

        fig, ax = plt.subplots(figsize=(self.figWidth, self.figHeight))
            
        hfmt = matplotlib.dates.DateFormatter(dateFormat)
        ax.xaxis.set_major_formatter(hfmt)
        
        ax.set_title(title, fontsize=xLabelSize)
        ax.set_xlabel(xlabel, fontsize=xLabelSize)
        ax.set_ylabel(ylabel, fontsize=xLabelSize)
        
        columns = list(inDF)

        inDF[columns[0]] = pd.to_datetime(inDF[columns[0]])

        ax.plot(inDF[columns[0]],inDF[channel], label=channel, lw=self.linewidth)

        top_lim = inDF[channel].max()

        ax.legend(loc='upper left', prop={'size': xLabelSize-10}, shadow=True, frameon=True)
        ax.tick_params(axis='both', which='major', labelsize=xLabelSize)
        ax.set_ylim(bottom = 0, top=top_lim*1.3)

        if tilt:
            fig.autofmt_xdate(rotation=xTickRotation)
            
        if len(outputFileName) > 0:
            plt.savefig(self.outDir+outputFileName)

        return

###################################################################
###################################################################

    def plotBackgroundGraph(self, bgDF, channel, title="", xlabel="", ylabel="", legendLabel1="", outputFileName="", xLabelSize=25, tilt=False, xTickRotation=0, dateFormat='%Y-%m'):
        
        fig, ax = plt.subplots(figsize=(self.figWidth, self.figHeight))
            
        hfmt = matplotlib.dates.DateFormatter(dateFormat)
        ax.xaxis.set_major_formatter(hfmt)
        
        ax.set_title(title, fontsize=xLabelSize)
        ax.set_xlabel(xlabel, fontsize=xLabelSize)
        ax.set_ylabel(ylabel, fontsize=xLabelSize)
        
        x1 = bgDF['Time']
        y1 = bgDF[channel]

        ax.plot(x1,y1, label=legendLabel1, lw=self.linewidth)

        inDF = bgDF.copy()

        inDF['Hours'] = inDF['Time'].apply(lambda x: x.time())
        backgroundDF = inDF[(inDF['Hours']>=self.backgroundStartHour) & (inDF['Hours']<=self.backgroundEndHour)]

        ax.plot(backgroundDF['Time'],backgroundDF[channel], label="Background", color='red', marker='*', ls='None')
        ax.legend(loc='upper left', prop={'size': xLabelSize-10}, shadow=True, frameon=True)
        ax.tick_params(axis='both', which='major', labelsize=xLabelSize)
        if tilt:
            fig.autofmt_xdate(rotation=xTickRotation)
            
        if len(outputFileName) > 0:
            plt.savefig(self.outDir+outputFileName)

        return

###################################################################
###################################################################

    def plotGraph(self, x1, y1, title="", xlabel="", ylabel="", legendLabel1="", outputFileName="", xLabelSize=25, tilt=False, xTickRotation=0, dateFormat='%Y-%m'):
        
        fig, ax = plt.subplots(figsize=(self.figWidth, self.figHeight))
            
        hfmt = matplotlib.dates.DateFormatter(dateFormat)
        ax.xaxis.set_major_formatter(hfmt)
        
        ax.set_title(title, fontsize=xLabelSize)
        ax.set_xlabel(xlabel, fontsize=xLabelSize)
        ax.set_ylabel(ylabel, fontsize=xLabelSize)
        
        ax.plot(x1,y1, label=legendLabel1, lw=self.linewidth)
        ax.legend(loc='upper left', prop={'size': xLabelSize-10}, shadow=True, frameon=True)
        ax.tick_params(axis='both', which='major', labelsize=xLabelSize)
        if tilt:
            fig.autofmt_xdate(rotation=xTickRotation)
            
        if len(outputFileName) > 0:
            plt.savefig(self.outDir+outputFileName)

        return

###################################################################
###################################################################