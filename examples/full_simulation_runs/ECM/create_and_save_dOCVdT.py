import pickle

import matplotlib.pyplot as plt
import numpy as np
import scipy

import SPPy
from parameter_sets.test.funcs import dOCPdT_p, dOCPdT_n


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

# Setup battery components
cell1 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T1)
cell1.cap = 1.92
cell2 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T2)
cell2.cap = 1.92

# set-up cycler and solver
dc1 = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB=1, SOC_LIB_min=0)
dc2 = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB=1, SOC_LIB_min=0)
solver1 = SPPy.SPPySolver(b_cell=cell1, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')
solver2 = SPPy.SPPySolver(b_cell=cell2, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate
sol1 = solver1.solve(cycler_instance=dc1)
sol2 = solver2.solve(cycler_instance=dc2)

# save important results in files, from where the results can be extracted for later
with open("SOC_dOCVdT", "wb") as f_SOC:
    pickle.dump(sol1.SOC_LIB, f_SOC)

with open("dOCVdT", "wb") as f_OCV:
    pickle.dump(dOCPdT_p(sol1.x_surf_p) - dOCPdT_n(sol1.x_surf_n), f_OCV)

# Plot
plt.plot(sol1.SOC_LIB, dOCPdT_p(sol1.x_surf_p) - dOCPdT_n(sol1.x_surf_n))
# plt.plot(array_SOC, dOCVdT)
plt.xlabel('SOC')
plt.ylabel(r'$\frac{dOCV}{dT} [V/K]$')

plt.show()
