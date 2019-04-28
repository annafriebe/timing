#!/usr/bin/env python
import math
import numpy as np
import scipy.special as special
import scipy.stats as stats
from matplotlib import pyplot as plt

def nSmallerThan(data, limit):
    smallerVec = data < limit
    nSmallerThan = np.count_nonzero(smallerVec)
    return nSmallerThan        
        

def logLikelihood(lam, data):
    output = np.zeros(len(data))
    for i in range(len(data)):
        logfacdatai = 0
        for j in range(1, int(data[i] + 0.5)):
            logfacdatai += np.log(j)
        output[i] = data[i]*np.log(lam) - logfacdatai - lam
    return output

def calcT(measuredW, expW, varW):
    tmp = 0
    for i in range(len(measuredW)):
        tmp += np.square(measuredW[i] - expW)/varW
    return tmp/len(measuredW)

#def countInIntervals

def calcPFAPoisson(data):
    dataNorm = np.zeros(len(data), dtype=int)
    minData = np.min(data)
    scale = 1000
    for i in range(len(data)):
        dataNorm[i] = (data[i] - minData)/scale
    lambdaML = np.mean(dataNorm)
    print("ML lambda: ", lambdaML)
    nGenerated = 100
    generatedData = np.random.poisson(lambdaML, (nGenerated, len(data)))
    generatedW = np.zeros((nGenerated, len(data)))
    #print(generatedData)
    for i in range(nGenerated):
        generatedW[i] = logLikelihood(lambdaML, generatedData[i])
    print(generatedW.shape)
    expW = np.mean(generatedW)
    varW = np.var(generatedW)
    print(expW.shape)
    measuredW = logLikelihood(lambdaML, dataNorm)
    measuredT = calcT(measuredW, expW, varW)
    print(measuredT.shape)
    print(measuredT)
    generatedT = np.zeros(nGenerated)
    for i in range(nGenerated):
        generatedT[i] = calcT(generatedW[i], expW, varW) 
    print(np.mean(generatedT))
    beta = np.count_nonzero(generatedT <= measuredT)/nGenerated
    print(beta)


    plt.figure()
    s = np.random.poisson(lambdaML, 10000)
    plt.hist(s, bins='auto')  # arguments are passed to np.histogram
    plt.show()


    


