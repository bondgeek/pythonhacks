#ifndef __PYX_HAVE__dateparser
#define __PYX_HAVE__dateparser


/* "dateparser.pyx":36
 *             "by", self.height, "cubits."
 * 
 * cdef public enum otherstuff:             # <<<<<<<<<<<<<<
 *     sausage=1
 *     eggs=2
 */
enum otherstuff {
  sausage = 1,
  eggs = 2,
  lettuce = 4
};

#ifndef __PYX_HAVE_API__dateparser

#ifndef __PYX_EXTERN_C
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

#endif /* !__PYX_HAVE_API__dateparser */

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC initdateparser(void);
#else
PyMODINIT_FUNC PyInit_dateparser(void);
#endif

#endif /* !__PYX_HAVE__dateparser */
