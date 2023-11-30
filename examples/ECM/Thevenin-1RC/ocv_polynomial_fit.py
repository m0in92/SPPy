"""
This module attempts to fit an OCV datapoints to a polynomial function using scipy.
"""
import pickle

import numpy as np
import numpy.typing as npt
import scipy
import matplotlib.pyplot as plt


# the saved data is loaded below. It contains the interpolation function that was constructed using the interpolation
# function. Calling the interpolation function is computationally slow.
with open("../saved_results/SOC", "rb") as f_SOC:
    SOC = pickle.load(f_SOC)

with open("../saved_results/OCV", "rb") as f_OCV:
    OCV = pickle.load(f_OCV)

with open("../saved_results/SOC_dOCVdT", "rb") as f_SOC:
    SOC_dOCVdT = pickle.load(f_SOC)

with open("../saved_results/dOCVdT", "rb") as f_OCV:
    dOCVdT = pickle.load(f_OCV)

# Fitting happens below
func_OCV = scipy.interpolate.interp1d(SOC, OCV, fill_value='extrapolate')
func_dOCVdT = scipy.interpolate.interp1d(SOC_dOCVdT, dOCVdT, fill_value='extrapolate')

array_soc: npt.ArrayLike = np.linspace(0, 1)
array_soc_extended: npt.ArrayLike = np.linspace(-0.1, 1.1)  # to observe the curve behaviour outside of the SOC limits,
# and hopefully they are reasonable
array_ocv: npt.ArrayLike = func_OCV(array_soc)
array_docv: npt.ArrayLike = func_dOCVdT(array_soc)

polyfit_degree: int = 11
array_polyfit_ocv: npt.ArrayLike = np.polyfit(array_soc, array_ocv, deg=polyfit_degree)
func_ocv_fit = np.poly1d(array_polyfit_ocv)
array_polyfit_docv: npt.ArrayLike = np.polyfit(array_soc, array_docv, deg=polyfit_degree)
func_docv_fit = np.poly1d(array_polyfit_docv)
print('OCV fit Poly Array: ', array_polyfit_ocv,
      'dOCV fit Poly Array: ', array_polyfit_docv)

# Prints some numbers for testing purposes
print(func_ocv_fit(0.5))
print(func_docv_fit(0.5))

# Plotting happens below
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(array_soc, array_ocv, label='actual')
ax1.plot(array_soc_extended, func_ocv_fit(array_soc_extended), label='fit')

ax2 = ax1.twinx()
ax2.plot(array_soc, array_docv, 'r', label='actual')
ax2.plot(array_soc, func_docv_fit(array_soc), label='fit')

ax1.set_xlabel('SOC')
ax1.set_ylabel('OCV [V]')
ax2.set_ylabel('dOCV/dT [V/K]')

ax1.legend()
ax2.legend(loc='lower right')

plt.tight_layout()
plt.show()

