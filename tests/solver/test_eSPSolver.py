import unittest
import numpy as np

import SPPy
from SPPy.solvers.battery_solver import eSPSolver


class TestESPSolver(unittest.TestCase):
    """
    This class contains the test cases for intializing and performing simulations using solver for single particle model
    with electrolyte dynamics
    """
    T = 298.15
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    t = np.arange(0, 4000, 0.1)
    I = -1.656 * np.ones(len(t))
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', soc_lib_init=1.0,
                                                         # SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n,
                                                         temp_init=T)

    def test_constructor(self):
        test_solver = eSPSolver(b_cell=self.test_cell, isothermal=True, degradation=False)

        self.assertEqual(self.test_cell.elec_p.a_s, test_solver.b_cell.elec_p.a_s)
        self.assertEqual(True, test_solver.bool_isothermal)
        self.assertEqual(False, test_solver.bool_degradation)
        self.assertEqual('poly', test_solver.electrode_SOC_solver)
