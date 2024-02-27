import unittest

import numpy as np

from SPPy.models.degradation import ROMSEI


class TESTROMSEI(unittest.TestCase):
    def test_method_calc_j_i(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        j_tot: float = -I / (96487 * 0.7824)  # represents the molar flux to the negative electrode
        j_s: float = 0.0

        solver: ROMSEI = ROMSEI()
        j_i: float = solver.calc_j_i(j_tot=j_tot, j_s=j_s)
        self.assertAlmostEqual(-2.193626517e-5, j_i, places=12)

    def test_method_calc_eta_n(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        j_tot: float = -I / (96487 * 0.7824)  # represents the molar flux to the negative electrode
        j_s: float = 0.0
        temp: float = 298.15

        solver: ROMSEI = ROMSEI()
        j_i: float = solver.calc_j_i(j_tot=j_tot, j_s=j_s)
        j_0_i: float = solver.calc_j_0_i(k=1.764e-11, c_s_max=31833,
                                         soc=0.7522, c_e=1000)
        calculated_eta_n: float = solver.calc_eta_n(temp=temp, j_i=j_i, j_0_i=j_0_i)
        self.assertAlmostEqual(7.666435137e-6, j_0_i, places=10)
        self.assertAlmostEqual((2 * 8.314 * temp / 96487) * np.arcsinh(j_i / (2 * j_0_i)),
                               calculated_eta_n, places=5)

    def test_method_eta_s(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        j_tot: float = -I / (96487 * 0.7824)  # represents the molar flux to the negative electrode
        j_s: float = 0.0
        temp: float = 298.15

        solver: ROMSEI = ROMSEI()
        j_0_i: float = solver.calc_j_0_i(k=1.764e-11, c_s_max=31833,
                                         soc=0.7522, c_e=1000)
        j_i: float = solver.calc_j_i(j_tot = j_tot, j_s=j_s)

        eta_n: float = (2 * 8.314 * temp / 96487) * np.arcsinh(j_i/(2*j_0_i))
        calculated_eta_s: float = solver.calc_eta_s(eta_n=eta_n, ocp=0.081566, ocp_s=0.4)
        self.assertAlmostEqual(-0.377814, calculated_eta_s, places=5)

    def test_method_calc_j_s(self) -> None:
        i_0_s: float = 1.14264e-5
        temp: float = 298.15
        eta_s: float = -0.377814

        solver: ROMSEI = ROMSEI()
        self.assertAlmostEqual(1.783e-2, solver.calc_j_s(temp=temp, j_0_s=i_0_s,
                                                         eta_s=eta_s), places=1)

        i_0_s: float = 1.14264e-15
        self.assertAlmostEqual(-1.783e-12, solver.calc_j_s(temp=temp, j_0_s=i_0_s,
                                                           eta_s=eta_s), places=14)
