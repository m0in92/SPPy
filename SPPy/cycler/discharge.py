"""
Contains classes and functionality to represent the current during battery discharge.
"""

__all__ = ['Discharge', 'DischargeRest', 'CustomDischarge']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by SPPy. All rights reserved.'
__status__ = 'deployed'


import numpy as np

from SPPy.cycler.base import BaseCycler


class Discharge(BaseCycler):
    def __init__(self, discharge_current: float, v_min: float, SOC_LIB_min: float, SOC_LIB: float):
        super().__init__(SOC_LIB_min=SOC_LIB_min, SOC_LIB=SOC_LIB)
        self.discharge_current = -discharge_current
        self.v_min = v_min
        self.num_cycles = 1
        self.cycle_steps = ['discharge']
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        return self.discharge_current

    def reset(self) -> None:
        self.time_elapsed = 0
        self.SOC_LIB = self.SOC_LIB_init


class DischargeRest(BaseCycler):
    def __init__(self, discharge_current, rest_time, V_min, SOC_LIB_min, SOC_LIB, SOC_LIB_max):
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max)
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_min = V_min
        self.num_cycles = 1
        self.cycle_steps = ['discharge', 'rest']
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == 'discharge':
            return self.discharge_current
        elif step_name == 'rest':
            return 0

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class CustomDischarge(BaseCycler):
    def __init__(self, t_array, I_array, V_min):
        # Check for input type.
        if not isinstance(t_array, np.ndarray):
            raise TypeError("t_array needs to be a numpy array.")
        if not isinstance(I_array, np.ndarray):
            raise TypeError("I_array needs to be a numpy array.")
        # Check is the size of the time and current arrays are equal
        if len(t_array) != len(I_array):
            raise ValueError("t_array and I_array needs to be of the same length.")
        super().__init__()
        self.t_array = t_array
        self.t_max = t_array[-1] # maximum time
        self.I_array = -I_array
        self.V_min = V_min
        self.charge_current = 0.0
        self.num_cycles = 1
        self.cycle_steps = ['discharge']

    def get_current(self, step_name: str, t_input: float) -> float:
        """
        This method returns the current at the given time. This method overwrites the Base charger's respective method.
        :param step_name: The step name.
        :param t_input: time input.
        :return: The value of the current.
        """
        if step_name == "discharge":
            # find the index in t_array that matches the t_input
            t_index = np.where(self.t_array == t_input)
            # find the index in t_array that matches the t_input
            if np.any(t_index):
                return self.I_array[t_index][0]
            else:
                return 0.0
        else:
            return 0.0
