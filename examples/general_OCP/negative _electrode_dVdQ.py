import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP.negative_electrode_ocps import graphite
from SPPy.calc_helpers.numerical_diff import dVdQ


SOC_graphite: np.ndarray = np.linspace(0.05, 0.815)
OCP_graphite: np.ndarray = graphite(soc=SOC_graphite)

plt.plot(SOC_graphite[1:-1], dVdQ(cap=SOC_graphite, v=-OCP_graphite))
plt.show()
