import time

import matplotlib.pyplot as plt

from SPPy.solvers.electrode_surf_conc import EigenFuncExp, CNSolver, PolynomialApproximation


# Electrode parameters below
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.7568  # initial electrode SOC

# initiate solver instances below
eigen_solver = EigenFuncExp(x_init=SOC_init, n=5, electrode_type='n')
cn_solver = CNSolver(c_init=SOC_init*c_max, electrode_type='n')
poly_solver = PolynomialApproximation(c_init=SOC_init*c_max, electrode_type='n', type='higher')

# ----------------------------------Eigen Solver------------------------------------------------------------------------
# Simulation parameters below
i_app = -1.65  # Applied current [A]
SOC_eigen = SOC_init  # electrode current SOC
dt = 0.1  # time increment [s]
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_eigen, lst_eigen_SOC = [], []
t_start = time.time()  # start timer
while SOC_eigen > 0:
    SOC_eigen = eigen_solver(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_eigen.append(t_prev)
    lst_eigen_SOC.append(SOC_eigen)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"eigen solver solved in {t_end - t_start} s")

# -------------------------------------- CN Solver ---------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_cn, lst_cn_solver = [], []
t_start = time.time()  # start timer
SOC_cn = SOC_init
while SOC_cn > 0:
    SOC_cn = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max, solver_method="TDMA")
    lst_time_cn.append(t_prev)
    lst_cn_solver.append(SOC_cn)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# -------------------------------------- Poly Solver -------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_poly, lst_poly_solver = [], []
t_start = time.time()  # start timer
SOC_poly = SOC_init
while SOC_poly > 0:
    SOC_poly = poly_solver(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_poly.append(t_prev)
    lst_poly_solver.append(SOC_poly)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"Poly solver solved in {t_end - t_start} s")


# ----------------------------------------------Plots------------------------------------------------------------------

plt.plot(lst_time_eigen, lst_eigen_SOC, label="Eigen Expansion Method")
plt.plot(lst_time_cn, lst_cn_solver, label="Crank-Nicolson Scheme")
plt.plot(lst_time_poly, lst_poly_solver, label="Polynomial Approximation")

plt.xlabel("Time [s]")
plt.ylabel("Negative Electrode SOC")
plt.legend()
plt.show()



