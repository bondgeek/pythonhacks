
from libcpp cimport bool
from libcpp.string cimport string
from cython.operator cimport dereference as deref

cdef extern from "_dateparser.hpp" namespace "DP":
    cdef string year(string date)


cpdef int mydate(char *_date):
    cdef string *datestr = new string(_date)
    cdef string nyear = year(deref(datestr))
    
    return int(nyear.c_str())
   
def sdate(int _date):
    s = str(_date)
    _s = <char *>s
    cdef string *datestr = new string(_s)
    cdef string nyear = year(deref(datestr))
    
    return int(nyear.c_str())   

cdef class Shrubbery:

    cdef int width, height
        		
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def describe(self):
        print "This shrubbery is", self.width, \
            "by", self.height, "cubits."

cdef public enum otherstuff:
    sausage=1
    eggs=2
    lettuce=4

cdef class spamdish:
    cdef int oz_of_spam
    cdef otherstuff filler