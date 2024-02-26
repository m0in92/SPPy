import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
V_max = 4
num_cycles = 2
charge_current = 1.656
discharge_current = 1.656
rest_time = 30

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al.

# Setup battery components
cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                temp_init=T)

# set-up cycler and solver
cycler = SPPy.CC(num_cycles=num_cycles, charge_current=charge_current, discharge_current=discharge_current,
                 rest_time=rest_time, V_max=V_max, V_min=V_min)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False)

# simulate
sol = solver.solve(cycler_instance=cycler)

# Plot
sol.comprehensive_plot()
