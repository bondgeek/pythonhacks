import os
import glob

def collect_ext_dirpaths():
    cython_extension_directories = []
    for dirpath, directories, files in os.walk('quantlib'):
        print 'Path', dirpath

        # skip the settings package
        if dirpath.find('settings') > -1 or dirpath.find('test') > -1:
            continue

        # if the directory contains pyx files, cythonise it
        if len(glob.glob('{}/*.pyx'.format(dirpath))) > 0:
            cython_extension_directories.append(dirpath)

    return cython_extension_directories
    
def ext_dirpaths():
    cython_extension_directories = []
    for dirpath, directories, files in os.walk('quantlib'):
        print 'Path', dirpath

        candidates = glob.glob('{}/*.pyx'.format(dirpath))
        if len(candidates) > 0:
            cython_extension_directories.extend(candidates)

    return cython_extension_directories
    
extract_name = lambda x: x[:-4].replace('/', '.')
pths = ext_dirpaths()
pths_names = [(extract_name(x), [x]) for x in pths]
# this has to be cleaned up for settings and other modules that have more 
# complicated build
ext  = [
 ('quantlib.currency', ['quantlib/currency.pyx']),
 ('quantlib.index', ['quantlib/index.pyx']),
 ('quantlib.quotes', ['quantlib/quotes.pyx']),
# ('quantlib.indexes.euribor', ['quantlib/indexes/euribor.pyx']),
 ('quantlib.indexes.ibor_index', ['quantlib/indexes/ibor_index.pyx']),
 ('quantlib.indexes.interest_rate_index', ['quantlib/indexes/interest_rate_index.pyx']),
# ('quantlib.indexes.libor', ['quantlib/indexes/libor.pyx']),
# ('quantlib.instruments.bonds', ['quantlib/instruments/bonds.pyx']),
# ('quantlib.instruments.option', ['quantlib/instruments/option.pyx']),
# ('quantlib.instruments.payoffs', ['quantlib/instruments/payoffs.pyx']),
 ('quantlib.math.optimization', ['quantlib/math/optimization.pyx']),
# ('quantlib.models.equity.bates_model', ['quantlib/models/equity/bates_model.pyx']),
# ('quantlib.models.equity.heston_model', ['quantlib/models/equity/heston_model.pyx']),
# ('quantlib.pricingengines.blackformula', ['quantlib/pricingengines/blackformula.pyx']),
# ('quantlib.pricingengines.swap', ['quantlib/pricingengines/swap.pyx']),
# ('quantlib.pricingengines.vanilla', ['quantlib/pricingengines/vanilla.pyx']),
# ('quantlib.processes.bates_process', ['quantlib/processes/bates_process.pyx']),
# ('quantlib.processes.black_scholes_process', ['quantlib/processes/black_scholes_process.pyx']),
# ('quantlib.processes.heston_process', ['quantlib/processes/heston_process.pyx']),
 ('quantlib.settings.settings', ['quantlib/settings/settings.pyx']),
# ('quantlib.sim.simulate', ['quantlib/sim/simulate.pyx']),
 ('quantlib.termstructures.volatility.equityfx.black_vol_term_structure', ['quantlib/termstructures/volatility/equityfx/black_vol_term_structure.pyx']),
 ('quantlib.termstructures.yields.flat_forward', ['quantlib/termstructures/yields/flat_forward.pyx']),
 ('quantlib.termstructures.yields.piecewise_yield_curve', ['quantlib/termstructures/yields/piecewise_yield_curve.pyx']),
 ('quantlib.termstructures.yields.rate_helpers', ['quantlib/termstructures/yields/rate_helpers.pyx']),
 ('quantlib.termstructures.yields.yield_term_structure', ['quantlib/termstructures/yields/yield_term_structure.pyx']),
 ('quantlib.termstructures.yields.zero_curve', ['quantlib/termstructures/yields/zero_curve.pyx']),
# ('quantlib.test.test_cython_bug', ['quantlib/test/test_cython_bug.pyx']),
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
 