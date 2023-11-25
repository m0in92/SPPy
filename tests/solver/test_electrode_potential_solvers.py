import unittest

import numpy as np

from SPPy.calc_helpers.constants import Constants
from SPPy.solvers.co_ordinates import FVMCoordinates
from SPPy.solvers.electrode_potential import ElectrodePotentialFVMSolver


class TestElectrodePotentialFVMSolver(unittest.TestCase):
    # Parameters values are obtained from the Shangwoo et al.
    L_n = 81e-6
    L_s = 20e-6
    L_p = 78e-6

    e_s_n = 0.68
    e_s_p = 0.65
    R_n = 6e-6
    R_p = 5e-6
    a_s_n = 3 * e_s_n / R_n
    a_s_p = 3 * e_s_p / R_p

    instance_coords = FVMCoordinates(L_n=L_n, L_s=L_s, L_p=L_p, num_grid_n=5, num_grid_s=5, num_grid_p=5)

    # The instance below has the realistic parameter values for the NMC electrode
    instance_p = ElectrodePotentialFVMSolver(fvm_coords=instance_coords, electrode_type='p',
                                             a_s=a_s_p, sigma_eff=1.57)
    # The instance below has realistic input parameters values for the graphite electrode
    instance_n = ElectrodePotentialFVMSolver(fvm_coords=instance_coords, electrode_type='n',
                                             a_s=a_s_n, sigma_eff=56.074)

    def test_constructor(self):
        dx = self.instance_p.coords[2] - self.instance_p.coords[1]
        self.assertAlmostEqual(dx, self.instance_p.dx)

    def test_M_phi_s(self):
        actual_p = np.array([[-1., 1., 0., 0., 0.],
                             [1., -2., 1., 0., 0.],
                             [0., 1., -2., 1., 0.],
                             [0., 0., 1., -2., 1.],
                             [0., 0., 0., 1., -3.]])
        actual_n = np.array([[-3., 1., 0., 0., 0.],
                             [1., -2., 1., 0., 0.],
                             [0., 1., -2., 1., 0.],
                             [0., 0., 1., -2., 1.],
                             [0., 0., 0., 1., -1.]])
        self.assertTrue(np.array_equal(actual_p, self.instance_p._M_phi_s))
        self.assertTrue(np.array_equal(actual_n, self.instance_n._M_phi_s))

    def test_array_j(self):
        dx = self.instance_p.dx

        # The flux [mol m-2 s-1] below is when a current of 1A is applied during discharge.
        j = -5.679e-6 * np.ones(5)  # row vector
        self.assertTrue(
            np.allclose(dx ** 2 * Constants.F * self.instance_p.a_s * j.reshape(-1, 1) / self.instance_p.sigma_eff,
                        self.instance_p._array_j(j=j)))

        j = j.reshape(-1, 1)  # column vector
        self.assertTrue(
            np.array_equal(dx ** 2 * Constants.F * self.instance_p.a_s * j.reshape(-1, 1) / self.instance_p.sigma_eff,
                           self.instance_p._array_j(j=j)))

    def test_array_V(self):
        actual_p = np.array([0, 0, 0, 0, 4.2]).reshape(-1, 1)
        actual_n = np.array([0, 0, 0, 0, 0]).reshape(-1, 1)

        self.assertTrue(np.array_equal(actual_p, self.instance_p._array_V(terminal_potential=4.2)))
        self.assertTrue(np.array_equal(actual_n, self.instance_n._array_V()))

    def test_solve_for_relative_potential(self):
        # Below solves for the relative potential in the positive electrode
        # The flux [mol m-2 s-1] below is when a current of 2.627A is applied during discharge.
        j_n = 2.51e-5 * np.ones(5)
        j_p = -2.27e-5 * np.ones(5)

        array_actual_relative_potential_n = np.array([[-9.63451689e-06], [-2.50497439e-05], [-3.66111642e-05],
                                                      [-4.43187777e-05], [-4.81725844e-05]])
        array_actual_relative_potential_p = np.array([[0.00165508], [0.00152267], [0.00125786], [0.00086064],
                                                      [0.00033102]])

        self.assertTrue(np.allclose(array_actual_relative_potential_n,
                                    self.instance_n.solve_phi_s(j=j_n)))
        self.assertTrue(np.allclose(array_actual_relative_potential_p,
                                    self.instance_p.solve_phi_s(j=j_p, terminal_potential=0.0), atol=1e-8))
