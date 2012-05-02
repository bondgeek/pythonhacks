include 'types.pxi'


from libcpp.vector cimport vector

from cython.operator cimport dereference as deref

cimport _cashflow as _cf
cimport quantlib.time._date as _date

from quantlib.handle cimport shared_ptr
from quantlib.time.date cimport Date, date_from_qldate

from quantlib.handle cimport shared_ptr

cdef class CashFlow:
    cdef shared_ptr[_cf.CashFlow]* _thisptr
    
cdef class SimpleCashFlow(CashFlow):
    pass

