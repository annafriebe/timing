#!/usr/bin/env python
import math
import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt
from PoissonPFAcalc import calcT


nGenerated = 100


def calcPFAGaussian(z):
    zMean = np.mean(z)
    print("mean: ", zMean)
    zStdDev = math.sqrt(np.var(z))
    print("stddev: ", zStdDev)
    generatedData = np.random.normal(zMean, zStdDev, (nGenerated, len(z)))
    dataProbabilities = stats.norm.pdf(z, zMean, zStdDev)
    logLikelihoodsData = np.log(dataProbabilities)
    generatedDataProbabilities =stats.norm.pdf(generatedData, zMean, zStdDev)  
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
    return zMean, zStdDev

def calcPFASkewNorm(z):
    a, loc, scale = stats.skewnorm.fit(z)
  #  print("a", a)
   # print("loc", loc)
   # print("scale", scale)
   # zMean = np.mean(z)
   # print("mean: ", zMean)
   # zStdDev = math.sqrt(np.var(z))
   # print("stddev: ", zStdDev)
    generatedData = stats.skewnorm(a, loc, scale).rvs((nGenerated, len(z)))
    # np.random.normal(zMean, zStdDev, (nGenerated, len(z)))
    dataProbabilities = stats.skewnorm.pdf(z, a, loc, scale)
    logLikelihoodsData = np.log(dataProbabilities)
    generatedDataProbabilities =stats.skewnorm.pdf(generatedData, a, loc, scale)  
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
    return a, loc, scale
    #TODO, draw z and probability distribution



        
        
  
#print(generatedData)
       

