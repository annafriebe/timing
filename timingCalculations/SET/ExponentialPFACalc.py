#!/usr/bin/env python
import math
import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt
from PoissonPFAcalc import calcT


nGenerated = 100


def calcPFAExp(z):
    minVal = np.min(z)
    diffMin = z - minVal
    betaExp = np.mean(diffMin)
    print("exponential")
    print(betaExp)
    generatedData = np.random.exponential(scale=betaExp, size=(nGenerated, len(z))) + minVal
    generatedData = np.around(generatedData)
    drawTimeHist(generatedData[0], "generated release times")
    dataProbabilities = stats.expon.pdf(z, loc=minVal, scale=betaExp)
    logLikelihoodsData = np.log(dataProbabilities)
    generatedDataProbabilities =stats.expon.pdf(generatedData, loc=minVal, scale=betaExp)  
    logLikelihoodsGen = np.log(generatedDataProbabilities)
    expW = np.mean(logLikelihoodsGen)
    varW = np.var(logLikelihoodsGen)
    measuredT = calcT(logLikelihoodsData, expW, varW)
    generatedT = np.zeros(nGenerated)
    for k in range(nGenerated):
        generatedT[k] = calcT(logLikelihoodsGen[k], expW, varW)
    beta = np.count_nonzero(generatedT <= measuredT)/nGenerated
    print("Beta:", beta)
    PFA = min(beta, 1-beta)
    print("PFA:", PFA)
    return 



        
        
  
#print(generatedData)
       

