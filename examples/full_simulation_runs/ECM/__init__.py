"""
Contains the script for plotting the electrolyte parameters for general interest.
"""

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'developement'

import numpy as np
import matplotlib.pyplot as plt


def kappa_e(c_e: float, temp: float) -> float:
    c_e = 0.001 * c_e
    kappe_e_ = c_e * (-10.5 + 0.074*temp - 6.96e-5*temp**2 + 0.668*c_e -
                  0.0178*c_e*temp + 2.8e-5*c_e*temp**2 + 0.494*c_e*2 - 8.86e-4 * c_e ** 2 * temp) ** 2
    return kappe_e_ * 1e-2

def df(c_e, t_c):
    c_e = 0.001 * c_e
    return (0.601 - 0.24*c_e**0.5 + (0.982 - 5.1064e-3 * (298.15-294.15)) * c_e**1.5) / (1-t_c)


array_ce = np.linspace(0, 3000)

fig = plt.figure()

ax1 = fig.add_subplot(121)
ax1.plot(array_ce, kappa_e(array_ce, temp=263.15), label='263.15')
ax1.plot(array_ce, kappa_e(array_ce, temp=298.15), label='298.15')
ax1.plot(array_ce, kappa_e(array_ce, temp=313.15), label='313.15')
ax1.plot(array_ce, kappa_e(array_ce, temp=333.15), label='333.15')
ax1.legend()

ax2 = fig.add_subplot(122)
ax2.plot(array_ce, (1-0.38) * df(array_ce, 0.38))

plt.show()
