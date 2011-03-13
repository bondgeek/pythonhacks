#! /usr/bin/env python

from datetime import date

from alprion import DROPBOX, DATADIR, PathJoin
from bgpy.xldb import XLdb

import alprion.db.marketdb as marketdb

timeseries = marketdb.Timeseries
series = marketdb.Series
instruments = marketdb.Instruments


if __name__ == "__main__":

    crv_file = PathJoin(DROPBOX, "MarketData/Benchmarks/BBGCurves_static.xls")
    
    curves = [#sheet_index, ticker, outfile
             (0, "USSW", "ussw.out"),
             (2, "BMARATIO", "bmaratio.out"),
             (3, "USSV", "ussv.out"),
             (4, "MMA_AAA", "mma.out"),
             ]
    
    curves = [(n, t, f, 
               instruments.get(ticker=t)[0].id,
               XLdb(crv_file, startrow=4, sheet_index=n)) 
               for n, t, f in curves]
            
    nrow = timeseries.max_id()+1
    
    for sh_num, ticker, filename, instr_id, curvedata in curves:
        tenors = dict( [(tnr, series.from_label(tnr)) 
                        for tnr in curvedata.hdr[1:]] )
        outfile = open(PathJoin(DATADIR, filename), "w") 
    
        for dt in curvedata.refcolumn:
            for tnr in tenors:
                ser_id = tenors[tnr]
                #print nrow, dt, instr_id, ser_id, curvedata[dt][tnr]
                outfile.write("%d,%s,%d,%d,%s\n" % (nrow, 
                                                      dt,
                                                      instr_id,
                                                      ser_id,
                                                      curvedata[dt][tnr]) )
                nrow += 1
    
        print("Rows: %s" % nrow)
        print("Writing file: %s" % outfile.name)
        outfile.close()
        