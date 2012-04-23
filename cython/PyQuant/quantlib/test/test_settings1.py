import unittest

#from quantlib.instruments.bonds import FixedRateBond
from quantlib.time.api import (
    Date, Days, August, Period, Jul, Annual, today, Years, TARGET,
    Unadjusted, Schedule, ModifiedFollowing, Backward, ActualActual, ISMA,
    Following
)

from quantlib.settings import Settings

class SettingsTestCase(unittest.TestCase):

    def test_using_settings(self):

        settings = Settings()

        evaluation_date = today()

        # have to set the evaluation date before the test as it is a global
        # attribute for the whole library ... meaning that previous test_cases
        # might have set this to another date
        settings.evaluation_date = evaluation_date

        self.assertTrue(
            evaluation_date == settings.evaluation_date
        )

        self.assertTrue(settings.version.startswith('1'))

    def test_settings_instance_method(self):

        Settings.instance().evaluation_date = today()

        self.assertEquals(
                today(),
                Settings.instance().evaluation_date
        )

