"""
This module calculates and stores a function for the OCV and the dOCV/dT using the simulation results from the
simgle particle model.
"""

__author__ = "Moin Ahmed"

import pickle

import matplotlib.pyplot as plt

import SPPy


# Operating parameters
I = 1.92
T = 298.15
V_min = 2.5
SOC_min = 0.1
SOC_LIB = 1

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, temp_init=T)
cell.cap = 1.92

# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB=1, SOC_LIB_min=0)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate
sol = solver.solve(cycler_instance=dc)

# save to a file
with open("SOC", "wb") as f_SOC:
    pickle.dump(sol.SOC_LIB, f_SOC)

with open("OCV", "wb") as f_OCV:
    pickle.dump(sol.OCV_LIB, f_OCV)

# Plot
plt.plot(sol.SOC_LIB, sol.OCV_LIB)
plt.show()
