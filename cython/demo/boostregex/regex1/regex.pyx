from libcpp cimport bool
from cython.operator cimport dereference as deref

cdef extern from 'boost/shared_ptr.hpp' namespace 'boost':

    cdef cppclass shared_ptr[T]:
        shared_ptr()
        shared_ptr(T*)
        shared_ptr(shared_ptr[T]&)
        T* get()
        long use_count()
        #void reset(shared_ptr[T]&)

cdef extern from 'boost/regex.hpp' namespace 'boost';
    
    cdef cppclass match_results[T]:
        match_results(T&)
        
        # size:
       long size() const
       bool empty() const
       
       # element access:
       const_reference operator[](int n) 

        