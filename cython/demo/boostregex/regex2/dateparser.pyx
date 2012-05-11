
from libcpp cimport bool
from libcpp.string cimport string
from cython.operator cimport dereference as deref

cdef extern from "_dateparser.hpp" namespace "DP":
    cdef string year(string date)

def mydate(char *_date):
    cdef string *datestr = new string(_date)
    cdef string nyear = year(deref(datestr))
    
    return int(nyear.c_str())
   
def sdate(int _date):
    s = str(_date)
    _s = <char *>s
    cdef string *datestr = new string(_s)
    cdef string nyear = year(deref(datestr))
    
    return int(nyear.c_str())   
