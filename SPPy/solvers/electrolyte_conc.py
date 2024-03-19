"""
Contains classes for electrolyte solvers.
"""

__all__ = ['ElectrolyteConcFVMSolver']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright by SPPy. All rights reserved."
__status__ = "deployed"

from typing import Callable, Union

import numpy as np
import numpy.typing as npt
import scipy.interpolate

from SPPy.calc_helpers.matrix_operations import TDMAsolver
from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates
from SPPy.calc_helpers import ode_solvers


class ElectrolyteConcFVMSolver:
    """
    This solver solves for the lithium-ion concentration in the electrolyte across the battery cell thickness. It uses
    the finite volume method (FVM) as indicated by Han et al. [1].

    In their paper, Han et al. defined the flux in terms of A/m2/s. Here, the relevant equations have been modified
    to refer to flux in terms of mol/m2/s.

    [1] Han, S., Tang, Y., & Khaleghi Rahimian, S. (2021). A numerically efficient method of solving the full-order
    pseudo-2-dimensional (P2D) Li-ion cell model. Journal of Power Sources, 490, 229571.
    https://doi.org/10.1016/J.JPOWSOUR.2021.229571Han, S., Tang, Y., & Khaleghi Rahimian, S. (2021).
    """
    def __init__(self, fvm_co_ords: ElectrolyteFVMCoordinates, c_e_init: float, transference: float,
                 epsilon_en: float, epsilon_esep: float, epsilon_ep: float,
                 a_sn: float, a_sp: float,
                 D_e: float, brugg: float):
        self.co_ords = fvm_co_ords
        self.t_c = transference
        self.c_e_init: float = c_e_init
        self.array_c_e_ = self.c_e_init * np.ones(len(self.co_ords.array_x))  # assuming consistent electrolyte conc.
        # across the battery cell.

        self.epsilon_en: float = epsilon_en
        self.epsilon_esep: float = epsilon_esep
        self.epsilon_ep: float = epsilon_ep

        self.a_sn: float = a_sn
        self.a_sp: float = a_sp

        self.D_e: float = D_e
        self.brugg: float = brugg

    @property
    def array_epsilon_e(self) -> np.ndarray:
        """
        Returns an array containing the volume fraction of the electrolyte at each spatial region
        :return:
        """
        array_epsilon_n: np.ndarray = self.epsilon_en * np.ones(len(self.co_ords.array_x_n))
        array_epsilon_s: np.ndarray = self.epsilon_esep * np.ones(len(self.co_ords.array_x_s))
        array_epsilon_p: np.ndarray = self.epsilon_ep * np.ones(len(self.co_ords.array_x_p))
        return np.append(np.append(array_epsilon_n, array_epsilon_s), array_epsilon_p)

    @property
    def array_D_eff(self) -> npt.ArrayLike:
        """
        Returns an array containing the effective electrolyte diffusivity at spatial FVM points.
        :return:
        """
        array_D_eff_n: np.ndarray = self.D_e * (self.epsilon_en ** self.brugg) * np.ones(len(self.co_ords.array_x_n))
        array_D_eff_s: np.ndarray = self.D_e * (self.epsilon_esep ** self.brugg) * np.ones(len(self.co_ords.array_x_s))
        array_D_eff_p: np.ndarray = self.D_e * (self.epsilon_ep ** self.brugg) * np.ones(len(self.co_ords.array_x_p))
        return np.append(np.append(array_D_eff_n, array_D_eff_s), array_D_eff_p)

    @property
    def array_a_s(self) -> npt.ArrayLike:
        array_asn = self.a_sn * np.ones(len(self.co_ords.array_x_n))
        array_asep = np.zeros(len(self.co_ords.array_x_s))
        array_asp = self.a_sp * np.ones(len(self.co_ords.array_x_p))
        return np.append(np.append(array_asn, array_asep), array_asp)

    @property
    def array_c_e(self) -> npt.ArrayLike:
        return self.array_c_e_

    @array_c_e.setter
    def array_c_e(self, new_array_c_e_prev: np.ndarray) -> None:
        self.array_c_e_ = new_array_c_e_prev

    def diags(self, dt: float) -> tuple[list[float], list[float], list[float]]:
        # initialize the diagonals
        diag_elements = []
        upper_diag_elements = []
        lower_diag_elements = []
        # update first elements
        dx = (self.co_ords.array_x[1] - self.co_ords.array_x[0])
        D1 = self.array_D_eff[0]
        D2 = self.array_D_eff[1]
        A = dt / (2 * self.co_ords.array_dx[0])
        diag_elements.append(self.array_epsilon_e[0] + A * (D2 + D1) / dx)
        upper_diag_elements.append(-A * (D2 + D1) / dx)
        for i in range(1, len(self.co_ords.array_x) - 1):
            dx1 = self.co_ords.array_x[i] - self.co_ords.array_x[i - 1]
            dx2 = self.co_ords.array_x[i + 1] - self.co_ords.array_x[i]
            D1 = self.array_D_eff[i - 1]
            D2 = self.array_D_eff[i]
            D3 = self.array_D_eff[i + 1]
            A = dt / (2 * self.co_ords.array_dx[i])
            diag_elements.append(self.array_epsilon_e[i] + A * ((D1 + D2) / dx1 + (D2 + D3) / dx2))
            upper_diag_elements.append(-A * (D3 + D2) / dx2)
            lower_diag_elements.append(-A * (D1 + D2) / dx1)
        # update last elements
        dx = (self.co_ords.array_x[-1] - self.co_ords.array_x[-2])
        D1 = self.array_D_eff[-1]
        D2 = self.array_D_eff[-1]
        A = dt / (2 * self.co_ords.array_dx[-1])
        diag_elements.append(self.array_epsilon_e[-1] + A * (D2 + D1) / dx)
        lower_diag_elements.append(-A * (D2 + D1) / dx)
        return lower_diag_elements, diag_elements, upper_diag_elements

    def M_ce(self, dt) -> npt.ArrayLike:
        l_diag, diag, u_diag = self.diags(dt)
        return np.diag(diag) + np.diag(u_diag, 1) + np.diag(l_diag, -1)

    def ce_j_vec(self, c_prev: npt.ArrayLike, j: npt.ArrayLike, dt: float) -> npt.ArrayLike:
        ce_j_vec_1_ = (c_prev * self.array_epsilon_e).reshape(-1, 1)
        ce_j_vec_2_ = ((1 - self.t_c) * self.array_a_s * j * dt).reshape(-1, 1)
        return ce_j_vec_1_ + ce_j_vec_2_

    def solve_ce(self, j: npt.ArrayLike, dt: float, solver_method: str = 'TDMA') -> None:
        b = self.ce_j_vec(c_prev=self.array_c_e, j=j, dt=dt)
        if solver_method == 'TDMA':
            l_diag, diag, u_diag = self.diags(dt)
            self.array_c_e = TDMAsolver(l_diag=l_diag, diag=diag, u_diag=u_diag, col_vec=b)
        elif solver_method == 'inverse':
            M = np.linalg.inv(self.M_ce(dt=dt))
            self.array_c_e = np.ndarray.flatten(M @ b)

    def extrapolate_conc(self, L_value: float) -> float:
        """
        Returns the electrolyte conc. [mol/m3] at the specified value L_value.
        :param L_value: float representing the cross-sectional length of the battery cell.
        :return: (float) electrolyte conc [mol/m3] at the specified value of L_value.
        """
        return scipy.interpolate.interp1d(self.co_ords.array_x, self.array_c_e, fill_value='extrapolate')(L_value)


class ElectrolyteConcVolAvgSolver:
    """
    Volume average technique for the electrolyte concentration.
    """
    def __init__(self, L_n: float, L_s: float, L_p: float,
                 epsilon_n: float, epsilon_s: float, epsilon_p: float,
                 D_n: float, D_s: float, D_p: float,
                 a_n: float, a_p: float,
                 t_c: float,
                 c_e_init: float):
        self.L_s: float = L_s
        self.L_p: float = L_p
        self.L_n: float = L_n
        self.L_cell: float = L_n + L_s + L_p
        self.D_s: float = D_s
        self.D_p: float = D_p
        self.D_n: float = D_n
        self.c_e_init: float = c_e_init

        num_first_term: float = (L_n * L_s * epsilon_n) / (2 * D_s)
        num_second_term: float = (L_s**2 * epsilon_s) / (6*D_s)
        num_third_term: float = (L_n**2 * epsilon_n) / (3*D_n)
        dem: float = L_n * epsilon_n + L_s * epsilon_s + L_p * epsilon_p
        self.alpha_n: float = (num_first_term + num_second_term + num_third_term) / dem

        num_first_term: float = (L_p * L_s * epsilon_p) / (2 * D_s)
        num_second_term: float = (L_s ** 2 * epsilon_s) / (6 * D_s)
        num_third_term: float = (L_p ** 2 * epsilon_p) / (3 * D_p)
        self.alpha_p: float = (num_first_term + num_second_term + num_third_term) / dem

        self.A_1: float = L_n * epsilon_n * self.alpha_n + L_s * L_n * epsilon_n / (2*D_s) + L_n**2 * epsilon_n / (3*D_n)
        self.A_2: float = L_p * epsilon_p * self.alpha_p - L_p**2 * epsilon_p / (3*D_p)
        self.A_3: float = (1-t_c) * a_n * L_n

        self.B_1: float = L_p * epsilon_p * self.alpha_n
        self.B_2: float = L_p * epsilon_p * self.alpha_p - L_p**2 * epsilon_p / (3 * D_p)
        self.B_3: float = (1-t_c) * a_p * L_p

        self.D_: float = self.A_1 * self.B_2 - self.A_2 * self.B_1

        # The variables refer to the interfacial area and flux
        self.c_e_n: float = self.c_e_init
        self.c_e_p: float = self.c_e_init
        self.q_n: float = 0.0
        self.q_p: float = 0.0

    def func_q_n(self, avg_j_n: float, avg_j_p: float) -> Callable:
        def wrapper(x: float, t: float) -> float:
            return (1/self.D_) * (-self.B_2*x - self.A_2*x + self.A_3*self.B_2*avg_j_n - self.A_2*self.B_3*avg_j_p)
        return wrapper

    def func_q_p(self, avg_j_n: float, avg_j_p: float) -> Callable:
        def wrapper(x: float, t: float) -> float:
            return (1/self.D_) * (self.B_1*x + self.A_1*x - self.A_3*self.B_1*avg_j_n + self.A_1*self.B_3*avg_j_p)
        return wrapper

    def func_c_n(self, c_p: float) -> float:
        return c_p + self.L_s * (self.q_n + self.q_p) / (2 * self.D_s)

    def func_c_p(self) -> float:
        return self.c_e_init + self.alpha_n * self.q_n + self.alpha_p * self.q_p

    def conc_profile_n(self, L_value: Union[float, np.ndarray] = 0.0) -> float:
        return self.c_e_n + self.q_n * (self.q_n * (self.L_n**2 - L_value**2)) / (2 * self.L_n * self.D_n)

    def conc_profile_p(self, L_value: Union[float, np.ndarray]) -> float:
        return self.c_e_p - self.q_p * (self.L_p**2 - (self.L_cell - L_value)**2) / (2 * self.L_p * self.D_p)

    def solve(self, t_prev: float, dt: float,
              avg_j_n: float, avg_j_p: float) -> None:
        self.q_n = ode_solvers.rk4(func=self.func_q_n(avg_j_n=avg_j_n, avg_j_p=avg_j_p),
                                   t_prev=t_prev, y_prev=self.q_n, step_size=dt)
        self.q_p = ode_solvers.rk4(func=self.func_q_n(avg_j_n=avg_j_n, avg_j_p=avg_j_p),
                                   t_prev=t_prev, y_prev=self.q_p, step_size=dt)
        self.c_e_p = self.func_c_p()
        self.c_e_n = self.func_c_n(c_p=self.c_e_p)

