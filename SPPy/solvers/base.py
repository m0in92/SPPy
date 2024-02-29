# __author__ = 'Moin Ahmed'
# __copyright__ = 'Copyright 2023 by Moin Ahmed. All rights are reserved.'
# __status__ = 'deployed'
#
#
# from SPPy.battery_components.battery_cell import BatteryCell
# from SPPy.models.battery import SPM
# from SPPy.warnings_and_exceptions.custom_exceptions import *
# import time
#
#
# class BaseSolver:
#     def __init__(self, b_cell: BatteryCell, isothermal: bool, degradation: bool, electrode_SOC_solver: str = 'eigen'):
#         # Below checks and initializes the battery cell instance
#         if not isinstance(b_cell, BatteryCell):
#             raise TypeError('b_cell needs to be a BatteryCell object.')
#         else:
#             self.b_cell = b_cell
#
#             # Check for incorrect input argument types.
#             if not isinstance(isothermal, bool):
#                 raise TypeError("isothermal argument needs to be a bool type.")
#             if not isinstance(degradation, bool):
#                 raise TypeError("degradation argument needs to be a bool type.")
#             # Assign class attributes.
#             self.bool_isothermal = isothermal
#             self.bool_degradation = degradation
#
#         if (electrode_SOC_solver=='eigen') or ((electrode_SOC_solver == 'cn') or (electrode_SOC_solver == 'poly')):
#             self.electrode_SOC_solver = electrode_SOC_solver
#         else:
#             raise ValueError('''Electrode SOC solver supports Eigen expansion method ('eigen)
#             or Crank-Nicolson Scheme ('cn') or Two-Term Polynomial Approximation ('poly')''')
#
#         self.b_model = SPM()  # initializes the single particle model instance.
#
#     def check_potential_limits(self, V):
#         if V < self.b_cell.V_min:
#             raise PotientialThesholdReached
#
#     def update_lists(self, x_p_list, x_n_list, V_list, cap_list, T_list,
#                      V, cap, T):
#         # Check for input arguments
#         if not isinstance(x_p_list, list):
#             raise TypeError("x_p_list needs to be a list type.")
#         if not isinstance(x_n_list, list):
#             raise TypeError("x_n_list needs to be a list type.")
#         if not isinstance(V_list, list):
#             raise TypeError("V_list needs to be list type.")
#         if not isinstance(cap_list, list):
#             raise TypeError("cap_list needs to be a list type.")
#         if not isinstance(T_list, list):
#             raise TypeError("T_list needs to be T type")
#         x_p_list.append(self.b_cell.elec_p.SOC)
#         x_n_list.append(self.b_cell.elec_n.SOC)
#         V_list.append(V)
#         cap_list.append(cap)
#         T_list.append(T)
#
#
# def timer(solver_func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         sol = solver_func(*args, **kwargs)
#         print(f"Solver execution time: {time.time() - start_time}s")
#         return sol
#     return wrapper