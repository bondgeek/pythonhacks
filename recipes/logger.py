#!/usr/bin/env python
from __future__ import with_statement

from bgprod.bglogger import getBGLogger

bglogger = getBGLogger("testlog")

for i in range(20):
    bglogger.info('count i = %d' % i)

bglogger.file_handler.doRollover()

bglogger.log(10, "rolled")

