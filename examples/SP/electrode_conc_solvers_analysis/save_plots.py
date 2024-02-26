from neg_electrode import *
from examples.solvers.electrode_conc_solvers.pos_electrode_single_particle import *


fig = plt.figure(figsize=(7.5, 3), dpi=300)

ax1 = fig.add_subplot(121)
ax1.plot(lst_time_eigen, lst_eigen_SOC, label="Eigen Expansion Method")
ax1.plot(lst_time_cn, lst_cn_solver, label="Crank-Nicolson Scheme")
ax1.plot(lst_time_poly, lst_poly_solver, label="Polynomial Approximation")
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Negative Electrode SOC")
ax1.legend()

ax2 = fig.add_subplot(122)
ax2.plot(lst_time_eigen_p, lst_eigen_SOC_p, label="Eigen Expansion Method")
ax2.plot(lst_time_cn_p, lst_cn_solver_p, label="Crank-Nicolson Scheme")
ax2.plot(lst_time_poly_p, lst_poly_solver_p, label="Polynomial Approximation")
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Positive Electrode SOC")
ax2.legend()

plt.tight_layout()
plt.savefig("G:\My Drive\Writings\Electrochemical_models\SPM\ElectrodeSOCDiffSolvers.png")
plt.show()
