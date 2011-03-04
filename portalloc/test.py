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

#initial estimate
vol0 = np.var(U)

def ewma_est(L_, sigma_, xret_):
    return L_ * sigma_ + (1. - L_) * xret_ * xret_

def likelihood(sigma_, xret_):
    return -(np.log(sigma_) + (xret_ * xret_) / sigma_)

def mle(L_, rets):
    pass
    