#! /usr/bin/env python
import sys; sys.path.append("/Users/bartmosley/sandbox")

import bgpy.QL as ql
import bgpy.xldb as xl

from alprion import DATADIR

from bgpy import PathJoin

import numpy as np

data_file = PathJoin(DATADIR, "Benchmarks", "AllocationStudy.xls")
dailyseries = xl.XLdb(data_file, startrow=9, sheet_index=0)

# index values
spx = [dailyseries[dt]['SPX'] for dt in dailyseries.refcolumn
          if dailyseries[dt]['SPX']]

# returns vector
U = [np.log(spx[n]/spx[n-1]) for n in range(1, len(spx))]
#mu = np.average(U)
#U = [u-mu for u in U]

#initial estimate
vol0 = np.var(U)

def ewma(L_, sigma_, xret_):
    return L_ * sigma_ + (1. - L_) * xret_ * xret_

def loglikelihood_x(sigma_, xret_):
    return -(np.log(sigma_) + (xret_ * xret_) / sigma_)

def loglikelihood(L_, ydata, v0_):
    
    variances =[v0_]

    for n in range(1, len(ydata)):
        vnew = ewma(L_, variances[n-1], ydata[n-1])
        
        variances.append(vnew)
    
    ll = [loglikelihood_x(v, r) for v, r in zip(variances, ydata) ]
    for l in ll:
        print l
    return sum([loglikelihood_x(v, r) for v, r in zip(variances, ydata) ])
    
