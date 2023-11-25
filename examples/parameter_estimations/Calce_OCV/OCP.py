from typing import Union

import numpy.typing as npt
import matplotlib.pyplot as plt
import scipy.interpolate

from parameter_sets.Calce_NMC_18650.funcs import OCP_ref_n, OCP_ref_p
from SPPy.parameter_estimations.procedural import OCVData
from extract_exp_data import *

# Modelling parameters
SOC_n_min = 0.006
SOC_n_max = 0.7953467
SOC_p_min = 0.43144714
SOC_p_max = 0.90
T = 298.15

SOC_init_p, SOC_init_n = SOC_p_min, SOC_n_max  # from GA results

cell = SPPy.BatteryCell(parameter_set_name='Calce_NMC_18650', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

obj_OCV = OCVData(b_cell=cell, sol_exp=sol_exp,
                  SOC_n_min_init=SOC_n_min, SOC_p_min_init=SOC_init_p,
                  SOC_n_max_init=SOC_n_max, SOC_p_max_init=SOC_p_max)

print(obj_OCV.SOC_from_OCV(4.19787216))

obj_OCV.plot()



