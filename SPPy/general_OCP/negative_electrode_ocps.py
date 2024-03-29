"""
Contains the functions for the negative electode's OCP as found in Schmit et al. and others

Note that the electrode temperatures are assumed to be at 298.15 K.

References:
Schmitt, J., Schindler, M., & Jossen, A. (2021). Change in the half-cell open-circuit potential curves of
silicon–graphite and nickel-rich lithium nickel manganese cobalt oxide during cycle aging.
Journal of Power Sources, 506, 230240. https://doi.org/10.1016/J.JPOWSOUR.2021.230240

Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
"""

from typing import Union

import numpy as np

from .positive_electrodes_ocps import calc_ocp_schmit


def MCMB(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        1115.732,
        -114405.2,
        -98955.51,
        -84726.47,
        -267608.3,
        -476169.2,
        603250.8,
        1867866,
        -1698309,
        -5707850,
        873999.3,
        7780654,
        1486486,
        -4703010,
        -2275145]
    K: float = 1.000052
    U0: float = -0.4894122
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def PetroleumCoke(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        3257341,
        3324795,
        3293786,
        3305070,
        3341687,
        3286297,
        2786389,
        2943793,
        6028857,
        8242393,
        1365959,
        -10369090,
        -13287330,
        -6890890,
        -1366119]
    K: float = 1.02E-05
    U0: float = 17.37471
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def HardCarbon(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    A_list: list = [
        643.3323,
        92777.34,
        120803.9,
        39097.09,
        70427.33,
        452782.1,
        925998.1,
        111.1642,
        -1853447,
        -323266.3,
        3899277,
        2862780,
        -2837527,
        -4199996,
        -1406372]
    K: float = 0.9896854
    U0: float = 0.5839445
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def LTO(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    # # function calculations
    A_list: list = [
        -2730.278,
        5232.911,
        -8075.451,
        -4993.786,
        36438.75,
        110508.7,
        -361370.2,
        -502525.3,
        1401392,
        1148841,
        -2857197,
        -1211581,
        2819998,
        479102.9,
        -1091785]
    K: float = 0.1291628
    U0: float = 1.596152
    return calc_ocp_schmit(A_list=A_list, K=K, U0=U0, x=soc)


def graphite(soc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Obtained from Guo et al.
    :param soc: electrode state of charge
    :return: electrode open-circuit potential [V]

    Reference:
    Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
    Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
    """
    return 0.13966 + 0.68920 * np.exp(-49.20361 * soc) + 0.41903 * np.exp(-254.40067 * soc) \
            - np.exp(49.97886 * soc - 43.37888) - 0.028221 * np.arctan(22.52300 * soc - 3.65328) \
            -0.01308 * np.arctan(28.34801 * soc - 13.43960)


