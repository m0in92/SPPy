"""
This script contains the example usage of the single particle model for the discharge operation.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by SPPy. All rights reserved.'
__status__ = 'deployed'

import SPPy

# Operating parameters
I = 1.656
temp = 298.15
V_min = 3
SOC_min = 0.1
soc_lib_init = 1.0

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', soc_lib_init=soc_lib_init,
                                                # SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n,
                                                temp_init=temp)

# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate
sol = solver.solve(cycler_instance=dc)

print(sol.cycle_summary)

# Plot
sol.comprehensive_isothermal_plot()
