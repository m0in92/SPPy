"""
Contains test associated with the Django App for SPPy.
"""

import unittest

from django.test import TestCase, Client

from .views import Simulator


class TestSimulatorFromViews(unittest.TestCase):
    instance: Simulator = Simulator(battery_model='SP')

    def test_constructor(self):
        pass

    def test_battery_model_check(self):
        self.assertTrue(self.instance.check_for_valid_battery_models('SP'))
        self.assertTrue(self.instance.check_for_valid_battery_models('ECM'))

        with self.assertRaises(ValueError) as e:
            self.instance.check_for_valid_battery_models('non-sense')


class TestIndexPage(TestCase):
    def test_response(self):
        """
        Tests for an OK HTTP status codes on home and about.
        """
        client: Client = Client()
        self.assertEqual(client.get('').status_code, 200)
        self.assertEqual(client.get('/').status_code, 200)


class TestBatterySimulationPages(TestCase):
    """
    Tests for an OK HTTP status codes on pages pertaining to battery cell simulations.
    """
    def test_response(self):
        client: Client = Client()
        self.assertEqual(client.get('/api/batterysim/sp').status_code, 200)  # sp
        self.assertEqual(client.get('/api/batterysim/ecm').status_code, 200)  # ecm

