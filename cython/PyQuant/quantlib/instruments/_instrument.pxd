include '../types.pxi'

from libcpp.vector cimport vector
from libcpp cimport bool

from quantlib.handle cimport shared_ptr
from quantlib.time._date cimport Date
from quantlib.pricingengines._pricing_engine cimport PricingEngine

cdef extern from 'boost/optional.hpp' namespace 'boost':
    cdef cppclass optional[T]:
        optional(T*)

cdef extern from 'ql/instrument.hpp' namespace 'QuantLib':
    cdef cppclass Instrument:
        Instrument()

        Real NPV()
        Date& valuationDate()
        void setPricingEngine(shared_ptr[PricingEngine]&)
