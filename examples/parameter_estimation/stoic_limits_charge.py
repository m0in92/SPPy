import numpy as np
import pandas as pd

import SPPy

BATTERY_CELL_CAP: float = 1.69230688135793

df: pd.DataFrame = pd.read_csv("data/INR18650_slow_charge.csv")
t_charge: np.ndarray = df['t [s]'].to_numpy()
v_charge: np.ndarray = df['V [V]'].to_numpy()
cap_charge: np.ndarray = df['charge cap [Ahr]'].to_numpy() / BATTERY_CELL_CAP

SOC_MIN_P: float = 0.35
SOC_MAX_P: float = 0.9
SOC_MIN_N: float = 0.0125
SOC_MAX_N: float = 0.8
param_estimator: SPPy.OCVData = SPPy.OCVData(func_ocp_p="LCO", func_ocp_n="graphite",
                                             soc_p_min_1=0.35, soc_p_min_2=0.45,
                                             soc_p_max_1=0.9, soc_p_max_2=1.0,
                                             soc_n_min_1=0.0, soc_n_min_2=0.05,
                                             soc_n_max_1=0.75, soc_n_max_2=0.81,
                                             charge_or_discharge='charge')

soc_lib: np.ndarray = param_estimator.array_soc(0, 1)
array_ocp_p: np.ndarray = param_estimator.array_ocp_p(soc_min=SOC_MIN_P, soc_max=SOC_MAX_P)
array_ocp_n: np.ndarray = param_estimator.array_ocp_n(soc_min=SOC_MIN_N, soc_max=SOC_MAX_N)

result: np.ndarray = param_estimator.find_optimized_parameters(array_cap_exp=cap_charge, array_v_exp_=v_charge)

# plots
param_estimator.plot_fit(cap_exp=cap_charge, v_exp=v_charge)
