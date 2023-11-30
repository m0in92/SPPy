"""
Contains test associated with the Django App for SPPy.
"""

import unittest

from django.test import TestCase

from .views import Simulator


class TestSimulatorFromViews(unittest.TestCase):
    instance: Simulator = Simulator(battery_model='SP')

    def test_battery_model_check(self):
        self.assertTrue(self.instance.check_for_valid_battery_models('SP'))
        self.assertTrue(self.instance.check_for_valid_battery_models('ECM'))

        with self.assertRaises(ValueError) as e:
            self.instance.check_for_valid_battery_models('non-sense')


