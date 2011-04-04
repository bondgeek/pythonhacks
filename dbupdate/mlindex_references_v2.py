from alprion import DROPBOX, DATADIR, PathJoin
from bgpy.xldb import XLdb, xl_to_date, xlValue, xlrd

import alprion.db.marketdb as marketdb

instruments = marketdb.Instruments
series = marketdb.Series

def update_tickers(tickers_):
    for key in tickers_.refcolumn:
        rowx = instruments.get(ticker=key)
        
        if not rowx:
            rowx = instruments(ticker=key)
        else:
            rowx = rowx[0]
            
        rowx.name = name=tickers_[key]['Name']
        rowx.bbgkey = 'IND'
        rowx.source = 'BBG IND Function'
        
        rowx.save()
        
def update_columns(col_header):
    for h in col_header:
        rowx = series.get(label=h)
        
        if not rowx:
            rowx = series(label=h)
        else:
            rowx = rowx[0]
        
        rowx.name = h + " ML Index"
        rowx.save()
    
if __name__ == "__main__":
    
    indexfile = PathJoin(DROPBOX, "MarketData", "Benchmarks", 
                          "MLIndexData.xls")
         
    mltickers = XLdb(indexfile, sheet_index=1, startrow=0)
    
    # data structure
    hdrdata = XLdb(indexfile, sheet_index=0, startrow=0)
    hdr = [hdrdata[x]['HDR'] for x in hdrdata.refcolumn]
    
    #update_tickers(mltickers)
    
    update_columns(hdr)