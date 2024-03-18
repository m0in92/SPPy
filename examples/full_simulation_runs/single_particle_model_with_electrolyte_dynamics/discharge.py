"""
This script contains the example usage of the single particle model with electrolyte dynamics for the discharge
operation.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by SPPy. All rights reserved.'
__status__ = 'Deployed'

import SPPy

# Operating parameters
I: float = 1.656
temp: float = 298.15
V_min: float = 3.0
SOC_min: float = 0.1
soc_lib_init: float = 1.0

# Modelling parameters
soc_init_p: float = 0.4956  # from Guo et. al.
soc_init_n: float = 0.7568  # from Guo et. al.

# Setup battery components
cell: SPPy.BatteryCell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                                  soc_init_p=soc_init_p, soc_init_n=soc_init_n,
                                                                  temp_init=temp)
# set-up cycler and solver
dc: SPPy.Discharge = SPPy.Discharge(discharge_current=I, v_min=V_min,
                                    SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init)
solver: SPPy.EnhancedSPSolver = SPPy.EnhancedSPSolver(b_cell=cell, electrode_soc_solver="poly",
                                                      isothermal=True, degradation=False)
sol: SPPy.Solution = solver.solve(cycler=dc, verbose=True)

sol.comprehensive_isothermal_plot()
# print(sol.electrolyte_conc)

