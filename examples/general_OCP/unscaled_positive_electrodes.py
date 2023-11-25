import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP import funcs


electrode_temp = 298.15

# SOC_LCO = np.linspace(0.39, 1)
# OCP_LCO = funcs.extract_OCP(SOC_LCO, specie_name='LCO', T=electrode_temp)
#
# SOC_LFP = np.linspace(0.05, 1)
# OCP_LFP = funcs.extract_OCP(SOC_LFP, specie_name='LFP', T=electrode_temp)
#
# SOC_LMO = np.linspace(0.18, 0.95)
# OCP_LMO = funcs.extract_OCP(SOC_LMO, specie_name='LMO', T=electrode_temp)
#
# SOC_NCA = np.linspace(0.19, 1)
# OCP_NCA = funcs.extract_OCP(SOC_NCA, specie_name='NCA', T=electrode_temp)

SOC_NMC = np.linspace(0.39, 0.99)
OCP_NMC = funcs.extract_OCP(SOC_NMC, specie_name='NMC', T=electrode_temp)

# a_min_LCO = OCP_LCO[0]
# a_min_LMO = OCP_LMO[0]
# a_min_NCA = OCP_NCA[0]
# a_min_NMC = OCP_NMC[0]
#
# a_max_LCO = OCP_LCO[-1]
# a_max_LMO = OCP_LMO[-1]
# a_max_NCA = OCP_NCA[-1]
# a_max_NMC = OCP_NMC[-1]
#
# plt.hlines(4.3, 0, 1, colors='red', linestyles='--')
# plt.plot(SOC_LCO, OCP_LCO, label="LCO")
# plt.plot(SOC_LFP, OCP_LFP, label="LFP")
# plt.plot(SOC_LMO, OCP_LMO, label="LMO")
# plt.plot(SOC_NCA, OCP_NCA, label="NCA")
plt.plot(SOC_NMC, OCP_NMC, label="NMC")

plt.legend()
plt.show()
