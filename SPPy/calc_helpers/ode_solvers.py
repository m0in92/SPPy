"""
Contains the functionalities for performing ODEs using different solvers.
"""

__all__ = ["euler", "rk4", "TDMAsolver"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."

from typing import Callable

import numpy as np
import numpy.typing as npt


def euler(func, t_prev, y_prev, step_size):
    return y_prev + func(y_prev, t_prev) * step_size


def rk4(func: Callable, t_prev: float, y_prev: float, step_size: float):
    """
    Solves for the value of y in the next time step for a ODE
                dy/dt = f(y,t)
    :param func: (Callable) function that takes y and t as its input arguments (in that order).
    :param t_prev: The value of time in the previous time step [s]
    :param y_prev: The value of y in the previous time step
    :param step_size: the difference in time between the current and previous time steps [s]
    :return: The value of y at the next time step
    """
    k1 = func(y_prev, t_prev)
    k2 = func(y_prev + 0.5*k1*step_size, t_prev + 0.5*step_size)
    k3 = func(y_prev + 0.5*k2*step_size, t_prev + 0.5*step_size)
    k4 = func(y_prev + k3*step_size, t_prev + step_size)
    return y_prev + (1/6.0) * (k1 + 2*k2 + 2*k3 + k4) * step_size


def TDMAsolver(l_diag: npt.ArrayLike, diag: npt.ArrayLike, u_diag: npt.ArrayLike, col_vec: npt.ArrayLike) \
        -> npt.ArrayLike:
    '''
    TDMA (a.k.a Thomas algorithm) solver for tridiagonal system of equations.
    Code Modified from:
    https://gist.github.com/cbellei/8ab3ab8551b8dfc8b081c518ccd9ada9?permalink_comment_id=3109807
    '''
    nf = len(col_vec)  # number of equations
    c_l_diag, c_diag, c_u_diag, c_col_vec = map(np.array, (l_diag, diag, u_diag, col_vec))  # copy arrays
    for it in range(1, nf):
        mc = c_l_diag[it - 1] / c_diag[it - 1]
        c_diag[it] = c_diag[it] - mc * c_u_diag[it - 1]
        c_col_vec[it] = c_col_vec[it] - mc * c_col_vec[it - 1]

    xc = c_diag
    xc[-1] = c_col_vec[-1] / c_diag[-1]

    for il in range(nf - 2, -1, -1):
        xc[il] = (c_col_vec[il] - c_u_diag[il] * xc[il + 1]) / c_diag[il]
    return xc
