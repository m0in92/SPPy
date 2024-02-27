import numpy as np

import SPPy
from SPPy.solvers.degradation_solvers import ROMSEISolver

import matplotlib.pyplot as plt


# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al
temp: float = 298.15

# Setup battery components
cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                temp_init=temp)
cell.elec_n.i_s = 1.14264e-15  # in mol/m2/s
soc_n: np.ndarray = np.linspace(0.01, 0.7568)
ocp_n: np.ndarray = cell.elec_n.func_OCP(soc_n)

solver: ROMSEISolver = ROMSEISolver(b_cell=cell)
print(solver.solve_current(SOC_n=0.7522, OCP_n=cell.elec_n.func_OCP(0.7522),
                           temp=temp, I=1.656, rel_tol=1e-12))

j_s: np.ndarray = np.array([solver.solve_current(SOC_n=soc_, OCP_n=ocp_,
                           temp=temp, I=1.656)[1] for soc_, ocp_ in zip(soc_n, ocp_n)])
j_i: np.ndarray = np.array([solver.solve_current(SOC_n=soc_, OCP_n=ocp_,
                           temp=temp, I=1.656)[0] for soc_, ocp_ in zip(soc_n, ocp_n)])

fig, ax1 = plt.subplots()
ax1.plot(soc_n, j_i)

ax2 = ax1.twinx()
ax2.plot(soc_n, j_s, color="red")

plt.show()
