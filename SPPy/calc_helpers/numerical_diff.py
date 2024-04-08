"""
Contains the functionality for numerical differentiations.
"""
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by SPPy. All Rights Reserved."
__status__ = "deployed"

import numpy as np
import numpy.typing as npt


def first_centered_FD(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    calculates the first order differential using centered finite difference of the equation:
    :param array_x: x value at the x step
    :param array_t: t value at the t step
    :return: array containing the differential values.
    """
    array_diff = np.zeros(len(x)-2)
    for i in range(1, len(array_diff)+1):
        array_diff[i-1] = (y[i+1] - y[i-1]) / (x[i+1] - x[i-1])
    return array_diff


def dVdQ(cap: np.ndarray, v: np.ndarray) -> np.ndarray:
    return first_centered_FD(y=v, x=cap)
