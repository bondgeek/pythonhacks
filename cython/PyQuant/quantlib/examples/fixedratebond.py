from quantlib.instruments.bonds import (
    FixedRateBond, ZeroCouponBond
)
from quantlib.time.calendar import (
    TARGET, Unadjusted, ModifiedFollowing, Following
)
from quantlib.time.calendars.united_states import (
    UnitedStates, GOVERNMENTBOND
)
from quantlib.time.calendars.null_calendar import NullCalendar
from quantlib.compounding import Compounded, Continuous
from quantlib.time.date import (
    Date, Days, Semiannual, January, August, Period, March, February,
    Jul, Annual, Years
)
from quantlib.time.daycounter import Actual365Fixed
from quantlib.time.daycounters.actual_actual import ActualActual, Bond, ISMA
from quantlib.time.schedule import Schedule, Backward
from quantlib.settings import Settings
from quantlib.termstructures.yields.api import (
    FlatForward, YieldTermStructure
)

def test_pricing_bond():
       '''Inspired by the C++ code from http://quantcorner.wordpress.com/.'''

       settings = Settings()

       # Date setup
       calendar = TARGET()

       # Settlement date
       settlement_date = calendar.adjust(Date(28, January, 2011))

       # Evaluation date
       fixing_days = 1
       settlement_days = 1

       todays_date = calendar.advance(
           settlement_date, -fixing_days, Days
       )

       settings.evaluation_date = todays_date

       # Bound attributes
       face_amount = 100.0
       redemption = 100.0
       issue_date = Date(27, January, 2011)
       maturity_date = Date(31, August, 2020)
       coupon_rate = 0.03625
       bond_yield = 0.034921

       discounting_term_structure = YieldTermStructure(relinkable=True)
       flat_term_structure = FlatForward(
           reference_date = settlement_date,
           forward        = bond_yield,
           daycounter     = Actual365Fixed(), #actual_actual.ActualActual(actual_actual.Bond),
           compounding    = Compounded,
           frequency      = Semiannual)
       # have a look at the FixedRateBondHelper to simplify this
       # construction
       discounting_term_structure.link_to(flat_term_structure)


       #Rate
       fixed_bond_schedule = Schedule(
           issue_date,
           maturity_date,
           Period(Semiannual),
           UnitedStates(market=GOVERNMENTBOND),
           Unadjusted,
           Unadjusted,
           Backward,
           False);


       bond = FixedRateBond(
           settlement_days,
           face_amount,
           fixed_bond_schedule,
           [coupon_rate],
           ActualActual(Bond),
           Unadjusted,
           redemption,
           issue_date
       )

       bond.set_pricing_engine(discounting_term_structure)
       
       return bond
       
if __name__ == "__main__":

    b = test_pricing_bond()
    
    print("Bond: \nAccrued: %s" % b.accrued_amount())