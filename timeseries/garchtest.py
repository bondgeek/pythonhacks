#! /usr/bin/env python
import sys; sys.path.append("/Users/bartmosley/sandbox")

import matplotlib.pyplot as plt

import bgpy.QL as ql
import bgpy.xldb as xl
from bgpy import PathJoin

import numpy as np
from scipy.optimize import fmin

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
R = [np.log(dow[n]/dow[n-1]) for n in range(1, len(dow))]
mu = np.average(R)
V = np.var(R)
U = [u-mu for u in R]

#initial estimate
vol0 = np.var(U)

def ewma(L_, sigma_, xret_):
    return L_ * sigma_ + (1. - L_) * xret_ * xret_

def gVar(L_, var, ret):
    omega, beta, gamma = L_
    
    return omega + beta*var + gamma*(ret**2)

def loglikelihood_x(sigma_, xret_):
    return -(np.log(sigma_) + (xret_ * xret_) / sigma_)

def gLogLike(parms, ydata):
    mu, beta, gamma = parms
    
    V0 = np.var(ydata)
        
    y = [u - mu for u in ydata]
    
    omega = V0 * (1. - beta - gamma)
    
    variances = [V0]
    for n in range(1, len(y)):
        vnew = gVar((omega, beta, gamma), variances[n-1], y[n-1])
        variances.append(vnew)
        
    return -sum([loglikelihood_x(v, r) for v, r in zip(variances, y) ])
    
def ewmaLogLike(L_, ydata, v0_):
    l = L_[0]
    
    variances =[v0_]
    for n in range(1, len(ydata)):
        vnew = ewma(l, variances[n-1], ydata[n-1])        
        variances.append(vnew)

    return -sum([loglikelihood_x(v, r) for v, r in zip(variances, ydata) ])

def ewmaLogLike2(L_, ydata):
    mu, l = L_
    V0 = np.var(ydata)
        
    y = [u - mu for u in ydata]
    
    variances =[V0]
    for n in range(1, len(ydata)):
        vnew = ewma(l, variances[n-1], y[n-1])        
        variances.append(vnew)

    return -sum([loglikelihood_x(v, r) for v, r in zip(variances, y) ])

# solve for smoothing factor in ewma estimate
ewmaEst = fmin(ewmaLogLike2, [0., .86], args=(U, ), xtol=1e-8)
ewmaVarEst = [ V ]
for n in range(len(U)):
    ewmaVarEst.append( ewma(ewmaEst[1], ewmaVarEst[n-1], U[n-1]) )

ewmaVolEst = [np.sqrt(v*252) for v in ewmaVarEst]

garchEst = fmin(gLogLike, [.0, .5, .5], args=(R, ), xtol=1e-8)
mu, beta, gamma = garchEst
gVarEst = [V]
for n in range(len(U)):
    omega = V * (1. - beta - gamma)
    gVarEst.append( gVar((omega, beta, gamma), gVarEst[n-1], R[n-1]) )

gVolEst = [np.sqrt(v*252) for v in gVarEst]

plt.plot(gVolEst)
plt.plot(ewmaVolEst)
plt.show()
