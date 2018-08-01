# coding=utf-8

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

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