# Cython imports
from cython.operator cimport dereference as deref
from libcpp cimport bool

cimport _bonds #fixme :should move the PricingEngine declaration somewhere else
cimport _exercise
cimport _option
cimport _payoffs
from quantlib.pricingengines cimport _pricing_engine as _pe

from quantlib.handle cimport shared_ptr
from quantlib.instruments.payoffs cimport Payoff, PlainVanillaPayoff
from quantlib.time.date cimport Date
from quantlib.pricingengines.vanilla cimport PricingEngine

# Python imports
import logging

logger = logging.getLogger('quantlib')

cdef public enum OptionType:
    Put = _option.Put
    Call = _option.Call

cdef public enum ExerciseType:
    American = _exercise.American
    Bermudan  = _exercise.Bermudan
    European = _exercise.European

EXERCISE_TO_STR = {
    American : 'American',
    Bermudan : 'Bermudan',
    European : 'European'
}

cdef class Exercise:

    def __cinit__(self):
        self._thisptr = NULL


    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr
            logger.debug('Exercise deallocated')

    def __str__(self):
        return 'Exercise type: %s' % EXERCISE_TO_STR[self._thisptr.get().type()]

cdef class EuropeanExercise(Exercise):

    def __init__(self, Date exercise_date):
        self._thisptr = new shared_ptr[_exercise.Exercise]( \
            new _exercise.EuropeanExercise(
                deref(exercise_date._thisptr.get())
            )
        )

cdef class AmericanExercise(Exercise):

    def __init__(self, Date latest_exercise_date, Date earliest_exercise_date=None):
        """ Creates an AmericanExercise.

        :param latest_exercise_date: Latest exercise date for the option
        :param earliest_exercise_date: Earliest exercise date for the option (default to None)

        """
        if earliest_exercise_date is not None:
            self._thisptr = new shared_ptr[_exercise.Exercise]( \
                new _exercise.AmericanExercise(
                    deref(earliest_exercise_date._thisptr.get()),
                    deref(latest_exercise_date._thisptr.get())
                )
            )
        else:
            self._thisptr = new shared_ptr[_exercise.Exercise]( \
                new _exercise.AmericanExercise(
                    deref(latest_exercise_date._thisptr.get())
                )
            )

cdef class VanillaOption:

    cdef _option.VanillaOption* _thisptr
    cdef public bool has_pricing_engine

    cdef public Exercise _exercise_ref
    cdef public PlainVanillaPayoff _payoff_ref

    def __cinit__(self):
        self._thisptr = NULL
        self.has_pricing_engine = False
        self._exercise_ref = None
        self._payoff_ref = None

    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr
            logger.debug('Vanilla option deallocated')

    def __str__(self):
        return 'Vanilla option %s %s' % (str(self._exercise_ref), str(self._payoff_ref))

    def __init__(self, PlainVanillaPayoff payoff, Exercise exercise):

        # keep reference to other objects. This prevents them to be deallocated
        # before this object (causing a segfault in the C++ deallocation
        # mechanism). 
        # FIXME: by using shared_ptr in the Exercise and Payoff classes, this
        # should not happend and we could avoid storing those references.
        self._exercise_ref = exercise
        self._payoff_ref = payoff

        # create shared_ptr

        cdef shared_ptr[_payoffs.StrikedTypePayoff] payoff_ptr = \
            shared_ptr[_payoffs.StrikedTypePayoff](
                deref(payoff._thisptr)
        )

        cdef shared_ptr[_exercise.Exercise] exercise_ptr = \
            shared_ptr[_exercise.Exercise](
                deref(exercise._thisptr)
            )

        self._thisptr = new _option.EuropeanOption(payoff_ptr, exercise_ptr)

    def set_pricing_engine(self, PricingEngine engine):
        '''Sets the pricing engine for the option. '''

        cdef shared_ptr[_pe.PricingEngine] engine_ptr = \
                shared_ptr[_pe.PricingEngine](
                    deref(engine._thisptr)
                )

        self._thisptr.setPricingEngine(engine_ptr)
        self.has_pricing_engine = True

    property net_present_value:
        """ Option net present value. """
        def __get__(self):
            if self.has_pricing_engine:
                return self._thisptr.NPV()


