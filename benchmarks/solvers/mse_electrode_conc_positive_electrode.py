import time
from typing import Union, Optional
import pickle

import numpy as np

from SPPy.solvers.electrode_surf_conc import EigenFuncExp, CNSolver, PolynomialApproximation


def mse(actual: np.ndarray, sim: np.ndarray) -> float:
    return np.mean((actual - sim) ** 2)


# actual results
with open("t_p", "rb") as fp:
    t_p = pickle.load(fp)

with open("soc_p", "rb") as fp:
    soc_p = pickle.load(fp)


# Electrode parameters below
R = 8.5e-6  # electrode particle radius in [m]
c_max = 51410  # max. electrode concentration [mol/m3]
D = 1e-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# initiate solver instances below
eigen_solver = EigenFuncExp(x_init=SOC_init, n=5, electrode_type='p')
poly_solver = PolynomialApproximation(c_init=SOC_init*c_max, electrode_type='p', type='higher')
poly_solver_two: PolynomialApproximation = PolynomialApproximation(c_init=SOC_init*c_max, electrode_type='p',
                                                                   type='two')

# ----------------------------------Eigen Solver------------------------------------------------------------------------
# Simulation parameters below
i_app = -1.65  # Applied current [A]
SOC_eigen = SOC_init  # electrode current SOC
dt = 0.1  # time increment [s]
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_eigen_p, lst_eigen_SOC_p = [], []
t_start = time.time()  # start timer
while SOC_eigen < 1:
    SOC_eigen = eigen_solver(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_eigen_p.append(t_prev)
    lst_eigen_SOC_p.append(SOC_eigen)

    t_prev += dt  # update the time
t_end = time.time()  # end timer

print(f"MSE in {mse(actual=soc_p[:4000], sim=np.array(lst_eigen_SOC_p)[:4000])}")

# -------------------------------------- Poly Solver -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_poly_p, lst_poly_solver_p = [], []
t_start = time.time()  # start timer
SOC_poly = SOC_init
while SOC_poly < 1:
    SOC_poly = poly_solver(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_poly_p.append(t_prev)
    lst_poly_solver_p.append(SOC_poly)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"MSE in {mse(actual=soc_p[:4000], sim=np.array(lst_poly_solver_p)[:4000])}")

# -------------------------------------- Poly Solver _ two terms -------------------------------------------------------------------

# Simulation parameters below
t_prev: float = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_poly_two_p, lst_poly_solver_two_p = [], []
t_start = time.time()  # start timer
SOC_poly = SOC_init
while SOC_poly < 1:
    SOC_poly = poly_solver_two(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_poly_two_p.append(t_prev)
    lst_poly_solver_two_p.append(SOC_poly)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"MSE in {mse(actual=soc_p[:4000], sim=np.array(lst_poly_solver_two_p)[:4000])}")

