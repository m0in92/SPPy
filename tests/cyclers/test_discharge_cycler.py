import numpy as np
import unittest

from SPPy.cycler.discharge import Discharge, CustomDischarge


class TestDischargeCycler(unittest.TestCase):
    discharge_current = 1.5
    V_min = 2.5
    dc = Discharge(discharge_current=discharge_current, v_min=V_min, SOC_LIB_min=0, SOC_LIB=0)

    def test_constructor(self):
        self.assertEqual(-self.discharge_current, self.dc.discharge_current)
        self.assertEqual(self.V_min, self.dc.v_min)
        self.assertEqual(0.0, self.dc.time_elapsed)
        self.assertEqual('discharge', self.dc.cycle_steps[0])

    def test_get_current(self):
        self.assertEqual(-self.discharge_current, self.dc.get_current(step_name=self.dc.cycle_steps[0]))

class TestCustomDischargeCycler(unittest.TestCase):
    def test_constructor(self):
        t_array = np.array([0,1,2])
        I_array = np.array([1,1,1])
        V_min = 2.5
        dc = CustomDischarge(t_array=t_array, I_array=I_array, V_min=V_min)
        self.assertTrue(np.array_equal(t_array, dc.t_array))
        self.assertTrue(np.array_equal(-I_array, dc.I_array))
        self.assertEqual(V_min, dc.V_min)
        self.assertEqual(0.0, dc.time_elapsed)
        self.assertEqual('discharge', dc.cycle_steps[0])
        self.assertEqual(2.0, dc.t_max)

    def test_get_current(self):
        pass