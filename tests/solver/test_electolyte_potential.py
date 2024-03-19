import unittest

import numpy as np

from SPPy.calc_helpers.constants import Constants
from SPPy.solvers.co_ordinates import FVMCoordinates
from SPPy.solvers.electrolyte_potential import ElectrolytePotentialFVMSolver


class TestElectrolytePotentialFVMSolver(unittest.TestCase):
    # Parameters values are obtained from the Shangwoo et al.
    L_n = 81e-6
    L_s = 20e-6
    L_p = 78e-6

    epsilon_en = 0.264
    epsilon_esep = 0.46
    epsilon_ep = 0.281
    e_s_n = 0.68
    e_s_p = 0.65
    R_n = 6e-6
    R_p = 5e-6
    a_s_n = 3 * e_s_n / R_n
    a_s_p = 3 * e_s_p / R_p
    t_c = 0.38
    kappa_e = 1.194
    brugg = 1.5
    temp = 298.15

    instance_coords = FVMCoordinates(L_n=L_n, L_s=L_s, L_p=L_p, num_grid_n=5, num_grid_s=5, num_grid_p=5)
    instance_solver = ElectrolytePotentialFVMSolver(fvm_coords=instance_coords,
                                                    epsilon_en=epsilon_en, epsilon_esep=epsilon_esep,
                                                    epsilon_ep=epsilon_ep,
                                                    a_s_n=a_s_n, a_s_p=a_s_p,
                                                    t_c=t_c, kappa_e=kappa_e, brugg=brugg, temp=temp)

    def test_constructor(self):
        actual_array_x = np.array([8.100e-06, 2.430e-05, 4.050e-05, 5.670e-05, 7.290e-05, 8.300e-05, 8.700e-05,
                                   9.100e-05, 9.500e-05, 9.900e-05, 1.088e-04, 1.244e-04, 1.400e-04, 1.556e-04,
                                   1.712e-04])
        self.assertTrue(np.allclose(actual_array_x, self.instance_solver.coords.array_x))
        self.assertEqual(-2 * Constants.R * self.temp * self.kappa_e * (self.t_c - 1) / Constants.F,
                         self.instance_solver.kappa_D)

    def test_kappa_eff_e(self):
        array_actual = np.append(0.16196091330066031 * np.ones(5),
                                 np.append(0.3725126919931722 * np.ones(5), 0.17785406944761203 * np.ones(5)))

        self.assertTrue(np.array_equal(array_actual, self.instance_solver.array_kappa_eff))

    def test_epsilon_kappa_D_eff(self):
        array_actual = np.append(-0.00515981 * np.ones(5),
                                 np.append(-0.01186765 * np.ones(5),
                                 -0.00566614 * np.ones(5)))

        self.assertTrue(np.allclose(-array_actual, self.instance_solver.array_kappa_D_eff))

    def test_array_a_s(self):
        array_actual = np.append(self.a_s_n * np.ones(5),
                                 np.append(np.zeros(5), self.a_s_p * np.ones(5)))
        self.assertTrue(np.array_equal(array_actual, self.instance_solver.array_a_s))

    def test_m_(self):
        self.assertAlmostEqual(-9997.587037037038, self.instance_solver._m_phi_e()[0,0], places=3)
        self.assertAlmostEqual(9997.587037037038, self.instance_solver._m_phi_e()[0,1], places=3)

        self.assertAlmostEqual(11400.901887667458, self.instance_solver._m_phi_e()[-1, -2])
        self.assertAlmostEqual(-11400.901887667458, self.instance_solver._m_phi_e()[-1, -1], places=3)

    def test_vec_phi_e(self):
        array_c_e = 1000 * np.ones(len(self.instance_coords.array_x))

        j_n = 2.51e-5 * np.ones(5)
        j_p = -2.27e-5 * np.ones(5)
        array_j = np.append(j_n, np.append(np.zeros(5), j_p))

        print(self.instance_solver._vec_phi_e(j=array_j, c_e=array_c_e))

    def test_solve(self):
        array_c_e = 1000 * np.ones(len(self.instance_coords.array_x))

        j_n = 2.51e-5 * np.ones(5)
        j_p = -2.27e-5 * np.ones(5)
        array_j = np.append(j_n, np.append(np.zeros(5), j_p))
        print(array_j)

        print(self.instance_solver.solve_phi_e(j=array_j, c_e=array_c_e))
