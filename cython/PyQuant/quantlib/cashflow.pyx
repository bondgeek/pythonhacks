
from libcpp.vector cimport vector

from cython.operator cimport dereference as deref

cimport _cashflow as _cf
cimport quantlib.time._date as _date

from quantlib.handle cimport shared_ptr
from quantlib.time.date cimport Date, date_from_qldate

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


cdef class Leg:

    def __cinit__(self):
        self._thisptr = NULL

    def __dealloc__(self):
        if self._thisptr is not NULL:
            self._thisptr = NULL
    
    def __init__(self, cashFlows):
        assert hasattr(cashFlows, "__iter__"), "Class Leg must be iterable"
        
        cdef _cf.Leg leg
        cdef shared_ptr[_cf.CashFlow]  _cashflow
        
        self._thisptr = new _cf.Leg(len(cashFlows))
        cdef CashFlow cash_flow
        for cash_flow in cashFlows:
            print("-push")
            self._thisptr.push_back(deref(cash_flow._thisptr))
        
        print("done")
        leg = deref(self._thisptr)
        self._size = leg.size()
        print "size:: ", self._size
        
        cdef int i
        cdef _cf.CashFlow _thiscf
        for i in range(self._size):
            _cashflow = leg[i]
            
        
    property size:
        def __get__(self):
            return self._size

dbg = """   

        
    def cashflow(self, int n):
        cdef _cf.Leg _thisleg = deref(self._thisptr)
        cdef shared_ptr[_cf.CashFlow] _thiscf 
        cdef _date.Date cf_date
        print("amount")
        _thiscf = _thisleg[1]
        cf_amount = _thiscf.get().amount()
        print("cf_amount %s" % cf_amount)
        print("date")
        cf_date = _thiscf.get().date()
        print(">> %s " % date_from_qldate(cf_date))
        print("5")
        return (cf_amount, date_from_qldate(cf_date))
        """
        