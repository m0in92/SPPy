"""
This script demonstrates the example usage of the solid phase electrode potential using the finite volume method (FVM).
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by SPPy. All rights reserved."
__status__ = "deployed"

import numpy as np
import matplotlib.pyplot as plt

from SPPy.models.battery import SPMe
from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates
from SPPy.solvers.electrode_potential import ElectrodePotentialFVMSolver

L_n: float = 8e-5
L_s: float = 2.5e-5
L_p: float = 8.8e-5

a_s_p: float = 7.28e3
a_s_n: float = 5.78e3

brugg_p: float = 1.5
brugg_n: float = 1.5
epsilon_ep: float = 0.485
epsilon_sep: float = 0.785
epsilon_en: float = 0.385
sigma_p: float = 3.8
sigma_n: float = 100
sigma_eff_p: float = sigma_p * (epsilon_ep ** brugg_p)
sigma_eff_n: float = sigma_n * (epsilon_ep ** brugg_n)

coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
fvm_solver_p: ElectrodePotentialFVMSolver = ElectrodePotentialFVMSolver(fvm_coords=coords,
                                                                        electrode_type='p',
                                                                        sigma_eff=sigma_eff_p, a_s=a_s_p)
fvm_solver_n: ElectrodePotentialFVMSolver = ElectrodePotentialFVMSolver(fvm_coords=coords,
                                                                        electrode_type='n',
                                                                        sigma_eff=sigma_eff_n, a_s=a_s_n)
j_n: np.ndarray = SPMe.molar_flux_electrode(I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(coords.array_x_n))
# [mol/m2/s]
j_p: np.ndarray = SPMe.molar_flux_electrode(I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(coords.array_x_n))
# [mol/m2/s]

plt.plot(coords.array_x_n, fvm_solver_n.solve_phi_s(j=j_n, terminal_potential=0.0).flatten())
plt.plot(coords.array_x_p, fvm_solver_p.solve_phi_s(j=j_p, terminal_potential=4.2).flatten())

plt.ticklabel_format(axis='x', scilimits=[-1, 1])
plt.show()


