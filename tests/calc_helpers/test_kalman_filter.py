"""
Contains the unit test for the kalman filters
"""

import unittest

import numpy as np

from SPPy.calc_helpers.kalman_filter import NormalRandomVector, SigmaPointKalmanFilter


class TestSPKFProperties(unittest.TestCase):
    vector_x = np.array([2, 2]).reshape(-1, 1)
    vector_w = np.array([0]).reshape(-1, 1)
    vector_v = np.array([0]).reshape(-1, 1)

    vector_x2 = np.array([2]).reshape(-1, 1)
    vector_w2 = np.array([0]).reshape(-1, 1)
    vector_v2 = np.array([0]).reshape(-1, 1)

    cov_x = np.array([[2, 0], [0, 2]])
    cov_w = np.array([[1]])
    cov_v = np.array([[2]])

    cov_x2 = np.array([[1]])
    cov_w2 = np.array([[1]])
    cov_v2 = np.array([[2]])

    x = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
    w = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
    v = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

    x2 = NormalRandomVector(vector_init=vector_x2, cov_init=cov_x2)
    w2 = NormalRandomVector(vector_init=vector_w2, cov_init=cov_w2)
    v2 = NormalRandomVector(vector_init=vector_v2, cov_init=cov_v2)

    y_dim = 1

    @staticmethod
    def func_f(x_k, u_k, w_k):
        return np.sqrt(5 + x_k) + w_k

    @staticmethod
    def func_h(x_k, u_k, v_k):
        return x_k ** 3 + v_k

    spkf_instance: SigmaPointKalmanFilter = SigmaPointKalmanFilter(x=x, w=w, v=v, y_dim=y_dim,
                                                                   state_equation=func_f, output_equation=func_h)
    spkf_instance2: SigmaPointKalmanFilter = SigmaPointKalmanFilter(x=x2, w=w2, v=v2, y_dim=y_dim,
                                                                    state_equation=func_f, output_equation=func_h)

    def test_constructor(self):
        self.assertTrue(np.array_equal(self.vector_x, self.spkf_instance.x.get_vector()))
        self.assertTrue(np.array_equal(self.vector_w, self.spkf_instance.w.get_vector()))
        self.assertTrue(np.array_equal(self.vector_v, self.spkf_instance.v.get_vector()))
        self.assertEqual(self.y_dim, self.spkf_instance.y_dim)

    def test_calc_sqrt_matrix(self):
        test_matrix = np.array([[4, 12, -16], [12, 37, -43], [-16, -43, 98]])
        result = np.array([[2, 0, 0], [6, 1, 0], [-8, 5, 3]])
        result2 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1.41421356]])

        self.assertTrue(np.array_equal(result, self.spkf_instance.calc_sqrt_matrix(matrix=test_matrix)))
        self.assertTrue(np.allclose(result2, self.spkf_instance2.calc_sqrt_matrix(self.spkf_instance2.aug_cov)))

    def test_aug_vector(self):
        self.assertTrue(np.array_equal(np.array([2, 2, 0, 0]).reshape(-1, 1), self.spkf_instance.aug_vector))

    def test_aug_cov(self):
        test_aug_cov = np.array([[2, 0, 0, 0],
                                 [0, 2, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 2]])
        self.assertTrue(np.array_equal(test_aug_cov, self.spkf_instance.aug_cov))

    def test_gamma(self):
        self.assertEqual(np.sqrt(3), self.spkf_instance.gamma)
        self.assertEqual(np.sqrt(3), self.spkf_instance2.gamma)

    def test_h(self):
        self.assertEqual(np.sqrt(3), self.spkf_instance.h)
        self.assertEqual(np.sqrt(3), self.spkf_instance2.h)

    def test_alpha_m0(self):
        self.assertAlmostEqual(0.0, self.spkf_instance2.alpha_m_0)

    def test_alpha_mk(self):
        self.assertAlmostEqual(1 / 6, self.spkf_instance2.alpha_m)

    def test_alpha_m_vec(self):
        self.assertTrue(np.all(np.isclose(np.array([[0], [1 / 6], [1 / 6], [1 / 6], [1 / 6], [1 / 6], [1 / 6]]),
                                          self.spkf_instance2.array_alpha_m)))

    def test_alpha_c0(self):
        self.assertAlmostEqual(0.0, self.spkf_instance2.alpha_c_0)

    def test_alpha_ck(self):
        self.assertAlmostEqual(1 / 6, self.spkf_instance2.alpha_c)

    def test_xsp(self):
        result = np.array([[2, 3.73205081, 2, 2, 0.26794919, 2, 2],
                           [0, 0, 1.73205081, 0, 0, -1.73205081, 0],
                           [0, 0, 0, 2.44948974, 0, 0, -2.44948974]])
        self.assertTrue(np.all(np.isclose(result, self.spkf_instance2.x_sp)))


class TestSPKFSolve(unittest.TestCase):
    def test_state_and_cov_estimate(self):
        vector_x = np.array([2]).reshape(-1, 1)
        vector_w = np.array([0]).reshape(-1, 1)
        vector_v = np.array([0]).reshape(-1, 1)

        cov_x = np.array([[1]])
        cov_w = np.array([[1]])
        cov_v = np.array([[2]])

        x = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
        w = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
        v = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

        y_dim = 1

        @staticmethod
        def func_f(x_k, u_k, w_k):
            return np.sqrt(5 + x_k) + w_k

        @staticmethod
        def func_h(x_k, u_k, v_k):
            return x_k ** 3 + v_k

        spkf_instance = SigmaPointKalmanFilter(x=x, w=w, v=v, y_dim=y_dim, state_equation=func_f, output_equation=func_h)

        x_cov_actual = 1.0363730825455537
        x_estimate_actual = 2.638868491883301
        Y_actual = np.array([18.52025918, 25.80324827, 83.90124036, 20.96974892, 12.09100405, 0.7628016, 16.07076943])
        output_pred_actual = 26.5998021

        Xx = spkf_instance._SigmaPointKalmanFilter__state_prediction(u=0)
        self.assertEqual(x_estimate_actual, spkf_instance.x.get_vector()[0, 0])
        Xs = spkf_instance._SigmaPointKalmanFilter__cov_prediction(Xx=Xx)
        self.assertAlmostEqual(x_cov_actual, spkf_instance.x.get_cov()[0, 0])
        y, y_hat = spkf_instance._SigmaPointKalmanFilter__output_estimate(Xx=Xx, u=0)
        self.assertTrue(np.all(np.isclose(Y_actual, y)))
        self.assertAlmostEqual(output_pred_actual, y_hat[0, 0])

    def test_update(self):
        vector_x = np.array([2]).reshape(-1, 1)
        vector_w = np.array([0]).reshape(-1, 1)
        vector_v = np.array([0]).reshape(-1, 1)

        cov_x = np.array([[1]])
        cov_w = np.array([[1]])
        cov_v = np.array([[2]])

        x = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
        w = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
        v = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

        y_dim = 1

        @staticmethod
        def func_f(x_k, u_k, w_k):
            return np.sqrt(5 + x_k) + w_k

        @staticmethod
        def func_h(x_k, u_k, v_k):
            return x_k ** 3 + v_k

        spkf_instance1 = SigmaPointKalmanFilter(x=x, w=w, v=v, y_dim=y_dim,
                                                state_equation=func_f, output_equation=func_h)

        gain_actual = 0.03457607
        xhat_update_actual = 1.8966845497917038
        cov_update_actual = 0.17865761849939343

        Xx = spkf_instance1._SigmaPointKalmanFilter__state_prediction(u=0)
        Xs = spkf_instance1._SigmaPointKalmanFilter__cov_prediction(Xx=Xx)
        y, y_hat = spkf_instance1._SigmaPointKalmanFilter__output_estimate(Xx=Xx, u=0)

        # Step 2a
        SigmaY, Lx = spkf_instance1._SigmaPointKalmanFilter__estimator_gain_matrix(y=y, yhat=y_hat, xs=Xs)
        self.assertAlmostEqual(gain_actual, Lx[0, 0])

        # Step 2b
        xhat_update = spkf_instance1._SigmaPointKalmanFilter__state_update(L=Lx, ytrue=5.134553960326726, yhat=y_hat)
        self.assertAlmostEqual(xhat_update_actual, spkf_instance1.x.get_vector()[0, 0])

        # Step 2c
        SigmaX = spkf_instance1._SigmaPointKalmanFilter__cov_measurement_update(Lx, SigmaY=SigmaY)
        self.assertAlmostEqual(cov_update_actual, spkf_instance1.x.get_cov()[0, 0])
