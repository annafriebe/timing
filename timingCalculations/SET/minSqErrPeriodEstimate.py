#!/usr/bin/env python
def calcSumi(n):
    sumi = 0
    for i in range(n):
        sumi += i
    return sumi

def calcSumiSq(n):
    sumiSq = 0
    for i in range(n):
        sumiSq += i*i
    return sumiSq

def calcSumTimes(releaseTimes):
    sumTimes = 0
    for time in releaseTimes:
        sumTimes += time
    return sumTimes
        
def calcSumiTimes(releaseTimes, n):
    sumiTimes = 0
    for i in range(n):
        sumiTimes += i*releaseTimes[i]
    return sumiTimes
        
def periodEstimate(releaseTimes):
    n = len(releaseTimes)
    sumi = calcSumi(n)
    sumiSq = calcSumiSq(n)
    sumTimes = calcSumTimes(releaseTimes)
    sumitimes = calcSumiTimes(releaseTimes, n)
    numerator = sumi*sumTimes/n - sumitimes
    denominator = sumi*sumi/n - sumiSq
    estimatedPeriod = numerator/ denominator
    print("period estimate min sq err", estimatedPeriod)
    return estimatedPeriod







