import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from parameter_sets.test import funcs


array_soc_p: npt.ArrayLike = np.linspace(0.45, 1)
array_soc_n: npt.ArrayLike = np.linspace(0.01, 0.85)
array_ocp_p: npt.ArrayLike = funcs.OCP_ref_p(array_soc_p)
array_ocp_n: npt.ArrayLike = funcs.OCP_ref_n(array_soc_n)

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.plot(array_soc_n, array_ocp_n, label='n')
ax1.set_xlabel('SOC_n')
ax1.set_ylabel('OCP [V]')

ax2 = fig.add_subplot(222)
ax2.plot(array_soc_p, array_ocp_p)
ax2.set_xlabel('SOC_p')
ax2.set_ylabel('OCP [V]')

# ax3 = fig.add_subplot(223)
# ax3.plot(arr)
# ax3.plot(array_soc_n, array_ocp_n)

plt.tight_layout()
plt.legend()
plt.show()
