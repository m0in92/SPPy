import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP import positive_electrodes_ocps
from SPPy.calc_helpers.numerical_diff import dVdQ

SOC_NMC: np.ndarray = np.linspace(0.39, 0.99)
OCP_NMC: np.ndarray = positive_electrodes_ocps.NMC(soc=SOC_NMC)
SOC_LIB: np.ndarray = np.linspace(0, 1)

# plots
# plt.plot(SOC_LIB, OCP_NMC, label="NMC")
plt.plot(SOC_LIB[1:-1], -dVdQ(cap=SOC_LIB, v=OCP_NMC))

plt.xlabel("SOC")
plt.ylabel("OCP [V]")

plt.title("OCP of Positive Electrodes at 298.15 K")

plt.legend()
plt.show()