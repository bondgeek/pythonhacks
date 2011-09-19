import os

from tempfile import mkstemp

fd, fpath = mkstemp(dir="sandbox", suffix=".xls")
	
try:
    os.close(fd)

finally:
    os.unlink(fpath) # get rid of it

