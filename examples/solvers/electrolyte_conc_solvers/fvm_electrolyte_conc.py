"""
Contains an example of using electrolyte solver in a simulation. The solver uses numerical finite volume
method (FVM).
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright SPPy 2024. All rights reserved."
__status__ = "Deployed"

import time

import numpy as np
import matplotlib.pyplot as plt

from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates
from SPPy.solvers.electrolyte_conc import ElectrolyteConcFVMSolver
from SPPy.models.battery import SPMe

# Simulation parameters
dt: float = 0.1
max_iter: int = 1000

co_ords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
conc_solver: ElectrolyteConcFVMSolver = ElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=0.354,
                                                                 epsilon_en=0.385, epsilon_esep=0.785, epsilon_ep=0.485,
                                                                 a_sn=5.78e3, a_sp=7.28e3,
                                                                 D_e=3.5e-10,
                                                                 brugg=4,
                                                                 c_e_init=1000)

j_p = SPMe.molar_flux_electrode(I=-1.656, S=1.1167, electrode_type='p') * np.ones(len(co_ords.array_x_p))  # [mol/m2/s]
j_sep = np.zeros(len(co_ords.array_x_s))  # [mol/m2/s]
j_n = SPMe.molar_flux_electrode(I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(co_ords.array_x_n))  # [mol/m2/s]
j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]

time_start: int = time.time()
for i in range(max_iter):
    conc_solver.solve_ce(j=j, dt=dt, solver_method='TDMA')
time_end: int = time.time()

print("Simulation loop solution time ", time_end - time_start, " s.")

print(f"Electrolyte Length Dimensions [m]: {conc_solver.co_ords.array_x}")
print(f"Electrolyte conc. [mol/m3]: {conc_solver.array_c_e}")
print(f"Electrolyte conc. at L=0 [mol/m3]: {conc_solver.extrapolate_conc(L_value=0.0)} mol/m3")
print(f"Electrolyte conc. at L=L_cell [mol/m3]: {conc_solver.extrapolate_conc(L_value=19.3e-5)} mol/m3")

plt.xlabel("Battery Cell Thickness [m]")
plt.ylabel("Electrolyte Conc. [mol/m3]")
plt.title(f"Electrolyte Conc. [mol/m3] after {max_iter * dt} s of discharge")
plt.ticklabel_format(axis="x", scilimits=[-3, 1])
plt.plot(co_ords.array_x, conc_solver.array_c_e)
plt.show()
