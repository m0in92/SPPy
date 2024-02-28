import unittest

import numpy as np

import SPPy
from SPPy.solvers.degradation_solvers import ROMSEISolver


class TestROMSEISolver(unittest.TestCase):
    def test_method_solve_current(self) -> None:
        # Modelling parameters
        SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al
        temp: float = 298.15

        # Setup battery components
        cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                        soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                        temp_init=temp)
        solver: ROMSEISolver = ROMSEISolver(b_cell=cell)

        # the first test case
        soc: float = 0.01
        ocp: float = 0.64981159
        I_i, I_s = solver.solve_current(SOC_n=soc, OCP_n=ocp, temp=temp, I=1.656)
        self.assertAlmostEqual(1.656, I_i, places=3)
        self.assertAlmostEqual(8.35925983e-12, I_s, places=16)

        # the second case
        soc: float = 0.7568
        ocp: float = 0.07464309895951012
        I_i, I_s = solver.solve_current(SOC_n=soc, OCP_n=ocp, temp=temp, I=1.656)
        self.assertAlmostEqual(1.65599984, I_i, places=6)
        self.assertAlmostEqual(1.55111785e-07, I_s, places=15)
