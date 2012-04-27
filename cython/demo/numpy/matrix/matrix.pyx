from libcpp.vector cimport vector

from cython.operator cimport dereference as deref

import numpy as np
cimport numpy as cnp

ctypedef vector[double] dVect
ctypedef vector[double*] pVect

def mysum(cnp.ndarray a not None):
    cdef double *p = <double *>a.data
    cdef int ndim = a.ndim
    cdef int dim = a.shape[0]
    cdef double s=0
    
    if ndim > 1:
        print("Warning strange results for ndim: %s" % ndim)
        
    for i from 0 <= i < dim:
        s += p[i]
        
    p[0] = 13.
    return s
    

def mysum2(a not None):
    
    a = np.array(a)
    return mysum(a)
    
    
def mysum3(myarray not None):
        
    cdef cnp.ndarray a = np.array(myarray)
    cdef double *p = <double *>a.data
    cdef int ndim = a.ndim
    cdef int dim = a.shape[0]
    cdef double s=0
    
    if ndim > 1:
        print("Warning strange results for ndim: %s" % ndim)
        
    for i from 0 <= i < dim:
        s += p[i]
        
    p[0] = 13.
    return s

cdef class summer:    
    cdef pVect* _thisptr
    
    def __cinit__(self):
        #self._thisptr = NULL
        self._thisptr = new pVect()
        
    def __dealloc__(self):
        if self._thisptr is not NULL:
            self._thisptr = NULL
                
    def __init__(self, myarray not None):
        cdef cnp.ndarray a = np.array(myarray)
        cdef double *p = <double *>a.data
        cdef int ndim = a.ndim
        cdef int dim = a.shape[0]
        cdef int i
        
        if ndim > 1:
            print("bad input")
        
        #self._thisptr = new pVect()
        for i from 0 <= i < dim:
            print("pushing: %s %s" % (i, p[i]))
            self._thisptr.push_back(&p[i])
            
        print("check")
        for i from 0 <= i < self._thisptr.size():
                print(">> %s: %s" % (i, deref(self._thisptr.at(i))))
              
        print("check 2")
        for x in self.items:
            print(">>> %s" % x)
                
    property size:
        def __get__(self):
            return self._thisptr.size()
        
    property items:
        def __get__(self):
            cdef int i
            a = []
            
            for i from 0 <= i < self.size:
                print(">> %s: %s" % (i, deref(self._thisptr.at(i))))
                a.append(deref(self._thisptr.at(i)))
            return a
            
           
            
        
        
        