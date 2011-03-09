import numpy as np
from scipy.optimize import fmin

def garch_var(parms, variance, observed_value):
    '''
    GARCH variance estimate
    
    parms:          GARCH parameters
    variance:       previous variance estimate
    observed_value: previous observed value.
    
    '''
    omega, alpha, beta = parms

    return omega + alpha*variance + beta*observed_value*observed_value

def loglikelihood_x(variance, observed):
    '''
    Log Likelihood of observation, for zero-mean normal probability 
    distribution function.
    
    '''
    return -(np.log(variance) + (observed * observed) / variance)

def arch_loglike(parms, ydata, V0=None):
    '''
    Log likelihood function for GARCH estimation.
    
    parms:  mu, alpha, [beta]  
            mu: long term drft
            alpha: first persistence parameter
            beta: if only two parameters are given
                  model is assumed to be EWMA, beta=(1-alpha)
            
            NOTE: model constrains gamma = (1-alpha-beta) > 0.
            
    ydata:  timeseries to be fitted via mle
    V0:     long run variance
    
    '''
    # if no long term variance estimate is given, use sample variance
    V0 = np.var(ydata) if not V0 else V0
    
    if len(parms) > 2:
        mu, alpha, beta = parms
        
        # if omega is negative, use EWMA (i.e. omega = 0.)
        omega = np.max( (0., V0 * (1.0 - beta - alpha)) )
        
    else:
        mu, alpha = parms
        
        omega = 0.0
        beta = (1. - alpha)
        
    # use estimate of drift to normalize data
    y = [u - mu for u in ydata]
    
    # create time series of variance estimates, 
    # set initial value to long term variance
    variances = [V0]
    for n in range(1, len(y)):
        variances.append( garch_var((omega, alpha, beta), variances[n-1], y[n-1]) )
         
    return -sum([loglikelihood_x(v, r) for v, r in zip(variances, y) ])
 
def garch_estimator(yseries, x0):
    '''
    MLE estimation of GARCH parameters and drift for time series
    
    yseries:    time series vector
    x0:         mu, alpha, beta
                initial guess of parameter values
                mu: long term drft
                alpha: first persistence parameter
                beta: if only two parameters are given
                      model is assumed to be EWMA, beta=(1-alpha)
            
                NOTE: model constrains gamma = (1-alpha-beta) > 0.   
    
    returns a dictionary with keys:
    v:          time series of variance estimates
    mu:         drift estimate
    garch:      estimated GARCH parameters
    
    Uses scipy.optimize.fmin to minimize the negative of the likelihood function.
    
    '''
    # sample variance 
    var0 = np.var(yseries)
    
    # maximum likelihood estimates of GARCH parameters
    mleEst = fmin(arch_loglike, x0, args=(yseries, var0), xtol=1e-8)
    if len(x0) > 2:
        mu, alpha, beta = mleEst    
        omega = var0 * (1. - alpha - beta)
    else:
        mu, alpha = mleEst    
        omega = 0.
        beta = (1. - alpha)
        
    variance_est = [var0]
    for n in range(len(yseries)):
        variance_est.append( garch_var((omega, alpha, beta), 
                                       variance_est[n-1], 
                                       yseries[n-1]) )
    
    return {'v': variance_est, 'mu': mu, 'garch': (omega, alpha, beta)}

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    import sys; sys.path.append("/Users/bartmosley/sandbox")
    import bgpy.xldb as xl
    from bgpy import PathJoin

    from alprion import DATADIR
    
    # data files
    spx_file = PathJoin(DATADIR, "Benchmarks", "AllocationStudy.xls")
    spxdaily = xl.XLdb(spx_file, startrow=9, sheet_index=0)
    
    dow_file = PathJoin(DATADIR, "Benchmarks", "dow.xls")
    dowdaily = xl.XLdb(dow_file, sheet_index=0)
    
    # index values
    if 'spx' not in vars():
        spx = [spxdaily[dt]['SPX'] for dt in spxdaily.refcolumn
                  if spxdaily[dt]['SPX']]
              
        dow = [dowdaily[dt]['Dow'] for dt in dowdaily.refcolumn
                  if dowdaily[dt]['Dow']]
              
    # returns vector
    retseries = [np.log(dow[n]/dow[n-1]) for n in range(1, len(dow))]
    
    print("\nEWMA Estimates")
    ewmaVarEst = garch_estimator(retseries,  [0., .86])
    ewmaVolEst = [np.sqrt(v*252) for v in ewmaVarEst['v']]
    print("\nResults\ndrift: %s" % ewmaVarEst['mu'])
    print("lambda: %s" % ewmaVarEst['garch'][1])
    
    print("\nGARCH Estimates")
    gVarEst = garch_estimator(retseries, [0., .5, .5])
    gVolEst = [np.sqrt(v*252) for v in gVarEst['v']]
    print("\nResults\ndrift: %s" % gVarEst['mu'])
    print("alpha: %s \nbeta: %s \ngamma: %s" % (gVarEst['garch'][1],
                                                gVarEst['garch'][2],
                                                gVarEst['garch'][0]))

    #plot results
    plt.plot(gVolEst)
    plt.plot(ewmaVolEst)
    plt.show()
