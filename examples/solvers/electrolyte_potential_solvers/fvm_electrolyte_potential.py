"""
Contains an example of using electrolyte potential solver in a simulation. The solver uses numerical finite volume
method (FVM).
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright SPPy 2024. All rights reserved."
__status__ = "Development"


import numpy as np
import matplotlib.pyplot as plt

from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates
from SPPy.solvers.electrolyte_conc import ElectrolyteConcFVMSolver
from SPPy.solvers.electrolyte_potential import ElectrolytePotentialFVMSolver
from SPPy.models.battery import SPMe


# Battery cell parameters
epsilon_ep: float = 0.485
epsilon_sep: float = 0.785
epsilon_en: float = 0.385
a_s_p: float = 7.28e3
a_s_n: float = 5.78e3
brugg: float = 4
t_c: float = 0.354
kappa_e: float = 0.2875
temp: float = 298.15

# Simulation parameters
dt: float = 0.1
t_end: int = 360  # [s]

co_ords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
conc_solver: ElectrolyteConcFVMSolver = ElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=t_c,
                                                                 epsilon_en=epsilon_en, epsilon_esep=epsilon_sep,
                                                                 epsilon_ep=epsilon_ep,
                                                                 a_sn=a_s_n, a_sp=a_s_p,
                                                                 D_e=3.5e-10,
                                                                 brugg=brugg,
                                                                 c_e_init=1000)
potential_solver: ElectrolytePotentialFVMSolver = ElectrolytePotentialFVMSolver(fvm_coords=co_ords,
                                                                                epsilon_en=epsilon_en,
                                                                                epsilon_esep=epsilon_sep,
                                                                                epsilon_ep=epsilon_ep,
                                                                                a_s_n=a_s_n, a_s_p=a_s_p,
                                                                                brugg=brugg,
                                                                                t_c=t_c, kappa_e=kappa_e,
                                                                                temp=temp)

j_p = SPMe.molar_flux_electrode(I=-1.656, S=1.1167, electrode_type='p') * np.ones(len(co_ords.array_x_p))  # [mol/m2/s]
j_sep = np.zeros(len(co_ords.array_x_s))  # [mol/m2/s]
j_n = SPMe.molar_flux_electrode(I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(co_ords.array_x_n))  # [mol/m2/s]
j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]

for i in range(t_end):
    conc_solver.solve_ce(j=j, dt=dt, solver_method='TDMA')

terminal_phi, phi, rel_phi = potential_solver.solve_phi_e(j=j, c_e=conc_solver.array_c_e)

print(terminal_phi, rel_phi)

print(f"Electrolyte Length Dimensions [m]: {conc_solver.co_ords.array_x}")
print(f"Electrolyte conc. [mol/m3]: {conc_solver.array_c_e}")
print(f"Electrolyte conc. at L=0 [mol/m3]: {conc_solver.extrapolate_conc(L_value=0.0)} mol/m3")
print(f"Electrolyte conc. at L=L_cell [mol/m3]: {conc_solver.extrapolate_conc(L_value=19.3e-5)} mol/m3")

print(f"Electrolyte potential [V]: {phi-terminal_phi}")


plt.xlabel("Battery Cell Thickness [m]")
plt.ylabel("Electrolyte Potential. [V]")
plt.title(f"Electrolyte Potential. [V] after {t_end} s of discharge")
plt.ticklabel_format(axis="x", scilimits=[-3, 1])
plt.plot(co_ords.array_x, phi-terminal_phi)
plt.show()
