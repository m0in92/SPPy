"""
Python script to demonstrate the determination of stoiciometric ratios from slow battery discharge.
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All rights reserved."
__status__ = "deployed"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import SPPy

BATTERY_CELL_CAP: float = 1.987336011530793

df: pd.DataFrame = pd.read_csv("data/INR18650_slow_discharge.csv")
tdis_charge: np.ndarray = df['t [s]'].to_numpy()
v_discharge: np.ndarray = df['V [V]'].to_numpy()
cap_discharge: np.ndarray = df['discharge cap [Ahr]'].to_numpy() / BATTERY_CELL_CAP

print(cap_discharge[-1])

SOC_MIN_P: float = 0.35
SOC_MAX_P: float = 1
SOC_MIN_N: float = 0.0
SOC_MAX_N: float = 0.8
param_estimator: SPPy.OCVData = SPPy.OCVData(func_ocp_p="LCO", func_ocp_n="graphite",
                                             soc_p_min_1=0.25, soc_p_min_2=0.435,
                                             soc_p_max_1=0.85, soc_p_max_2=0.95,
                                             soc_n_min_1=0.0, soc_n_min_2=0.2,
                                             soc_n_max_1=0.65, soc_n_max_2=0.81,
                                             charge_or_discharge='discharge')

soc_lib: np.ndarray = param_estimator.array_soc(0, 1)
array_ocp_p: np.ndarray = param_estimator.array_ocp_p(soc_min=SOC_MIN_P, soc_max=SOC_MAX_P)
array_ocp_n: np.ndarray = param_estimator.array_ocp_n(soc_min=SOC_MIN_N, soc_max=SOC_MAX_N)

result: np.ndarray = param_estimator.find_optimized_parameters(array_cap_exp=cap_discharge, array_v_exp_=v_discharge)

# plots
# plt.plot(soc_lib, array_ocp_p)
# plt.plot(soc_lib, array_ocp_n)
# plt.plot(soc_lib, array_ocp_p - array_ocp_n)
# plt.plot(cap_discharge, v_discharge)
# plt.show()
# param_estimator.plot_fit(cap_exp=cap_discharge, v_exp=v_discharge)
