"""
Contains the source code for the battery solvers.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'

import time
from typing import Union

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from SPPy.battery_components.battery_cell import BatteryCell
# from SPPy.solvers.base import BaseSolver, timer
from SPPy.calc_helpers import ode_solvers
from SPPy.sol_and_visualization.solution import SolutionInitializer, Solution

from SPPy.warnings_and_exceptions.custom_exceptions import *

from SPPy.solvers.electrode_surf_conc import EigenFuncExp, CNSolver, PolynomialApproximation
from SPPy.models.thermal import Lumped
from SPPy.solvers.degradation_solvers import ROMSEISolver

from SPPy.models.battery import SPM, SPMe
from SPPy.solvers.electrolyte_conc import ElectrolyteFVMCoordinates, ElectrolyteConcFVMSolver

from SPPy.cycler.base import BaseCycler
from SPPy.cycler.discharge import CustomDischarge
from SPPy.cycler.custom import CustomCycler

from SPPy.calc_helpers.kalman_filter import NormalRandomVector, SigmaPointKalmanFilter


def timer(solver_func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        sol = solver_func(*args, **kwargs)
        print(f"Solver execution time: {time.time() - start_time}s")
        return sol

    return wrapper


class BaseSolver:
    def __init__(self, b_cell: BatteryCell, isothermal: bool, degradation: bool, electrode_SOC_solver: str = 'eigen'):
        # Below checks and initializes the battery cell instance
        if not isinstance(b_cell, BatteryCell):
            raise TypeError('b_cell needs to be a BatteryCell object.')
        else:
            self.b_cell = b_cell

            # Check for incorrect input argument types.
            if not isinstance(isothermal, bool):
                raise TypeError("isothermal argument needs to be a bool type.")
            if not isinstance(degradation, bool):
                raise TypeError("degradation argument needs to be a bool type.")
            # Assign class attributes.
            self.bool_isothermal = isothermal
            self.bool_degradation = degradation

        if (electrode_SOC_solver == 'eigen') or ((electrode_SOC_solver == 'cn') or (electrode_SOC_solver == 'poly')):
            self.electrode_SOC_solver = electrode_SOC_solver
        else:
            raise ValueError('''Electrode SOC solver supports Eigen expansion method ('eigen) 
            or Crank-Nicolson Scheme ('cn') or Two-Term Polynomial Approximation ('poly')''')

        self.b_model = SPM()  # initializes the single particle model instance.

    def check_potential_limits(self, V):
        if V < self.b_cell.V_min:
            raise PotientialThesholdReached

    def update_lists(self, x_p_list, x_n_list, V_list, cap_list, T_list,
                     V, cap, T):
        # Check for input arguments
        if not isinstance(x_p_list, list):
            raise TypeError("x_p_list needs to be a list type.")
        if not isinstance(x_n_list, list):
            raise TypeError("x_n_list needs to be a list type.")
        if not isinstance(V_list, list):
            raise TypeError("V_list needs to be list type.")
        if not isinstance(cap_list, list):
            raise TypeError("cap_list needs to be a list type.")
        if not isinstance(T_list, list):
            raise TypeError("T_list needs to be T type")
        x_p_list.append(self.b_cell.elec_p.SOC)
        x_n_list.append(self.b_cell.elec_n.SOC)
        V_list.append(V)
        cap_list.append(cap)
        T_list.append(T)


class SPPySolver(BaseSolver):
    """
    This class contains the attributes and methods to solve for the cell terminal voltage, battery cell temperature,
    and SEI degradation during battery cycling.
    The cell terminal voltage is solved using the single particle (SP) model. It uses the Eigen Expansion Function
    method to solve for the electrode surface SOC.
    The cell surface temperature is solved using the lumped cell thermal balance. The heat balance ODE is solved using
    the rk4 method.
    """

    def __init__(self, b_cell, isothermal: bool = True, degradation: bool = False,
                 electrode_SOC_solver: str = 'eigen', **electrode_SOC_solver_params):
        super().__init__(b_cell=b_cell, isothermal=isothermal, degradation=degradation,
                         electrode_SOC_solver=electrode_SOC_solver)
        self.N: int = 0  # number of roots for eigen-value solver

        # initialize result storage lists below.
        self.sol_init = SolutionInitializer()  # initializes the empty lists that will store the simulation results

        # initialize electrode surface SOC, temperature solvers, and degradation instances below.
        if self.electrode_SOC_solver == 'eigen':
            self.N = 5  # TODO: can be changed later to higher number or let user modify it as well
            self.SOC_solver_p = EigenFuncExp(x_init=self.b_cell.elec_p.SOC, n=self.N, electrode_type='p')
            self.SOC_solver_n = EigenFuncExp(x_init=self.b_cell.elec_n.SOC, n=self.N, electrode_type='n')
        elif self.electrode_SOC_solver == 'cn':
            self.SOC_solver_p = CNSolver(c_init=self.b_cell.elec_p.max_conc * self.b_cell.elec_p.SOC_init,
                                         electrode_type='p')
            self.SOC_solver_n = CNSolver(c_init=self.b_cell.elec_n.max_conc * self.b_cell.elec_n.SOC,
                                         electrode_type='n')
        elif self.electrode_SOC_solver == "poly":
            if electrode_SOC_solver_params:
                type = electrode_SOC_solver_params['type']
            else:
                type = 'higher'
            self.SOC_solver_p = PolynomialApproximation(
                c_init=self.b_cell.elec_p.max_conc * self.b_cell.elec_p.SOC_init,
                electrode_type='p', type=type)
            self.SOC_solver_n = PolynomialApproximation(
                c_init=self.b_cell.elec_n.max_conc * self.b_cell.elec_n.SOC_init,
                electrode_type='n', type=type)

        self.t_model = Lumped(b_cell=self.b_cell)  # thermal model object

        self.SEI_model = ROMSEISolver(b_cell=self.b_cell)  # ROM SEI solver object

    def calc_terminal_potential(self, I_p_i: float, I_n_i: float) -> float:
        """
        Returns the terminal potential [V]
        :param I_p_i: positive electrode intercalation current [A]
        :param I_n_i: negative electrode intercalation current [A]
        :return: (float) battery cell terminal potential [V]
        """
        return self.b_model(OCP_p=self.b_cell.elec_p.OCP, OCP_n=self.b_cell.elec_n.OCP, R_cell=self.b_cell.R_cell,
                            k_p=self.b_cell.elec_p.k, S_p=self.b_cell.elec_p.S, c_smax_p=self.b_cell.elec_p.max_conc,
                            SOC_p=self.b_cell.elec_p.SOC,
                            k_n=self.b_cell.elec_n.k, S_n=self.b_cell.elec_n.S, c_smax_n=self.b_cell.elec_n.max_conc,
                            SOC_n=self.b_cell.elec_n.SOC,
                            c_e=self.b_cell.electrolyte.conc, T=self.b_cell.T, I_p_i=I_p_i, I_n_i=I_n_i)

    @staticmethod
    def calc_cell_temp(t_model, t_prev, dt, temp_prev, V, I):
        """
        Solves for the heat balance using the ODE rk4 solver.
        :param t_model: Thermal model class
        :param t_prev: time values at the previous time step [s]
        :param dt: time difference between the current and previous times [s]
        :param V: cell terminal voltage [V]
        :param temp_prev: previous cell temperature [K]
        :param I: applied current [A]
        :return: cell temperature values [K]
        """
        if not isinstance(t_model, Lumped):
            raise TypeError("t_model needs to be a Thermal Model")
        func_heat_balance = t_model.heat_balance(V=V, I=I)
        return ode_solvers.rk4(func=func_heat_balance, t_prev=t_prev, y_prev=temp_prev, step_size=dt)

    @classmethod
    def delta_SOC_cap(cls, Q: float, I: float, dt: float):
        """
        returns the delta SOC capacity [unit-less].
        :param Q: Battery cell capacity
        :param I: Applied current [A]
        :param dt: time difference between the current and previous time step [s].
        :return: (float) change in delta SOC
        """
        if isinstance(Q, str):
            Q = float(Q)
        # print(type(I), type(dt),type(Q))
        return (1 / 3600) * (np.abs(I) * dt / Q)

    def calc_SOC_cap(self, cap_prev: float, Q: float, I: float, dt: float):
        return cap_prev + self.delta_SOC_cap(Q=Q, I=I, dt=dt)

    @classmethod
    def delta_cap(cls, I: float, dt: float):
        """
        Measures the change in battery cell's capacity [Ahr]
        :param I: applied current at the current time step [A]
        :param dt: difference in time in the time step [s]
        :return: change in battery cell capacity [Ahr]
        """
        return (1 / 3600) * (np.abs(I) * dt)

    def solve_iteration_one_step(self, t_prev: float, dt: float, I: float) -> float:
        # Account for SEI growth
        if self.bool_degradation:
            I_i, I_s, delta_R_SEI = self.SEI_model(soc=self.b_cell.elec_n.SOC, ocp=self.b_cell.elec_n.OCP,
                                                   dt=dt,
                                                   temp=self.b_cell.elec_n.T,
                                                   i_app=I)  # update the intercalation current (negative electrode
            # only)
            self.b_cell.R_cell += delta_R_SEI  # update the cell resistance
            self.b_cell.electrolyte.conc -= -self.SEI_model.J_s * dt  # update the electrolyte conc. to account
            # for mass balance.
        else:
            I_i = I  # intercalation current is same at the input current

        # Calc. electrode surface SOC below and update the battery cell's instance attributes.
        # if self.electrode_SOC_solver == 'eigen':
        self.b_cell.elec_p.SOC = self.SOC_solver_p(dt=dt, t_prev=t_prev, i_app=I,
                                                   R=self.b_cell.elec_p.R,
                                                   S=self.b_cell.elec_p.S,
                                                   D_s=self.b_cell.elec_p.D,
                                                   c_smax=self.b_cell.elec_p.max_conc)  # calc p surf SOC
        self.b_cell.elec_n.SOC = self.SOC_solver_n(dt=dt, t_prev=t_prev, i_app=I_i,
                                                   R=self.b_cell.elec_n.R,
                                                   S=self.b_cell.elec_n.S,
                                                   D_s=self.b_cell.elec_n.D,
                                                   c_smax=self.b_cell.elec_n.max_conc)  # calc n surf SOC

        V: float = self.calc_terminal_potential(I_p_i=I, I_n_i=I_i)  # calc battery cell terminal voltage

        # Calc temp below and update the battery cell's temperature attribute.
        if not self.bool_isothermal:
            self.b_cell.T = self.calc_cell_temp(t_model=self.t_model, t_prev=t_prev, dt=dt,
                                                temp_prev=self.b_cell.T, V=V, I=I)
        return V

    @timer
    def solve(self, cycler_instance: BaseCycler, sol_name: str = None, save_csv_dir: str = None, verbose: bool = False,
              t_increment: float = 0.1, termination_criteria: float = 'V'):
        # check for function input parameter types below.
        if not isinstance(cycler_instance, BaseCycler):
            raise TypeError("cycler needs to be a Cycler object.")

        if isinstance(cycler_instance, CustomCycler):
            return self._custom_cycler_solve(custom_cycler_instance=cycler_instance, sol_name=sol_name,
                                             save_csv_dir=save_csv_dir, verbose=verbose, t_increment=t_increment,
                                             termination_criteria=termination_criteria)
        else:
            return self._cycler_solve(cycler=cycler_instance, sol_name=sol_name,
                                      save_csv_dir=save_csv_dir, verbose=verbose, t_increment=t_increment,
                                      termination_criteria=termination_criteria)

    def _cycler_solve(self, cycler: BaseCycler, sol_name: str = None, save_csv_dir: str = None, verbose: bool = False,
                      t_increment: float = 0.1, termination_criteria: float = 'V'):
        # cycling simulation below. The first two loops iterate over the cycle numbers and cycling steps,
        # respectively. The following while loops checks for termination conditions and breaks when it reaches it.
        # The termination criteria are specified within the cycler instance.
        for cycle_no in tqdm(range(cycler.num_cycles)):
            for step in cycler.cycle_steps:
                cap = 0
                cap_charge = 0
                cap_discharge = 0
                t_prev = 0
                step_completed = False
                while not step_completed:
                    if isinstance(cycler, CustomDischarge):
                        I = cycler.get_current(step, t_prev)
                    else:
                        I = cycler.get_current(step, t_prev)
                    t_curr = t_prev + t_increment
                    dt = t_increment

                    # break condition for rest time
                    if ((step == "rest") and (t_curr > cycler.rest_time)):
                        step_completed = True

                    # All simulations parameters and battery cell attributes updates are done the in the code block
                    # below.
                    try:
                        V = self.solve_iteration_one_step(t_prev=t_prev, dt=dt, I=I)
                    except InvalidSOCException as e:
                        print(e)
                        break

                    # Calc charge capacity, discharge capacity, and overall LIB capacity
                    cap = self.calc_SOC_cap(cap_prev=cap, Q=self.b_cell.cap, I=I, dt=dt)
                    delta_cap = self.delta_SOC_cap(Q=self.b_cell.cap, I=I, dt=dt)
                    if step == "charge":
                        cap_charge += self.delta_cap(I=I, dt=dt)
                        cycler.SOC_LIB += delta_cap
                    elif step == "discharge":
                        cap_discharge += self.delta_cap(I=I, dt=dt)
                        cycler.SOC_LIB -= delta_cap

                    # break condition for charge and discharge if stop criteria is V-based
                    if termination_criteria == 'V':
                        if ((step == "charge") and (V > cycler.v_max)):
                            step_completed = True
                        if ((step == "discharge") and (V < cycler.v_min)):
                            step_completed = True
                    # break condition for charge and discharge if stop criteria is SOC-based
                    elif termination_criteria == 'SOC':
                        if ((step == "charge") and (cycler.SOC_LIB > cycler.SOC_max)):
                            step_completed = True
                        if ((step == "discharge") and (cycler.SOC_LIB < cycler.SOC_min)):
                            step_completed = True
                    # break condition for charge and discharge if stop criteria is time based
                    elif termination_criteria == 'time':
                        if step == "discharge" and cycler.time_elapsed > cycler.t_max:
                            step_completed = True

                    # update time
                    t_prev = t_curr
                    cycler.time_elapsed += t_increment

                    # Update results lists
                    self.sol_init.update(cycle_num=cycle_no,
                                         cycle_step=step,
                                         t=cycler.time_elapsed,
                                         I=I,
                                         V=V,
                                         OCV=self.b_cell.elec_p.OCP - self.b_cell.elec_n.OCP,
                                         x_surf_p=self.b_cell.elec_p.SOC,
                                         x_surf_n=self.b_cell.elec_n.SOC,
                                         cap=cap,
                                         cap_charge=cap_charge,
                                         cap_discharge=cap_discharge,
                                         SOC_LIB=cycler.SOC_LIB,
                                         battery_cap=self.b_cell.cap,
                                         temp=self.b_cell.T,
                                         R_cell=self.b_cell.R_cell)
                    if self.bool_degradation:
                        self.sol_init.lst_j_tot.append(self.SEI_model.J_tot)
                        self.sol_init.lst_j_i.append(self.SEI_model.J_i)
                        self.sol_init.lst_j_s.append(self.SEI_model.J_s)

                    if verbose:
                        print("time elapsed [s]: ", cycler.time_elapsed, ", cycle_no: ", cycle_no,
                              'step: ', step, "current [A]", I, ", terminal voltage [V]: ", V, ", SOC_LIB: ",
                              cycler.SOC_LIB, "SOC_p: ", self.b_cell.elec_p.SOC, "SOC_n: ", self.b_cell.elec_n.SOC,
                              "cap: ", cap)

        return Solution(base_solution_instance=self.sol_init, name=sol_name, save_csv_dir=save_csv_dir)

    def _custom_cycler_solve(self, custom_cycler_instance: CustomCycler, sol_name: str = None, save_csv_dir: str = None,
                             verbose: bool = False, t_increment: float = 0.1, termination_criteria: str = 'V'):
        if not isinstance(custom_cycler_instance, CustomCycler):
            raise TypeError('inputted cycler needs to be a CustomCycler object.')

        step_completed = False  # boolean that indicates if the cycling step is completed.

        cap = 0
        cap_charge = 0
        cap_discharge = 0
        t_curr = t_prev = 0.0  # time value of this current iteration step.
        while not step_completed:
            t_curr += t_increment
            dt = t_curr - t_prev

            I = custom_cycler_instance.get_current(step_name=custom_cycler_instance.cycle_steps[0], t=t_curr)

            # All simulations parameters and battery cell attributes updates are done the in the code block
            # below.
            try:
                V = self.solve_iteration_one_step(t_prev=t_prev, dt=dt, I=I)
            except InvalidSOCException as e:
                print(e)
                break

            if t_curr > custom_cycler_instance.t_max:
                print('cycling continued till the last time value in the t_array.')
                break

            # Calc charge capacity, discharge capacity, and overall LIB capacity
            cap = self.calc_SOC_cap(cap_prev=cap, Q=self.b_cell.cap, I=I, dt=dt)
            delta_SOC_cap = self.delta_SOC_cap(Q=self.b_cell.cap, I=I, dt=dt)
            if I < 0:
                cap_discharge += self.delta_cap(I=I, dt=dt)
                custom_cycler_instance.SOC_LIB -= delta_SOC_cap
            elif I > 0:
                cap_charge += self.delta_cap(I=I, dt=dt)
                custom_cycler_instance.SOC_LIB += delta_SOC_cap

            if verbose == True:
                print("time elapsed [s]: ", custom_cycler_instance.time_elapsed, ", cycle_no: ", 1,
                      'step: ', custom_cycler_instance.cycle_steps[0], "current [A]", I,
                      ", terminal voltage [V]: ", V, ", SOC_LIB: ", custom_cycler_instance.SOC_LIB,
                      "cap: ", cap)

            # update time
            t_prev = t_curr
            custom_cycler_instance.time_elapsed += t_increment

            # Update results lists
            self.sol_init.update(cycle_num=1,
                                 cycle_step='custom',
                                 t=custom_cycler_instance.time_elapsed,
                                 I=I,
                                 V=V,
                                 OCV=self.b_cell.elec_p.OCP - self.b_cell.elec_n.OCP,
                                 x_surf_p=self.b_cell.elec_p.SOC,
                                 x_surf_n=self.b_cell.elec_n.SOC,
                                 cap=cap,
                                 cap_charge=cap_charge,
                                 cap_discharge=cap_discharge,
                                 SOC_LIB=custom_cycler_instance.SOC_LIB,
                                 battery_cap=self.b_cell.cap,
                                 temp=self.b_cell.T,
                                 R_cell=self.b_cell.R_cell)
            if self.bool_degradation:
                self.sol_init.lst_j_tot.append(self.SEI_model.J_tot)
                self.sol_init.lst_j_i.append(self.SEI_model.J_i)
                self.sol_init.lst_j_s.append(self.SEI_model.J_s)

        return Solution(base_solution_instance=self.sol_init, name=sol_name, save_csv_dir=save_csv_dir)


class KFSPSolver(SPPySolver):
    """
    This class is intended to perform single particle model simulations using Kalman filter (specifically,
    sigma point Kalman filter). It is a derived class of the class for single particle model.
    """

    def __init__(self, b_cell, isothermal: bool = True, degradation: bool = False, N: int = 5,
                 electrode_SOC_solver: str = 'eigen', **electrode_SOC_solver_params):
        super().__init__(b_cell=b_cell, isothermal=isothermal, degradation=degradation, N=N,
                         electrode_SOC_solver=electrode_SOC_solver, **electrode_SOC_solver_params)
        self.__dt: float = 0.0  # See comments below for self.__t_prev
        self.__t_prev: float = 0.0  # The instance variables __dt and __t_prev are needed for the state equation.
        # The input parameters of the state equation are so that it represents the text book definition of the
        # state equation.

    def __state_equation_next(self, x_k: Union[float, np.ndarray],
                              u_k: Union[float, np.ndarray],
                              w_k: Union[float, np.ndarray]) -> None:
        self.b_cell.elec_p.SOC = self.SOC_solver_p(dt=self.__dt, t_prev=self.__t_prev, i_app=u_k + w_k,
                                                   R=self.b_cell.elec_p.R,
                                                   S=self.b_cell.elec_p.S,
                                                   D_s=self.b_cell.elec_p.D,
                                                   c_smax=self.b_cell.elec_p.max_conc)  # calc p surf SOC
        self.b_cell.elec_n.SOC = self.SOC_solver_n(dt=self.__dt, t_prev=self.__t_prev, i_app=u_k + w_k,
                                                   R=self.b_cell.elec_n.R,
                                                   S=self.b_cell.elec_n.S,
                                                   D_s=self.b_cell.elec_n.D,
                                                   c_smax=self.b_cell.elec_n.max_conc)  # calc n surf SOC

    def __output_equation(self, x_k: Union[float, np.ndarray],
                          u_k: Union[float, np.ndarray],
                          v_k: Union[float, np.ndarray]) -> float:
        """
        The output equation for the sigma-point Kalman filter for non-isothermal single particle model. Here the sensor
        noise is simply added to the cell terminal voltage equation.
        :param x_k: state
        :param u_k: input
        :param v_k: sensor noise
        :return: cell terminal voltage
        """
        return self.b_model(OCP_p=self.b_cell.elec_p.OCP, OCP_n=self.b_cell.elec_n.OCP, R_cell=self.b_cell.R_cell,
                            k_p=self.b_cell.elec_p.k, S_p=self.b_cell.elec_p.S, c_smax_p=self.b_cell.elec_p.max_conc,
                            SOC_p=x_k[0, :],
                            k_n=self.b_cell.elec_n.k, S_n=self.b_cell.elec_n.S, c_smax_n=self.b_cell.elec_n.max_conc,
                            SOC_n=x_k[1, :],
                            c_e=self.b_cell.electrolyte.conc, T=self.b_cell.T, I_p_i=u_k, I_n_i=u_k) + v_k

    def solve(self, sol_exp: Solution, cov_soc_p: float, cov_soc_n: float, cov_process: float, cov_sensor: float,
              v_min: float, v_max: float, soc_min: float, soc_max: float, soc_init: float) -> Solution:
        cycling_step = CustomCycler(array_t=sol_exp.t, array_I=sol_exp.I, V_min=v_min, V_max=v_max,
                                    SOC_LIB=soc_init, SOC_LIB_min=soc_min, SOC_LIB_max=soc_max)
        array_y_true = sol_exp.V  # array containing y_true is extracted from the solution object

        # create Normal Random Variables below
        vector_x: np.ndarray = np.array([[self.b_cell.elec_p.SOC], [self.b_cell.elec_n.SOC]])
        cov_x: np.ndarray = np.array([[cov_soc_p, 0], [0, cov_soc_n]])
        vector_w: np.ndarray = np.array([[0]])
        cov_w: np.ndarray = np.array([[cov_process]])
        vector_v: np.ndarray = np.array([[0]])
        cov_v: np.ndarray = np.array([[cov_sensor]])

        x: NormalRandomVector = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
        w: NormalRandomVector = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
        v: NormalRandomVector = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

        y_dim: int = 1

        # Create sigma-point kalman filter below
        spkf: SigmaPointKalmanFilter = SigmaPointKalmanFilter(x=x, w=w, v=v, y_dim=y_dim,
                                                              state_equation=self.__state_equation_next,
                                                              output_equation=self.__output_equation)

        # The solution loop is run below
        step_completed: bool = False

        i_sim: int = 1  # simulation index.
        while not step_completed:
            t_curr = cycling_step.array_t[i_sim]
            self.__dt = t_curr - self.__t_prev
            i_app_prev = cycling_step.array_I[i_sim - 1]
            i_app_curr = cycling_step.array_I[i_sim]

            spkf.solve(u=i_app_prev, y_true=array_y_true[i_sim])

            self.b_cell.elec_p.SOC = spkf.x.get_vector()[0, 0]
            self.b_cell.elec_n.SOC = spkf.x.get_vector()[1, 0]
            v: float = self.calc_terminal_potential(I_n_i=i_app_prev, I_p_i=i_app_prev)

            # loop termination criteria
            if v > cycling_step.V_max:
                step_completed = True
            if v < cycling_step.V_min:
                step_completed = True
            if t_curr > cycling_step.array_t[-1]:
                step_completed = True
            if i_sim >= len(cycling_step.array_t) - 1:
                step_completed = True

            # update sol attributes
            self.sol_init.update(cycle_num=1,
                                 cycle_step='custom',
                                 t=cycling_step.time_elapsed,
                                 I=t_curr,
                                 V=v,
                                 OCV=self.b_cell.elec_p.OCP - self.b_cell.elec_n.OCP,
                                 x_surf_p=self.b_cell.elec_p.SOC,
                                 x_surf_n=self.b_cell.elec_n.SOC,
                                 cap=0.0,
                                 cap_charge=0.0,
                                 cap_discharge=0.0,
                                 SOC_LIB=cycling_step.SOC_LIB,
                                 battery_cap=self.b_cell.cap,
                                 temp=self.b_cell.T,
                                 R_cell=self.b_cell.R_cell)

            # update simulation parameters
            t_prev = t_curr
            i_sim += 1

        return Solution(base_solution_instance=self.sol_init)


class EnhancedSPSolver(SPPySolver):
    """
    Solver for performing simulations using single-particle model with electrolyte dynamics.
    """

    def __init__(self, b_cell: BatteryCell, isothermal: bool, degradation: bool, electrode_soc_solver: str = 'poly'):
        super().__init__(b_cell=b_cell, isothermal=isothermal, degradation=degradation,
                         electrode_SOC_solver=electrode_soc_solver)
        if b_cell.electrolyte.D_e is None or b_cell.electrolyte.t_c is None:
            raise InsufficientParameters

        # The electrode solver is initialized from the parent class __init__ method.

        # The electrolyte solver is initialized below.
        self.electrolyte_co_ords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=self.b_cell.elec_n.L,
                                                                                        L_s=self.b_cell.electrolyte.L,
                                                                                        L_p=self.b_cell.elec_p.L)
        a_s_p: float = self.b_cell.elec_p.S / self.b_cell.elec_p.L
        a_s_n: float = self.b_cell.elec_n.S / self.b_cell.elec_n.L
        self.electrolyte_conc_solver: ElectrolyteConcFVMSolver = ElectrolyteConcFVMSolver(fvm_co_ords=self.electrode_soc_solver,
                                                                                          transference=self.b_cell.electrolyte.t_c,
                                                                                          epsilon_en=0.385,
                                                                                          epsilon_esep=0.785,
                                                                                          epsilon_ep=0.485,
                                                                                          a_sn=a_s_n, a_sp=a_s_p,
                                                                                          D_e=self.b_cell.electrolyte.D_e,
                                                                                          brugg=self.b_cell.electrolyte.brugg,
                                                                                          c_e_init=self.b_cell.electrolyte.conc)

    def solve_one_iteration(self):
        pass

    def solver(self, cycling_step: BaseCycler, dt: float = 0.1) -> npt.ArrayLike:
        step_completed: bool = False

        t_prev = 0
        for cycle_no in cycling_step.num_cycles:
            for step in cycling_step.cycle_steps:
                while not step_completed:
                    t_curr = t_prev + dt
                    i_app = cycling_step.get_current(step_name=step, t=t_curr)

                    # Calculate the electrode flux below
                    j_p = SPMe.molar_flux_electrode(I=i_app, S=self.b_cell.elec_p.S, electrode_type='p')
                    j_n = SPMe.molar_flux_electrode(I=i_app, S=self.b_cell.elec_n.S, electrode_type='n')

                    # Solve for electrode SOC below
                    self.b_cell.elec_p.SOC = self.SOC_solver_p(dt=dt, t_prev=t_prev, i_app=i_app,
                                                               R=self.b_cell.elec_p.R,
                                                               S=self.b_cell.elec_p.S,
                                                               D_s=self.b_cell.elec_p.D,
                                                               c_smax=self.b_cell.elec_p.max_conc)  # calc p surf SOC
                    self.b_cell.elec_n.SOC = self.SOC_solver_n(dt=dt, t_prev=t_prev, i_app=i_app,
                                                               R=self.b_cell.elec_n.R,
                                                               S=self.b_cell.elec_n.S,
                                                               D_s=self.b_cell.elec_n.D,
                                                               c_smax=self.b_cell.elec_n.max_conc)  # calc n surf SOC

                    # Solve for the electrolyte conc. below
                    # electrolyte_co_ord = ElectrolyteFVMCoordinates(D_e=self.b_cell.electrolyte.D)
