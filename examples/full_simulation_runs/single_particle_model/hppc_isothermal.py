"""
Contains the example implementation of SPPy using custom cycler under isothermal conditions.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by SPPy. All rights reserved.'
__status__ = 'development'

import pandas as pd

import SPPy

# Operating parameters
I = 1.656
T = 298.15
V_min = 3
V_max = 4
num_cycles = 10
charge_current = 1.656
discharge_current = 1.656
rest_time = 30

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                temp_init=T)

# set-up cycler and solver. Also plot the cycler time [s] and current [A]. For this example the data is extracted from
# a csv file.
df = pd.read_csv('example_data.csv')
cycler = SPPy.HPPCCycler(t1=500, t2=100, i_app=1.5,
                         charge_or_discharge='discharge',
                         V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                         soc_lib_max=1.0, soc_lib=1.0, hppc_steps=10)
cycler.plot()
solver = SPPy.SPPySolver(b_cell=cell, isothermal=True, degradation=False,
                         electrode_SOC_solver="poly")

# simulate and plot
sol = solver.solve(cycler_instance=cycler, verbose=True)

sol.comprehensive_isothermal_plot()
