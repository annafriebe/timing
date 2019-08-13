#!/usr/bin/env python
import math
import numpy as np
import switchDataForCPU
import drawTimingDistributions
import GaussianPFAcalc
#import StateTransitionPFAcalc
import minSqErrPeriodEstimate
import cluster

def getTimesInInterval(times, low, hi):
    timesInInterval = []
    for time in times:
        if time > low and time < hi:
            timesInInterval.append(time)
    return timesInInterval

def periodicAdjustedTimes(times, period):
    periodicAdjustedTimes = np.zeros(len(times))
    for i in range(len(times)):
        periodicAdjustedTimes[i] = times[i] % period
    return periodicAdjustedTimes

def logTransform(times):
    logTransformedTimes = np.zeros(len(times))
    for i in range(len(times)):
        logTransformedTimes[i] = np.log(times[i])
    return logTransformedTimes


def getProcessStates(previousProcessList):
    states = np.zeros(len(previousProcessList), dtype=int)
    processes = []
    processCount = []
    for i in range(len(previousProcessList)):
        process = previousProcessList[i]
        if not process in processes:
            processes.append(process)
            processCount.append(0)
        states[i] = processes.index(process)
        processCount[processes.index(process)] += 1
    print(processes)
    print(processCount)
    print(states)
    return len(processes), states

def getTwoProcessStates(previousProcessList):
    states = np.zeros(len(previousProcessList), dtype=int)
    for i in range(len(previousProcessList)):
        process = previousProcessList[i]
        if process.startswith("simplePeriodic"):
            states[i] = 0
        else:
            states[i] = 1
    print(states)
    return states



np.random.seed(300)

#switchWakeupData = getSwitchAndWakeupDataForCPU('../../../../reports/20190416-CPU2-report', '[001]')
switchWakeupData = getSwitchAndWakeupDataForCPU('../../../../tracesReportsPreemptRT/log_p06_1t_0417_1_20sec.txt', '[003]', True)

releaseTimeDict, schedulingTimeDict, executionTimeDict, previousProcessList = \
getTimeDicts(switchWakeupData, 'program06', 5000)

#getTimeDicts(switchWakeupData, 'simplePeriodic')

for item in executionTimeDict:
    print(item, len(executionTimeDict[item]))
    if len(executionTimeDict[item]) > 100:
        mu, sigma = calcPFAGaussian(executionTimeDict[item])
        #as a test, generate from this distr
        a, loc, scale = calcPFASkewNorm(executionTimeDict[item])
        drawExecutionTimeDistr(item, executionTimeDict[item])
 #       drawSeqExectionTimesAutoCorr(item, executionTimeDict[item])
 #       logTransformedTimes = logTransform(executionTimeDict[item])
 #       a, loc, scale = calcPFASkewNorm(logTransformedTimes)
 #       drawExecutionTimeDistr(item, logTransformedTimes)
 #       if item.startswith('simplePeriodic'):
 #           print("restricted")
 #           restrictedIntervalTimes = getTimesInInterval(executionTimeDict[item], 25000, 35000)
 #           logTransformedTimes = logTransform(executionTimeDict[item])
 #           a, loc, scale = calcPFASkewNorm(logTransformedTimes)
 #           drawExecutionTimeDistr(item, logTransformedTimes)
#drawSeqExectionTimesAutoCorr(executionTimeDict['all'])

#releaseTimesDiffInRange = np.zeros(0)
#loLimit = 19996000
#hiLimit = 20005000
#for item in releaseTimeDict:
#    releaseTimes = releaseTimeDict[item]
#    if len(releaseTimes) > 100:
#        releaseTimesDiff = np.zeros(len(releaseTimes) - 1)
#        for i in range(len(releaseTimes) - 1):
#            releaseTimesDiff[i] = releaseTimes[i+1] - releaseTimes[i]
 #       drawReleaseTimeDiffDistr(item, releaseTimesDiff)
#        diffArrayInd = np.where(np.logical_and(releaseTimesDiff>loLimit, releaseTimesDiff<hiLimit))
#        releaseTimesDiffInRange = np.concatenate((releaseTimesDiffInRange, releaseTimesDiff[diffArrayInd]))
#drawReleaseTimeDiffDistr("all in range", releaseTimesDiffInRange)
#estimatedPeriod = int(np.mean(releaseTimesDiffInRange)/2 + 0.5) 

estimatedPeriod = int(periodEstimate(releaseTimeDict['all']) + 0.5)
print("Estimated period from release times:", estimatedPeriod)

estimatedPeriod = int(periodEstimate(schedulingTimeDict['all']) + 0.5)
print("Estimated period from release times:", estimatedPeriod)

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

allSchedulingTimes = np.zeros(0)
allReleaseTimes = np.zeros(0)

for item in releaseTimeDict:
    releaseTimeDict[item] = periodicAdjustedTimes(releaseTimeDict[item], estimatedPeriod)
    if item == 'all':
        allReleaseTimes = releaseTimeDict[item]

drawTimeHist(allReleaseTimes, "all release times")
calcPFAGaussian(allReleaseTimes)

for item in schedulingTimeDict:
    schedulingTimeDict[item] = periodicAdjustedTimes(schedulingTimeDict[item], estimatedPeriod)
    if item == 'all':
        allSchedulingTimes = schedulingTimeDict[item]
#    if len(schedulingTimes) > 100:
#        calcPFAGaussian(schedulingTimes)
#        drawReleaseTimeDistr(item, releaseTimes)
        
nProcesses, processes = getProcessStates(previousProcessList)
twoProcesses = getTwoProcessStates(previousProcessList)
print(len(allReleaseTimes))
print(len(executionTimeDict['all']))

schedulingReleaseDiff = allSchedulingTimes - allReleaseTimes
responseTimes = schedulingReleaseDiff +  executionTimeDict['all']
drawTimeHist(responseTimes, "all response times")

calcPFAExp(allReleaseTimes)

drawTimesPerProcess(allReleaseTimes, executionTimeDict['all'], processes, "release time", "execution time")
drawTimesPerProcess(allSchedulingTimes, executionTimeDict['all'], processes, "scheduling time", "execution time")
drawTimesPerProcess(schedulingReleaseDiff, executionTimeDict['all'], processes, "release delay", "execution time")
drawTimesPerProcess(allReleaseTimes, schedulingReleaseDiff, processes, "release time", "release delay")

#for item in releaseTimeDict:
#    if len(releaseTimeDict[item]) > 100:
#        drawReleaseTimeDistr(item, releaseTimeDict[item])

#drawTimesPerProcess(allReleaseTimes, allSchedulingTimes, processes)

#nStates = 7
#labels = kMeansCluster(schedulingReleaseDiff, executionTimeDict['all'], nStates)

#timesPerCluster, schedulingTimesPerCluster, executionTimesPerCluster = \
#splitTimesPerCluster(allSchedulingTimes, executionTimeDict['all'], labels, nStates)

#timesPerCluster, schedulingReleaseDiffPerCluster, executionTimesPerCluster = \
#splitTimesPerCluster(schedulingReleaseDiff, executionTimeDict['all'], labels, nStates)

#for i in range(len(schedulingReleaseDiffPerCluster)):
#    if len(schedulingReleaseDiffPerCluster[i]) > 100:
#        responseTimes =  schedulingReleaseDiffPerCluster[i] + executionTimesPerCluster[i]
#        title = "response times for cluster" + str(i)
#        drawTimeHist(responseTimes, title)
    

#for item in schedulingReleaseDiffPerCluster:
#    if len(item) > 50:
#        print(len(item))
#        calcPFASkewNorm(item)

#for item in schedulingTimesPerCluster:
#    if len(item) > 50:
#        print(len(item))
#        calcPFASkewNorm(item)

#for item in executionTimesPerCluster:
#    if len(item) > 50:
#        print(len(item))
#        calcPFASkewNorm(item)

#for item in timesPerCluster:
#    if len(item) > 100:
#        print(len(item))
#        calcPFA2DGaussian(item)

#calcPFAStateTransitions(labels, twoProcesses, nStates, 2)
#calcPFAStatePredictions(labels, processes, nStates, nProcesses)


#calcPFAMarkovChain(labels, nStates)
    

         
