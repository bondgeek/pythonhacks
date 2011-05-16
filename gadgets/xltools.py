from bgpy.xldb import XLOut
from alprion import PathJoin, DROPBOX, DATADIR, HOMEPATH

fout = PathJoin(HOMEPATH, "sandbox/excelVBA", "linktothis.xls")

wkb = XLOut(fout, overwrite_ok=True)

wkb.write('a', 2, 0)

wkb.save()
