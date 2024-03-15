import unittest

import numpy as np

from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates
from SPPy.solvers.electrolyte_conc import ElectrolyteConcFVMSolver


class TestElectrolyteFVMCoordinates(unittest.TestCase):
    instance = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)

    def test_array_xn(self):
        self.assertEqual(8e-5 / 10, self.instance.dx_n)
        self.assertAlmostEqual(4e-6, self.instance.array_x_n[0])
        self.assertAlmostEqual(4e-6 + 1 * 8e-6, self.instance.array_x_n[1])
        self.assertAlmostEqual(4e-6 + 2 * 8e-6, self.instance.array_x_n[2])
        self.assertAlmostEqual(4e-6 + 3 * 8e-6, self.instance.array_x_n[3])
        self.assertAlmostEqual(4e-6 + 4 * 8e-6, self.instance.array_x_n[4])
        self.assertAlmostEqual(4e-6 + 5 * 8e-6, self.instance.array_x_n[5])
        self.assertAlmostEqual(4e-6 + 6 * 8e-6, self.instance.array_x_n[6])
        self.assertAlmostEqual(4e-6 + 7 * 8e-6, self.instance.array_x_n[7])
        self.assertAlmostEqual(4e-6 + 8 * 8e-6, self.instance.array_x_n[8])
        self.assertAlmostEqual(4e-6 + 9 * 8e-6, self.instance.array_x_n[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_n))

    def test_array_xs(self):
        self.assertEqual(2.5e-5 / 10, self.instance.dx_s)
        self.assertAlmostEqual(8e-5 + 1.25e-6, self.instance.array_x_s[0])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 1 * self.instance.dx_s, self.instance.array_x_s[1])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 2 * self.instance.dx_s, self.instance.array_x_s[2])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 3 * self.instance.dx_s, self.instance.array_x_s[3])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 4 * self.instance.dx_s, self.instance.array_x_s[4])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 5 * self.instance.dx_s, self.instance.array_x_s[5])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 6 * self.instance.dx_s, self.instance.array_x_s[6])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 7 * self.instance.dx_s, self.instance.array_x_s[7])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 8 * self.instance.dx_s, self.instance.array_x_s[8])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 9 * self.instance.dx_s, self.instance.array_x_s[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_s))

    def test_array_xp(self):
        self.assertEqual(8.8e-5 / 10, self.instance.dx_p)
        self.assertAlmostEqual(1.05e-4 + 4.4e-6, self.instance.array_x_p[0])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 1 * self.instance.dx_p, self.instance.array_x_p[1])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 2 * self.instance.dx_p, self.instance.array_x_p[2])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 3 * self.instance.dx_p, self.instance.array_x_p[3])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 4 * self.instance.dx_p, self.instance.array_x_p[4])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 5 * self.instance.dx_p, self.instance.array_x_p[5])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 6 * self.instance.dx_p, self.instance.array_x_p[6])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 7 * self.instance.dx_p, self.instance.array_x_p[7])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 8 * self.instance.dx_p, self.instance.array_x_p[8])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 9 * self.instance.dx_p, self.instance.array_x_p[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_s))

    def test_array_dx(self):
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[0])
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[5])
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[9])

        self.assertEqual(self.instance.dx_s, self.instance.array_dx[11])
        self.assertEqual(self.instance.dx_s, self.instance.array_dx[15])
        self.assertEqual(self.instance.dx_s, self.instance.array_dx[18])

        self.assertEqual(self.instance.dx_p, self.instance.array_dx[20])
        self.assertEqual(self.instance.dx_p, self.instance.array_dx[25])
        self.assertEqual(self.instance.dx_p, self.instance.array_dx[-1])
        self.assertEqual(30, len(self.instance.array_dx))


class TestElectrolyteConcFVMSolver(unittest.TestCase):
    def test_array_a_s(self):
        epsilon_en: float = 0.385
        epsilon_esep: float = 0.785
        epsilon_ep: float = 0.485

        D_e: float = 3.5e-10  # [mol/m3]
        brugg: float = 4

        co_ords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
        conc_solver: ElectrolyteConcFVMSolver = ElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=0.354,
                                                                         epsilon_en=epsilon_en,
                                                                         epsilon_esep=epsilon_esep,
                                                                         epsilon_ep=epsilon_ep,
                                                                         a_sn=5.78e3, a_sp=7.28e3,
                                                                         D_e=3.5e-10,
                                                                         brugg=brugg,
                                                                         c_e_init=1000)
        self.assertTrue(np.array_equal(epsilon_en * np.ones(10), conc_solver.array_epsilon_e[:10]))
        self.assertTrue(np.array_equal(epsilon_esep * np.ones(10), conc_solver.array_epsilon_e[10:20]))
        self.assertTrue(np.array_equal(epsilon_ep * np.ones(10), conc_solver.array_epsilon_e[20:30]))

    def test_array_D_e(self):
        epsilon_en: float = 0.385
        epsilon_esep: float = 0.785
        epsilon_ep: float = 0.485

        D_e: float = 3.5e-10  # [mol/m3]
        brugg: float = 4

        co_ords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
        conc_solver: ElectrolyteConcFVMSolver = ElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=0.354,
                                                                         epsilon_en=epsilon_en,
                                                                         epsilon_esep=epsilon_esep,
                                                                         epsilon_ep=epsilon_ep,
                                                                         a_sn=5.78e3, a_sp=7.28e3,
                                                                         D_e=D_e,
                                                                         brugg=brugg,
                                                                         c_e_init=1000)
        self.assertTrue(np.allclose(7.689727719e-12 * np.ones(10), conc_solver.array_D_eff[:10]))
        self.assertTrue(np.allclose(1.329066377e-10 * np.ones(10), conc_solver.array_D_eff[10:20]))
        self.assertTrue(np.allclose(1.936578022e-11 * np.ones(10), conc_solver.array_D_eff[20:30]))

    def test_array_a_s(self):
        epsilon_en: float = 0.385
        epsilon_esep: float = 0.785
        epsilon_ep: float = 0.485

        D_e: float = 3.5e-10  # [mol/m3]
        brugg: float = 4

        a_s_n: float = 5.78e3
        a_s_p: float = 7.28e3

        co_ords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
        conc_solver: ElectrolyteConcFVMSolver = ElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=0.354,
                                                                         epsilon_en=epsilon_en,
                                                                         epsilon_esep=epsilon_esep,
                                                                         epsilon_ep=epsilon_ep,
                                                                         a_sn=a_s_n, a_sp=a_s_p,
                                                                         D_e=D_e,
                                                                         brugg=brugg,
                                                                         c_e_init=1000)
        self.assertTrue(np.allclose(a_s_n * np.ones(10), conc_solver.array_a_s[:10]))
        self.assertTrue(np.allclose(np.zeros(10), conc_solver.array_a_s[10:20]))
        self.assertTrue(np.allclose(a_s_p * np.ones(10), conc_solver.array_a_s[20:30]))



