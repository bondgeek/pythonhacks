#!/usr/bin/env python
import logging
import logging.handlers

LOG_FILE = '/tmp/logging_example_basic.out'

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

logging.debug('This message will go to debub log file')
#appends to file if run repeatedly


LOG_FILE_HDL = '/tmp/logging_example.out'
mylogger = logging.getLogger("MyLogger")
mylogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(
            LOG_FILE_HDL, maxBytes=2000, backupCount=5)

mylogger.addHandler(handler)

for i in range(20):
    mylogger.debug('i = %d' % i)
    
