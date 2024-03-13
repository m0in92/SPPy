"""
This module is intended to serve as an example for the use of Sigma Point Kalman Filter (SPKF) containing two states
and one output variable.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All rights reserved."
__status__ = "developement"

from typing import Union

import numpy as np

from SPPy.calc_helpers.kalman_filter import NormalRandomVector, SigmaPointKalmanFilter

# from examples.kalman_filter.spkf_ecm_non_isothermal import func_ocv, func_eta, func_dOCVdT

# Global variables
# ECM Parameters
R0 = 0.1
R1 = 0.1
C1 = 0.1
delta_t = 1
Q = 3600 * 1.5  # 1.5 A.hr which is converted to A.s


def func_ocv(soc):
    a, b, c, d, e, f, g, h, i, j, k, l, m = \
        [3.39803735e+04, -1.86083253e+05, 4.40650925e+05, -5.86500338e+05,
         4.74171271e+05, -2.29840038e+05, 5.53052667e+04, 3.05616190e+03,
         -6.45471514e+03, 1.99278174e+03, -2.99381888e+02, 2.29345284e+01,
         2.53496894e+00]

    return a * soc ** 12 + b * soc ** 11 + c * soc ** 10 + \
           d * soc ** 9 + e * soc ** 8 + f * soc ** 7 + \
           g * soc ** 6 + h * soc ** 5 + i * soc ** 4 + \
           j * soc ** 3 + k * soc ** 2 + l * soc + m


# below are the definitions of the state and output equations.
def state_equation(x_k: np.ndarray, u_k: np.ndarray, w_k: np.ndarray) -> np.ndarray:
    """
    State function definition
    :param x_k: column vector containing the states. In this example, the number of states are 2 hence the size of the
    vector should be of size (2 x 1).
    :param u_k:
    :param w_k:
    :return:
    """
    m1 = np.array([[1, 0], [0, np.exp(-delta_t / (R1 * C1))]])
    m2 = np.array([[-delta_t / Q], [1 - np.exp(-delta_t / (R1 * C1))]])
    return m1 @ x_k + m2 * (u_k + w_k)


def output_equation(x_k: np.ndarray, u_k: Union[float, np.ndarray], v_k: Union[float, np.ndarray]) -> np.ndarray:
    """
    Output Equation.
    :param x_k:
    :param u_k:
    :param v_k:
    :return:
    """
    return func_ocv(x_k[0, :]) - R1 * x_k[1, :] - R0 * u_k + v_k


# Below are the variables (including Normal Random Variable) to be used to the SPKF. At the end the instance for
# Sigma-point kalman filter (SPKF) is introduced.
i_r1_init: float = 0.0  # [A]
soc_init: float = 0.8993866666666667
cov_soc: float = 1e-3
cov_current: float = 1e-3
cov_sensor: float = 1e-3
cov_process: float = 1e-3

x_array: np.ndarray = np.array([[soc_init], [i_r1_init]])
x_cov: np.ndarray = np.array([[cov_soc, 0],
                              [0, cov_current]])
w_array: np.ndarray = np.array([[0]])
w_cov: np.ndarray = np.array([[cov_process]])
v_array: np.ndarray = np.array([[0]])
v_cov: np.ndarray = np.array([[cov_sensor]])

x: NormalRandomVector = NormalRandomVector(vector_init=x_array, cov_init=x_cov)
w = NormalRandomVector(vector_init=w_array, cov_init=w_cov)
v = NormalRandomVector(vector_init=v_array, cov_init=v_cov)

spkf: SigmaPointKalmanFilter = SigmaPointKalmanFilter(x=x, w=w, v=v, y_dim=1,
                                                      state_equation=state_equation,
                                                      output_equation=output_equation)

# Simulation loop is performed below
t: np.ndarray = np.array([0, 1, 2])  # time values at each time step [s]
i_app: np.ndarray = -1.656 * np.ones(len(t))  # applied current [A]
# y_true: float = output_equation(x_k=x_array, u_k=-1.656, v_k=0)
# print(y_true)

x_true: np.ndarray = np.array([0.9, 0.899693333, 0.899386667])
y_true: np.ndarray = np.array([3.56130097, 3.56108907, 3.56088061])

t_prev: float = 0.0  # [s]
step_completed: bool = False
loop_index: int = 1
for i in range(1, len(t)):
    i_app_prev: float = i_app[loop_index-1]
    dt: float = t[loop_index] - t[loop_index-1]

    spkf.solve(u=i_app_prev, y_true=y_true[loop_index])

    print(f"loop_interation {loop_index}: ", spkf.x.get_vector())

    loop_index += 1

