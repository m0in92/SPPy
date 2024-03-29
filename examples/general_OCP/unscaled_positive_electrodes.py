import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP import funcs
from SPPy.general_OCP import positive_electrodes_ocps


electrode_temp = 298.15

SOC_LCO: np.ndarray = np.linspace(0.39, 1)
OCP_LCO: np.ndarray = positive_electrodes_ocps.LCO(soc=SOC_LCO)
# OCP_LCO = funcs.extract_OCP(SOC_LCO, specie_name='LCO', T=electrode_temp)

SOC_LFP: np.ndarray = np.linspace(0.05, 1)
OCP_LFP: np.ndarray = positive_electrodes_ocps.LFP(soc=SOC_LFP)
# OCP_LFP: np.ndarray = funcs.extract_OCP(SOC_LFP, specie_name='LFP', T=electrode_temp)

SOC_LMO: np.ndarray = np.linspace(0.18, 0.95)
OCP_LMO: np.ndarray = positive_electrodes_ocps.LMO(soc=SOC_LMO)
# OCP_LMO: np.ndarray = funcs.extract_OCP(SOC_LMO, specie_name='LMO', T=electrode_temp)

SOC_NCA: np.ndarray = np.linspace(0.19, 1)
OCP_NCA: np.ndarray = positive_electrodes_ocps.NCA(soc=SOC_NCA)
# OCP_NCA: np.ndarray = funcs.extract_OCP(SOC_NCA, specie_name='NCA', T=electrode_temp)

SOC_NMC: np.ndarray = np.linspace(0.39, 0.99)
OCP_NMC: np.ndarray = positive_electrodes_ocps.NMC(soc=SOC_NMC)
# OCP_NMC = funcs.extract_OCP(SOC_NMC, specie_name='NMC', T=electrode_temp)

a_min_LCO: float = OCP_LCO[0]
a_min_LMO: float = OCP_LMO[0]
a_min_NCA: float = OCP_NCA[0]
a_min_NMC: float = OCP_NMC[0]

a_max_LCO: float = OCP_LCO[-1]
a_max_LMO: float = OCP_LMO[-1]
a_max_NCA: float = OCP_NCA[-1]
a_max_NMC: float = OCP_NMC[-1]

plt.hlines(4.3, 0, 1, colors='red', linestyles='--')
plt.plot(SOC_LCO, OCP_LCO, label="LCO")
plt.plot(SOC_LFP, OCP_LFP, label="LFP")
plt.plot(SOC_LMO, OCP_LMO, label="LMO")
plt.plot(SOC_NCA, OCP_NCA, label="NCA")
plt.plot(SOC_NMC, OCP_NMC, label="NMC")

plt.xlabel("SOC")
plt.ylabel("OCP [V]")

plt.title("OCP of Positive Electrodes at 298.15 K")

plt.legend()
plt.show()
