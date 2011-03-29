from bgpy.xldb import XLdb
from alprion import DROPBOX, PathJoin, DATADIR

from bgpy.math.garch import GARCH

import numpy as np
import scipy as sp
import scipy.stats as ss
import scipy.linalg as sl

studybook = PathJoin(DROPBOX, 
                     "MarketData/Benchmarks", 
                     "mlindex_study_v2.xls")

if 'studydata' not in vars():
    studydata = XLdb(studybook, 
                     sheet_name="Summary", 
                     startrow=9, 
                     idx_column=1)

rkeys = ['TRCoreLong', 
          'TRCoreLong Int', 
          'TRCoreIntermediate',
          'TRCoreShort Int',
          'TRCoreShort',
          'TRRiskLong',
          'TRRiskLong Int',
          'HTRCoreLong', 
          'HTRCoreLong Int', 
          'HTRCoreIntermediate',
          'HTRCoreShort Int',
          'HTRCoreShort',
          'HTRRiskLong',
          'HTRRiskLong Int'
          ]


rdata = [[] for k in rkeys]
covmtx = {}
for dt in studydata.refcolumn[1:]:
    
    for n in range(len(rkeys)):
        k = rkeys[n]
        rdata[n].append(studydata[dt][k])        

    if len(rdata[0]) > 30:
        covmtx[dt] = np.cov(rdata)

fdfd =  [studydata[dt]['FDFD'] for dt in studydata.refcolumn[1:]]
