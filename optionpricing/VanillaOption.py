import numpy as np

from scipy.stats import norm

from random1 import gaussianBoxMuller
    
class PayOff(object):
    '''
    Defines the option.
    
    bs_flag class variable indicates if option should be treated as call or put
    in Black Scholes
    
    '''
    class BSFLAG:
        call = 1
        put = 2
        
    bs_flag = None
    def __init__(self, strike):
        self._strike = strike
    
    def payoff(self, spot):
        '''
        Override in derived class to define option payoff
        
        When called this function will return the payoff given the spot price 
        of the option.
        
        '''
        return None
    
    @property
    def strike(self):
        return self._strike

class Call(PayOff):
    bs_flag = BSFLAG.call
    
    def payoff(self, spot):
        return max(0, spot - self.strike)

class Put(PayOff):
    bs_flag = BSFLAG.put
    
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
    def payoff(self):
        # return the payoff object's payoff function
        return self._payoff.payoff
    
    @property
    def strike(self):
        return self._payoff.strike

    @property
    def bs_flag(self):
        return self._payoff.bs_flag        

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
    

def SimpleBlackScholes(option, spot, vol, r):
    '''
    Black Scholes Formula
    
    '''
    
    T = option.expiry
    X = option.strike
    variance = vol * vol
    
    d1 = (np.log(spot/X)+(r+variance/2.)*T)/(vol*np.sqrt(T))

    d2 = d1-vol*np.sqrt(T)
    
    if option.bs_flag == PayOff.BSFLAG.call:
        return spot*norm.cdf(d1)-X*np.exp(-r*T)*norm.cdf(d2)

    else:
        return X*np.exp(-r*T)*norm.cdf(-d2)-spot*norm.cdf(-d1)

def black76(expry, F, X, r, vol):
    '''
    Black 76 call price
    
    '''
    d1 = (np.log(F/X)-(0.5*(vol**2)*expry))/(vol*np.sqrt(expry))   
    pv = np.exp(-r * expry)

    nd1 = norm.cdf(d1)

    c = pv*(F*norm.cdf(d1) - X*norm.cdf(d1 - vol * np.sqrt(expry)))

    return (c, d1, pv, nd1, pv*nd1)