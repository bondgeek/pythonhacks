from libcpp cimport bool
from cython.operator cimport dereference as deref

cdef extern from "_dateparser.hpp" namespace "DP":
    cdef int year(int date)

cdef inline int mydate(int _date):
    cdef int nyear = year(_date)
    return nyear

def test(_date):
    return mydate(_date)