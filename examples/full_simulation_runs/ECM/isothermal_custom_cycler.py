"""
This example script conducts the Thevenin ECM simulation (with 1 RC pair) using custom cycler.
"""
__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'developement'

import pickle

import SPPy
import scipy

# Read experimental data below
sol_exp = SPPy.ECMSolution().read_from_csv_file(filepath='A1-A123-Dynamics.csv')

# Simulation Parameters
R0: float = 0.225
R1: float = 0.001
C1: float = 0.03
Q: float = 1.1


def func_ocv(soc):
    a, b, c, d, e, f, g, h, i, j, k, l, m = \
        [3.39803735e+04, -1.86083253e+05, 4.40650925e+05, -5.86500338e+05,
         4.74171271e+05, -2.29840038e+05, 5.53052667e+04, 3.05616190e+03,
         -6.45471514e+03, 1.99278174e+03, -2.99381888e+02, 2.29345284e+01,
         2.53496894e+00]

    return a * soc ** 12 + b * soc ** 11 + c * soc ** 10 + \
           d * soc ** 9 + e * soc ** 8 + f * soc ** 7 + \
           g * soc ** 6 + h * soc ** 5 + i * soc ** 4 + \
           j * soc ** 3 + k * soc ** 2 + l * soc + m


with open("SOC_dOCVdT", "rb") as f_SOC:
    SOC_dOCVdT = pickle.load(f_SOC)

with open("dOCVdT", "rb") as f_OCV:
    dOCVdT = pickle.load(f_OCV)

func_dOCVdT = scipy.interpolate.interp1d(SOC_dOCVdT, dOCVdT, fill_value='extrapolate')


def func_eta(i_app: float, temp: float) -> float:
    return 1 if i_app <= 0 else 0.9995


v_min = 1.0
v_max = 4.5
soc_min = 0.0
soc_LIB = 1

# setup the battery cell
cell = SPPy.ECMBatteryCell(R0_ref=R0, R1_ref=R1, C1=C1, temp_ref=298.15, Ea_R0=4000, Ea_R1=4000,
                           rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085, cap=Q, v_max=4.2, v_min=2.5,
                           soc_init=soc_min, temp_init=298.15,
                           func_eta=func_eta, func_ocv=func_ocv, func_docvdtemp=func_dOCVdT)
# set-up cycler and solver
custom_step = SPPy.CustomCycler(array_t=sol_exp.array_t, array_I=sol_exp.array_I, V_min=v_min, V_max=v_max,
                                SOC_LIB=0.0, SOC_LIB_min=0.0, SOC_LIB_max=1.0)
solver = SPPy.DTSolver(battery_cell_instance=cell, isothermal=True)
# solve
sol = solver.solve(cycling_step=custom_step, dt=10)

# Plots
sol.comprehensive_plot()
