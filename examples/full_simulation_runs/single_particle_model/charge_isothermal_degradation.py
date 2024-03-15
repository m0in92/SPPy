"""
This script contains the example usage of the single particle model in the charge operation. The degradation mode used
if the reduced-order SEI model.
"""

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2024 by Moin Ahmed. All rights reserved.'
__status__ = 'deployed'

import matplotlib.pyplot as plt

import SPPy

# Operating parameters
I: float = 1.656
T: float = 298.15
V_max: float = 4.2
SOC_max: float = 0.9
SOC_LIB: float = 0.9

# Modelling parameters
SOC_init_p: float = 0.989011
SOC_init_n: float = 0.01890232

# Setup battery components
cell: SPPy.BatteryCell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                  soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                  temp_init=T)

# set-up cycler and solver
dc: SPPy.Charge = SPPy.Charge(charge_current=I, V_max=V_max, SOC_LIB_max=SOC_max, SOC_LIB=SOC_LIB)
solver: SPPy.SPPySolver = SPPy.SPPySolver(b_cell=cell, isothermal=True, degradation=True,
                                          electrode_SOC_solver='poly')

# simulate
sol: SPPy.Solution = solver.solve(cycler_instance=dc)

# Plot
sol.plot_degradation()

