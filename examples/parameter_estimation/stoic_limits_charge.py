import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from SPPy.parameter_estimations.procedural import OCVData
from SPPy.general_OCP.positive_electrodes_ocps import LCO
from SPPy.general_OCP.negative_electrode_ocps import graphite


BATTERY_CELL_CAP: float = 1.69230688135793

df: pd.DataFrame = pd.read_csv("data/INR18650_slow_charge.csv")
t_charge: np.ndarray = df['t [s]'].to_numpy()
v_charge: np.ndarray = df['V [V]'].to_numpy()
cap_charge: np.ndarray = df['charge cap [Ahr]'].to_numpy()

SOC_MIN_P: float = 0.35
SOC_MAX_P: float = 0.9
SOC_MIN_N: float = 0.0125
SOC_MAX_N: float = 0.8
param_estimator: OCVData = OCVData(func_ocp_p=LCO, func_ocp_n=graphite,
                                   soc_p_min_1=0.35, soc_p_min_2=0.45,
                                   soc_p_max_1=0.9, soc_p_max_2=1.0,
                                   soc_n_min_1=0.0, soc_n_min_2=0.05,
                                   soc_n_max_1=0.75, soc_n_max_2=0.81,
                                   charge_or_discharge='charge')

soc_lib: np.ndarray = param_estimator.array_soc(0, 1)
array_ocp_p: np.ndarray = param_estimator.array_ocp_p(soc_min=SOC_MIN_P, soc_max=SOC_MAX_P)
array_ocp_n: np.ndarray = param_estimator.array_ocp_n(soc_min=SOC_MIN_N, soc_max=SOC_MAX_N)

print(param_estimator.find_optimized_parameters(array_cap_exp=cap_charge, array_v_exp_=v_charge))

# plots
plt.plot(cap_charge / BATTERY_CELL_CAP, v_charge)
plt.plot(soc_lib, array_ocp_p)
plt.plot(soc_lib, array_ocp_n)
plt.plot(soc_lib, array_ocp_p - array_ocp_n, 'r--')
plt.show()

