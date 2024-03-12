"""
This module is intended to serve as an example for the use of Sigma Point Kalman Filter (SPKF) containing two states
and one output variable.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All rights reserved."
__status__ = "developement"

import numpy as np

from SPPy.calc_helpers.kalman_filter import NormalRandomVector, SigmaPointKalmanFilter

from examples.kalman_filter.spkf_ecm_non_isothermal import func_ocv, func_eta, func_dOCVdT

# Global variables
# ECM Parameters
R0 = 0.1
R1 = 0.1
C1 = 0.1
delta_t = 1
Q = 3600 * 1.5  # 1.5 A.hr which is converted to A.s


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


def output_equation(x_k: np.ndarray, u_k: np.ndarray, v_k: np.ndarray) -> float:
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
soc_init: float = 1.0
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
t: np.ndarray = np.array([0, 1])  # time values at each time step [s]
i_app: np.ndarray = -1.656 * np.ones(len(t))  # applied current [A]
y_true: np.ndarray = np.array([4.2, 4.15])

t_prev: float = 0.0  # [s]
step_completed: bool = False
loop_index: int = 1
for i in range(1, len(t)):
    i_app_prev: float = i_app[loop_index-1]
    dt: float = t[loop_index] - t[loop_index-1]

    spkf.solve(u=i_app_prev, y_true=y_true[loop_index])

    print(spkf.x.get_vector())

    loop_index += 1

