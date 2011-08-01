from scipy.stats import norm
import numpy as np

def black76(expry, F, X, r, vol):
    '''
    Black 76 call price
    
    '''
    d1 = (np.log(F/X)-(0.5*(vol**2)*expry))/(vol*np.sqrt(expry))   
    pv = np.exp(-r * expry)

    nd1 = norm.cdf(d1)

    c = pv*(F*norm.cdf(d1) - X*norm.cdf(d1 - vol * np.sqrt(expry)))

    return (c, d1, pv, nd1, pv*nd1)

def CND(X):
    ''' 
    Cumulative normal distribution

    '''

    a1, a2, a3, a4, a5 = (0.31938153, -0.356563782, 1.781477937, 
                         -1.821255978, 1.330274429)
    L = np.abs(X)

    K = 1.0 / (1.0 + 0.2316419 * L)

    w1 = 1.0/np.sqrt(2*pi)*np.exp(-L*L/2.)
    
    w2 = (a1*K+a2*K*K+a3*np.pow(K,3) + a4*pow(K,4) + a5*pow(K,5))
    
    w = 1.0 - w1 * w2
    
    if X<0:
        w = 1.0-w

    return w

def BlackScholes(CallPutFlag,S,X,T,r,v):
    '''
    Black Scholes Formula
    
    '''
    d1 = (log(S/X)+(r+v*v/2.)*T)/(v*sqrt(T))

    d2 = d1-v*sqrt(T)
    if CallPutFlag=='c':

        return S*CND(d1)-X*exp(-r*T)*CND(d2)

    else:
        return X*exp(-r*T)*CND(-d2)-S*CND(-d1)
        
        