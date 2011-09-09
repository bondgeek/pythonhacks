#! /usr/bin/env python
from os import path

import bgpy.QL as QL

from bgpy.xldb import XLOut
from alprion import DROPBOX, SHAREDDATA

dt = QL.Date(1, 1, 1988)

fileout = XLOut(path.join(DROPBOX, "Analysis", 'HolidayHistory.xls'))

calendars = (QL.USGovernmentBond,
             QL.USNYSE,
             QL.UnitedStates())

nullCal = QL.TARGET()

enddt = QL.Date(31, 12, 2049)

row_n = 1
while dt <= enddt:
    dt = nullCal.advance(dt, 1, QL.Days, QL.Following)
    
    fileout.write(QL.toPyDate(dt), row_n, 0, 0, format="date")
    
    for col_n in range(len(calendars)):
        fileout.write(calendars[col_n].isBusinessDay(dt), row_n, col_n+1, 0)

    row_n += 1

print("\nNumber of rows: %s" % row_n)
fileout.save()

