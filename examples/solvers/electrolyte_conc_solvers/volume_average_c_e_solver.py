"""
Contains an example of the use of electrolyte concentration volume averaging solver
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by SPPy. All rights reserved."
__status__ = "development"

import numpy as np
import matplotlib.pyplot as plt

from SPPy.solvers.electrolyte_conc import ElectrolyteConcVolAvgSolver
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
D_e: float = 3.5e-10
D_e_eff_p: float = D_e * (epsilon_ep**1.5)
D_e_eff_s: float = D_e * (epsilon_sep**1.5)
D_e_eff_n: float = D_e * (epsilon_en**1.5)
L_n: float = 7.35e-5
L_s: float = 2e-5
L_p: float = 7e-5

# Simulation parameters
dt: float = 0.1
t_end: int = 3600  # [s]

# Simulation below
conc_solver: ElectrolyteConcVolAvgSolver = ElectrolyteConcVolAvgSolver(L_n=L_n, L_s=L_s, L_p=L_p,
                                                                       epsilon_n=epsilon_en,
                                                                       epsilon_s=epsilon_sep,
                                                                       epsilon_p=epsilon_ep,
                                                                       D_n=D_e_eff_n, D_s=D_e_eff_s, D_p=D_e_eff_p,
                                                                       a_n=a_s_n, a_p=a_s_p, t_c=t_c, c_e_init=1000)

j_p: float = SPMe.molar_flux_electrode(I=-1.656, S=1.1167, electrode_type='p')
j_n: float = SPMe.molar_flux_electrode(I=-1.656, S=0.7824, electrode_type='n')  # [mol/m2/s]

t_prev: float = 0.0
for simulation_index in range(t_end):
    conc_solver.solve(t_prev=t_prev, avg_j_p=j_p, avg_j_n=j_n, dt=dt)
    t_prev += dt

x_n: np.ndarray = np.linspace(0.0, L_n)
x_p: np.ndarray = np.linspace(L_n+L_s, L_n+L_s+L_p)
print(conc_solver.conc_profile_n(x_n))
print(conc_solver.conc_profile_p(x_p))

plt.plot(x_n, conc_solver.conc_profile_n(L_value=x_n))
plt.plot(x_p, conc_solver.conc_profile_p(L_value=x_p))
plt.show()
