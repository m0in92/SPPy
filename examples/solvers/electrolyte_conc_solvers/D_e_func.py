from typing import Union

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt


def func_D_e(c_e: Union[float, npt.ArrayLike], temp: float) -> float:
    """
    Calculates the lithium-ion diffusivity in the electrolyte as a func of lithium-ion concentration and temperature
    Reference: Han et al. A numerically efficient method for solving the full-order pseudo-2D Li-ion cell model.
    2021. Journal of Power Sources. 490

    :param c_e: lithium-ion concentration [mol/m3]
    :param temp: electrolyte temp [K]
    :return: (float) diffusivity of the lithium-ion [m2/s]
    """
    c_e = 0.001 * c_e  # in the original work the concentration was in mol/l
    return (10 ** (-4.43 - 54 / (temp - (229+5*c_e)) - 0.22 * c_e)) * 1e-4  # the original D_e was in cm2/s


temp1 = 298.15
temp2 = 333.0
temp3 = 262.0
array_c_e = np.linspace(0, 5000)
array_D_e1 = func_D_e(array_c_e, temp=temp1)
array_D_e2= func_D_e(array_c_e, temp=temp2)
array_D_e3= func_D_e(array_c_e, temp=temp3)

print('D_e at 800 mol/3 at 288.15: ', func_D_e(800, temp=288.15))
print('D_e at 1000 mol/3 at 288.15: ', func_D_e(1000, temp=288.15))
print('D_e at 800 mol/3 at 298.15: ', func_D_e(800, temp=298.15))
print('D_e at 1000 mol/3 at 298.15: ', func_D_e(1000, temp=298.15))
print('D_e at 800 mol/3 at 308.15: ', func_D_e(800, temp=308.15))
print('D_e at 1000 mol/3 at 308.15: ', func_D_e(1000, temp=308.15))

plt.plot(array_c_e, array_D_e1, label=temp1)
plt.plot(array_c_e, array_D_e2, label=temp2)
plt.plot(array_c_e, array_D_e3, label=temp3)
plt.xlabel('conc [$mol/m^3$]')
plt.ylabel('$D_e [m^2/s]$')

plt.legend()
plt.tight_layout()
plt.show()
