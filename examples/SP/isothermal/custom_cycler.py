import pandas as pd
import matplotlib.pyplot as plt

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
cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n,
                                                temp_init=T)

# set-up cycler and solver. Also plot the cycler time [s] and current [A]. For this example the data is extracted from
# a csv file.
df = pd.read_csv('example_data.csv')
cycler = SPPy.CustomCycler(array_t=df['t [s]'].to_numpy(), array_I=df['I [A]'].to_numpy(), SOC_LIB=1.0,
                           V_min=V_min, V_max=V_max)
cycler.plot()
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False)

# simulate and plot
sol = solver.solve(cycler_instance=cycler, verbose=False)

sol.plot_tV()
