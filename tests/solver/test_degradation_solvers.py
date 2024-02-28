import unittest

import numpy as np

import SPPy
from SPPy.solvers.degradation_solvers import ROMSEISolver


class TestROMSEISolver(unittest.TestCase):
    def test_method_solve_current(self) -> None:
        # instantiating the solver class below
        SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al
        temp: float = 298.15
        cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                        soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                        temp_init=temp)
        solver: ROMSEISolver = ROMSEISolver(b_cell=cell)

        # tests below
        ## the first test case
        soc: float = 0.01
        ocp: float = 0.64981159
        I_i, I_s = solver.solve_current(soc=soc, ocp=ocp, temp=temp, I=1.656)
        self.assertAlmostEqual(1.656, I_i, places=3)
        self.assertAlmostEqual(8.35925983e-12, I_s, places=16)

        ## the second case
        soc: float = 0.7568
        ocp: float = 0.07464309895951012
        I_i, I_s = solver.solve_current(soc=soc, ocp=ocp, temp=temp, I=1.656)
        self.assertAlmostEqual(1.65599984, I_i, places=6)
        self.assertAlmostEqual(1.55111785e-07, I_s, places=15)

    def test_method_solve_delta_L(self) -> None:
        # instantiating the solver class below
        SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al
        temp: float = 298.15

        cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                        soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                        temp_init=temp)
        solver: ROMSEISolver = ROMSEISolver(b_cell=cell)

        # tests below
        j_s: float = -1.55111785e-7 / (96487 * 0.7824)
        delta_L: float = solver.solve_delta_L(j_s=j_s, dt=0.1)
        self.assertAlmostEqual(2.049977783e-17, delta_L, places=18)

    def test_method_update_delta_L(self) -> None:
        # instantiating the solver class below
        SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al
        temp: float = 298.15

        cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                        soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                        temp_init=temp)
        solver: ROMSEISolver = ROMSEISolver(b_cell=cell)

        # tests below
        self.assertEqual(0.0, solver.L)
        j_s: float = -1.55111785e-7 / (96487 * 0.7824)
        solver.update_L(j_s=j_s, dt=0.1)
        self.assertAlmostEqual(2.049977783e-17, solver.L, places=18)

    def test_method_delta_R_SEI(self) -> None:
        # instantiating the solver class below
        SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et. al.
        temp: float = 298.15

        cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                        soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                        temp_init=temp)
        solver: ROMSEISolver = ROMSEISolver(b_cell=cell)

        # tests below
        solver: ROMSEISolver = ROMSEISolver(b_cell=cell)
        j_s: float = -1.55111785e-7 / (96487 * 0.7824)
        self.assertAlmostEqual(6.879127e-11, solver.solve_delta_R_SEI(j_s=j_s, dt=0.1), places=12)

    def test_class_magic_call_method(self):
        # instantiating the solver class below
        SOC_INIT_P, SOC_INIT_N = 0.4956, 0.7568  # conditions in the literature source. Guo et al
        temp: float = 298.15

        cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                        soc_init_p=SOC_INIT_P, soc_init_n=SOC_INIT_N,
                                                        temp_init=temp)
        solver: ROMSEISolver = ROMSEISolver(b_cell=cell)

        # tests below
        soc: float = 0.7568
        ocp: float = 0.07464309895951012
        temp: float = 298.15
        i_app: float = 1.656
        dt: float = 0.1

        self.assertEqual(0.0, solver.R_SEI)
        I_i, I_s, delta_R_SEI = solver(soc=soc, ocp=ocp, temp=temp, i_app=i_app, dt=dt)
        self.assertAlmostEqual(1.65599984, I_i, places=6)
        self.assertAlmostEqual(1.55111785e-07, I_s, places=15)
        self.assertAlmostEqual(6.879127e-11, delta_R_SEI, places=12)
        self.assertAlmostEqual(6.879127e-11, solver.R_SEI, places=12)
