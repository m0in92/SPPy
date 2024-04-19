import time
import pickle

from SPPy.solvers.electrode_surf_conc import CNSolver


# Electrode parameters below
R = 8.5e-6  # electrode particle radius in [m]
c_max = 51410  # max. electrode concentration [mol/m3]
D = 1e-14  # electrode diffusivity [m2/s]
S = 1.1167  # electrode electrochemical active area [m2]
SOC_init = 0.4956  # initial electrode SOC

# initiate solver instances below
cn_solver_p = CNSolver(c_init=c_max*SOC_init, electrode_type='p')
cn_solver_n = CNSolver(c_init=c_max*SOC_init, electrode_type='n')

# Simulation parameters below
i_app = -1.65  # Applied current [A]
dt = 0.1  # time increment [s]

# -------------------------------------- Positive Electrode CN Solver --------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_cn_p, lst_cn_solver_p = [], []
t_start = time.time()  # start timer
SOC_cn = SOC_init
while SOC_cn < 1:
    SOC_cn = cn_solver_p(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_cn_p.append(t_prev)
    lst_cn_solver_p.append(SOC_cn)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# -------------------------------------- Negative Electrode CN Solver --------------------------------------------------

# Simulation parameters below
t_prev = 0  # previous time [s]

# solve for SOC wrt to time
lst_time_cn_n, lst_cn_solver_n = [], []
t_start = time.time()  # start timer
SOC_cn = SOC_init
while SOC_cn > 0:
    SOC_cn = cn_solver_n(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_cn_n.append(t_prev)
    lst_cn_solver_n.append(SOC_cn)

    t_prev += dt  # update the time
t_end = time.time()  # end timer
print(f"CN solver solved in {t_end - t_start} s")

# save results
with open("t_p", "wb") as fp:
    pickle.dump(lst_time_cn_p, fp)

with open("soc_p", "wb") as fp:
    pickle.dump(lst_cn_solver_p, fp)

with open("t_n", "wb") as fp:
    pickle.dump(lst_time_cn_n, fp)

with open("soc_n", "wb") as fp:
    pickle.dump(lst_cn_solver_n, fp)







