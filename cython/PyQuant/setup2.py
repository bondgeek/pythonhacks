import os
import sys
import glob

import numpy

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

if sys.platform == 'darwin':
    INCLUDE_DIRS = ['/usr/local/include', '.'] + [numpy.get_include()]
    LIBRARY_DIRS = ["/usr/local/lib"]

def collect_ext_dirpaths():
    cython_extension_directories = []
    for dirpath, directories, files in os.walk('quantlib'):
        print 'Path', dirpath

        # skip the settings package
        if (dirpath.find('settings') > -1 or 
           dirpath.find('test') > -1 or 
           dirpath.find('termstructures') > -1):
            print(">>Skipping %s" % dirpath)
            continue

        # if the directory contains pyx files, cythonise it
        if len(glob.glob('{}/*.pyx'.format(dirpath))) > 0:
            cython_extension_directories.append(dirpath)

    return cython_extension_directories

extension_paths  = [
 ('quantlib.version', ['quantlib/version.pyx']),
 ('quantlib.currency', ['quantlib/currency.pyx']),
 ('quantlib.index', ['quantlib/index.pyx']),
 ('quantlib.cashflow', ['quantlib/cashflow.pyx']),
 ('quantlib.quotes', ['quantlib/quotes.pyx']),
 ('quantlib.indexes.euribor', ['quantlib/indexes/euribor.pyx']),
 ('quantlib.indexes.ibor_index', ['quantlib/indexes/ibor_index.pyx']),
 ('quantlib.indexes.interest_rate_index', [
            'quantlib/indexes/interest_rate_index.pyx']),
 ('quantlib.indexes.libor', ['quantlib/indexes/libor.pyx']),
 ('quantlib.instruments.bonds', ['quantlib/instruments/bonds.pyx']),
 ('quantlib.instruments.payoffs', ['quantlib/instruments/payoffs.pyx']),
 ('quantlib.instruments.option', ['quantlib/instruments/option.pyx']),
 ('quantlib.instruments.swaps', ['quantlib/instruments/swaps.pyx']),
 ('quantlib.math.optimization', ['quantlib/math/optimization.pyx']),
 ('quantlib.models.equity.bates_model', ['quantlib/models/equity/bates_model.pyx']),
 ('quantlib.models.equity.heston_model', ['quantlib/models/equity/heston_model.pyx']),
 ('quantlib.pricingengines.blackformula', ['quantlib/pricingengines/blackformula.pyx']),
 ('quantlib.pricingengines.swap', ['quantlib/pricingengines/swap.pyx']),
 ('quantlib.pricingengines.vanilla', ['quantlib/pricingengines/vanilla.pyx']),
 ('quantlib.processes.bates_process', ['quantlib/processes/bates_process.pyx']),
 ('quantlib.processes.black_scholes_process', ['quantlib/processes/black_scholes_process.pyx']),
 ('quantlib.processes.heston_process', ['quantlib/processes/heston_process.pyx']),
 ('quantlib.settings', [
            'quantlib/settings/settings.pyx', 'quantlib/settings/ql_settings.cpp'
            ]),
 ('quantlib.sim.simulate', [
            'quantlib/sim/simulate.pyx',
            'quantlib/sim/_simulate_support_code.cpp'
        ]),
 ('quantlib.termstructures.volatility.equityfx.black_vol_term_structure', [
            'quantlib/termstructures/volatility/equityfx/black_vol_term_structure.pyx'
            ]),
 ('quantlib.termstructures.yields.flat_forward', [
            'quantlib/termstructures/yields/flat_forward.pyx'
            ]),
 ('quantlib.termstructures.yields.piecewise_yield_curve', [
            'quantlib/termstructures/yields/piecewise_yield_curve.pyx',
            'quantlib/termstructures/yields/_piecewise_support_code.cpp'
            ]),
 ('quantlib.termstructures.yields.yield_term_structure', ['quantlib/termstructures/yields/yield_term_structure.pyx']),
 ('quantlib.termstructures.yields.zero_curve', ['quantlib/termstructures/yields/zero_curve.pyx']),
 ('quantlib.termstructures.yields.rate_helpers', ['quantlib/termstructures/yields/rate_helpers.pyx']),
 ('quantlib.test.test_cython_bug', [
            'quantlib/test/test_cython_bug.pyx', 
            'quantlib/settings/ql_settings.cpp'
            ]),
 ('quantlib.time.calendar', ['quantlib/time/calendar.pyx']),
 ('quantlib.time.date', ['quantlib/time/date.pyx']),
 ('quantlib.time.daycounter', ['quantlib/time/daycounter.pyx']),
 ('quantlib.time.schedule', ['quantlib/time/schedule.pyx']),
 ('quantlib.time.calendars.germany', ['quantlib/time/calendars/germany.pyx']),
 ('quantlib.time.calendars.null_calendar', ['quantlib/time/calendars/null_calendar.pyx']),
 ('quantlib.time.calendars.united_kingdom', ['quantlib/time/calendars/united_kingdom.pyx']),
 ('quantlib.time.calendars.united_states', ['quantlib/time/calendars/united_states.pyx']),
 ('quantlib.time.daycounters.actual_actual', ['quantlib/time/daycounters/actual_actual.pyx']),
 ('quantlib.time.daycounters.thirty360', ['quantlib/time/daycounters/thirty360.pyx'])]
 
print("\nCythonizing...\n")    
collected_extensions = cythonize(
        [Extension(
                extname, # name of extension
                sources=extsources, #  our Cython source
                include_dirs=INCLUDE_DIRS,
                library_dirs=LIBRARY_DIRS,
                libraries = ['QuantLib'], # libraries to link
                language="c++") # causes Cython to create C++ source
        for extname, extsources in extension_paths
        ]
        )


extensions = collected_extensions
print("\nAll the extensions are gathered:")
for ext in extensions:
    print ext.name
print("\n\nBeginning\n\n")

setup(name="quantlib",
      ext_modules=extensions,  
      cmdclass={'build_ext': build_ext})