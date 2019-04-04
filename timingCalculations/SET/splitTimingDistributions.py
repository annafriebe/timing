#!/usr/bin/env python
import math
import numpy as np
import switchDataForCPU
import drawTimingDistributions
import GaussianPFAcalc
import minSqErrPeriodEstimate

def getTimesInInterval(times, low, hi):
    timesInInterval = []
    for time in times:
        if time > low and time < hi:
            timesInInterval.append(time)
    return timesInInterval

def periodicAdjustedReleaseTimes(times, period):
    periodicAdjustedTimes = np.zeros(len(times))
    for i in range(len(times)):
        periodicAdjustedTimes[i] = times[i] % period
    return periodicAdjustedTimes

def logTransform(times):
    logTransformedTimes = np.zeros(len(times))
    for i in range(len(times)):
        logTransformedTimes[i] = np.log(times[i])
    return logTransformedTimes

def findState(rangesLimits, releaseTime):
    for i in range(len(rangesLimits)):
        if releaseTime < rangesLimits[i]:
            return i
    return len(rangesLimits)

def getStates(rangesLimits, releaseTimes):
    states = np.zeros(len(releaseTimes), dtype=int)
    for i in range(len(releaseTimes)):
        releaseTime = releaseTimes[i]
        states[i] = findState(rangesLimits, releaseTime)
    return states

def getProcessStates(previousProcessList):
    states = np.zeros(len(previousProcessList), dtype=int)
    processes = []
    for i in range(len(previousProcessList)):
        process = previousProcessList[i]
        if not process in processes:
            processes.append(process)
        states[i] = processes.index(process)
    print(processes)
    print(states)
    return states

def stateTransitionProbabilities(states, nStates):
    transitionProbabilities = np.zeros((nStates, nStates))
    for i in range(len(states)-1):
        transitionProbabilities[states[i], states[i+1]]+=1
    sumRows = np.sum(transitionProbabilities, axis=1)
    print(transitionProbabilities[0, 2])
    print(transitionProbabilities)
    print(sumRows)
    return transitionProbabilities/ sumRows[:, None]
        



switchData = getSwitchDataForCPU('../../../../reports/20190313-2-CPU2-report', '[001]')
#wakeupData = getWakeupDataForCPU('../../reports/20190313-2-CPU2-report', '[001]')
print(len(switchData))
executionTimeDict, releaseTimeDict, previousProcessList = getExecutionTimeReleaseTimeDict(switchData, 'simplePeriodic')
for item in executionTimeDict:
    print(item, len(executionTimeDict[item]))
    if len(executionTimeDict[item]) > 100:
        mu, sigma = calcPFAGaussian(executionTimeDict[item])
        #as a test, generate from this distr
        a, loc, scale = calcPFASkewNorm(executionTimeDict[item])
        drawExecutionTimeDistr(item, executionTimeDict[item])
 #       logTransformedTimes = logTransform(executionTimeDict[item])
 #       a, loc, scale = calcPFASkewNorm(logTransformedTimes)
 #       drawExecutionTimeDistr(item, logTransformedTimes)
 #       if item.startswith('simplePeriodic'):
 #           print("restricted")
 #           restrictedIntervalTimes = getTimesInInterval(executionTimeDict[item], 25000, 35000)
 #           logTransformedTimes = logTransform(executionTimeDict[item])
 #           a, loc, scale = calcPFASkewNorm(logTransformedTimes)
 #           drawExecutionTimeDistr(item, logTransformedTimes)

releaseTimesDiffInRange = np.zeros(0)
loLimit = 19996000
hiLimit = 20005000
for item in releaseTimeDict:
    releaseTimes = releaseTimeDict[item]
    if len(releaseTimes) > 100:
        releaseTimesDiff = np.zeros(len(releaseTimes) - 1)
        for i in range(len(releaseTimes) - 1):
            releaseTimesDiff[i] = releaseTimes[i+1] - releaseTimes[i]
 #       drawReleaseTimeDiffDistr(item, releaseTimesDiff)
        diffArrayInd = np.where(np.logical_and(releaseTimesDiff>loLimit, releaseTimesDiff<hiLimit))
        releaseTimesDiffInRange = np.concatenate((releaseTimesDiffInRange, releaseTimesDiff[diffArrayInd]))
#drawReleaseTimeDiffDistr("all in range", releaseTimesDiffInRange)
estimatedPeriod = int(np.mean(releaseTimesDiffInRange)/2 + 0.5) 
print("Estimated period from release times:", estimatedPeriod)

estimatedPeriod = int(periodEstimate(releaseTimeDict['all']) + 0.5)

#wakeUpTimesDiff = np.zeros(len(wakeupData) - 1)
#loLimit = 9996000
#hiLimit = 10005000

#for i in range(len(wakeupData) - 1):
#    wakeUpTimesDiff[i] = wakeupData[i+1] - wakeupData[i]

#drawReleaseTimeDiffDistr("wakeup", wakeUpTimesDiff)
#diffArrayInd = np.where(np.logical_and(wakeUpTimesDiff>loLimit, wakeUpTimesDiff<hiLimit))
#wakeUpTimesDiff = wakeUpTimesDiff[diffArrayInd]
#drawReleaseTimeDiffDistr("wakeup in range", wakeUpTimesDiff)

#estimatedPeriod = int(np.mean(wakeUpTimesDiff) + 0.5) 
#print("estimated period from wakeup times", estimatedPeriod)        

allReleaseTimes = np.zeros(0)
for item in releaseTimeDict:
    releaseTimes = releaseTimeDict[item]
    releaseTimes = periodicAdjustedReleaseTimes(releaseTimeDict[item], estimatedPeriod)
    if item == 'all':
        allReleaseTimes = releaseTimes
    if len(releaseTimes) > 100:
        calcPFAGaussian(releaseTimes)
#        drawReleaseTimeDistr(item, releaseTimes)
        
#rangesLimits = [9935000, 9945000, 9965000]   
#states = getStates(rangesLimits, allReleaseTimes)     
processes = getProcessStates(previousProcessList)
print(len(allReleaseTimes))
print(len(executionTimeDict['all']))
drawTimesPerProcess(allReleaseTimes, executionTimeDict['all'], processes)
#drawStates(states, processes)
#transitionProbabilities = stateTransitionProbabilities(states, 4)
#print(transitionProbabilities)
#periodicAdjustedWakeupTimes = periodicAdjustedReleaseTimes(wakeupData, estimatedPeriod)
#drawWakeUpTimeDistr(periodicAdjustedWakeupTimes, 0, 10000000)
         
