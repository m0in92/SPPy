import unittest

import numpy as np

import SPPy
from SPPy.sol_and_visualization.solution import SolutionInitializer


class TestSolutionInitializer(unittest.TestCase):
    def test_constructor(self):
        """
        Tests for default values in case of class initialization.
        """
        sol = SolutionInitializer()
        self.assertEqual([], sol.lst_cycle_num)
        self.assertEqual([], sol.lst_cycle_step)
        self.assertEqual([], sol.lst_t)
        self.assertEqual([], sol.lst_I)
        self.assertEqual([], sol.lst_V)
        self.assertEqual([], sol.lst_x_surf_p)
        self.assertEqual([], sol.lst_x_surf_n)
        self.assertEqual([], sol.lst_cap)
        self.assertEqual([], sol.lst_cap_charge)
        self.assertEqual([], sol.lst_cap_discharge)
        self.assertEqual([], sol.lst_battery_cap)
        self.assertEqual([], sol.lst_temp)
        self.assertEqual([], sol.lst_R_cell)
        self.assertEqual([], sol.lst_j_tot)
        self.assertEqual([], sol.lst_j_i)
        self.assertEqual([], sol.lst_j_s)

        # spatial electrolyte related quantities
        self.assertEqual(None, sol.electrolyte_conc)


class TestSolution(unittest.TestCase):
    def test_classmethod_read_from_arrays(self):
        t: np.ndarray = np.linspace(0, 100)
        i_app: np.ndarray = -1.656 * np.ones(len(t))
        v: np.ndarray = 4.2 * np.ones(len(t))
        temp: np.ndarray = 298.15 * np.ones(len(t))
        soc_p: np.ndarray = 0.7 * np.ones(len(t))
        soc_n: np.ndarray = 0.4 * np.ones(len(t))

        sol: SPPy.Solution = SPPy.Solution.read_from_arrays(t=t, i_app=i_app, v=v, temp=temp,
                                                            soc_p=soc_p, soc_n=soc_n)

        self.assertTrue(np.array_equal(t, sol.t))
        self.assertTrue(np.array_equal(i_app, sol.I))
        self.assertTrue(np.array_equal(v, sol.V))
        self.assertTrue(np.array_equal(soc_p, sol.x_surf_p))
        self.assertTrue(np.array_equal(soc_n, sol.x_surf_n))
