import unittest

import numpy as np

from SPPy.calc_helpers.numerical_diff import first_centered_FD, dVdQ


class TestFirstCenteredFD(unittest.TestCase):
    def test_sin_func(self):
        t_array = np.linspace(0, 2 * np.pi)
        x_array = np.sin(t_array)
        dxdt = first_centered_FD(y=x_array, x=t_array)
        self.assertEqual(len(t_array)-2, len(dxdt))
        self.assertAlmostEqual(2.53654584e-01 / 0.25645654, dxdt[0])

    def test_dVdQ(self):
        cap: np.ndarray = np.linspace(0, 2 * np.pi)
        v: np.ndarray = np.sin(cap)
        cap_, dVdQ_ = dVdQ(cap=cap, v=v)

        self.assertEqual(len(cap) - 2, len(cap_))
        self.assertEqual(cap[1], cap_[0])

        self.assertEqual(len(v)-2, len(dVdQ_))
        self.assertAlmostEqual(2.53654584e-01 / 0.25645654, dVdQ_[0])
