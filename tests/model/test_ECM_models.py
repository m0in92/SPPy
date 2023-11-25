import unittest

from SPPy.models.ECM import Thevenin1RC, ESC


class TestESC(unittest.TestCase):
    eta = 1.0
    cap = 1
    i_app = 2
    soc_prev = 0.5
    dt = 0.5

    R0: float = 0.1
    R1: float = 0.1
    C1: float = 1000
    i_R1_prev = 0.0

    gamma: float = 523.8311
    h_prev: float = 0.0
    s_prev: float = 0.0
    m: float = 4.4782e-4
    m_0: float = 0.0012

    ocv: float = 3.8

    def test_classmethod_sign(self):
        negative_float = -100.0
        zero_float = 0.0
        positive_float = 100.0

        negative_int = -100
        zero_int = 0
        positive_int = 100

        self.assertEqual(-1, ESC.sign(num=negative_float))
        self.assertEqual(0, ESC.sign(num=zero_float))
        self.assertEqual(1, ESC.sign(num=positive_float))

        self.assertEqual(-1, ESC.sign(num=negative_int))
        self.assertEqual(0, ESC.sign(num=zero_int))
        self.assertEqual(1, ESC.sign(num=positive_int))

    def test_classmethod_s(self):
        s_prev = 100
        zero_float = 0.0
        zero_int = 0

        positive_float = 1.0
        positive_int = 1

        self.assertEqual(100, ESC.s(i_app=zero_float, s_prev=s_prev))
        self.assertEqual(100, ESC.s(i_app=zero_int, s_prev=s_prev))

        self.assertEqual(1, ESC.s(i_app=positive_float, s_prev=s_prev))
        self.assertEqual(1, ESC.s(i_app=positive_int, s_prev=s_prev))

    def test_classmethod_soc_next(self):
        self.assertAlmostEqual(0.4997222222222222, ESC.soc_next(dt=self.dt, i_app=self.i_app,
                                                                SOC_prev=self.soc_prev, Q=self.cap, eta=self.eta))

    def test_classmethod_i_R1_next(self):
        self.assertAlmostEqual(9.975041612e-3, ESC.i_R1_next(dt=self.dt, i_app=self.i_app, i_R1_prev=self.i_R1_prev,
                                                             R1=self.R1, C1=self.C1))

    def test_classmethod_h_next(self):
        self.assertEqual(-0.13541757898977902,
                         ESC.h_next(dt=self.dt, i_app=self.i_app, eta=self.eta, gamma=self.gamma, cap=self.cap,
                                    h_prev=self.h_prev))

    def test_classmethod_v(self):
        self.assertEqual(3.6011999999999995, ESC.v(i_app=self.i_app, ocv=self.ocv, R0=self.R0, R1=self.R1,
                                                   i_R1=self.i_R1_prev, m=self.m, h=self.h_prev, s_prev=self.s_prev,
                                                   m_0=self.m_0))
