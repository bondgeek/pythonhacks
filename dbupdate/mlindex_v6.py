#! /usr/bin/env python

from datetime import date

from alprion import DROPBOX, DATADIR, PathJoin
from bgpy.xldb import XLdb, xl_to_date, xlValue, xlrd

import alprion.db.marketdb as marketdb

timeseries = marketdb.Timeseries
series = marketdb.Series
instruments = marketdb.Instruments

def read_sheet2(book, sheet_index, hdr_):
    datemode = book.datemode
    
    sh = book.sheet_by_index(sheet_index)
    ncolumns = sh.ncols

    #utility functions
    cleanrow_ = lambda row_: [x if x is not '' else None for x in row_]
    xlCellValue = lambda cell_: xlValue(cell_, datemode, 1)

    irow = map(xlCellValue, sh.row(0))

    idx = [n for n in range(len(irow)) if irow[n].find("Index") ==0]        
    hdata = [(n, irow[n+1]) for n in idx]

    qdata = dict( [(irow[n+1], {}) for n in idx] )
    
    for rowx in range(2, sh.nrows): 
        try:
            xr = map(xlCellValue, sh.row(rowx))
        except:
            print("problem in row: %s\n%s" % (rowx, sh.row(rowx)))
            continue
        else:
            xrvalues = cleanrow_(xr)
            
            for n, key in hdata:
                if xrvalues[n+1]:
                    qdata[key][xrvalues[n]] = xrvalues[n+1:n+1+len(hdr_)]
                else:
                    # if there are gaps in the data, reset
                    # because ML resets the cumm index to 100 when
                    # it starts again.
                    qdata[key] = {}

    return qdata


def read_sheet1(book, sheet_index):
    datemode = book.datemode
    
    sh = book.sheet_by_index(sheet_index)
    ncolumns = sh.ncols
    
    #utility functions
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

def fileout(idxdata, hdr_, filename="updatedb.csv", mode='a', startkey=1):
    
    hdr_idx = [(n, series.get(label=hdr_[n])[0].id) for n in range(len(hdr_))]
    
    f = open(filename, mode)
    
    key_id = startkey
    for key in idxdata.keys():
        instr_id = instruments.get(ticker=key)[0].id
        print("key/id: %s / %s, rows: %s" % (key, instr_id, key_id))
        
        for dt in idxdata[key]:
            rowx = idxdata[key][dt]
            
            for n, idx in hdr_idx:
                
                f.write("%d,%s,%d,%d,%s\n" % (key_id,
                                                  dt,
                                                  instr_id,
                                                  idx,
                                                  rowx[n]) )
                    
                key_id += 1
    
    print("writing file: %s" % filename)
    f.close()
    
    print("Rows %s" % key_id)
    return key_id
    
def updatedb(idxdata, hdr_):
    
    hdr_idx = [(n, series.get(label=hdr_[n])[0].id) for n in range(len(hdr_))]
    
    key_id = startkey
    for key in idxdata.keys():
        instr_id = instruments.get(ticker=key)[0].id
        print("key/id: %s / %s, rows: %s" % (key, instr_id, key_id))
        
        for dt in idxdata[key]:
            rowx = idxdata[key][dt]
            
            for n, idx in hdr_idx:
                ts = timeseries.get(date = dt, 
                                   instruments_id=instr_id,
                                   series_id=idx)
                if not ts:
                    ts = timeseries(date = dt, 
                                    instruments_id=instr_id,
                                    series_id=idx )
                else:
                    ts = ts[0]
                    
                ts.value = rowx[n]
                ts.save()

    return timeseries.db.conn.lastrowid()
    
if __name__ == "__main__":

    indexfile = PathJoin(DROPBOX, "MarketData", "Benchmarks", 
                         "INDEXUpdate.xls")
                         
    outputfile = PathJoin(DATADIR, "mlindex.out") 
        
    lastkey_id = timeseries.max_id()+1
    print("\n\nStarting with row: %s\n\n" % lastkey_id)
    
    # data structure
    hdrdata = XLdb(indexfile, sheet_index=0, startrow=0)
    hdr = [hdrdata[x]['HDR'] for x in hdrdata.refcolumn]
    print hdr
    
    if 'index_book' not in vars():
        index_book = xlrd.open_workbook(indexfile, on_demand=True)

    fmode = 'w'    
    #print("horizontal")
    #sheets = []
    #for sh in sheets:
    #    sh_data = read_sheet2(index_book, sh, hdr)
    #    lastkey_id = fileout(sh_data, hdr, outputfile, 'w')
    #    fmode = 'a'

    print("vertical")
    #sheets start with 1, sheet0 has column headers
    sheets = [1, 2]
    for sh in sheets:
        sh_data = read_sheet1(index_book, sh)
        lastkey_id = fileout(sh_data, hdr, outputfile, fmode, lastkey_id+1)
        fmode = 'a'
    
    print("\nTo load data in marketdb sqlite3 database: \n%s\n%s" %
         ('  sqlite> .separator ","', 
          '  sqlite> .import Data/mlindex.out timeseries') )
