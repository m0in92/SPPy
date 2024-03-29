"""
Contains the functions for the positive electode's OCP as found in Schmit et al.

Note that the electrode temperatures are assumed to be at 298.15 K.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2023, 2024 by SPPy. All rights reserved."
__status__ = "deployed"

from typing import Union

import numpy as np

from SPPy.calc_helpers.constants import Constants


def calc_ocp_schmit(A_list: list, K: float, U0: float, x: float) -> float:
    R: float = Constants.R
    F: float = Constants.F
    T: float = 298.15

    # second term
    sec_term = (R * T / F) * np.log((1 - x) / x)

    # third term
    pre_term = 1 / (K * (2 * x - 1) + 1) ** 2
    post_term = 0
    for i, A in enumerate(A_list):
        post_term += (A / F) * ((2 * x - 1) ** (i + 1) - 2 * i * x * (1 - x) / (2 * x - 1) ** (1 - i))
    third_term = pre_term * post_term

    # fourth term
    post_term = 0
    for i, A in enumerate(A_list):
        post_term += (A / F) * ((2 * x - 1) ** i) * (2 * (i + 1) * (x ** 2) - 2 * (i + 1) * x + 1)
    fou_term = K * post_term

    return U0 + sec_term + third_term + fou_term


def LCO(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    # # function calculations
    A_list: list = [5166082.0, -5191279.0, 5232986.0, -5257083.0, 5010583.0, -4520614.0, 7306952.0, -14634260.0,
                    6705611.0,
                    33894160.0, -63528110.0, 30487930.0, 21440020.0, -27731990.0, 8206452.0]
    K = -2.369020e-04
    U0: float = -2.276828e+01
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def NMC(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        -1306.411,
        -57995.21,
        128590.6,
        -141860.5,
        128196.9,
        -328128.3,
        817.6398,
        1373879,
        651141.4,
        -7315831,
        4983891,
        6925178,
        -6123714,
        -3595215,
        3340694
    ]
    K: float = -0.635961
    U0: float = 3.755472
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def LFP(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        -2244.923,
        -2090.675,
        -6045.274,
        -6046.354,
        -13952.1,
        49285.95,
        57688.95,
        -270619.6,
        -262397.3,
        695491.2,
        480539,
        -881803.7,
        -450067.5,
        425577.8,
        127814.6
    ]
    K: float = 0.03932999
    U0: float = 3.407141
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def LMO(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        28.88073,
        -19289.65,
        27516.93,
        25997.59,
        47959.29,
        -277348.8,
        -321162.5,
        998439.1,
        1227530,
        -2722189,
        -1973511,
        4613775,
        818839.4,
        -4157314,
        1709075
    ]
    K: float = -0.9996536
    U0: float = 4.004463
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def NCA(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        1545979,
        -1598187,
        1595170,
        -1605545,
        1521194,
        -1645695,
        1809373,
        -1578053,
        2032672,
        -2281842,
        -1678912,
        2858489,
        5443521,
        -9459781,
        3600413
    ]
    K: float = 0.000104664
    U0: float = -4.419803
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)
