from libcpp cimport bool
from cython.operator cimport dereference as deref

cdef extern from "_dateparser.hpp" namespace "DP":
    cdef int year(int date)


def myyear(_date):
    nyear = year(_date)
    
    return nyear