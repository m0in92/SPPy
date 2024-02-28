"""
Contains unit-tests for the random vector classes
"""

import unittest

import numpy as np

from SPPy.calc_helpers.kalman_filter import NormalRandomVector


class TestNormalRandomVector(unittest.TestCase):
    mean = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape(-1, 1)
    cov = np.ones(len(mean) ** 2).reshape(len(mean), len(mean))

    def test_constructor(self):
        rv = NormalRandomVector(vector_init=self.mean, cov_init=self.cov)
        self.assertTrue(np.array_equal(self.mean, rv.vector))
        self.assertEqual(len(self.mean), rv.dim)
        self.assertTrue(np.array_equal(self.cov, rv.cov))
        self.assertEqual(self.cov.shape[0], rv.cov.shape[0])
        self.assertEqual(self.cov.shape[1], rv.cov.shape[1])

    def test_constructor_with_invalid_expected_vector1(self):
        mean = 0.0
        with self.assertRaises(TypeError):
            NormalRandomVector(vector_init=mean, cov_init=self.cov)

    def test_constructor_with_invalid_expected_vector2(self):
        mean = np.array([1, 2, 3])
        with self.assertRaises(ValueError):
            NormalRandomVector(vector_init=mean, cov_init=self.cov)

    def test_constructor_with_invalid_expected_vector3(self):
        mean = np.array([[1, 1], [1, 1]])
        with self.assertRaises(ValueError):
            NormalRandomVector(vector_init=mean, cov_init=self.cov)

    def test_constructor_with_invalid_cov1(self):
        cov = 0.0
        with self.assertRaises(TypeError):
            NormalRandomVector(vector_init=self.mean, cov_init=cov)

    def test_constructor_with_invalid_cov2(self):
        with self.assertRaises(ValueError):
            NormalRandomVector(vector_init=self.mean, cov_init=self.mean)

    def test_constructor_with_invalid_cov3(self):
        cov = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
        with self.assertRaises(ValueError):
            NormalRandomVector(vector_init=self.mean, cov_init=cov)

    def test_constructor_with_invalid_cov3(self):
        cov = np.array([[1, 2], [1, 2]])
        with self.assertRaises(ValueError):
            NormalRandomVector(vector_init=self.mean, cov_init=cov)