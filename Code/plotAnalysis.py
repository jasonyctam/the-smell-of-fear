# coding=utf-8

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import time

###################################################################
###################################################################
###################################################################
###################################################################

class plotAnalysis():

###################################################################
###################################################################

    def __init__(self, plotsDir=""):

        sns.set_style("darkgrid")
        colors = ["windows blue", "amber", "greenish", "orange", "sky blue", "greyish", "salmon", "faded green", "lavender", "denim blue", "medium green"]
        # colors = ["windows blue", "aquamarine", "amber", "lightblue", "lavender"]
        custom_palette = sns.xkcd_palette(colors)
        sns.set_palette(custom_palette)
        self.outDir = plotsDir
        
        self.figWidth = 15
        self.figHeight = 8
        self.linewidth = 2
        
        return
        
###################################################################
###################################################################

    def plotMovieGasGraph(self, inDF, title="", xlabel="", ylabel="", outputFileName="", xLabelSize=25, tilt=False, xTickRotation=0, dateFormat='%H:%M:%S'):
        
        fig, ax = plt.subplots(figsize=(self.figWidth, self.figHeight))
            
        hfmt = matplotlib.dates.DateFormatter(dateFormat)
        ax.xaxis.set_major_formatter(hfmt)
        
        ax.set_title(title, fontsize=xLabelSize)
        ax.set_xlabel(xlabel, fontsize=xLabelSize)
        ax.set_ylabel(ylabel, fontsize=xLabelSize)
        
        columns = list(inDF)

        inDF[columns[0]] = pd.to_datetime(inDF[columns[0]])

        print(inDF[columns[0]].dtype)
        print(inDF[columns[1]].dtype)

        top_lim = 0

        for i in range(1, len(columns)):
            ax.plot(inDF[columns[0]],inDF[columns[i]], label=columns[i], lw=self.linewidth)
            if inDF[columns[i]].max() > top_lim:
                top_lim = inDF[columns[i]].max()

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

    def plotBackgroundGraph(self, inDF, channel, title="", xlabel="", ylabel="", legendLabel1="", outputFileName="", xLabelSize=25, tilt=False, xTickRotation=0, dateFormat='%Y-%m'):
        
        fig, ax = plt.subplots(figsize=(self.figWidth, self.figHeight))
            
        hfmt = matplotlib.dates.DateFormatter(dateFormat)
        ax.xaxis.set_major_formatter(hfmt)
        
        ax.set_title(title, fontsize=xLabelSize)
        ax.set_xlabel(xlabel, fontsize=xLabelSize)
        ax.set_ylabel(ylabel, fontsize=xLabelSize)
        
        x1 = inDF['Time']
        y1 = inDF[channel]

        ax.plot(x1,y1, label=legendLabel1, lw=self.linewidth)

        inDF['Hours'] = inDF['Time'].apply(lambda x: x.time())
        backgroundDF = inDF[(inDF['Hours']>=time(4, 0)) & (inDF['Hours']<=time(9, 0))]

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