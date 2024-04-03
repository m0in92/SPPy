import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from SPPy.parameter_estimations.procedural import OCVData
from SPPy.general_OCP.positive_electrodes_ocps import LCO
from SPPy.general_OCP.negative_electrode_ocps import graphite


df: pd.DataFrame = pd.read_csv("data/INR18650_slow_charge.csv")
t_charge: np.ndarray = df['t [s]'].to_numpy()
v_charge: np.ndarray = df['V [V]'].to_numpy()

param_estimator: OCVData = OCVData(func_ocp_p=LCO, func_ocp_n=graphite,
                                   soc_p_min_1=0.0, soc_p_min_2=0.0,
                                   soc_p_max_1=1.0, soc_p_max_2=1.0,
                                   soc_n_min_1=0.0, soc_n_min_2=0.0,
                                   soc_n_max_1=1.0, soc_n_max_2=1.0,
                                   charge_or_discharge='charge')


# plots
plt.plot(t_charge, v_charge)
plt.show()

