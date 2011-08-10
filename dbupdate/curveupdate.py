#! /usr/bin/env python

from datetime import date

from alprion import DROPBOX, DATADIR, PathJoin
from bgpy.xldb import XLdb

import alprion.db.marketdb as marketdb

timeseries = marketdb.Timeseries()
series = marketdb.Series()
instruments = marketdb.Instruments()

if __name__ == "__main__":

    curvefile = PathJoin(DROPBOX, "SharedData/AAAData.xls")
    outfile = open(PathJoin(DATADIR, "aaadata.out"), "w") #NEW file
    
    curvedata = XLdb(curvefile, sheet_index=0)
    
    tenors = [str(n)+"Y" for n in range(1, 31)]
    tenors = dict( [(tnr, series.get(label=tnr)[0].id) for tnr in tenors] )
    
    instr_id = instruments.get(ticker="MMDAAA")[0].id
    
    nrow = timeseries.max_id()
    for dt in curvedata.refcolumn:
        for tnr in tenors:
            nrow += 1
            ser_id = tenors[tnr]

            outfile.write("%d,%s,%d,%d,%s\n" % (nrow, 
                                                  dt,
                                                  instr_id,
                                                  ser_id,
                                                  curvedata[dt][tnr]) )

    print("Rows: %s" % nrow)
    print("Writing file: %s" % outfile.name)
    outfile.close()

    print("\nTo load data in marketdb sqlite3 database: \n%s\n%s" %
             ('  sqlite> .separator ","', 
              '  sqlite> .import Data/mlindex.out timeseries') )
              