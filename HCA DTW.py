#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 11:27:40 2018

@author: catherineliu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.cluster import AgglomerativeClustering
import scipy 
import scipy.cluster.hierarchy as shc
import scipy.stats as stats
from sklearn.metrics import silhouette_samples, silhouette_score
from scipy.cluster.hierarchy import fcluster
 
moviedatafull = pd.read_csv('movieAvgDF.csv', sep = ';')
print(moviedatafull.head(10))
#drop all columns that have at least one element missing
moviedatafull = moviedatafull.dropna(axis='columns')


cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
moviedatafull['labels-array'] = moviedatafull['labels'].apply(eval)


moviedatafull.dtypes
#cluster.fit_predict(moviedata['labels-array'])
label = moviedatafull['labels-array']

distancematrix = np.zeros((label.size,label.size))

for x in range(0,label.size):
    for y in range(0,label.size):
        u = label[x]
        v = label[y]
        distancematrix[x][y] = scipy.spatial.distance.hamming(u, v)


plt.figure(figsize=(10, 7))  
plt.title("Customer Dendograms")  
dend = shc.dendrogram(shc.linkage(distancematrix, method='ward')) 

#choose cutoff
max_d = 5
max_d1 = 10
max_d2 = 4
clusters = fcluster((shc.linkage(distancematrix, method='ward')), max_d, criterion='distance')
clusters1 = fcluster((shc.linkage(distancematrix, method='ward')), max_d1, criterion='distance')
clusters2 = fcluster((shc.linkage(distancematrix, method='ward')), max_d2, criterion='distance')

#Map cluster assignments back to original frame:

def add_clusters_to_frame(or_data, clusters):
    or_frame = pd.DataFrame(data=or_data)
    or_frame_labelled = pd.concat([or_frame, pd.DataFrame(clusters)], axis=1)
    return(or_frame_labelled)

df = add_clusters_to_frame(label, clusters)
dffull = add_clusters_to_frame(moviedatafull, clusters)
df.columns = ['label', 'cluster']

max(df['cluster'])
print(df)
print(dffull.head(10))
#delete first column as it was only indexing
dffull = dffull.drop(dffull.columns[[0]], axis=1)
dffull.rename(columns={dffull.columns[332]: 'cluster'}, inplace=True)

df1 = add_clusters_to_frame(label, clusters1)
df1.columns = ['label', 'cluster']
max(df1['cluster'])

df2 = add_clusters_to_frame(label, clusters2)
df2.columns = ['label', 'cluster']
max(df2['cluster'])
#use silhouette score to see if it is a good cutoff
silhouette_score(distancematrix, clusters, metric='euclidean')
silhouette_score(distancematrix, clusters1, metric='euclidean')
silhouette_score(distancematrix, clusters2, metric='euclidean')

#groupby cluster group and average concentrations
clusteravg = dffull.groupby(['cluster']).mean()
dffull.groupby(['cluster']).sum()
dffull.boxplot(column= 'CO2', by = 'cluster')
dffull.boxplot(column= 'm14.0028', by = 'cluster')
dffull.boxplot(column= 'm15.0238', by = 'cluster')
dffull.boxplot(column= 'm15.9962', by = 'cluster')
dffull.boxplot(column= 'm16.0201', by = 'cluster')
summary = dffull.groupby(['cluster']).describe()

#one way ANOVA

