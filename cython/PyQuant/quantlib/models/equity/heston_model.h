#ifndef __PYX_HAVE__quantlib__models__equity__heston_model
#define __PYX_HAVE__quantlib__models__equity__heston_model


/* "quantlib/models/equity/heston_model.pyx":35
 * )
 * 
 * cdef public enum CALIBRATION_ERROR_TYPE:             # <<<<<<<<<<<<<<
 *     RelativePriceError = _hm.RelativePriceError
 *     PriceError = _hm.PriceError
 */
enum CALIBRATION_ERROR_TYPE {

  /* "quantlib/models/equity/heston_model.pyx":38
 *     RelativePriceError = _hm.RelativePriceError
 *     PriceError = _hm.PriceError
 *     ImpliedVolError = _hm.ImpliedVolError             # <<<<<<<<<<<<<<
 * 
 * cdef class HestonModelHelper:
 */
  RelativePriceError = QuantLib::CalibrationHelper::RelativePriceError,
  PriceError = QuantLib::CalibrationHelper::PriceError,
  ImpliedVolError = QuantLib::CalibrationHelper::ImpliedVolError
};

#ifndef __PYX_HAVE_API__quantlib__models__equity__heston_model

#ifndef __PYX_EXTERN_C
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

#endif /* !__PYX_HAVE_API__quantlib__models__equity__heston_model */

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC initheston_model(void);
#else
PyMODINIT_FUNC PyInit_heston_model(void);
#endif

#endif /* !__PYX_HAVE__quantlib__models__equity__heston_model */
