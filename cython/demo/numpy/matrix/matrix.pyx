
import numpy as np
cimport numpy as cnp

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
    
