#!/usr/bin/env python

def timeInNanoSeconds(timeStampString):
    timeStampNoColon = timeStampString.split(':')[0]
    sepTimeStamp = timeStampNoColon.split('.')
    return int(sepTimeStamp[0]) * 1E9 + int(sepTimeStamp[1])

def getSwitchDataForCPU(filePath, CPU):
    with open(filePath) as f:
        lines = f.readlines()
        nLines = len(lines)
        switchDataForCPU = []
        for i in range(400, nLines - 100):
            line = lines[i].split()
            event = line[3]
            cpu = line[1]
            if event == 'sched_switch:' and cpu == CPU:
                time = timeInNanoSeconds(line[2])
                inProcess = line[8]
                outProcess = line[4]
                switchDataForCPU.append([time, inProcess, outProcess])
        return switchDataForCPU


def getWakeupDataForCPU(filePath, CPU):
    with open(filePath) as f:
        lines = f.readlines()
        nLines = len(lines)
        wakeupDataForCPU = []
        for i in range(400, nLines - 400):
            line = lines[i].split()
            event = line[3]
            cpu = line[1]
            if event == 'sched_wakeup:' and cpu == CPU:
                time = timeInNanoSeconds(line[2])
                wakeupDataForCPU.append(time)
#                wakeupDataForCPU.append([time, inProcess, outProcess])
        return wakeupDataForCPU

#TODO, get waking/ wakeup data

def getExecutionTimeDict(switchData, process, period=10000000):
    previousProcess = ""
    releaseTime = 0
    lastExecutionStoppedTime = 0
    executionTimeDict = {}
    executionTimeDict['all'] = []
    for infoItem in switchData:
        time = infoItem[0]
        inProcess = infoItem[1]
        outProcess = infoItem[2]
        if inProcess.startswith(process):
            releaseTime = time
        if outProcess.startswith(process):
            if not previousProcess in executionTimeDict:
                executionTimeDict[previousProcess] = []
            if releaseTime > 1e-5:
                if releaseTime - lastExecutionStoppedTime < period / 2:
                    executionTimeDict[previousProcess][-1] += (time - releaseTime)
                else:                    
                    executionTimeDict[previousProcess].append(time - releaseTime)
            previousProcess = outProcess
            lastExecutionStoppedTime = time
            executionTimeDict['all'].append(time - releaseTime)
        else:
            if not outProcess.startswith('swapper'):
                if not previousProcess.startswith(process):
                    outProcess += '+extra'
                previousProcess = outProcess
    return executionTimeDict
            
        
def getExecutionTimeReleaseTimeDict(switchData, process, period=10000000):
    previousProcess = ""
    releaseTime = 0
    lastExecutionStoppedTime = 0
    executionTimeDict = {}
    executionTimeDict['all'] = []
    releaseTimeDict = {}
    releaseTimeDict['all'] = []
    previousProcessList = []
    for infoItem in switchData:
        time = infoItem[0]
        inProcess = infoItem[1]
        outProcess = infoItem[2]
        if inProcess.startswith(process):
            releaseTime = time
        if outProcess.startswith(process):
            if not previousProcess in executionTimeDict:
                executionTimeDict[previousProcess] = []
                releaseTimeDict[previousProcess] = []
            if releaseTime > 1e-5:
                if releaseTime - lastExecutionStoppedTime < period / 2:
                    executionTimeDict[previousProcess][-1] += (time - releaseTime)
                    executionTimeDict['all'][-1] += (time - releaseTime)
                else:                    
                    executionTimeDict[previousProcess].append(time - releaseTime)
                    executionTimeDict['all'].append(time - releaseTime)
                    releaseTimeDict[previousProcess].append(releaseTime)
                    releaseTimeDict['all'].append(releaseTime)
                    previousProcessList.append(previousProcess)
            previousProcess = outProcess
            lastExecutionStoppedTime = time
        else:
            if not outProcess.startswith('swapper'):
                if not previousProcess.startswith(process):
                    outProcess += previousProcess
#                    outProcess += '+extra'
                previousProcess = outProcess
    return executionTimeDict, releaseTimeDict, previousProcessList
            
        


