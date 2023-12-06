"""
This script contains the example usage of the single particle model for the discharge operation.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by SPPy. All rights reserved.'
__status__ = 'deployed'

import SPPy

# Operating parameters
I = 0.5
temp = 298.15
V_min = 2.5
SOC_min = 0.0

# Modelling parameters
soc_lib_init = 1.0

# Setup battery components
cell: SPPy.BatteryCell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='Chen_2020',
                                                                  soc_lib_init=soc_lib_init,
                                                                  temp_init=temp)
# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate
sol: SPPy.Solution = solver.solve(cycler_instance=dc, verbose=False,
                                  t_increment=0.1)

# Plot
sol.comprehensive_isothermal_plot()
