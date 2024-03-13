"""
This module is intended to serve as an example for the use of Sigma Point Kalman Filter (SPKF) containing two states
and one output variable.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All rights reserved."
__status__ = "developement"

from typing import Union

import numpy as np
import matplotlib.pyplot as plt

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


def calc_v(i_app: float, soc_: float) -> float:
    """
    Output Equation.
    :param x_k:
    :param u_k:
    :param v_k:
    :return:
    """
    return func_ocv(soc_) + R1 * soc_ + R0 * i_app


# Below are the variables (including Normal Random Variable) to be used to the SPKF. At the end the instance for
# Sigma-point kalman filter (SPKF) is introduced.
i_r1_init: float = 0.0  # [A]
soc_init: float = 0.9
cov_soc: float = 1e-6
cov_current: float = 1e-6
cov_sensor: float = 1e-6
cov_process: float = 1e-6

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
t: np.ndarray = np.arange(0.0, 10.0, 1.0)  # time values at each time step [s]
i_app: np.ndarray = 1.656 * np.ones(len(t))  # applied current [A]

w_array: np.ndarray = np.random.normal(loc=0, scale=cov_sensor, size=(len(t), 2, 1))
v_array: np.ndarray = np.random.normal(loc=0, scale=cov_process, size=(len(t),))

x_true: np.ndarray = np.zeros((len(t), 2, 1))
x_true[0] = x_array
for i in range(1, len(t)):
    x_true[i] = state_equation(x_k=x_true[i-1], u_k=i_app[i-1], w_k=w_array[i])
print(x_true)
y_true: np.ndarray = np.zeros(len(t))
for i in range(len(t)):
    y_true[i] = output_equation(x_k=x_true[i], u_k=i_app[i], v_k=v_array[i])
# print(y_true)
x_calc: np.ndarray = np.zeros((len(t), 2, 1))
x_calc[0] = x_array

soc_calc: np.ndarray = np.zeros(len(t))  # array for storage of calculated values
soc_calc[0] = x_array[0, 0]
i_R1_calc: np.ndarray = np.zeros(len(t)) # array for storage of calculated values
v_calc: np.ndarray = np.zeros(len(t))

t_prev: float = 0.0  # [s]
step_completed: bool = False
loop_index: int = 1
for loop_index in range(0, len(t)):
    i_app_prev: float = i_app[loop_index-1]
    dt: float = t[loop_index] - t[loop_index-1]

    spkf.solve(u=i_app_prev, y_true=y_true[loop_index])
    soc_calc[loop_index] = spkf.x.get_vector()[0, 0]
    i_R1_calc[loop_index] = spkf.x.get_vector()[1, 0]
    v_calc[loop_index] = calc_v(i_app=i_app[loop_index-1], soc_=spkf.x.get_vector()[0, 0])

    print(f"loop_interation {loop_index}: ", spkf.x.get_vector())

# plots
soc_true: np.ndarray = x_true[:, 0, :]
print(soc_true)
# soc_calc: np.ndarray = x_calc[:, 0, :]
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(t, soc_true, label="true")
ax1.plot(t, soc_calc, label="calc")
ax1.legend()

ax2 = fig.add_subplot(212)
ax2.plot(t[1:], y_true[1:], label="true")
ax2.plot(t[1:], v_calc[1:], label="calc")
ax2.legend()

plt.show()

