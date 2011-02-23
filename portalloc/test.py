import bgpy.QL as ql
import bgpy.xldb as xl

from alprion import DATADIR

from bgpy import PathJoin

import numpy as np

returns_file = PathJoin(DATADIR, "Benchmarks", "AllocationStudy.xls")
returns = xl.XLdb(returns_file, sheet_index=1)


spx_tr = [returns[dt]['SPXTotalReturn'] for dt in returns.refcolumn
          if returns[dt]['SPXTotalReturn']]
leh_tr = [returns[dt]['LEHAGG_TR'] for dt in returns.refcolumn
          if returns[dt]['LEHAGG_TR']]

spx_x = [returns[dt]['SPXExcess'] for dt in returns.refcolumn
          if returns[dt]['SPXExcess']]
leh_x = [returns[dt]['LEHExcess'] for dt in returns.refcolumn
          if returns[dt]['LEHExcess']]


X = np.vstack((spx_tr, leh_tr))
C = np.cov(X)

m = np.array((np.average(spx_tr), np.average(leh_tr)))

