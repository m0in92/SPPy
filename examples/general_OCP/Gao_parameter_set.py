import numpy as np
import matplotlib.pyplot as plt

import SPPy


electrode_temp = 298.15
soc_init_p, soc_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et. al.


SOC_n = np.linspace(0, 0.8)
SOC_p = np.linspace(0.4, 1)
cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                soc_init_p=soc_init_p, soc_init_n=soc_init_n,
                                                temp_init=electrode_temp)
cell.elec_n.T = 300.15
cell.elec_n.SOC = 0.5

print(cell.elec_n.D)
print(cell.elec_n.k)
print(cell.elec_p.OCP)
print("Negative Electrode OCP: ", cell.elec_n.OCP, " V with SOC of ", cell.elec_n.SOC)

print(cell.elec_p.func_dOCPdT(0.5))
print(cell.elec_n.func_dOCPdT(0.5))

plt.plot(SOC_n, cell.elec_n.func_OCP(SOC_n), label='n')
plt.plot(SOC_p, cell.elec_p.func_OCP(SOC_p), label='p')
plt.xlabel('SOC_n')
plt.ylabel('OCP [V]')

plt.legend()
plt.show()