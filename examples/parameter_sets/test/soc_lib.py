"""
This modules uses interpolation to calculate the soc_lib from the boundaries of the stociometeric ratios of the
electrode ocps.
"""

import numpy as np
import matplotlib.pyplot as plt

from SPPy import parameter_estimations
from parameter_sets.test import funcs

# below describes the positive and negative electrode soc
SOC_P_MIN, SOC_P_MAX = 0.4956, 0.989011
SOC_N_MIN, SOC_N_MAX = 0.01890232, 0.7568
SOC_LIB = 1.0

array_soc_lib = np.linspace(0, 1)
array_ocp_p, array_ocp_n = parameter_estimations.OCVData.get_soc(soc_lib=array_soc_lib,
                                                                 soc_p_min=SOC_P_MIN, soc_p_max=SOC_P_MAX,
                                                                 soc_n_min=SOC_N_MIN, soc_n_max=SOC_N_MAX)

plt.plot(array_soc_lib, array_ocp_p, label='soc_p')
plt.plot(array_soc_lib, array_ocp_n, label='soc_n')

plt.legend()
plt.show()




