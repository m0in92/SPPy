"""
This module is intended to serve as an example for the use of Sigma Point Kalman Filter (SPKF) containing two states
and one output variable.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All rights reserved."
__status__ = "developement"

import numpy as np

from SPPy.calc_helpers.kalman_filter import NormalRandomVector, SigmaPointKalmanFilter

# Global variables
# ECM Parameters
R0 = 0.1
R1 = 0.1
C1 = 0.1
delta_t = 1
Q = 3600 * 1.5  # 1.5 A.hr which is converted to A.s


# below are the definitions of the state and output equations.
def f_func(x_k: np.ndarray, u_k: np.ndarray, w_k: np.ndarray) -> np.ndarray:
    m1 = np.array([[1, 0], [0, np.exp(-delta_t / (R1 * C1))]])
    m2 = np.array([[-delta_t / Q], [1 - np.exp(-delta_t / (R1 * C1))]])
    return m1 @ x_k + m2 * (u_k + w_k)
