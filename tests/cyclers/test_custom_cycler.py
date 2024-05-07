"""
Contains unittests for the custom cyclers
"""

__all__ = ["TestCustomCycler"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by Moin Ahmed. All Rights Reserved"

import unittest
import numpy as np

from SPPy.cycler.custom import CustomCycler


class TestCustomCycler(unittest.TestCase):
    t_array = np.arange(5)
    I_array = np.array([-1.656, 0, -1.656, 0, -2*1.656])
    V_min = 2.5
    V_max = 4.2

    def test_constructor1(self):
        cycler = CustomCycler(array_t=self.t_array, array_I=self.I_array, V_min=self.V_min, V_max=self.V_max)
        self.assertEqual(0.0, cycler.time_elapsed)
        self.assertEqual(1.0, cycler.SOC_LIB)

        self.assertTrue(np.array_equal(self.t_array, cycler.array_t))
        self.assertTrue(np.array_equal(self.I_array, cycler.array_I))
        self.assertEqual(self.V_min, cycler.V_min)

        with self.assertRaises(ValueError) as context:
            CustomCycler(array_t=self.t_array, array_I=np.array([0]), V_min=self.V_min, V_max=self.V_max)

    def test_constructor2(self):
        cycler = CustomCycler(array_t=self.t_array, array_I=self.I_array, V_min=self.V_min, V_max=self.V_max,
                              SOC_LIB=1.0)
        self.assertEqual(0.0, cycler.time_elapsed)
        self.assertEqual(1.0, cycler.SOC_LIB)

        self.assertTrue(np.array_equal(self.t_array, cycler.array_t))
        self.assertTrue(np.array_equal(self.I_array, cycler.array_I))


    def test_get_current_method(self):
        cycler = CustomCycler(array_t=self.t_array, array_I=self.I_array, V_min=self.V_min, V_max=self.V_max)
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.1))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.2))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.3))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.5))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.7))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.9))

        self.assertEqual(self.I_array[1], cycler.get_current(step_name='discharge', t=1))
        self.assertEqual(self.I_array[1], cycler.get_current(step_name='discharge', t=1.5))
        self.assertEqual(self.I_array[1], cycler.get_current(step_name='discharge', t=1.99))

        self.assertEqual(self.I_array[-2], cycler.get_current(step_name='discharge', t=3))
        self.assertEqual(self.I_array[-2], cycler.get_current(step_name='discharge', t=3.5))
        self.assertEqual(self.I_array[-2], cycler.get_current(step_name='discharge', t=3.99))

        self.assertEqual(self.I_array[-1], cycler.get_current(step_name='discharge', t=4.1))




