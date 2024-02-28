__all__ = ['BaseSolver', 'DTSolver', 'ESCDTSolver']

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'

from typing import Optional

import tqdm
import numpy as np

from SPPy.solvers.base import timer
from SPPy.battery_components.battery_cell import ECMBatteryCell
from SPPy.models.ECM import Thevenin1RC, ESC
from SPPy.cycler.base import BaseCycler
from SPPy.cycler.custom import CustomCycler
from SPPy.solvers.thermal_solvers import calc_cell_temp
from SPPy.sol_and_visualization.solution import ECMSolution

# from SPPy.calc_helpers.random_vectors import NormalRandomVector
from SPPy.calc_helpers.kalman_filter import NormalRandomVector, SigmaPointKalmanFilter


class BaseSolver:
    def __init__(self, battery_cell_instance: ECMBatteryCell, isothermal: bool):
        if isinstance(battery_cell_instance, ECMBatteryCell):
            self.b_cell = battery_cell_instance
        else:
            raise TypeError("ECM_obj must be an instance of Thevenin1RC class.")

        if isinstance(isothermal, bool):
            self.isothermal = isothermal
        else:
            raise TypeError("isothermal must be a boolean (True or False).")

        self.b_model = Thevenin1RC()


class DTSolver(BaseSolver):
    """
    This is the class that solves the ECM model equations for time and applied current arrays. It outputs the terminal
    SOC and voltage at the time steps specified by the input time array.

    The discrete time model for first-order Thevenin model is given by:

    z[k+1] = z[k] - delta_t*eta[k]*i_app[k]/capacity
    i_R1[k+1] = exp(-delta_t/(R1*C1))*i_R1[k] + (1-exp(-delta_t/(R1*C1))) * i_app[k]
    v[k] = OCV(z[k]) - R1*i_R1[k] - R0*i_app[k]

    Where k represents the time-point and delta_t represents the time-step between z[k+1] and z[k].
    """

    def __init__(self, battery_cell_instance: ECMBatteryCell, isothermal: bool):
        """
        The class constructor for the solver object.
        :params ECM_obj: (Thevenin1RC) ECM model object
        :params isothermal: (bool)
        :params t_app: (Numpy array) array of time.
        :params i_app: (Numpy array) array of applied battery current associated with the time array.
        :param v_exp: (Numpy array) array of experimental battery terminal voltage data.
        """
        super().__init__(battery_cell_instance=battery_cell_instance, isothermal=isothermal)
        self.__dt = 0.0  # delta_t is required for sigma point kalman filter solver.

    def __calc_v(self, dt: float, i_app: float, i_r1_prev: float) -> tuple[float, float]:
        """
        Calculates the cell terminal voltage by first calculating the current across the R-C pair
        :param dt:
        :param i_app:
        :param i_r1_prev:
        :return:
        """
        i_r1_prev = Thevenin1RC.i_R1_next(dt=dt, i_app=i_app, i_R1_prev=i_r1_prev,
                                          R1=self.b_cell.R1, C1=self.b_cell.C1)
        v = Thevenin1RC.v(i_app=i_app, OCV=self.b_cell.func_ocv(self.b_cell.soc),
                          R0=self.b_cell.R0, R1=self.b_cell.R1, i_R1=i_r1_prev)
        return i_r1_prev, v

    def __solve_custom_step(self, cycling_step: CustomCycler, dt: float, verbose: bool):
        sol = ECMSolution()  # initialize the solution object
        sol.update(t=0.0, i_app=0.0, v=self.b_cell.ocv, temp=self.b_cell.temp, soc=self.b_cell.soc, i_r1=0.0)

        t_prev = 0.0  # [s]
        i_r1_prev = 0.0  # [A]
        step_completed = False

        while not step_completed:
            t_curr = t_prev + dt
            i_app_prev = cycling_step.get_current(step_name='custom', t=t_prev)
            i_app_curr = cycling_step.get_current(step_name='custom', t=t_curr)

            # Calculate the SOC (and update the battery cell attribute), i_R1 [A], and v[V] for the current time step
            self.b_cell.soc = Thevenin1RC.soc_next(dt=dt, i_app=i_app_prev, SOC_prev=self.b_cell.soc,
                                                   Q=self.b_cell.cap,
                                                   eta=self.b_cell.eta)
            i_r1_prev, v = self.__calc_v(dt=dt, i_app=i_app_curr, i_r1_prev=i_r1_prev)

            # Calc temp
            if self.isothermal is not True:
                self.b_cell.temp = calc_cell_temp(t_prev=t_prev, dt=dt, temp_prev=self.b_cell.temp, V=v,
                                                  I=i_app_curr,
                                                  rho=self.b_cell.rho, Vol=self.b_cell.vol, C_p=self.b_cell.c_p,
                                                  OCV=self.b_cell.ocv, dOCVdT=self.b_cell.docpdtemp,
                                                  h=self.b_cell.h,
                                                  A=self.b_cell.area, T_amb=self.b_cell.temp_init)

            # loop termination criteria
            if v > cycling_step.V_max:
                step_completed = True
            if v < cycling_step.V_min:
                step_completed = True
            if t_curr > cycling_step.t_max:
                step_completed = True

            # update the sol object
            sol.update(t=t_curr, i_app=i_app_curr, v=v, temp=self.b_cell.temp, soc=self.b_cell.soc, i_r1=i_r1_prev)
            t_prev = t_curr

            if verbose == True:
                print('t=', t_curr, ' i_app=', i_app_curr, ' v=', v, ' temp=', self.b_cell.temp,
                      ' soc=', self.b_cell.soc, ' i_R1=', i_r1_prev)

        return sol

    def __solve_standard_cycling_step(self, cycler: BaseCycler, dt: float) -> ECMSolution:
        sol = ECMSolution()
        # update the initial values of sol object below
        sol.update(t=0.0, i_app=0.0, v=self.b_cell.ocv, temp=self.b_cell.temp, soc=self.b_cell.soc, i_r1=0.0)
        for cycle_no in tqdm.tqdm(range(cycler.num_cycles)):
            for step in cycler.cycle_steps:
                t_prev = 0
                i_r1_prev = 0
                step_completed = False
                while not step_completed:
                    t_curr = t_prev + dt
                    i_app = -cycler.get_current(step_name=step, t=t_curr)

                    # break condition for rest time
                    if step == "rest" and t_curr > cycler.rest_time:
                        step_completed = True

                    # calc. the SOC and i_R1 for the current time step
                    self.b_cell.soc = self.b_model.soc_next(dt=dt, i_app=i_app, SOC_prev=self.b_cell.soc,
                                                            Q=self.b_cell.cap, eta=self.b_cell.eta)
                    i_r1_prev, v = self.__calc_v(dt=dt, i_app=i_app, i_r1_prev=i_r1_prev)

                    # Calc temp
                    if self.isothermal is not True:
                        self.b_cell.temp = calc_cell_temp(t_prev=t_prev, dt=dt, temp_prev=self.b_cell.temp, V=v,
                                                          I=-i_app,
                                                          rho=self.b_cell.rho, Vol=self.b_cell.vol, C_p=self.b_cell.c_p,
                                                          OCV=self.b_cell.ocv, dOCVdT=self.b_cell.docpdtemp,
                                                          h=self.b_cell.h,
                                                          A=self.b_cell.area, T_amb=self.b_cell.temp_init)

                    # loop termination criteria
                    if (step == "charge") and (v > cycler.v_max):
                        step_completed = True
                    if (step == "discharge") and (v < cycler.v_min):
                        step_completed = True

                    # Below updates the simulation parameters for the next iteration
                    t_prev = t_curr

                    # update solution object
                    sol.update(t=t_curr, i_app=i_app, v=v, temp=self.b_cell.temp, soc=self.b_cell.soc, i_r1=i_r1_prev)
        return sol

    @timer
    def solve(self, cycling_step: BaseCycler, dt: float = 0.1, verbose: bool = False) -> ECMSolution:
        if isinstance(cycling_step, CustomCycler):
            return self.__solve_custom_step(cycling_step=cycling_step, dt=dt, verbose=verbose)
        else:
            return self.__solve_standard_cycling_step(cycler=cycling_step, dt=dt)

    def __func_f(self, x_k, u_k, w_k):
        """
        State Equation.
        :param x_k:
        :param u_k:
        :param w_k:
        :param delta_t:
        :return:
        """
        R1 = self.b_cell.R1
        C1 = self.b_cell.C1
        Q = self.b_cell.cap
        m1 = np.array([[1, 0], [0, np.exp(-self.__dt / (R1 * C1))]])
        m2 = np.array([[-self.__dt / (3600 * Q)], [1 - np.exp(-self.__dt / (R1 * C1))]])
        return m1 @ x_k + m2 * (u_k + w_k)

    def __func_h(self, x_k, u_k, v_k):
        """
        Output Equation.
        :param x_k:
        :param u_k:
        :param v_k:
        :return:
        """
        return self.b_cell.func_ocv(x_k[0, :]) - self.b_cell.R1 * x_k[1, :] - self.b_cell.R0 * u_k + v_k

    def solveSPKF(self, sol_exp: ECMSolution, cov_soc: float, cov_current: float, cov_process: float, cov_sensor: float,
                  v_min: float, v_max: float, soc_min: float, soc_max: float, soc_init: float,
                  dt: Optional[float] = None):
        """
        Performs the Thevenin equivalent circuit model using the sigma point kalman filter
        :param sol_exp: Solution object from the experimental data.
        :param cov_soc: covariance of the soc
        :param cov_current: covariance of i_r1
        :param cov_process: covariance of the system process
        :param cov_sensor: covariance of the voltage sensor
        :param v_min: threshold cell terminal voltage [V]
        :param v_max: threshold cell terminal voltage [V]
        :param soc_min: minimum LIB SOC
        :param soc_max: maximum LIB SOC
        :param soc_init: LIB SOC
        :param dt: time difference between calculation time step. If set to None, then the time difference
        from the experimental is used for each time step.
        :return: (Solution) Solution object containing the results from the simulations.
        """
        sol = ECMSolution()

        cycling_step = CustomCycler(array_t=sol_exp.array_t, array_I=sol_exp.array_I, V_min=v_min, V_max=v_max,
                                    SOC_LIB=soc_init, SOC_LIB_min=soc_min, SOC_LIB_max=soc_max)
        array_y_true = sol_exp.array_V  # y_true is extracted from the solution object

        # create Normal Random Variables below
        i_r1_init = 0.0  # [A]
        vector_x = np.array([[self.b_cell.soc], [i_r1_init]])
        cov_x = np.array([[cov_soc, 0], [0, cov_current]])
        vector_w = np.array([[0]])
        cov_w = np.array([[cov_process]])
        vector_v = np.array([[0]])
        cov_v = np.array([[cov_sensor]])

        x = NormalRandomVector(vector_init=vector_x, cov_init=cov_x)
        w = NormalRandomVector(vector_init=vector_w, cov_init=cov_w)
        v = NormalRandomVector(vector_init=vector_v, cov_init=cov_v)

        # Create sigma-point kalman filter below
        instance_spkf: SigmaPointKalmanFilter = SigmaPointKalmanFilter(x=x, w=w, v=v, y_dim=1,
                                                                       state_equation=self.__func_f,
                                                                       output_equation=self.__func_h)

        # The solution loop is run below
        t_prev: float = 0.0  # [s]
        step_completed: bool = False
        # cap_discharge = 0.0  # [A hr]

        i: int = 1
        while not step_completed:
            t_curr = cycling_step.array_t[i]
            if dt is None:
                self.__dt = t_curr - t_prev
            i_app_prev = cycling_step.array_I[i - 1]
            i_app_curr = cycling_step.array_I[i]

            instance_spkf.solve(u=i_app_prev, y_true=array_y_true[i])

            self.b_cell.soc = instance_spkf.x.get_vector()[0, 0]
            i_r1: float = instance_spkf.x.get_vector()[1, 0]
            v = self.__calc_v(dt=self.__dt, i_app=i_app_curr, i_r1_prev=i_r1)[1]

            # loop termination criteria
            if v > cycling_step.V_max:
                step_completed = True
            if v < cycling_step.V_min:
                step_completed = True
            if t_curr > cycling_step.array_t[-1]:
                step_completed = True
            if i >= len(cycling_step.array_t) - 1:
                step_completed = True

            # update sol attributes
            sol.update(t=t_curr, i_app=i_app_curr, v=v, temp=self.b_cell.temp, soc=self.b_cell.soc, i_r1=i_r1)

            # update simulation parameters
            t_prev = t_curr
            i += 1

        return sol


class ESCDTSolver(BaseSolver):
    def __init__(self, battery_cell_instance: ECMBatteryCell, isothermal: bool):
        super().__init__(battery_cell_instance=battery_cell_instance,
                         isothermal=isothermal)

    def solve_standard_cycling_step(self, cycler: BaseCycler, dt: float) -> ECMSolution:
        sol = ECMSolution()

        # Below are the intial simulation parameters
        i_R1: float = 0.0
        h: float = 0.0
        s: float = 0.0

        for cycle_no in range(cycler.num_cycles):
            for step in cycler.cycle_steps:
                t_prev: float = 0.0
                step_completed: bool = False

                while not step_completed:
                    t_curr = t_prev + dt
                    i_app: float = -cycler.get_current(step_name=step, t=t_curr)

                    # The steps below calculates the cell terminal potential
                    self.b_cell.soc = ESC.soc_next(dt=dt, i_app=i_app, SOC_prev=self.b_cell.soc, Q=self.b_cell.cap,
                                                   eta=self.b_cell.eta)
                    i_R1_prev: float = i_R1
                    i_R1 = ESC.i_R1_next(dt=dt, i_app=i_app, i_R1_prev=i_R1, R1=self.b_cell.R1, C1=self.b_cell.C1)
                    h_prev: float = h
                    h = ESC.h_next(dt=dt, i_app=i_app, eta=self.b_cell.eta, gamma=self.b_cell.gamma,
                                   cap=self.b_cell.cap, h_prev=h)
                    s_prev: float = s
                    s = ESC.s(i_app=i_app, s_prev=s)
                    v = ESC.v(i_app=i_app, ocv=self.b_cell.ocv, R0=self.b_cell.R0, R1=self.b_cell.R1, i_R1=i_R1_prev,
                              m_0=self.b_cell.M_0, m=self.b_cell.M, h=h_prev, s_prev=s_prev)
                    # print(t_curr, v)

                    # Loop termination criteria
                    if (step == 'charge') and (v > cycler.v_max):
                        step_completed = True
                    if (step == 'discharge') and (v < cycler.v_min):
                        step_completed = True
                    if (step == 'rest') and (t_curr > cycler.rest_time):
                        step_completed = True

                    # Below updates the simulation parameters
                    t_prev = t_curr

                    # update solution object
                    sol.update(t=t_curr, i_app=i_app, v=v, temp=self.b_cell.temp, soc=self.b_cell.soc, i_r1=i_R1_prev)

        return sol
