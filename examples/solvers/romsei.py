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
solver: ROMSEISolver = ROMSEISolver(b_cell=cell)

# print some class attributes and properties
print("k_n: ", solver.k_n)
print("c_e: ", solver.c_e)
print("S: ", solver.S_n)
print("c_s_max: ", solver.c_nmax)
print("U_s: ", solver.U_s)
print("i_s: ", solver.i_s)
print("A: ", solver.A)
print("MW_SEI", solver.MW_SEI)
print("rho_SEI: ", solver.rho)
print("kappa_SEI", solver.kappa)
print(solver.solve_current(SOC_n=0.7522, OCP_n=cell.elec_n.func_OCP(0.7522),
                           temp=temp, I=1.656, rel_tol=1e-12))

soc_n: np.ndarray = np.linspace(0.01, 0.7568)
ocp_n: np.ndarray = cell.elec_n.func_OCP(soc_n)
I_s: np.ndarray = np.array([solver.solve_current(SOC_n=soc_, OCP_n=ocp_,
                           temp=temp, I=1.656)[1] for soc_, ocp_ in zip(soc_n, ocp_n)])
I_i: np.ndarray = np.array([solver.solve_current(SOC_n=soc_, OCP_n=ocp_,
                           temp=temp, I=1.656)[0] for soc_, ocp_ in zip(soc_n, ocp_n)])
print(I_i)

# plots
fig, ax1 = plt.subplots()
ax1.plot(soc_n, I_i, label="J_i")
ax2 = ax1.twinx()
ax2.plot(soc_n, I_s, color="red", label="J_s")

plt.legend()
plt.show()
