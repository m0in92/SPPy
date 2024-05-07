""" solution.py
Contains the classes and functionality to store and plot the simulation results.
"""

__all__ = ['ECMSolution', 'SolutionInitializer', 'Solution']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'Deployed'

from dataclasses import dataclass, field
import pickle
from typing import Optional
import sys

import numpy as np
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

from SPPy.calc_helpers.constants import Constants


# Below checks for the Python3 version and imports the relevant packages for the type hinting. Note that the keyword
# Self was introduced in Python3.11
PYTHON_MAIN_VERSION = sys.version_info[0]
PYTHON_MINOR_VERSION = sys.version_info[1]
if PYTHON_MINOR_VERSION >= 11:
    from typing import Self
else:
    from typing_extensions import Self


@dataclass
class ECMSolution:
    array_t: np.ndarray = field(default_factory=lambda: np.array([]))  # solution time [s]
    array_I: np.ndarray = field(default_factory=lambda: np.array([]))  # applied current [A]
    array_V: np.ndarray = field(default_factory=lambda: np.array([]))  # cell terminal potential [V]
    array_temp: np.ndarray = field(default_factory=lambda: np.array([]))  # battery cell temperature [K]
    array_soc: np.ndarray = field(default_factory=lambda: np.array([]))  # np array containing the battery cell soc
    array_I_R1: np.ndarray = field(default_factory=lambda: np.array([]))  # current across the R1 resistor

    @classmethod
    def read_from_csv_file(cls, filepath: str):
        """
        Reads the csv file containing the experimental data and stores the data in its numpy arrays. The labelling
        of the columns in the experimental csv file needs to follow a certain naming conventions.
        :param filepath:
        :return:
        """
        df = pd.read_csv(filepath)
        array_t = df['t [s]'].to_numpy()
        array_I = df['I [A]'].to_numpy()
        array_V = df['V [V]'].to_numpy()
        return cls(array_t=array_t, array_I=array_I, array_V=array_V)

    @classmethod
    def read_from_arrays(cls, array_t: np.ndarray, array_i: np.ndarray, array_v: np.ndarray,
                         array_temp: np.ndarray, array_soc: Optional[np.ndarray]):
        """
        Initiates a Solution instance from the numpy arrays. This method is useful for conducting Kalman filter - based
        simulation from the experimental data.

        For instance, for pre-existing numpy arrays representing time, current, voltage, temperature, the class instance
        can be instantiated using:
                            sol_exp: ECMSolution = ECMSolution().read_from_arrays(...).
        :param array_t: array containing time values at each time-step [s]
        :param array_i: array containing current values at each time-step [A]
        :param array_v: array containing voltage at each time-step [V]
        :param array_temp: array containing temperature values at each time-step [K]
        :param array_soc: array containing battery cell SOC at each time-step
        :return: ECMSolution instance
        """
        return cls(array_t=array_t, array_I=array_i, array_V=array_v, array_temp=array_temp, array_soc=array_soc)

    @classmethod
    def __set_matplotlib_settings(cls) -> None:
        mpl.rcParams['lines.linewidth'] = 3
        plt.rc('axes', titlesize=20)
        plt.rc('axes', labelsize=12.5)
        plt.rc('axes', labelweight='bold')
        plt.rcParams['font.size'] = 15

    def update(self, t: float, i_app: float, v: float, temp: float, soc: float, i_r1: float) -> None:
        """
        Updates the instance's arrays with the new data values
        :param t: time [s]
        :param i_app: applied current [A]
        :param v: cell terminal potential [V]
        :param temp: cell surface temp. [K]
        :param soc: state-of-charge
        :param i_r1: current across the R1 resistor [A].
        :return: None
        """
        self.__set_matplotlib_settings()
        self.array_t = np.append(self.array_t, t)
        self.array_I = np.append(self.array_I, i_app)
        self.array_V = np.append(self.array_V, v)
        self.array_temp = np.append(self.array_temp, temp)
        self.array_soc = np.append(self.array_soc, soc)
        self.array_I_R1 = np.append(self.array_I_R1, i_r1)

    def comprehensive_plot(self, sol_exp: Optional[Self] = None, save_dir: Optional[str] = None,
                           plot_line_color: Optional[str] = None):
        fig = plt.figure(figsize=(6.4, 6), dpi=300)

        x_axis = self.array_t

        color: str = '#1f77b4'
        if plot_line_color is not None:
            color: str = plot_line_color

        ax1 = fig.add_subplot(221)
        ax1.plot(x_axis, self.array_V, label='sim', color=color)
        if sol_exp is not None:
            ax1.plot(sol_exp.array_t, sol_exp.array_V, label='exp', color='red')
            ax1.legend()
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Voltage [V]')

        ax2 = fig.add_subplot(222)
        if self.array_soc is not None:
            ax2.plot(x_axis, self.array_soc, color)
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel('SOC')

        ax3 = fig.add_subplot(223)
        ax3.plot(x_axis, self.array_temp - 273.15, label='sim', color=color)
        if sol_exp is not None:
            try:
                ax3.plot(sol_exp.array_t, sol_exp.array_temp - 273.15, label='exp', color=color)
                ax3.legend()
            except Exception as e:
                print("could not plot the experimental temp.")
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel(r'Temp. [$^0$C]')

        ax4 = fig.add_subplot(224)
        ax4.plot(x_axis, self.array_I, color=color)
        ax4.set_xlabel('Time [s]')
        ax4.set_ylabel('Current [A]')

        if save_dir is not None:
            plt.savefig(save_dir)

        plt.tight_layout()
        plt.show()


@dataclass
class SolutionInitializer:
    """
    Initializes the relevant data to be stored during a simulation by creating empty lists. Furthermore, it is intended
    to append these lists during simulations.
    """
    lst_cycle_num: list = field(default_factory=lambda: [])  # cycle number
    lst_cycle_step: list = field(default_factory=lambda: [])  # cycle step name
    lst_t: list = field(default_factory=lambda: [])  # time [s]
    lst_I: list = field(default_factory=lambda: [])  # applied current [A]
    lst_V: list = field(default_factory=lambda: [])  # cell terminal voltage [V]
    lst_OCV_LIB: list = field(default_factory=lambda: [])  # OCV of the LIB [V]
    lst_x_surf_p: list = field(default_factory=lambda: [])  # positive electrode surface SOC
    lst_x_surf_n: list = field(default_factory=lambda: [])  # negative electrode surface SOC
    lst_cap: list = field(default_factory=lambda: [])  # total capacity spent over cycling [Ahr]
    lst_cap_charge: list = field(default_factory=lambda: [])  # charge capacity [A hr]
    lst_cap_discharge: list = field(default_factory=lambda: [])  # discharge capacity [A hr]
    lst_SOC_LIB: list = field(default_factory=lambda: [])  # SOC of the LIB battery cell [unitless]
    lst_battery_cap: list = field(default_factory=lambda: [])  # battery cell capacity [A hr]
    lst_temp: list = field(default_factory=lambda: [])  # battery cell temperature [K]
    lst_R_cell: list = field(default_factory=lambda: [])  # battery cell internal resistance [ohms]

    # attributes below relates to the molar fluxes of the negative electrode.
    lst_j_tot: list = field(default_factory=lambda: [])  # total molar flux at the negative electrode [mol/m2/s]
    lst_j_i: list = field(default_factory=lambda: [])  # total intercalation flux at the negative electrode [mol/m2/s]
    lst_j_s: list = field(default_factory=lambda: [])  # side reaction molar flux at the negative electrode [mol/m2/s]

    # attributes below are related to the spatial electrolyte quantities
    electrolyte_conc: Optional[np.ndarray] = None

    def update(self, cycle_num: float = 0, cycle_step: str = 'rest', t: float = 0, I: float = 0, V: float = 0,
               OCV: float = 0, x_surf_p: float = 0, x_surf_n: float = 0,
               cap: float = 0, cap_charge: float = 0, cap_discharge: float = 0, SOC_LIB: float = 0,
               battery_cap: float = 0,
               temp: float = 0, R_cell: float = 0):
        self.lst_cycle_num.append(cycle_num)
        self.lst_cycle_step.append(cycle_step)
        self.lst_t.append(t)
        self.lst_I.append(I)
        self.lst_V.append(V)
        self.lst_OCV_LIB.append(OCV)
        self.lst_x_surf_p.append(x_surf_p)
        self.lst_x_surf_n.append(x_surf_n)

        self.lst_cap.append(cap)
        self.lst_cap_charge.append(cap_charge)
        self.lst_cap_discharge.append(cap_discharge)
        self.lst_SOC_LIB.append(SOC_LIB)

        self.lst_battery_cap.append(battery_cap)
        self.lst_temp.append(temp)
        self.lst_R_cell.append(R_cell)

    def update_via_lst(self, lst_cycle_num: list, lst_cycle_step: list, lst_t: list, lst_I: list, lst_V: list):
        self.lst_cycle_num = lst_cycle_num
        self.lst_cycle_step = lst_cycle_step
        self.lst_t = lst_t
        self.lst_I = lst_I
        self.lst_V = lst_V


class Solution:
    def __init__(self, base_solution_instance: SolutionInitializer = SolutionInitializer(),
                 name=None, save_csv_dir=None):
        if not isinstance(base_solution_instance, SolutionInitializer):
            raise TypeError("base_solution_instance needs to be a SolutionInitializer object.")

        # below preprocesses the attributes from the BaseSolution instance.
        self.cycle_num = np.array(base_solution_instance.lst_cycle_num)
        self.cycle_step = np.array(base_solution_instance.lst_cycle_step)
        self.t = np.array(base_solution_instance.lst_t[:len(base_solution_instance.lst_V)])
        self.I = np.array(base_solution_instance.lst_I[:len(base_solution_instance.lst_V)])
        self.V = np.array(base_solution_instance.lst_V)
        self.OCV_LIB = np.array(base_solution_instance.lst_OCV_LIB)
        self.x_surf_p = np.array(base_solution_instance.lst_x_surf_p)
        self.x_surf_n = np.array(base_solution_instance.lst_x_surf_n)
        self.cap = np.array(base_solution_instance.lst_cap)
        self.cap_charge = base_solution_instance.lst_cap_charge
        self.cap_discharge = base_solution_instance.lst_cap_discharge
        self.SOC_LIB = base_solution_instance.lst_SOC_LIB
        self.battery_cap = base_solution_instance.lst_battery_cap
        self.T = np.array(base_solution_instance.lst_temp)
        self.R_cell = np.array(base_solution_instance.lst_R_cell)
        self.j_tot = np.array(base_solution_instance.lst_j_tot)
        self.j_i = np.array(base_solution_instance.lst_j_i)
        self.js = np.array(base_solution_instance.lst_j_s)

        self.name = name  # name of the solution

        self.electrolyte_conc_enabled: bool = False
        if base_solution_instance.electrolyte_conc is not None:
            self.electrolyte_conc_enabled = True
            self.electrolyte_conc: np.ndarray = base_solution_instance.electrolyte_conc

        if save_csv_dir is not None:
            self.save_csv_func(save_csv_dir)

    @property
    def cycle_summary(self):
        """
        Contains a summary of the cycling information
        :return: (dict) contains summary of the cycling information, including cycle number
        """
        total_cycles = len(np.unique(self.cycle_num))
        return {'cycle_no': total_cycles}

    @classmethod
    def read_from_arrays(cls, t: np.ndarray, i_app: np.ndarray, v: np.ndarray,
                         temp: np.ndarray,
                         soc_n: Optional[np.ndarray] = None, soc_p: Optional[np.ndarray] = None) -> Self:
        sol_instance: SolutionInitializer = SolutionInitializer()

        sol_instance.lst_t = t.tolist()
        sol_instance.lst_I = i_app.tolist()
        sol_instance.lst_V = v.tolist()
        sol_instance.lst_temp = temp.tolist()
        if soc_p is not None:
            sol_instance.lst_x_surf_p = soc_p
        if soc_n is not None:
            sol_instance.lst_x_surf_n = soc_n

        return cls(base_solution_instance=sol_instance)

    @classmethod
    def upload_exp_data(cls, filename: str, cycle_num: int | npt.ArrayLike = None,
                        step_num: int | str = None, cell_cap: float = None) -> Self:
        sol_init = SolutionInitializer()
        df = pd.read_csv(filename)
        if cycle_num is not None:
            if isinstance(cycle_num, int):
                df = df[df['Cycle_Index'] == cycle_num]
            elif (isinstance(cycle_num, np.ndarray) or isinstance(cycle_num, list)):
                for cycle_num_i in cycle_num:
                    df_res = pd.DataFrame()
                    df_res.append(df[df['Cycle_Index'] == cycle_num_i])
                df = df_res
        if step_num is not None:
            df = df[df['Step_Index'] == step_num]
        array_t = df['t [s]'].to_numpy()
        array_t = array_t - array_t[0]
        lst_t = list(array_t)
        lst_V = df['V [V]'].tolist()
        lst_I = df['I [A]'].tolist()
        lst_cycle_num = df['Cycle_Index'].tolist()
        lst_cycle_step = df['Step_Index'].tolist()
        sol_init.update_via_lst(lst_cycle_num=lst_cycle_num, lst_cycle_step=lst_cycle_step, lst_t=lst_t, lst_I=lst_I,
                                lst_V=lst_V)
        if 'cap [Ahr]' not in df.columns:
            if cell_cap is not None:
                dt = np.diff(np.array(sol_init.lst_t), prepend=0)
                dcap = dt * np.array(sol_init.lst_I) / (3600 * cell_cap)
                cap = 1 + np.cumsum(dcap)
                sol_init.lst_cap = cap.tolist()
        else:
            sol_init.lst_cap = ((cell_cap - df['cap [Ahr]']) / cell_cap).tolist()
        return cls(base_solution_instance=sol_init)

    @classmethod
    def set_matplotlib_plot_line_color(cls, plot_line_color: Optional[str] = None) -> str:
        color: str = '#1f77b4'  # default Matplotlib color for the first line plot
        if plot_line_color is not None:
            color: str = plot_line_color
        return color

    def create_df(self):
        df = pd.DataFrame({
            'Time [s]': self.t,
            'Cycle No': self.cycle_num,
            'Step Name': self.cycle_step,
            'I [A]': self.I,
            'SOC_p': self.x_surf_p,
            'SOC_n': self.x_surf_n,
            'V [V]': self.V,
            'Temp [K]': self.T,
            'capacity [Ahr]': self.cap,
            'Charge cap. [Ahr]': self.cap_charge,
            'Discharge cap. [Ahr]': self.cap_discharge,
            'R_cell [ohm]': self.R_cell,
            'Battery cap [Ahr]': self.battery_cap,
            'j_s [A/m2]': self.js
        })
        return df

    def save_csv_func(self, output_file_dir):
        df = self.create_df()
        if self.name is not None:
            df.to_csv(output_file_dir + self.name + '.csv')
        else:
            raise ValueError("Sol name not given.")

    def initiate_single_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        return ax

    def single_plot(self, x_var, y_var, x_label, y_label, plot_title: str = None):
        self.set_matplotlib_settings()

        ax = self.initiate_single_plot()
        ax.plot(x_var, y_var)
        ax.set_xlabel(xlabel=x_label)
        ax.set_ylabel(ylabel=y_label)

        if plot_title is not None:
            ax.set_title(plot_title)

        plt.tight_layout()
        plt.show()

    def filter_cycle_nums(self):
        return np.unique(self.cycle_num)

    def filter_cap(self, cycle_no):
        """
        returns the discharge capacity of specified cycle no
        :param cycle_no: (int) cycle no.
        :return: returns the discharge capacity of specified cycle no
        """
        df = self.create_df()
        return df[(df['Cycle No'] == cycle_no) & (df['Step Name'] == 'discharge')]['Discharge cap. [Ahr]'].to_numpy()

    def filter_charge_cap(self, cycle_no):
        """
        returns the charge capacity of specified cycle no
        :param cycle_no: (int) cycle no.
        :return: returns the discharge capacity of specified cycle no
        """
        return [cap_ for i, cap_ in enumerate(self.cap) if ((self.cycle_num[i] == cycle_no) and
                                                            (self.cycle_step[i] == 'charge'))]

    def filter_battery_cap(self, cycle_no):
        """
        Returns the battery cap at the end of the inputted cycle no.
        :param cycle_no: (int) cycle number
        :return: (double) battery cap found at the of the cycle num.
        """
        df = self.create_df()
        return df[(df['Cycle No'] == cycle_no)]['Battery cap [Ahr]'].to_numpy()[-1]

    def filter_V(self, cycle_no):
        """
        returns the potential during the discharge phase of the cycling
        :param cycle_no: (int) cycle no.
        :return: returns the discharge capacity of specified cycle no
        """
        return [V_ for i, V_ in enumerate(self.V) if ((self.cycle_num[i] == cycle_no) and
                                                      (self.cycle_step[i] == 'discharge'))]

    def filter_T(self, cycle_no):
        """
        returns the temperature during the discharge phase of the cycling.
        :param cycle_no: (int) cycle no.
        :return: returns the temperature of the specified cycle no
        """
        return [T_ for i, T_ in enumerate(self.T) if ((self.cycle_num[i] == cycle_no) and
                                                      (self.cycle_step[i] == 'discharge'))]

    def filter_R_cell(self, cycle_no):
        return [R_cell_ for i, R_cell_ in enumerate(self.R_cell) if self.cycle_num[i] == cycle_no][-1]

    def calc_discharge_cap(self, cycle_no):
        return self.filter_cap(cycle_no=cycle_no)[-1]

    def calc_discharge_R_cell(self):
        """
        calulates the internal battery cell resistance after each cycle.
        :return:
        """
        all_cycle_no = np.unique(self.cycle_num)
        return np.array([self.filter_R_cell(all_cycle_no[i]) for i in range(self.total_cycles)])

    def calc_battery_cap_array(self):
        return np.array([self.filter_battery_cap(i) for i in self.filter_cycle_nums()])

    def plot_tV(self):
        self.single_plot(self.t, self.V, x_label='t [s]', y_label='V [V]', plot_title="V vs. Time")

    def plot_tTemp(self):
        self.single_plot(self.t, self.T,
                         x_label='t [s]', y_label=r'Temperature [$0^C$]',
                         plot_title="Battery Cell Surface Temp.")

    def plot_capV(self):
        self.single_plot(self.cap, self.V, x_label='capacity [Ahr]', y_label='V [V]')

    def dis_cap_array(self):
        return np.array([self.calc_discharge_cap(cycle_no_) for cycle_no_ in np.unique(self.cycle_num)])

    def set_matplotlib_settings(self, plot_line_color: Optional[str] = None):
        mpl.rcParams['lines.linewidth'] = 3
        plt.rc('axes', titlesize=20)
        plt.rc('axes', labelsize=20)
        plt.rcParams['font.size'] = 15

    def comprehensive_isothermal_plot(self,
                                      save_dir: str = None,
                                      plot_line_color: Optional[str] = None) -> None:
        self.set_matplotlib_settings()
        color: str = self.set_matplotlib_plot_line_color(plot_line_color=plot_line_color)

        num_rows: int = 2
        num_cols: int = 2
        if not self.electrolyte_conc_enabled:
            fig = plt.figure(figsize=(6.4 * 2, 4.8 * 2), dpi=300)
        else:
            fig = plt.figure(figsize=(6.4 * 2, 4.8 * 3), dpi=300)

        if self.electrolyte_conc_enabled:
            num_rows = 3

        ax1 = fig.add_subplot(num_rows, num_cols, 1)
        ax1.plot(self.t, self.V)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('V [V]')
        ax1.set_title('V vs. Time')

        ax2 = fig.add_subplot(num_rows, num_cols, 2)
        if len(np.unique(self.cycle_num)) == 1:
            ax2.plot(self.cap, self.V)
        else:
            # omit cycle 0
            first_cycle_no = np.unique(self.cycle_num)[1]
            last_cycle_no = np.unique(self.cycle_num)[-1]
            cap_list_first = self.filter_cap(first_cycle_no)
            cap_list_last = self.filter_cap(last_cycle_no)
            V_list_first = self.filter_V(first_cycle_no)
            V_list_last = self.filter_V(last_cycle_no)
            ax2.plot(cap_list_first, V_list_first, label=f"cycle {first_cycle_no}")
            ax2.plot(cap_list_last, V_list_last, label=f"cycle {last_cycle_no}")
        ax2.set_xlabel('Capacity [Ahr]')
        ax2.set_ylabel('V [V]')
        ax2.set_title('V vs. Capacity')
        ax2.legend()

        ax3 = fig.add_subplot(num_rows, num_cols, 3)
        ax3.plot(self.t, self.x_surf_p)
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel('SOC')
        ax3.set_title('Positive Electrode SOC')

        ax4 = fig.add_subplot(num_rows, num_cols, 4)
        ax4.plot(self.t, self.x_surf_n)
        ax4.set_xlabel('Time [s]')
        ax4.set_ylabel('SOC')
        ax4.set_title('Negative Electrode SOC')

        if self.electrolyte_conc_enabled:
            ax5 = fig.add_subplot(num_rows, num_cols, 5)
            ax5.plot(self.electrolyte_conc[0, :], self.electrolyte_conc[1, :])
            ax5.plot(self.electrolyte_conc[0, :], self.electrolyte_conc[2, :])
            ax5.set_xlabel('thickness [m]')
            ax5.set_ylabel('$c_{e} [mol/{m^3}]$')
            ax5.ticklabel_format(axis="x", scilimits=[-1, 1])

        plt.tight_layout()

        if save_dir is not None:
            plt.savefig(save_dir)

        plt.show()

    def comprehensive_plot(self, save_dir: str = None, plot_line_color: Optional[str] = None):
        self.set_matplotlib_settings()

        num_rows = 3
        num_cols = 2
        fig = plt.figure(figsize=(6.4 * 2, 4.8 * 3), dpi=300)

        color: str = self.set_matplotlib_plot_line_color(plot_line_color=plot_line_color)

        ax1 = fig.add_subplot(num_rows, num_cols, 1)
        ax1.plot(self.t, self.V, color=color)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('V [V]')
        ax1.set_title('V vs. Time')

        ax2 = fig.add_subplot(num_rows, num_cols, 2)
        if len(np.unique(self.cycle_num)) == 1:
            ax2.plot(self.cap, self.V, color=color)
        else:
            # omit cycle 0
            first_cycle_no = np.unique(self.cycle_num)[1]
            last_cycle_no = np.unique(self.cycle_num)[-1]
            cap_list_first = self.filter_cap(first_cycle_no)
            cap_list_last = self.filter_cap(last_cycle_no)
            V_list_first = self.filter_V(first_cycle_no)
            V_list_last = self.filter_V(last_cycle_no)
            ax2.plot(cap_list_first, V_list_first, label=f"cycle {first_cycle_no}")
            ax2.plot(cap_list_last, V_list_last, label=f"cycle {last_cycle_no}")
        ax2.set_xlabel('Capacity [Ahr]')
        ax2.set_ylabel('V [V]')
        ax2.set_title('V vs. Capacity')
        ax2.legend()

        ax3 = fig.add_subplot(num_rows, num_cols, 3)
        ax3.plot(self.t, self.x_surf_p, color=color)
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel('SOC')
        ax3.set_title('Positive Electrode SOC')

        ax4 = fig.add_subplot(num_rows, num_cols, 4)
        ax4.plot(self.t, self.x_surf_n, color=color)
        ax4.set_xlabel('Time [s]')
        ax4.set_ylabel('SOC')
        ax4.set_title('Negative Electrode SOC')

        ax5 = fig.add_subplot(num_rows, num_cols, 5)
        ax5.plot(self.t, self.T - Constants.T_abs, color=color)
        ax5.set_xlabel('Time [s]')
        ax5.set_ylabel('Temperature [C]')
        ax5.set_title('Battery Cell Surface Temp.')

        ax6 = fig.add_subplot(num_rows, num_cols, 6)
        if len(np.unique(self.cycle_num)) == 1:
            ax6.plot(self.cap, self.T - Constants.T_abs, color=color)
        else:
            # omit cycle 0
            first_cycle_no = np.unique(self.cycle_num)[1]
            last_cycle_no = np.unique(self.cycle_num)[-1]
            cap_list_first = self.filter_cap(first_cycle_no)
            cap_list_last = self.filter_cap(last_cycle_no)
            T_list_first = self.filter_T(first_cycle_no)
            T_list_last = self.filter_T(last_cycle_no)
            ax6.plot(cap_list_first, np.array(T_list_first) - Constants.T_abs, label=f"cycle {first_cycle_no}")
            ax6.plot(cap_list_last, np.array(T_list_last) - Constants.T_abs, label=f"cycle {last_cycle_no}")
        ax6.set_xlabel('Capacity [Ahr]')
        ax6.set_ylabel('Temperature [C]')
        ax6.set_title('Battery Cell Surface Temp.')
        ax6.legend()

        # ax7 = fig.add_subplot(num_rows, num_cols, 7)
        # ax7.scatter(np.unique(self.cycle_num), self.dis_cap_array())
        # ax7.set_xlabel('Cycle No.')
        # ax7.set_ylabel('Discharge Capacity [A hr]')
        # ax7.set_title('Cycling Performance')

        # ax8 = fig.add_subplot(num_rows, num_cols, 8)
        # ax8.scatter(np.unique(self.cycle_num), self.calc_discharge_R_cell()*1e3)
        # ax8.set_xlabel('Cycle No.')
        # ax8.set_ylabel(r'Internal resistance [m$\Omega$]')
        # ax8.set_title('Cycling Performance')

        plt.tight_layout()

        if save_dir is not None:
            plt.savefig(save_dir)

        plt.show()

    def plot_degradation(self):
        fig = plt.figure(figsize=(6.4 * 2, 5.4))
        ax1 = fig.add_subplot(121)
        ax1.plot(self.t, self.R_cell)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('$R_{cell}$ $[\Omega]$')

        ax2 = fig.add_subplot(122)
        ax2.plot(self.x_surf_n, self.js)
        ax2.set_xlabel('SOC_surf_n')
        ax2.set_ylabel('Side Reaction flux [mol/m2/s]')

        color = 'tab:red'
        ax3 = ax2.twinx()
        ax3.plot(self.x_surf_n, self.j_i, color=color)
        ax3.tick_params(axis='y', labelcolor=color)
        ax3.set_ylabel('intercalation flux [mol/m2/s]')

        ax1.ticklabel_format(axis="y", scilimits=[-1, 1])
        plt.tight_layout()
        plt.show()

    def save_instance(self, file_name: str):
        with open(file_name, "wb") as output_file:
            pickle.dump(self, output_file, pickle.HIGHEST_PROTOCOL)
