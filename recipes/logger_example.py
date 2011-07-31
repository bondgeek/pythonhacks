#!/usr/bin/env python
from __future__ import with_statement

import logging
import logging.handlers


LOG_FILE_HDL = '/tmp/logging_example.out'
mylogger = logging.getLogger("MyLogger")
mylogger.setLevel(logging.DEBUG)

ch_handler = logging.StreamHandler()
ch_handler.setLevel(logging.DEBUG+1)

mylogger.addHandler(ch_handler)

handler = logging.handlers.TimedRotatingFileHandler(
            LOG_FILE_HDL, 'M', 1, backupCount=6)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("%(asctime)s--%(levelname)s--%(message)s")) 

mylogger.addHandler(handler)

mylogger.log(logging.DEBUG+1, "begin")

for i in range(20):
    mylogger.debug('count i = %d' % i)

#handler.doRollover()

mylogger.log(logging.INFO, "rolled")

logging.shutdown()
