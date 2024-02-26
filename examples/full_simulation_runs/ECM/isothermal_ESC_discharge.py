import pickle

import scipy

import SPPy


with open("saved_results/SOC", "rb") as f_SOC:
    SOC = pickle.load(f_SOC)

with open("saved_results/OCV", "rb") as f_OCV:
    OCV = pickle.load(f_OCV)

with open("saved_results/SOC_dOCVdT", "rb") as f_SOC:
    SOC_dOCVdT = pickle.load(f_SOC)

with open("saved_results/dOCVdT", "rb") as f_OCV:
    dOCVdT = pickle.load(f_OCV)


def func_eta(SOC, temp):
    return 1


func_OCV = scipy.interpolate.interp1d(SOC, OCV, fill_value='extrapolate')
func_dOCVdT = scipy.interpolate.interp1d(SOC_dOCVdT, dOCVdT, fill_value='extrapolate')


# Simulation Parameters
I = 1.65
v_min = 2.5
SOC_min = 0
SOC_LIB = 1

# setup the battery cell
cell = SPPy.ECMBatteryCell(R0_ref=0.005, R1_ref=0.001, C1=0.03, temp_ref=298.15, Ea_R0=4000, Ea_R1=4000,
                           rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085, cap=1.65, v_max=4.2, v_min=2.5,
                           soc_init=0.98, temp_init=298.15, func_eta=func_eta, func_ocv=func_OCV,
                           func_docvdtemp=func_dOCVdT, M_0=4.4782e-4, M=0.0012, gamma=523.8311)
# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, v_min=v_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
solver = SPPy.ESCDTSolver(battery_cell_instance=cell, isothermal=True)
# solve
sol = solver.solve_standard_cycling_step(dt=0.1, cycler=dc)

# Plots
sol.comprehensive_plot()