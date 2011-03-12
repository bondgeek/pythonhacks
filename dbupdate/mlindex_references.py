from alprion import DROPBOX, DATADIR, PathJoin
from bgpy.xldb import XLdb, xl_to_date, xlValue, xlrd

import alprion.db.marketdb as marketdb

indexfile = PathJoin(DROPBOX, "MarketData", "Benchmarks", "IndexData.xls")
# data structure
hdr = ['TRIDX', 'PRIDX', 'AvgMty', 'MtyW',   'MDur', 'MDurW',
       'YTM',   'YTW',   'NumIss', 'ParVal', 'Cpn',  'CpnMV']
          
mltickers = XLdb(indexfile, sheet_index=0, startrow=0)

instruments = marketdb.Instruments
series = marketdb.Series

for key in mltickers.refcolumn:
    rowx = instruments.get(ticker=key)
    
    if not rowx:
        rowx = instruments(ticker=key)
    else:
        rowx = rowx[0]
        
    rowx.name = name=mltickers[key]['Name']
    rowx.bbgkey = 'IND'
    rowx.source = 'BBG IND Function'
    
    rowx.save()

for h in hdr:
    rowx = series.get(label=h)
    
    if not rowx:
        rowx = series(label=h)
    else:
        rowx = rowx[0]
    
    rowx.name = h + " ML Index"
    rowx.save()
    
    