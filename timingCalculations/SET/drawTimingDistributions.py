#!/usr/bin/env python
import math
import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

def drawExecutionTimeDistr(prevProcess, executionTimes):
    plt.figure()
    title = "Execution time distribution, previous process: " + prevProcess
    plt.title(title)
    n, bins, patches = plt.hist(executionTimes, bins=150)
#    print(bins)
#    y = 50000* stats.skewnorm.pdf(bins, a, loc, scale)
 #   print(y)
 #   plt.plot(bins, y)
 #   plt.figure()
 
def drawSeqExectionTimesAutoCorr(prevProcess, executionTimes):
    plt.figure()
    title = "Sequential execution times, previous process: " + prevProcess
    plt.title(title)
    plt.plot(executionTimes)
    autoCorr = np.correlate(executionTimes, executionTimes, mode='full')
    etNorm = 0
    for i in range(len(executionTimes)):
        etNorm += executionTimes[i]**2
    autoCorr = autoCorr[(int)(autoCorr.size/2):]/etNorm
    plt.figure()
    title = "Autocorrelation function, previous process: " + prevProcess
    plt.title(title)
    plt.plot(autoCorr)
    plt.xlim(0, 50)
    plt.ylim(0.8, 1.0)
    
    
def drawReleaseTimeDiffDistr(prevProcess, releaseTimesDiff):
    plt.figure()
    title = "Release time diff , previous process: " + prevProcess
    plt.title(title)
    plt.hist(releaseTimesDiff, bins=70)
        
def drawReleaseTimeDistr(prevProcess, releaseTimes):
    plt.figure()
    title = "Release time, previous process: " + prevProcess
    plt.title(title)
    plt.hist(releaseTimes, bins=70)
#    plt.figure()
#    title = "Sequential release times, previous process: " + prevProcess
#    plt.title(title)
#    plt.plot(releaseTimes)
 
def drawWakeUpTimeDistr(wakeupTimes):
    plt.figure()
    title = "Wake up times: "
    plt.title(title)
    plt.hist(wakeupTimes, bins=70)

#TODO: draw y-axix lines at separation between 4 states
def drawAllReleaseTimeDistr(releaseTimes):
    plt.figure()
    title = "All release times: "
    plt.title(title)
    plt.hist(releaseTimes, bins=70)

def drawTimesPerProcess(releaseTimes, executionTimes, processes):
    releaseTimesPerProcess = []
    executionTimesPerProcess = []
    for i in range(len(processes)):
        releaseTimesPerProcess.append([])
        executionTimesPerProcess.append([])
    nTimes = len(releaseTimes)
    for i in range(nTimes):
        rt = releaseTimes[i]
        releaseTimesPerProcess[processes[i]].append(rt)
        executionTimesPerProcess[processes[i]].append(executionTimes[i])
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    plt.figure()
    for i in range(7):
        plt.scatter(releaseTimesPerProcess[i], executionTimesPerProcess[i], c=cycle[i])

def drawStates(states, processes):
    x = np.arange(len(states))
    plt.figure()
    plt.plot(x[100:200], states[100:200])

