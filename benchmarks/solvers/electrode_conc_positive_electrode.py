import time
import matplotlib.pyplot as plt

from SPPy.solvers.electrode_surf_conc import EigenFuncExp, CNSolver, PolynomialApproximation


# Electrode parameters below
R = 8.5e-6  # electrode particle radius in [m]
c_max = 51410  # max. electrode concentration [mol/m3]
D = 1e-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# initiate solver instances below
eigen_solver = EigenFuncExp(x_init=SOC_init, n=5, electrode_type='p')
cn_solver = CNSolver(c_init=c_max*SOC_init, electrode_type='p')
poly_solver = PolynomialApproximation(c_init=SOC_init*c_max, electrode_type='p', type='higher')

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
print(f"eigen solver solved in {t_end - t_start} s")

# -------------------------------------- CN Solver ---------------------------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_cn_p, lst_cn_solver_p = [], []
t_start = time.time()  # start timer
SOC_cn = SOC_init
while SOC_cn < 1:
    SOC_cn = cn_solver(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_cn_p.append(t_prev)
    lst_cn_solver_p.append(SOC_cn)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

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
print(f"Poly solver solved in {t_end - t_start} s")

# ----------------------------------------------Plots------------------------------------------------------------------

plt.plot(lst_time_eigen_p, lst_eigen_SOC_p, label="Eigen Expansion Method")
plt.plot(lst_time_cn_p, lst_cn_solver_p, label="Crank-Nicolson Scheme")
plt.plot(lst_time_poly_p, lst_poly_solver_p, label="Polynomial Approximation")
plt.xlabel("Time [s]")
plt.ylabel("Positive Electrode SOC")
plt.legend()
plt.show()



