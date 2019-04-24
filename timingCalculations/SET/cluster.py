# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:00:10 2019

@author: annaf
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


def kMeansCluster(releaseTimes, executionTimes, k):
    df = pd.DataFrame({
    'x': releaseTimes,
    'y': executionTimes
    })
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(df)
    labels = kmeans.predict(df)
    centroids = kmeans.cluster_centers_
    print(centroids)
    fig = plt.figure()

    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colors = []
    for label in labels:
        colors.append(cycle[label])
    plt.scatter(df['x'], df['y'], color=colors, alpha=0.5, edgecolor='k')
    for idx, centroid in enumerate(centroids):
        print('color' + cycle[idx])
        plt.scatter(*centroid, color=cycle[idx])
    plt.show()
    return labels

def splitTimesPerCluster(releaseTimes, executionTimes, labels, k):
    splitTimes = []
    splitReleaseTimes = []
    splitExecutionTimes = []
    unique, counts = np.unique(labels, return_counts=True)
    for i in range(k):
        kTimes = np.zeros((counts[i], 2))
        splitTimes.append(kTimes)
        kTimes = np.zeros(counts[i])
        splitReleaseTimes.append(kTimes)
        splitExecutionTimes.append(kTimes)
    labelIndices = np.zeros(k, dtype=int)
    for i in range(labels.size):
        label = labels[i]
        splitTimes[label][labelIndices[label]][0] = releaseTimes[i]
        splitTimes[label][labelIndices[label]][1] = executionTimes[i]
        splitReleaseTimes[label][labelIndices[label]] = releaseTimes[i]
        splitExecutionTimes[label][labelIndices[label]] = executionTimes[i]
        labelIndices[label] += 1
    return splitTimes, splitReleaseTimes, splitExecutionTimes
        
    