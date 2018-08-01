# coding=utf-8
# import matplotlib
# import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import pandas as pd
import math
from datetime import datetime

###################################################################
###################################################################
###################################################################
###################################################################

class DFFunctions():

###################################################################
###################################################################

    def __init__(self):
        
        return
        
###################################################################
###################################################################

    def getCSVDF(self, csv, skiprow=0, timeCol=[], timeFormat=[]):

        ## lists timeCol and timeFormat must have the same length

        outDF = pd.read_csv(csv, skiprows=skiprow)
        if len(timeCol) > 0:
            for i in range(0,len(timeCol)):
                ## Converts the string in specified column with time data to datetime object
                outDF[timeCol[i]] = pd.to_datetime(outDF[timeCol[i]],format=timeFormat[i])
        
        return outDF

###################################################################
###################################################################