"""
This script analyses the relation between the electrolyte concentration and temperature with the expression:
        1+dlnf/dlnc_e
This expression is taken from the reference: Han et al. A numerically efficient method of solving  the full order pseudo
2-D Li-ion cell model. 2021. JPS
"""
from typing import Optional, Union

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt


def func_dlnf(c_e: Union[float, npt.ArrayLike], temp: float, t_c: float) -> float:
    c_e = c_e * 0.001
    return (0.601-0.24*c_e+(0.982-5.1064e-3*(temp-294.15))*c_e**1.5)/(1-t_c)


temp1 = 298.15
temp2 = 263
temp3 = 333
t_c = 0.38
array_ce = np.linspace(0, 4000)
array_dlnf1 = func_dlnf(c_e=array_ce, temp=temp1, t_c=t_c)
array_dlnf2 = func_dlnf(c_e=array_ce, temp=temp2, t_c=t_c)
array_dlnf3 = func_dlnf(c_e=array_ce, temp=temp3, t_c=t_c)

# important results below
print('1 + dlnf at 800 mol/3 at 288.15: ', func_dlnf(800, temp=288.15, t_c=0.384))
print('1 + dlnf at 1000 mol/3 at 288.15: ', func_dlnf(1000, temp=288.15, t_c=0.384))
print('1 + dlnf at 800 mol/3 at 298.15: ', func_dlnf(800, temp=298.15, t_c=0.384))
print('1 + dlnf at 1000 mol/3 at 298.15: ', func_dlnf(1000, temp=298.15, t_c=0.384))
print('1 + dlnf at 800 mol/3 at 308.15: ', func_dlnf(800, temp=308.15, t_c=0.384))
print('1 + dlnf at 1000 mol/3 at 308.15: ', func_dlnf(1000, temp=308.15, t_c=0.384))

# plots below
plt.plot(array_ce, array_dlnf1, label=temp1)
plt.plot(array_ce, array_dlnf2, label=temp2)
plt.plot(array_ce, array_dlnf3, label=temp3)

plt.legend()
plt.show()
