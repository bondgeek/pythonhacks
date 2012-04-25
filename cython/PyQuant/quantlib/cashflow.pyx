
from libcpp.vector cimport vector

from cython.operator cimport dereference as deref
cimport numpy as 
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

    
ctypedef vector[double] Rates

cdef class RateLeg:
    cdef shared_ptr[Rates]* _thisptr
    cpdef Size _size
    
    def __cinit__(self):
        self._thisptr = NULL

    def __dealloc__(self):
        if self._thisptr is not NULL:
            self._thisptr = NULL
            
    def __init__(self, rates):
        assert hasattr(rates, "__iter__"), "Class Leg must be iterable"
        
        self._thisptr = new shared_ptr[Rates](new Rates())
        
        cdef double _rate
        for _rate in rates:
            
            deref(self._thisptr).get().push_back(_rate)
            print("push! %s >>> front/back: %s / %s" % 
                        (_rate, 
                         deref(self._thisptr).get().front(),
                         deref(self._thisptr).get().back())
                 )
        
        self._size = deref(self._thisptr).get().size()
        print("\ngo")
        print("size %s " % self._size)
        for i in range(self._size):
            r = deref(self._thisptr).get().at(i)
            print(">>%s %s " % (i, r))
        
    property size:
        def __get__(self):
            return self._size

ctypedef vector[double*] PRates

cdef class PRateLeg:
    cdef shared_ptr[PRates]* _thisptr
    cpdef Size _size
    
    def __cinit__(self):
        self._thisptr = NULL

    def __dealloc__(self):
        if self._thisptr is not NULL:
            self._thisptr = NULL
            
    def __init__(self, rates):
        assert hasattr(rates, "__iter__"), "Class Leg must be iterable"
        
        self._thisptr = new shared_ptr[PRates](new PRates())
        
        # TODO: use numpy
        # http://wiki.cython.org/WrappingNumpy
        cdef int i
        cdef int _rsize = len(rates)
        cdef double* _rates = <double *>rates
        for i in range(_rsize):
            deref(self._thisptr).get().push_back(_rate[i])
            
            print("push! %s  >> front/back: %s / %s" % 
                        (rates[i],
                         deref(deref(self._thisptr).get().front()),
                         deref(deref(self._thisptr).get().back())) 
                  )
        
        self._size = deref(self._thisptr).get().size()
        print("\ngo")
        print("size %s " % self._size)
        for i in range(self._size):
            r = deref(self._thisptr).get().at(i)
            print(">>%s %s " % (i, deref(r)))
        
    property size:
        def __get__(self):
            return self._size    
    dbg = """
    property items:
        def __get__(self):
            cdef int i
            cdef Rates _rates
            item_list = []
            
            for i in range(self.size):
                _rates = deref(self._thisptr.get())
                r = deref(_rates[i].get())
                print("r %s " % r)
                item_list.append(r)
                
            return item_list
    """     
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
        