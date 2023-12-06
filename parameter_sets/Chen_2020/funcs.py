import numpy as np


def OCP_ref_p(soc: float) -> float:
    """
    Reference Chen et al. 2020
    :param soc:
    :return:
    """
    # soc = 1 - soc
    return -0.8090*soc + 4.4875 - 0.0428*np.tanh(18.5138*(soc-0.5542)) - 17.7326*np.tanh(15.7890*(soc-0.3117)) + \
           17.5842 * np.tanh(15.9308 * (soc-0.3120))


def dOCPdT_p(soc: float) -> float:
    """
    reference Guo et al. TODO: Get this function for LGM50
    :param soc:
    :return:
    """
    num = -0.19952 + 0.92837*soc - 1.36455 * soc ** 2 + 0.61154 * soc ** 3
    dem = 1 - 5.66148 * soc + 11.47636 * soc**2 - 9.82431 * soc**3 + 3.04876 * soc**4
    return (num/dem) * 1e-3  # since the original unit are of mV/K


def OCP_ref_n(soc: float) -> float:
    """
    Reference Chen et al. 2020
    :param SOC:
    :return:
    """
    return 1.9793 * np.exp(-39.3631*soc) + 0.2482 - \
           0.0909 * np.tanh(29.8538 * (soc - 0.1234)) - \
           0.04478 * np.tanh(14.9159 * (soc - 0.2769)) - \
           0.0205 * np.tanh(30.4444 * (soc - 0.6103))

def dOCPdT_n(soc: float) -> float:
    num = 0.00527 + 3.29927 * soc - 91.79326 * soc ** 2 + 1004.91101 * soc ** 3 - \
          5812.27813 * soc ** 4 + 19329.75490 * soc ** 5 - 37147.89470 * soc ** 6 + \
          38379.18127 * soc ** 7 - 16515.05308 * soc ** 8
    dem = 1 - 48.09287 * soc + 1017.23480 * soc**2 - 10481.80419 * soc**3 + \
          59431.30001 * soc**4 - 195881.64880 * soc**5 + 374577.31520 * soc**6 - \
          385821.16070 * soc**7 + 165705.85970 * soc**8
    return (num/dem) * 1e-3  # since the original unit are of mV/K
