#!/usr/bin/env python

def timeInMicroOrNano(timeStampString, microSeconds):
    timeStampNoColon = timeStampString.split(':')[0]
    sepTimeStamp = timeStampNoColon.split('.')
    decimalFactor = 1E9
    if (microSeconds):
        decimalFactor = 1E6
    return int(sepTimeStamp[0]) * decimalFactor + int(sepTimeStamp[1])

def getSwitchDataForCPU(filePath, CPU, microSeconds = False):
    with open(filePath) as f:
        lines = f.readlines()
        nLines = len(lines)
        switchDataForCPU = []
        for i in range(400, nLines - 100):
            line = lines[i].split()
            event = line[3]
            cpu = line[1]
            if event == 'sched_switch:' and cpu == CPU:
                time = timeInMicroOrNano(line[2], microSeconds)
                inProcess = line[8]
                outProcess = line[4]
                switchDataForCPU.append([time, inProcess, outProcess])
        return switchDataForCPU


def getWakeupDataForCPU(filePath, CPU, microSeconds = False):
    with open(filePath) as f:
        lines = f.readlines()
        nLines = len(lines)
        wakeupDataForCPU = []
        for i in range(400, nLines - 100):
            line = lines[i].split()
            event = line[3]
            cpu = line[1]
            if event == 'sched_wakeup:' and cpu == CPU:
                time = timeInMicroOrNano(line[2], microSeconds)
                process = line[4]
                wakeupDataForCPU.append([time, process])
        return wakeupDataForCPU

def getWakeupTimes(wakeupData, process):
    wakeupTimesList = []
    for item in wakeupData:
        time = item[0]
        wakeupProcess = item[1]
        if wakeupProcess.startswith(process):
            wakeupTimesList.append(time)
    return wakeupTimesList

def getSwitchAndWakeupDataForCPU(filePath, CPU, microSeconds = False):
    timingData = []
    with open(filePath) as f:
        lines = f.readlines()
        nLines = len(lines)
        for i in range(400, nLines - 100):
            line = lines[i].split()
            event = line[3]
            cpu = line[1]
            if (cpu == CPU):
                if event == 'sched_switch:':
                    time = timeInMicroOrNano(line[2], microSeconds)
                    inProcess = line[8]
                    outProcess = line[4]
                    timingData.append([0, time, inProcess, outProcess])
                if event == 'sched_wakeup:': 
                    time = timeInMicroOrNano(line[2], microSeconds)
                    process = line[4]
                    timingData.append([1, time, process])
        return timingData
                    
             
def getTimeDicts(switchWakeupData, process, period=10000000):
    previousProcess = ""
    releaseTime = 0
    schedulingTime = 0
    lastExecutionStoppedTime = 0
    executionTimeDict = {}
    executionTimeDict['all'] = []
    releaseTimeDict = {}
    releaseTimeDict['all'] = []
    schedulingTimeDict = {}
    schedulingTimeDict['all'] = []
    previousProcessList = []
    for infoItem in switchWakeupData:
        eventWakeup = infoItem[0]
        time = infoItem[1]
        if eventWakeup == 1:
            wakeupProcess = infoItem[2]
            if wakeupProcess.startswith(process):
                releaseTime = time
        else:
            inProcess = infoItem[2]
            outProcess = infoItem[3]
            if inProcess.startswith(process):
                schedulingTime = time
            if outProcess.startswith(process):
                if not previousProcess in executionTimeDict:
                    executionTimeDict[previousProcess] = []
                    releaseTimeDict[previousProcess] = []
                    schedulingTimeDict[previousProcess] = []
                if releaseTime > 1e-5 and schedulingTime > 1e-5:
                    if schedulingTime - lastExecutionStoppedTime < period / 2:
                        executionTimeDict[previousProcess][-1] += (time - schedulingTime)
                        executionTimeDict['all'][-1] += (time - schedulingTime)
                    else:                    
                        executionTimeDict[previousProcess].append(time - schedulingTime)
                        executionTimeDict['all'].append(time - schedulingTime)
                        schedulingTimeDict[previousProcess].append(schedulingTime)
                        schedulingTimeDict['all'].append(schedulingTime)
                        releaseTimeDict[previousProcess].append(releaseTime)
                        releaseTimeDict['all'].append(releaseTime)
                        previousProcessList.append(previousProcess)
                previousProcess = outProcess
                lastExecutionStoppedTime = time
            else:
                if not outProcess.startswith('swapper'):
                    if not previousProcess.startswith(process):
                        outProcess += previousProcess
                    previousProcess = outProcess
    return releaseTimeDict, schedulingTimeDict, executionTimeDict, previousProcessList
            
        
        


