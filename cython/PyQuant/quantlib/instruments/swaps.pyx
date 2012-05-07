"""
Adaptation of QuantLib/Swaps

"""
import datetime
import numpy as np

cimport _swaps

from cython.operator cimport dereference as deref
from libcpp.vector cimport vector
from libcpp cimport bool as cbool

cimport quantlib.time._date as _date
from quantlib.handle cimport Handle, shared_ptr, RelinkableHandle
from quantlib.time._calendar cimport BusinessDayConvention
from quantlib.time._daycounter cimport DayCounter as QlDayCounter
from quantlib.time._schedule cimport Schedule as QlSchedule
from quantlib.time.calendar cimport Calendar
from quantlib.time.date cimport Date, date_from_qldate
from quantlib.time.schedule cimport Schedule
from quantlib.time.daycounter cimport DayCounter
from quantlib.termstructures.yields._flat_forward cimport YieldTermStructure \
        as ts
from quantlib.termstructures.yields.flat_forward cimport YieldTermStructure

cimport quantlib._cashflow as _cf
cimport quantlib.cashflow as cf
      
cdef class Swap:
    """ Base swap class

    """

    cdef shared_ptr[_swaps.Swap]* _thisptr
    cdef cbool _has_pricing_engine

    def __cinit__(self):
        self._thisptr = NULL
        self._has_pricing_engine = False

    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr
    
    def __init__(self, firstLeg, secondLeg):
        """
        Each Leg is an array of tuples (amount, date)
        
        """
        cdef vector[shared_ptr[_cf.CashFlow]] _leg1
        cdef vector[shared_ptr[_cf.CashFlow]] _leg2
        
        cdef cf.SimpleLeg leg1 = cf.SimpleLeg(firstLeg)
        cdef cf.SimpleLeg leg2 = cf.SimpleLeg(secondLeg)
        
        _leg1 = deref(leg1._thisptr.get())
        _leg2 = deref(leg2._thisptr.get())
        self._thisptr = new shared_ptr[_swaps.Swap]( \
                                new _swaps.Swap(_leg1, _leg2)
                                )
        
        
    property maturity:
        """ Swap maturity date. """
        
        def __get__(self):
            cdef _date.Date maturity_date
            if self._thisptr:
                maturity_date = self._thisptr.get().maturityDate()
                return date_from_qldate(maturity_date)
            return None

bg = '''
cdef class VanillaSwap(Swap):
    """
    VanillaSwap (Type type, Real nominal, const Schedule &fixedSchedule, 
    Rate fixedRate, const DayCounter &fixedDayCount, 
    const Schedule &floatSchedule, 
    const boost::shared_ptr< IborIndex > &iborIndex, Spread spread, 
    const DayCounter &floatingDayCount, 
    boost::optional< BusinessDayConvention > paymentConvention=boost::none)
    """
    def __init__(self,
                Type type, 
                Real nominal, 
                Schedule fixedSchedule, 
                Rate fixedRate, 
                DayCounter fixedDayCount, 
                Schedule floatSchedule, 
                IborIndex iborIndex, 
                Spread spread, 
                DayCounter floatingDayCount, 
                BusinessDayConvention paymentConvention=None
                ):
        pass
        
    '''