
from libcpp.vector cimport vector

from cython.operator cimport dereference as deref

cimport _cashflow as _cf
cimport quantlib.time._date as _date

from quantlib.handle cimport shared_ptr
from quantlib.time.date cimport Date, date_from_qldate

from quantlib.handle cimport shared_ptr

cdef class CashFlow:
    """Abstract Base Class.
    
    Use SimpleCashFlow instead
    
    """
    def __cinit__(self):
        self._thisptr = NULL

    def __init__(self):
        raise ValueError(
            'This is an abstract class.'
        )

    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr
  
    property date:
        def __get__(self):
            cdef _date.Date cf_date
            if self._thisptr:
                cf_date = self._thisptr.get().date()
                return date_from_qldate(cf_date)
            else:
                return None
                
    property amount:
        def __get__(self):
            if self._thisptr:
                return self._thisptr.get().amount()
            else:
                return None


cdef class SimpleCashFlow(CashFlow):

    def __init__(self, Real amount, Date cfdate):
        _cfdate = <_date.Date*>((<Date>cfdate)._thisptr.get())
        
        self._thisptr = new shared_ptr[_cf.CashFlow]( \
                            new _cf.SimpleCashFlow(amount,
                                                   deref(_cfdate))
                            )

    def __str__(self):
        return 'Simple Cash Flow: %f, %s' % (self.amount,
                                             self.date)
                                             

cdef class SimpleLeg:
    cdef shared_ptr[_cf.Leg] *_thisptr
    
    def __cinit__(self):
        self._thisptr = NULL

    def __init__(self, leg):
        cdef shared_ptr[_cf.CashFlow] thiscf
        
        self._thisptr = new shared_ptr[_cf.Leg]()
        
        cdef _date.Date *_thisdate
        for i in range(len(leg)):
            _thisamount = leg[i][0]
            _thisdate = <_date.Date*>((<Date>leg[i][1])._thisptr.get())
            print("%s %s" % (_thisamount, date_from_qldate(deref(_thisdate))))
            _thiscf = new shared_ptr[_cf.CashFlow](\
                                new _cf.SimpleCashFlow(_thisamount,
                                                       deref(_thisdate))
                                                  )
            print("amount: %s" % _thiscf.get().amount())

    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr
