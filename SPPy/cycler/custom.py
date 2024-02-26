import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from scipy import interpolate
from SPPy.cycler.base import BaseCycler


class CustomCycler(BaseCycler):
    def __init__(self, array_t: npt.ArrayLike, array_I: npt.ArrayLike, V_min: float, V_max: float,
                 SOC_LIB: float=1.0, SOC_LIB_min: float=0.0, SOC_LIB_max: float=1.0):
        """
        CustomCycler constructor.
        :param t_array: numpy array containing the time values in sequence [s].
        :param I_array: numpy array containing the current values.
        :param SOC_LIB:
        """
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max)
        # check is t_array and I_array are numpy arrays.
        if (not isinstance(array_t, np.ndarray)) and (not isinstance(array_I, np.ndarray)):
            raise TypeError("t_array and I_array needs to be a numpy array.")

        # t_array and I_array needs to be of equal sizes
        if array_t.shape[0] != array_I.shape[0]:
            raise ValueError("t_array and I_array are not of equal sizes.")

        self.array_t = array_t
        self.array_I = array_I
        self.cycle_steps = ['custom']
        self.SOC_LIB_init = self.SOC_LIB
        self.V_min = V_min
        self.V_max = V_max

    @property
    def t_max(self):
        """
        Returns the time value at the last iteration.
        :return: (float) time value at the last iteration
        """
        return self.array_t[-1]

    def get_current(self, step_name: str, t: float) -> float:
        """
        Returns the current value from the inputted time value. This current value is interpolation based on the
        current value at the previous time step.
        :param step_name: cycling step name
        :param t: time [s]
        :returns: current value [A]
        """
        i_app = interpolate.interp1d(self.array_t, self.array_I, kind='previous', fill_value='extrapolate')(t)
        if np.isnan(i_app):
            return 0.0
        return i_app

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init

    def plot(self):
        """
        Plots the cycler's instance time [s] vs. current [A]. According to the convention, the discharge current is
        negative.
        :return:
        """
        plt.plot(self.array_t, self.array_I)
        plt.xlabel('Time [s]')
        plt.ylabel('I [A]')
        plt.show()


class HPPCCycler(CustomCycler):
    def __init__(self, t1: float, t2: float, i_app: float, charge_or_discharge: str,
                 V_min: float, V_max: float,
                 soc_lib_min: float, soc_lib_max: float, soc_lib: float,
                 hppc_steps: int = 10) -> None:
        """intended to be the cycler class for HPPC experiments. HPPC defined here has the following profile
                1. Rest for t1
                2. Current pulse, with the amplitude of i_app, for a time period of t2. THh current is negative if
                    the battery cell is discharging and positive if is charging.
                3. Repeat steps 1 and 2 until the desired terminal voltage is attained

        Args:
            t1 (float): time period [s] for the initial rest and between the current pulse
            t2 (float): time period [s] of the current pulse
            current (float): current value [A] during the pulse
            charge_or_discharge (str): options are 'charge' or 'discharge'
            V_min (float): minimum terminal voltage [V]
            V_max (float): maximum terminal voltage [V]
            soc_lib_min (float): minimum LIB SOC
            soc_lib_max (float): max. LIB SOC
            soc_lib (float): SOC LIB at the start of the HPPC cycling step.
            hppc_steps (int): number of HPPC repetitions. DEfault is 10.
        """
        dt: float = 0.1  # the time difference between the time steps
        if charge_or_discharge == 'discharge':
            i_app_actual: float = -i_app
        elif charge_or_discharge == 'charge':
            i_app_actual: float = i_app
        else:
            raise ValueError(
                f"input for charge_discharge parameter, {charge_or_discharge}, cannot be reconigized.")

        # This is the first iteration of the HPPC cycler
        t1_array: np.ndarray = np.arange(0, t1, dt)
        i_app1_array: np.ndarray = np.zeros(len(t1_array))
        t2_array: np.ndarray = np.arange(t1, t1+t2+dt, dt)
        i_app2_array: np.ndarray = i_app_actual * np.ones(len(t2_array))

        t_array: np.ndarray = np.append(t1_array, t2_array)
        current_array: np.ndarray = np.append(i_app1_array, i_app2_array)

        # This is the successive iteration of the HPPC cycler. Alternatively, the first and successive iterations
        # could have been coded into one iteration by introducing an empty t_array and current_array. However,
        # this lead to unpredictable behaviour in numpy arrays.
        for i in range(hppc_steps-1):
            t1_array: np.ndarray = np.arange(
                t_array[-1] + dt, t_array[-1] + t1, dt)
            i_app1_array: np.ndarray = np.zeros(len(t1_array))
            t2_array: np.ndarray = np.arange(
                t_array[-1] + t1, t_array[-1] + t1 + t2 + dt, dt)
            i_app2_array: np.ndarray = i_app_actual * np.ones(len(t2_array))

            t_array: np.ndarray = np.append(t_array, t1_array)
            t_array: np.ndarray = np.append(t_array, t2_array)
            current_array: np.ndarray = np.append(current_array, i_app1_array)
            current_array: np.ndarray = np.append(current_array, i_app2_array)

        super().__init__(array_t=t_array, array_I=current_array,
                         V_min=V_min, V_max=V_max,
                         SOC_LIB_min=soc_lib_min, SOC_LIB_max=soc_lib_max, SOC_LIB=soc_lib)




