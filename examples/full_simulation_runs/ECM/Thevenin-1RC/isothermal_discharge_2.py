"""
This module is similiar to the isotherm_discharge.py, however it uses the .read_from_parametersets method for
parameter determination.
"""


import SPPy


# Simulation Parameters
I = 1.65
V_min = 2.5
SOC_min = 0
SOC_LIB = 1

# setup the battery cell
cell = SPPy.ECMBatteryCell.read_from_parametersets(parameter_set_name='test', soc_init=1.0, temp_init=298.15)
# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
solver = SPPy.DTSolver(battery_cell_instance=cell, isothermal=True)
# solve
sol = solver.solve(cycling_step=dc)

# Plots
sol.comprehensive_plot()
