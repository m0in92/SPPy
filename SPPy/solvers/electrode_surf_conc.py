"""
This module contains classes and functionality to calculate the lithium concentrations in the solid phase of the
electrode region
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'


from typing import Callable
import numpy as np
import numpy.typing as npt
from scipy.optimize import bisect

from SPPy.calc_helpers.constants import Constants
from SPPy.calc_helpers import ode_solvers
from SPPy.warnings_and_exceptions.custom_exceptions import InvalidElectrodeType
from SPPy.models.battery import SPM


class BaseElectrodeConcSolver:
    def __init__(self, electrode_type: str):
        if electrode_type == 'p' or electrode_type == 'n':
            self.electrode_type = electrode_type  # either positive electrode ('p') or negative electrode ('n').
        else:
            raise InvalidElectrodeType


class EigenFuncExp(BaseElectrodeConcSolver):
    """
    This solver uses the Eigen Function Expansion method as detailed in ref 1 to calculate the electrode
    surface SOC. As such, it stores all the necessary variables required for the iterative calculations for all time
    steps. After initiating the class, the object instance can be called iteratively to solve for electrode surface SOC
    for all time steps.

    The equation solved is
        x_j_surf = x_ini + (1/5)*j_scaled + 3 * integration{D_sj * j_scaled / R_j ** 2} * dt +
                    summation{u_jk - 2 * scaled_j / lambda_k ** 2}
    In the above equation, the integration is performed from t=0 to the current time. Moreover, the summation is
    performed from k=1 to k=N. Here k represents the kth term of the solution series.

    Reference:
    1. Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
    Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
    """

    def __init__(self, x_init: float, n: int, electrode_type: str):
        self.x_init_ = x_init  # initial electrode SOC
        self.N_ = n  # the number of terms in the solution series

        self.integ_term = 0  # the integration term, which is initialized as zero
        self.lst_u_k = [0 for i in range(self.N)]  # a list of solved values of eigenfunctions, the values of which are
        # all initialized to zero.

        super().__init__(electrode_type=electrode_type)

    @property
    def x_init(self) -> float:
        """
        Initial electrode SOC
        :return: (float) Initial electrode SOC
        """
        return self.x_init_

    @property
    def N(self) -> int:
        """
        The number of terms in the solution series.
        :return: (int) number of terms in the solution series.
        """
        return self.N_

    @staticmethod
    def lambda_func(lambda_k) -> float:
        """
        Algebraic equation from which the eigenvalues can be calculated.
        :param lambda_k: (float) eigen value ot the kth term.
        :return: (float) the value of the elgebraic equation.
        """
        return np.sin(lambda_k) - lambda_k * np.cos(lambda_k)

    def lambda_bounds(self) -> npt.ArrayLike:
        """
        The list which contains the tuple containing the lower and upper bounds of the eigenvalues.
        :return: (list) list containing the tuple of bounds for the eigenvalues.
        """
        return [(np.pi * (1 + k), np.pi * (2 + k)) for k in range(self.N)]  # k refers to the kth term of the series

    @property
    def lambda_roots(self) -> npt.ArrayLike:
        """
        Uses the bisect method to solve for the eigenvalue algebraic equation within the bounds.
        :return: (list) list containing the eigenvalues for all solution terms.
        """
        bounds = self.lambda_bounds()
        return [bisect(self.lambda_func, bounds[k][0], bounds[k][1]) for k in range(self.N)]  # k refers to the kth
        # term of the series

    def j_scaled(self, i_app, R, S, D_s, c_smax) -> float:
        """
        Returns the dimensionless lithium-ion flux
        :return: (float) dimensionless lithium-ion flux
        """
        j_scaled_ = i_app * R / (Constants.F * S * D_s * c_smax)
        if self.electrode_type == 'p':
            return -j_scaled_
        elif self.electrode_type == 'n':
            return j_scaled_

    def update_integ_term(self, dt, i_app, R, S, D_s, c_smax) -> float:
        """
        Updates the integration term. Integration is performed using simple algebraic integration.
        :return: (float) updated integration term.
        """
        self.integ_term += 3 * (D_s * self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax) / (R ** 2)) * dt

    @staticmethod
    def u_k_expression(lambda_k, D, R, scaled_flux) -> Callable:
        """
        Returns a function that represents the eigenfunction ode.
        :param lambda_k: eigenvalue of the kth term
        :param D: diffusivity [m2/s]
        :param R: electrode particle radius [m]
        :param scaled_flux: dimensionless scaled lithium-ion flux
        :return: (func) a function representing the eigenfunction ode
        """
        def u_k_odeFunc(x, t):
            return -(lambda_k ** 2) * D * x / (R ** 2) + 2 * D * scaled_flux / (R ** 2)
        return u_k_odeFunc

    def solve_u_k(self, root_value, t_prev, dt, u_k_prev, i_app, R, S, D_s, c_smax) -> float:
        """
        Calculates the eigenfunction value from the eigen values using the ode function. This ode function is solved
        using the rk4 ode solver.
        :param root_value:
        :param t_prev:
        :param u_k_j_prev:
        :param dt:
        :return:
        """
        j_scaled_ = self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        u_k_p_func = self.u_k_expression(lambda_k=root_value, D=D_s, R=R, scaled_flux=j_scaled_)
        return ode_solvers.rk4(func=u_k_p_func, t_prev=t_prev, y_prev=u_k_prev, step_size=dt)

    def get_summation_term(self, dt, t_prev, i_app, R, S, D_s, c_smax) -> float:
        """
        Calculates and returns the summation term of the Eigen Expansion equation.
        :param t_prev:
        :param dt:
        :param j_scaled:
        :return:
        """
        sum_term = 0
        # Solve for the eigenfunction for all roots using the iteration below:
        j_scaled_ = self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        for iter_root, root_value in enumerate(self.lambda_roots):
            self.lst_u_k[iter_root] = self.solve_u_k(root_value=root_value, t_prev=t_prev,
                                                     u_k_prev=self.lst_u_k[iter_root], dt=dt,
                                                     i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
            sum_term += self.lst_u_k[iter_root] - (2 * j_scaled_ / (root_value ** 2))
        return sum_term

    def calc_SOC_surf(self, dt, t_prev, i_app, R, S, D_s, c_smax) -> float:
        """
        Calculates the electrode surface SOC using the Eigen Expansion method.
        :param dt: The time difference between the current and the previous time steps [s].
        :param t_prev: Time value of the previous time step [s].
        :return: (float) The electrode's surface SOC.
        """
        j_scaled_ = self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        sum_term = self.get_summation_term(t_prev=t_prev, dt=dt, i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        self.update_integ_term(dt=dt, i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        return self.x_init + j_scaled_ / 5 + self.integ_term + sum_term

    def __call__(self, dt, t_prev, i_app, R, S, D_s, c_smax) -> float:
        """
        This method calculates the electrode surface SOC
        :param dt: Time difference between current and previous time steps [s].
        :param t_prev: Time value at the previous time step [s].
        :param i_app: Applied current at the current time step [A].
        :param R:  Electrode particle radius [m]
        :param S: Electrode electroactive area [m2]
        :param D_s: Electrode diffusivity [m2/s]
        :param c_smax: Electrode max. conc [mol/m3]
        :return: (float) The electrode's surface SOC.
        """
        return self.calc_SOC_surf(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)


class CNSolver(BaseElectrodeConcSolver):
    """
    Crank Nickelson Scheme for solving for spherical diffusion in solid electrode in lithium-ion batteries models. The
    associated PDE uses the mass transport with symmetry condition imposed at r=0 and flux boundary condition at r=R.

    The PDE is:
    dx/dt = (D/(R^2 * r_scaled^2)) * d(r_scaled^2 * dx/dr_scaled)/dr_scaled

    with BC:
    dx/dr_scaled = 0 at r_scaled=0
    dx/dr_scaled = -jR/D*c_smax at r_scaled=1
    """
    def __init__(self, c_init: float, electrode_type: str, spatial_grid_points: int = 100):
        super().__init__(electrode_type=electrode_type)
        self.K = spatial_grid_points  # number of spatial grid points
        self.c_prev = c_init * np.ones(self.K).reshape(-1, 1)  # column vector used for storing concentrations at t_prev

    def dr(self, R: float) -> float:
        """
        Difference in radial coordinate [m].
        :param R: electrode particle radius
        :return:
        """
        return R / self.K

    def A(self, dt: float, R: float, D: float) -> float:
        """
        Value of the constant A (delta_t * D / delta_r^2)
        :return: Returns the value of the A constant, used for the forming the matrices
        """
        return dt * D / (self.dr(R) ** 2)

    def B(self, dt: float, R: float, D: float) -> float:
        """
        Value of constant B (delta_t * D / (2 * delta_r))
        :return:
        """
        return dt * D / (2 * self.dr(R))

    def array_R(self, R: float) -> npt.ArrayLike:
        """
        Array containing the values of r at every grid point.
        :return: Array containing the values of r at every grid point.
        """
        return np.linspace(0, R, self.K)

    def _LHS_diag_elements(self, dt: float, R: float, D: float) -> npt.ArrayLike:
        A_ = self.A(dt=dt, R=R, D=D)
        array_elements = (1 + A_) * np.ones(self.K)
        array_elements[0] = 1 + 3 * A_  # for symmetry boundary condition at r=0
        array_elements[-1] = 1 + A_
        return array_elements

    def _LHS_lower_diag(self, dt: float, R: float, D: float) -> npt.ArrayLike:
        A_ = self.A(dt=dt, R=R, D=D)
        B_ = self.B(dt=dt, R=R, D=D)
        array_elements = -(A_/2 - B_/self.array_R(R)[1:]) * np.ones(self.K-1)
        array_elements[-1] = -A_  # for the flux at r=R
        return array_elements

    def _LHS_upper_diag(self, dt: float, R: float, D: float) -> npt.ArrayLike:
        A_ = self.A(dt=dt, R=R, D=D)
        B_ = self.B(dt=dt, R=R, D=D)
        array_elements = -(A_ / 2 + B_ / self.array_R(R)[1:-1]) * np.ones(self.K - 2)
        array_elements = np.insert(array_elements, 0, -3 * A_)  # for symmetry boundary condition at r=0
        return array_elements

    def M(self, dt: float, R: float, D: float) -> npt.ArrayLike:
        return np.diag(self._LHS_diag_elements(dt=dt, R=R, D=D)) + \
               np.diag(self._LHS_lower_diag(dt=dt, R=R, D=D), -1) + \
               np.diag(self._LHS_upper_diag(dt=dt, R=R, D=D), 1)

    def _RHS_array(self, j: float, dt: float, R: float, D: float):
        A_ = self.A(dt=dt, R=R, D=D)
        B_ = self.B(dt=dt, R=R, D=D)
        array_c_temp = np.zeros(self.K).reshape(-1,1)
        array_c_temp[0][0] = (1-3*A_)*self.c_prev[0][0] + 3*A_*self.c_prev[1][0]  # for the symmetry boundary condition
        # at r=0
        array_c_temp[-1][0] = (1-A_) * self.c_prev[-1][0] - (A_+B_/R) * (2*self.dr(R=R)*j/D) + \
                              A_ * self.c_prev[-2][0]  # for the boundary condition at r=R
        for i in range(1, len(array_c_temp) - 1):
            array_c_temp[i][0] = (1 - A_) * self.c_prev[i][0] + \
                                 (A_ / 2 + B_ / self.array_R(R=R)[i]) * self.c_prev[i + 1][0] + \
                                 (A_ / 2 - B_ / self.array_R(R=R)[i]) * self.c_prev[i - 1][0]
        return array_c_temp

    def solve(self, dt: float, i_app: float, R: float, S: float, D: float, solver_method:str):
        """
        Solves for the lithium-ion concentration after dt. It then updates the class instance's c_prev attribute.
        :param c_prev: (numpy array) matrix (Kx1) containing the concentrations at t_prev [mol/m3]
        :param j: (float) lithium flux at r=R [mol/m2/s]
        :param dt: (float) time difference [s]
        :param R: (float) electrode particle radius [m]
        :param D: (float) electrode diffusivity [m2/s]
        :return:
        """
        j = SPM.molar_flux_electrode(I=i_app, S=S, electrode_type=self.electrode_type)
        if solver_method == "inverse":
            self.c_prev = np.linalg.inv(self.M(dt=dt, R=R, D=D)) @ self._RHS_array(j=j, dt=dt, R=R, D=D)
        elif solver_method == "TDMA":
            self.c_prev = ode_solvers.TDMAsolver(l_diag=self._LHS_lower_diag(dt=dt, R=R, D=D),
                                                 diag=self._LHS_diag_elements(dt=dt, R=R, D=D),
                                                 u_diag=self._LHS_upper_diag(dt=dt, R=R, D=D),
                                                 col_vec=self._RHS_array(j=j, dt=dt, R=R, D=D)).flatten().reshape(-1, 1)

    def __call__(self, dt: float, t_prev: float, i_app:float, R: float, S:float, D_s: float, c_smax: float,
                 solver_method: str = "TDMA") -> float:
        """
        Returns the electrode surface SOC
        """
        self.solve(dt=dt, i_app=i_app, R=R, S=S, D=D_s, solver_method=solver_method)
        return self.c_prev[-1][0] / c_smax


class PolynomialApproximation(BaseElectrodeConcSolver):
    """
    Two=parameter polynomial approximation for the spherical diffusion using two parameters [1].

    Reference:
    [1] Torchio, M., Magni, L., Gopaluni, R. B., Braatz, R. D., & Raimondo, D. M. (2016).
    LIONSIMBA: A Matlab Framework Based on a Finite Volume Model Suitable for Li-Ion Battery Design, Simulation,
    and Control.
    Journal of The Electrochemical Society, 163(7), A1192–A1205.
    https://doi.org/10.1149/2.0291607JES/XML
    """
    def __init__(self, c_init: float, electrode_type: str, type: str = 'higher'):
        super().__init__(electrode_type=electrode_type)
        self.c_s_avg_prev = c_init
        self.c_surf = c_init
        if type=='two' or type == 'higher':
            self.type = type
        else:
            raise ValueError(f"{type} is not recognized as a solver type")
        if self.type == 'higher':
            self.q = 0

    def func_c_s_avg(self, j: float, R: float) -> Callable:
        def wrapper(r, t):
            return -3 * j / R
        return wrapper

    def func_q(self, j: float, R: float, D: float) -> Callable:
        def wrapper(x, t):
            return -30 * (D/R**2) * x - (45*j/(2 * R**2))
        return wrapper

    def solve(self, dt: float, t_prev: float, i_app: float, R: float, S: float, D: float):
        j = SPM.molar_flux_electrode(I=i_app, S=S, electrode_type=self.electrode_type)
        self.c_s_avg_prev = ode_solvers.rk4(func=self.func_c_s_avg(j=j, R=R), t_prev=t_prev,
                                             y_prev=self.c_s_avg_prev, step_size=dt)
        if self.type != 'two':
            self.q = ode_solvers.rk4(self.func_q(j=j, R=R, D=D), t_prev=t_prev, y_prev=self.q, step_size=dt)
            self.c_surf = -(j*R)/(35*D) + 8 * R * self.q / 35 + self.c_s_avg_prev
        else:
            self.c_surf = -(R/D) * (j/5) + self.c_s_avg_prev

    def __call__(self, dt: float, t_prev: float, i_app: float, R: float, S: float, D_s: float, c_smax: float) -> float:
        self.solve(dt=dt, i_app=i_app, t_prev=t_prev, R=R, S=S, D=D_s)
        return self.c_surf / c_smax


