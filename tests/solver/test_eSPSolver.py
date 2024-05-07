__all__ = ["TestESPSolver"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All Rights Reserved."
__status__ = "Deployed"

import unittest
import numpy as np

import SPPy
from SPPy.solvers.battery_solver import EnhancedSPSolver
from SPPy.warnings_and_exceptions.custom_exceptions import *


class TestESPSolver(unittest.TestCase):
    """
    This class contains the test cases for initializing and performing simulations using solver for single particle model
    with electrolyte dynamics
    """
    T = 298.15
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    t = np.arange(0, 4000, 0.1)
    I = -1.656 * np.ones(len(t))
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                         soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                         temp_init=T)

    def test_constructor(self):
        test_solver = EnhancedSPSolver(b_cell=self.test_cell, isothermal=True, degradation=False)

        self.assertEqual(self.test_cell.elec_p.a_s, test_solver.b_cell.elec_p.a_s)
        self.assertEqual(True, test_solver.bool_isothermal)
        self.assertEqual(False, test_solver.bool_degradation)
        self.assertEqual('poly', test_solver.electrode_SOC_solver)

        self.assertEqual(7.35e-5 / 10, test_solver.electrolyte_co_ords.dx_n)
        self.assertEqual(2.0e-5 / 10, test_solver.electrolyte_co_ords.dx_s)

        self.assertEqual([], test_solver.sol_init.lst_V)

        c_init: np.ndarray = 1000 * np.ones(30)
        c_init = c_init[np.newaxis, :]
        self.assertTrue(np.array_equal(c_init, test_solver.sol_init.electrolyte_conc[1:]))

    def test_constructor_with_insufficient_parameters(self):
        b_cell: SPPy.BatteryCell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name="test_single_particle_only",
                                                                            soc_init_p=self.SOC_init_p,
                                                                            soc_init_n=self.SOC_init_n,
                                                                            temp_init=self.T)
        with self.assertRaises(InsufficientParameters):
            test_solver = EnhancedSPSolver(b_cell=b_cell, isothermal=True, degradation=False)
