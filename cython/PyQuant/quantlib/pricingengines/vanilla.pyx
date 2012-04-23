include '../types.pxi'

from cython.operator cimport dereference as deref
from quantlib.handle cimport shared_ptr
cimport quantlib.processes._black_scholes_process as _bsp
cimport quantlib.models.equity._bates_model as _bm

from quantlib.models.equity.heston_model cimport HestonModel
from quantlib.models.equity.bates_model cimport (BatesModel, BatesDetJumpModel, BatesDoubleExpModel, BatesDoubleExpDetJumpModel)
from quantlib.processes.black_scholes_process cimport GeneralizedBlackScholesProcess

cdef class PricingEngine:
    """ Base class for all the pricing engines

    TODO: move this class in its own module
    """

    def __cinit__(self):
        self._thisptr = NULL

    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr

cdef class VanillaOptionEngine(PricingEngine):

    def __cinit__(self):
        self._thisptr = NULL
        self.process = None


cdef class AnalyticEuropeanEngine(VanillaOptionEngine):

    def __init__(self, GeneralizedBlackScholesProcess process):

        cdef shared_ptr[_bsp.GeneralizedBlackScholesProcess] process_ptr = \
            shared_ptr[_bsp.GeneralizedBlackScholesProcess](
                deref(process._thisptr)
            )

        self.process = process
        self._thisptr = new shared_ptr[_vanilla.PricingEngine](\
            new _vanilla.AnalyticEuropeanEngine(process_ptr)
        )

cdef class BaroneAdesiWhaleyApproximationEngine(VanillaOptionEngine):

    def __init__(self, GeneralizedBlackScholesProcess process):

        cdef shared_ptr[_bsp.GeneralizedBlackScholesProcess] process_ptr = \
            shared_ptr[_bsp.GeneralizedBlackScholesProcess](
                deref(process._thisptr)
            )

        self.process = process
        self._thisptr = new shared_ptr[_vanilla.PricingEngine](
            new _vanilla.BaroneAdesiWhaleyApproximationEngine(process_ptr)
        )

cdef class AnalyticHestonEngine(PricingEngine):

    def __init__(self, HestonModel model, int integration_order=144):

        self._thisptr = new shared_ptr[_vanilla.PricingEngine](
            new _vanilla.AnalyticHestonEngine(
                deref(model._thisptr),
                <Size>integration_order
            )
        )

cdef class BatesEngine(AnalyticHestonEngine):

    def __init__(self, BatesModel model, int integration_order=144):

        self._thisptr = new shared_ptr[_vanilla.PricingEngine](
            new _vanilla.BatesEngine(
                deref(<shared_ptr[_bm.BatesModel]*> model._thisptr),
                <Size>integration_order
            )
        )

cdef class BatesDetJumpEngine(BatesEngine):

    def __init__(self, BatesDetJumpModel model, int integration_order=144):

        self._thisptr = new shared_ptr[_vanilla.PricingEngine](
            new _vanilla.BatesDetJumpEngine(
                deref(<shared_ptr[_bm.BatesDetJumpModel]*> model._thisptr),
                <Size>integration_order))

cdef class BatesDoubleExpEngine(AnalyticHestonEngine):

    def __init__(self, BatesDoubleExpModel model, int integration_order=144):

        self._thisptr = new shared_ptr[_vanilla.PricingEngine](
            new _vanilla.BatesDoubleExpEngine(
                deref(<shared_ptr[_bm.BatesDoubleExpModel]*> model._thisptr),
                <Size>integration_order))

cdef class BatesDoubleExpDetJumpEngine(BatesDoubleExpEngine):

    def __init__(self, BatesDoubleExpDetJumpModel model, int integration_order=144):

        self._thisptr = new shared_ptr[_vanilla.PricingEngine](
            new _vanilla.BatesDoubleExpDetJumpEngine(
                deref(<shared_ptr[_bm.BatesDoubleExpDetJumpModel]*> model._thisptr),
                <Size>integration_order))
