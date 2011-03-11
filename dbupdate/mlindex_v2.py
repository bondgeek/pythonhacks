#! /usr/bin/env python

from datetime import date

from alprion import DROPBOX, DATADIR, PathJoin
from bgpy.xldb import XLdb, xl_to_date, xlValue, xlrd

import alprion.db.marketdb as marketdb

timeseries = marketdb.Timeseries
series = marketdb.Series
instruments = marketdb.Instruments

def read_sheet1(book, sheet_index):
    datemode = book.datemode
    
    sh = book.sheet_by_index(sheet_index)
    ncolumns = sh.ncols
    
    #utility function
    cleanrow_ = lambda row_: [x if x is not '' else None for x in row_]
    xlCellValue = lambda cell_: xlValue(cell_, datemode, 1)
    
    qdata = {}
    for rowx in range(sh.nrows):
        try:
            xr = map(xlCellValue, sh.row(rowx))
        except:
            print("problem in row: %s\n%s" % (rowx, sh.row(rowx)))
            continue
        else:
            xrvalues = cleanrow_(xr)
            
            if xrvalues:
                if type(xrvalues[0]) == str:
                    if xrvalues[0].find("Index") == 0:
                        key = xrvalues[1].strip()
                        qdata[key] = {}
        
                elif type(xrvalues[0]) == date:
                    if xrvalues[1]:
                        qdata[key][xrvalues[0]] = xrvalues[1:]
                    else:
                        # if there are gaps in the data, reset
                        # because ML resets the cumm index to 100 when
                        # it starts again.
                        qdata[key] = {}
    
    return qdata

def updatedb(idxdata, hdr):
    
    hdr_idx = [series.get(label=h)[0].id for h in hdr]

    for key in idxdata.keys():
        instr_id = instruments.get(ticker=key)[0].id
        
        for dt in idxdata[key]:
            rowx = idxdata[key][dt]
            for idx in hdr_idx:
                ts = timeseries(date = dt, 
                                instruments_id=instr_id,
                                series_id=idx,
                                value = rowx[idx-1])
                ts.save()

if __name__ == "__main__":

    indexfile = PathJoin(DROPBOX, "MarketData", "Benchmarks", "IndexData.xls")
     
    # data structure
    hdr = ['TRIDX', 'PRIDX', 'AvgMty', 'MtyW',   'MDur', 'MDurW',
           'YTM',   'YTW',   'NumIss', 'ParVal', 'Cpn',  'CpnMV']

    book = xlrd.open_workbook(indexfile, on_demand=True)
    
    wtr = read_sheet1(book, 6)
    
    updatedb(wtr, hdr)