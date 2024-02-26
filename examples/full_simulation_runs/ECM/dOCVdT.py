import pickle

import numpy as np
import matplotlib.pyplot as plt

from parameter_sets.test.funcs import dOCPdT_p, dOCPdT_n

import SPPy


# Operating parameters
I = 1.92
dT = 10
T1 = 298.15
T2 = 298.15 + dT
V_min = 2.5
SOC_min = 0.1
SOC_LIB = 1

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al


def dOCVdT(SOC_LIB):
    SOC_n_max = 0.7568
    SOC_n_min = 0
    SOC_p_min = 0.4956
    SOC_p_max = 1
    return dOCPdT_p((SOC_LIB - SOC_p_min)/(SOC_p_max-SOC_p_min)) - dOCPdT_n((SOC_n_max-SOC_LIB)/(SOC_n_max - SOC_n_min))


array_SOC = np.linspace(0, 1)

# Plot
plt.plot(array_SOC, dOCVdT(array_SOC))
plt.xlabel('SOC')
plt.ylabel(r'$\frac{dOCV}{dT} [V/K]$')

plt.show()
