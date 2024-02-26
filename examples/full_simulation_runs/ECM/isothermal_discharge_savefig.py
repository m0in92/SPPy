import pickle

import scipy
import matplotlib.pyplot as plt

import SPPy
from parameter_sets.test.funcs import OCP_ref_p, OCP_ref_n, dOCPdT_p, dOCPdT_n


with open("SOC", "rb") as f_SOC:
    SOC = pickle.load(f_SOC)

with open("OCV", "rb") as f_OCV:
    OCV = pickle.load(f_OCV)

with open("SOC_dOCVdT", "rb") as f_SOC:
    SOC_dOCVdT = pickle.load(f_SOC)

with open("dOCVdT", "rb") as f_OCV:
    dOCVdT = pickle.load(f_OCV)


def func_eta(SOC, temp):
    return 1


func_OCV = scipy.interpolate.interp1d(SOC, OCV, fill_value='extrapolate')
func_dOCVdT = scipy.interpolate.interp1d(SOC_dOCVdT, dOCVdT, fill_value='extrapolate')


# Simulation Parameters
I = 1.65
V_min = 2.5
SOC_min = 0
SOC_LIB = 1

# setup the battery cell
cell = SPPy.ECMBatteryCell(R0_ref=0.005, R1_ref=0.001, C1=0.03, T_ref=298.15, Ea_R0=4000, Ea_R1=4000,
                           rho=1626, Vol=3.38e-5, C_p=750, h=1, A=0.085, cap=1.65, V_max=4.2, V_min=2.5,
                           SOC_init=0.98, T_init=298.15, func_eta=func_eta, func_OCV=func_OCV, func_dOCVdT=func_dOCVdT)
# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
solver = SPPy.DTSolver(battery_cell_instance=cell, isothermal=True)
# solve
sol = solver.solve(cycler=dc)

# Plots
sol.comprehensive_plot(save_dir='../../../docs/source/Assests/example_ECM_isothermal.png')
