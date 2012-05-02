from libcpp.vector cimport vector

from cython.operator cimport dereference as deref

import numpy as np
cimport numpy as cnp

cdef extern from 'boost/shared_ptr.hpp' namespace 'boost':

    cdef cppclass shared_ptr[T]:
        shared_ptr()
        shared_ptr(T*)
        shared_ptr(shared_ptr[T]&)
        T* get()
        long use_count()
        #void reset(shared_ptr[T]&)

ctypedef vector[double] dVect
ctypedef vector[double*] pVect
ctypedef vector[shared_ptr[double]] spVect

def myvect(myarray not None):

    cdef vector[double] *_myvect = new vector[double]()
    for x in myarray:
        print("pushing %s" % x)
        _myvect.push_back(x)
    
    print("now...\nsize: %s" % _myvect.size())
    print("%s %s" % (_myvect.front(), _myvect.back())  )
    for i in range(_myvect.size()):
        print("%s, %s" % (i, deref(_myvect).at(i)))

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

cdef class Test1:    
    cdef spVect* _thisptr
    
    def __cinit__(self):
        print("cinit")
        self._thisptr = NULL
        
    def __dealloc__(self):
        print("dealloc")
        if self._thisptr is not NULL:
            self._thisptr = NULL
                
    def __init__(self, myarray not None):
        print("init")
        cdef cnp.ndarray a = np.array(myarray)
        cdef vector[double] p
        cdef int ndim = a.ndim
        cdef int dim = a.shape[0]
        cdef int i
        
        if ndim > 1:
            print("bad input")
        
        for i from 0 <= i < dim:
            p.push_back(myarray[i])
        
        self._thisptr = new spVect()
        
        for i from 0 <= i < dim:
            print("pushing: %s %s" % (i, p[i]))
            deref(self._thisptr).push_back( deref(new shared_ptr[double](&p[i])) )
            
        print("check")
        for i from 0 <= i < self._thisptr.size():
                print(">> %s: %s" % (i, deref(deref(self._thisptr)[i].get()) ))
    
    property items:
        def __get__(self):
            cdef int i
            a = []
            
            for i from 0 <= i < self._thisptr.size():
                print(">> %s: %s" % (i, deref(deref(self._thisptr)[i].get()) ))
                a.append( deref(self._thisptr.at(i).get()) )
            return a              

    property size:
        def __get__(self):
            return self._thisptr.size()
    
    def get_items(self):
        cdef int i
        a = []
        
        for i from 0 <= i < self._thisptr.size():
            print(">> %s: %s" % (i, deref(deref(self._thisptr)[i].get()) ))
            a.append( deref(self._thisptr.at(i).get()) )
        return a      
        
        
cdef class Test2:    
    cdef pVect* _thisptr
    
    def __cinit__(self):
        #self._thisptr = NULL
        print("cinit")
        self._thisptr = new pVect()
        
    def __dealloc__(self):
        print("dealloc")
        if self._thisptr is not NULL:
            self._thisptr = NULL
                
    def __init__(self, myarray not None):
        print("init")
        cdef cnp.ndarray a = np.array(myarray)
        cdef double *p = <double *>a.data
        cdef int ndim = a.ndim
        cdef int dim = a.shape[0]
        cdef int i
        
        if ndim > 1:
            print("bad input")

        for i from 0 <= i < dim:
            print("pushing: %s %s" % (i, p[i]))
            deref(self._thisptr).push_back( &p[i] )
            
        print("check")
        for i from 0 <= i < self._thisptr.size():
                print(">> %s: %s" % (i, deref(deref(self._thisptr)[i])) )
              
        print("check 2")
        for x in self.items:
            print(">>> %s" % x)

                
    property size:
        def __get__(self):
            return self._thisptr.size()
        

            
           
            
        
        
        