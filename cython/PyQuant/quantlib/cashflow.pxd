include 'types.pxi'

cimport _cashflow as _cf

from libcpp.vector cimport vector

from quantlib.handle cimport shared_ptr

cdef class CashFlow:
    cdef shared_ptr[_cf.CashFlow]* _thisptr
    
cdef class SimpleCashFlow(CashFlow):
    pass

cdef class Leg:
    cdef _cf.Leg* _thisptr
    cdef Size _size
    