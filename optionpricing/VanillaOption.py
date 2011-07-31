import numpy as np

from random1 import gaussianBoxMuller
    
class PayOff(object):
    def __init__(self, strike):
        self._strike = strike
    
    def payoff(self, spot):
        "override in derived class to define option payoff
        return None
    
    @property
    def strike(self):
        return self._strike

class Call(PayOff):
    def payoff(self, spot):
        return max(0, spot - self.strike)

class Put(PayOff):
    def payoff(self, spot):
        return max(0, self.strike - spot) 
        
class VanillaOption(object):
    def __init__(self, expiry, payoff):
        self._payoff = payoff
        self._expiry = expiry
    
    @property
    def expiry(self):
        return self._expiry

    @property
    def payoff(self)
        return self._payoff.payoff


def SimpleMC1(option,
             spot,
             vol,
             r,
             numPaths):
    
    expiry = option.expiry
    
    variance = vol * vol * expiry
    rootVariance = np.sqrt(variance)
    
    itoCorrection = -0.5 * variance
    
    movedSpot = spot * np.exp(r * expiry * itoCorrection)
        
    runningSum = 0.
    for g in [gaussianBoxMuller() for n in range(numPaths)]:
        thisSpot = movedSpot * np.exp(rootVariance * g)
        runningSum += option.payoff(thisSpot)
    
    mean = (runningSum / numPaths) * np.exp(-r*expiry)
    
    return mean
    
    