#! /usr/bin/env python

from datetime import date

from alprion import DROPBOX, DATADIR, PathJoin
from bgpy.xldb import XLdb

indexfile = PathJoin(DROPBOX, "MarketData", "Benchmarks", "IndexData.xls")

if 'wtrswr' not in vars():
    wtrswr = XLdb(indexfile, sheet_index=6, idx_column=-1, header=False)

wtrdata = {}
n = 0
for x in wtrswr:
    if not x:
        continue
    if type(x[0]) == str:
        if x[0].find("Index") == 0:
            key = x[1].strip()
            wtrdata[key] = {}
    
    elif type(x[0]) == date:
        wtrdata[key][x[0]] = x[1]

    n += 1