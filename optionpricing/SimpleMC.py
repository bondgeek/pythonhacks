import numpy as np

from random1 import gaussianBoxMuller

def SimpleMC(expiry, 
             strike,
             spot,
             vol,
             r,
             numPaths):
    
    variance = vol * vol * expiry
    rootVariance = np.sqrt(variance)
    
    itoCorrection = -0.5 * variance
    
    movedSpot = spot * np.exp(r * expiry * itoCorrection)
    
    thisPayoff = lambda x: 0 if x <= strike else x - strike
    
    runningSum = 0.
    for g in [gaussianBoxMuller() for n in range(numPaths)]:
        thisSpot = movedSpot * np.exp(rootVariance * g)
        runningSum += thisPayoff(thisSpot)
    
    mean = (runningSum / numPaths) * np.exp(-r*expiry)
    
    return mean

