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
print(solver.solve_current(soc=0.7522, ocp=cell.elec_n.func_OCP(0.7522),
                           temp=temp, I=1.656))

I_i: list = []
I_s: list = []
soc_n: np.ndarray = np.linspace(0.01, 0.7568)
for i, soc_ in enumerate(soc_n):
    cell.elec_n.SOC = soc_
    ocp_: float = cell.elec_n.OCP
    solver: ROMSEISolver = ROMSEISolver(b_cell=cell)
    I_i_, I_s_ = solver.solve_current(soc=soc_, ocp=ocp_, temp=temp, I=1.656)
    I_i.append(I_i_)
    I_s.append(I_s_)

# plots
fig, ax1 = plt.subplots()
ax1.plot(soc_n, I_i, label="intercalation current")
ax2 = ax1.twinx()
ax2.plot(soc_n, I_s, color="red", label="side-reaction current")

plt.xlabel("Negative Electrode SOC")
plt.ylabel("Lithium Ion Current [A]")

plt.legend()
plt.show()
