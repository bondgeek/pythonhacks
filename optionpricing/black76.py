from scipy.stats import norm
import numpy as np

def black76(expry, F, X, r, vol):
    d1 = (np.log(F/X)-(0.5*(vol**2)*expry))/(vol*np.sqrt(expry))   
    pv = np.exp(-r * expry)

    nd1 = norm.cdf(d1)

    c = pv*(F*norm.cdf(d1) - X*norm.cdf(d1 - vol * np.sqrt(expry)))

    return (c, d1, pv, nd1, pv*nd1)
