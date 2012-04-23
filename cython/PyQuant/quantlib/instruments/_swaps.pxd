include '../types.pxi'

from libcpp cimport bool
from libcpp.vector cimport vector

cimport quantlib._cashflow as _cf

from _instrument cimport Instrument, optional

from quantlib.handle cimport shared_ptr, Handle
from quantlib.time._calendar cimport BusinessDayConvention, Calendar
from quantlib.time._date cimport Date
from quantlib.time._daycounter cimport DayCounter
from quantlib.time._schedule cimport Schedule
from quantlib.indexes.ibor_index cimport IborIndex
from quantlib.termstructures.yields._flat_forward cimport YieldTermStructure
from quantlib.pricingengines._pricing_engine cimport PricingEngine
     
cdef extern from 'ql/instruments/swap.hpp' namespace 'QuantLib':
    cdef cppclass Swap(Instrument):
        #TODO: add constructors
        Swap (_cf.Leg& firstLeg, _cf.Leg& secondLeg)
        
        bool isExpired()
        
        #Additional interface prototypes
        Date startDate()
        Date maturityDate()
        Real 	legBPS(Size j)
        Real 	legNPV(Size j)
        DiscountFactor startDiscounts(Size j)
        DiscountFactor endDiscounts(Size j) 
        DiscountFactor npvDateDiscount() 
        _cf.Leg& leg(Size j)

dbg = '''
cdef extern from 'ql/instruments/vanillaswap.hpp' namespace 'QuantLib':
    cdef cppclass VanillaSwap(Swap):
            
        VanillaSwap(Type type, 
                    Real nominal, 
                    Schedule& fixedSchedule, 
                    Rate fixedRate, 
                    DayCounter& fixedDayCount, 
                    Schedule& floatSchedule, 
                    shared_ptr[IborIndex]& iborIndex, 
                    Spread spread, 
                    DayCounter& floatingDayCount, 
                    optional[BusinessDayConvention] paymentConvention
                    )
        '''