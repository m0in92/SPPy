"""
Contains the classes and functionalites for the electrolyte potential solver.
"""

__all__ = ['BaseElectrolytePotentialSolver', 'ElectrolytePotentialFVMSolver', 'ElectrolytePotentialVolAvgSolver']
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by SPPy. All rights reserved."

from typing import Union

import numpy as np
import numpy.typing as npt
import scipy

from SPPy.calc_helpers.constants import Constants
from SPPy.solvers.co_ordinates import FVMCoordinates, ElectrolyteFVMCoordinates


class BaseElectrolytePotentialSolver:
    pass


class ElectrolytePotentialFVMSolver(BaseElectrolytePotentialSolver):
    """
    This solver solves for the electrolyte potential across the battery cell thickness. It uses
    the finite volume method (FVM) as indicated by Han et al. [1].

    In their paper, Han et al. defined the flux in terms of A/m2/s. Here, the relevant equations have been modified
    to refer to flux in terms of mol/m2/s.

    [1] Han, S., Tang, Y., & Khaleghi Rahimian, S. (2021). A numerically efficient method of solving the full-order
    pseudo-2-dimensional (P2D) Li-ion cell model. Journal of Power Sources, 490, 229571.
    https://doi.org/10.1016/J.JPOWSOUR.2021.229571Han, S., Tang, Y., & Khaleghi Rahimian, S. (2021).
    """
    def __init__(self, fvm_coords: ElectrolyteFVMCoordinates,
                 epsilon_en: float, epsilon_esep: float, epsilon_ep: float,
                 a_s_n: float, a_s_p: float,
                 t_c: float, kappa_e: float, brugg: float, temp: float):
        self.coords = fvm_coords

        self.epsilon_en = epsilon_en
        self.epsilon_esep = epsilon_esep
        self.epsilon_ep = epsilon_ep
        self.a_s_n = a_s_n
        self.a_s_p = a_s_p

        self.t_c = t_c
        self.kappa_e = kappa_e
        self.temp = temp
        self.kappa_D = 2 * Constants.R * self.temp * self.kappa_e * (1 - self.t_c) / Constants.F
        self.brugg = brugg

        self.n: int = len(self.coords.array_x)  # the number of rows and columns of the matrix..

    @property
    def array_epsilon_e(self) -> npt.ArrayLike:
        """
        Returns an array containing the volume fraction of the electrolyte at each spatial region
        :return:
        """
        array_epsilon_n = self.epsilon_en * np.ones(len(self.coords.array_x_n))
        array_epsilon_s = self.epsilon_esep * np.ones(len(self.coords.array_x_s))
        array_epsilon_p = self.epsilon_ep * np.ones(len(self.coords.array_x_p))
        return np.append(np.append(array_epsilon_n, array_epsilon_s), array_epsilon_p)

    @property
    def array_kappa_eff(self) -> npt.ArrayLike:
        """
        Returns an array containing the effective electrolyte conductivity at spatial FVM points.
        :return:
        """
        array_kappa_eff_n = self.kappa_e * (self.epsilon_en ** self.brugg) * np.ones(len(self.coords.array_x_n))
        array_kappa_eff_s = self.kappa_e * (self.epsilon_esep ** self.brugg) * np.ones(len(self.coords.array_x_s))
        array_kappa_eff_p = self.kappa_e * (self.epsilon_ep ** self.brugg) * np.ones(len(self.coords.array_x_p))
        return np.append(np.append(array_kappa_eff_n, array_kappa_eff_s), array_kappa_eff_p)

    @property
    def array_kappa_D_eff(self) -> npt.ArrayLike:
        """
        Returns an array containing the effective kappa_D at spatial FVM points.
        :return:
        """
        array_D_eff_n = self.kappa_D * (self.epsilon_en ** self.brugg) * np.ones(len(self.coords.array_x_n))
        array_D_eff_s = self.kappa_D * (self.epsilon_esep ** self.brugg) * np.ones(len(self.coords.array_x_s))
        array_D_eff_p = self.kappa_D * (self.epsilon_ep ** self.brugg) * np.ones(len(self.coords.array_x_p))
        return np.append(np.append(array_D_eff_n, array_D_eff_s), array_D_eff_p)

    @property
    def array_a_s(self) -> npt.ArrayLike:
        """
        Array containing the interfacial specific area [1/m] throughout the battery cell.
        """
        array_a_s_n = self.a_s_n * np.ones(len(self.coords.array_x_n))
        array_a_s_sep = np.zeros(len(self.coords.array_x_s))
        array_a_s_p = self.a_s_p * np.ones(len(self.coords.array_x_p))
        return np.append(np.append(array_a_s_n, array_a_s_sep), array_a_s_p)

    def _m_phi_e(self):
        diag_elements = np.zeros(self.n)
        lower_diag_elements = np.zeros(self.n - 1)
        upper_diag_elements = np.zeros(self.n - 1)
        # setup first row
        k_eff1 = (self.array_kappa_eff[0] + self.array_kappa_eff[1]) / 2
        dx1 = self.coords.array_x[1] - self.coords.array_x[0]
        diag_elements[0] = -k_eff1 / dx1
        upper_diag_elements[0] = k_eff1 / dx1
        for i in range(1, self.n - 1):
            dx1 = self.coords.array_x[i] - self.coords.array_x[i - 1]
            dx2 = self.coords.array_x[i + 1] - self.coords.array_x[i]
            k_eff1 = (self.array_kappa_eff[i] + self.array_kappa_eff[i - 1]) / 2
            k_eff2 = (self.array_kappa_eff[i + 1] + self.array_kappa_eff[i]) / 2
            A = k_eff1 / dx1
            B = k_eff2 / dx2
            diag_elements[i] = -(A + B)
            lower_diag_elements[i - 1] = A
            upper_diag_elements[i] = B
        # set elements for the last row
        k_eff1 = (self.array_kappa_eff[-2] + self.array_kappa_eff[-1]) / 2
        dx1 = self.coords.array_x[-1] - self.coords.array_x[-2]
        diag_elements[-1] = -k_eff1 / dx1
        lower_diag_elements[-1] = k_eff1 / dx1
        m_ = np.diag(diag_elements) + np.diag(upper_diag_elements, 1) + np.diag(lower_diag_elements, -1)
        return m_

    def _vec_phi_e(self, j: npt.ArrayLike, c_e: npt.ArrayLike) -> npt.ArrayLike:
        """
        returns the vector for the matrix form of the  FVM equations.
        :param j: molar lithium-ion flux in the electrode throughout the battery cell.
        :param c_e: array containing the lithium-ion concentration in the electrolyte in the individual fvm nodes.
        :return: column vector for the matrix form of the FVM equations.
        """
        col_vec = np.zeros(self.n)

        if j.ndim == 1:
            j = j.reshape(-1, 1)  # below changes the array containing the flux to the column vector in case row
            # vector in inputted.

        dx = self.coords.array_x[1] - self.coords.array_x[0]
        kappa_D = (self.array_kappa_D_eff[1] + self.array_kappa_D_eff[0]) / 2
        c1 = c_e[0]
        c2 = c_e[1]
        col_vec[0] = (kappa_D / dx) * ((c2 - c1) / (c2 + c1))
        for i in range(1, len(col_vec) - 1):
            dx1 = self.coords.array_x[i] - self.coords.array_x[i - 1]
            dx2 = self.coords.array_x[i + 1] - self.coords.array_x[i]
            kappa_D1 = (self.array_kappa_D_eff[i] + self.array_kappa_D_eff[i - 1]) / 2
            kappa_D2 = (self.array_kappa_D_eff[i + 1] + self.array_kappa_D_eff[i]) / 2
            c1 = c_e[i - 1]
            c2 = c_e[i]
            c3 = c_e[i + 1]
            col_vec[i] = (kappa_D2 / dx2) * ((c3 - c2) / (c3 + c2)) - (kappa_D1 / dx1) * ((c2 - c1) / (c2 + c1))
        # update the last col entry
        dx = self.coords.array_x[-1] - self.coords.array_x[-2]
        kappa_D = (self.array_kappa_D_eff[-2] + self.array_kappa_D_eff[-1]) / 2
        c1 = c_e[-2]
        c2 = c_e[-1]
        col_vec[-1] = -(kappa_D / dx) * ((c2 - c1) / (c2 + c1))
        return 2 * col_vec.reshape(-1, 1) - self.array_a_s.reshape(-1, 1) * Constants.F * j * self.coords.array_dx.reshape(-1,1)

    def solve_phi_e(self, j: np.ndarray, c_e: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        M: np.ndarray = np.linalg.inv(self._m_phi_e())
        b: np.ndarray = self._vec_phi_e(j=j, c_e=c_e)
        array_phi_e: np.ndarray = np.ndarray.flatten(M @ b)
        terminal_phi_e: np.ndarray = self.extrapolate_terminal_potential(array_phi_e=array_phi_e)
        array_rel_phi_e: np.ndarray = array_phi_e - terminal_phi_e
        return terminal_phi_e, array_phi_e, array_rel_phi_e

    def extrapolate_terminal_potential(self, array_phi_e):
        L_tot = self.coords.L_n + self.coords.L_s + self.coords.L_p
        return scipy.interpolate.interp1d(self.coords.array_x, array_phi_e,
                                          fill_value='extrapolate')(L_tot)


class ElectrolytePotentialVolAvgSolver(BaseElectrolytePotentialSolver):
    def __init__(self, L_n: float, L_s: float, L_p: float,
                 kappa_en: float, kappa_es: float, kappa_ep: float,
                 t_c: float):
        self.L_n: float = L_n
        self.L_s: float = L_s
        self.L_p: float = L_p
        self.kappa_en: float = kappa_en
        self.kappa_es: float = kappa_es
        self.kappa_ep: float = kappa_ep
        self.t_c: float = t_c

    def phi_es(self, x: Union[float, np.ndarray],
               c_lin: float, c_lmid: float,
               i_app: float, temp: float) -> Union[float, np.ndarray]:
        return (2 * Constants.R * temp / Constants.F) * (1-self.t_c) * np.log(c_lin/c_lmid) * (i_app / self.kappa_es) * \
               (x - self.L_n - self.L_s/2)

    def phi_lin(self, c_e_in: float, c_e_mid: float,
                i_app: float, temp: float) -> float:
        return (2 * Constants.R * temp / Constants.F) * (1-self.t_c) * np.log(c_e_in/c_e_mid) + \
               i_app * self.L_s / (2 * self.kappa_es)

    def phi_lip(self, c_e_ip: float, c_e_mid: float,
                i_app: float, temp: float) -> float:
        return (2 * Constants.R * temp / Constants.F) * (1 - self.t_c) * np.log(c_e_ip / c_e_mid) - \
               i_app * self.L_s / (2 * self.kappa_es)

    def phi_en(self, L_value: float,
               c_e_mid: float, c_e_n: float, c_e_in: float,
               i_app: float, temp: float) -> float:
        phi_lin: float = self.phi_lin(c_e_in=c_e_in, c_e_mid=c_e_mid, i_app=i_app, temp=temp)
        return phi_lin + (2 * Constants.R * temp / Constants.F) * (1-self.t_c) * np.log(c_e_n/c_e_in) + \
               i_app * (self.L_n - L_value) / self.kappa_en - \
               i_app * (self.L_n - L_value) ** 2 / (2*self.L_n*self.kappa_es)

    def phi_ep(self, L_value: float,
               c_e_mid: float, c_e_p: float, c_e_ip: float,
               i_app: float, temp: float) -> float:
        phi_lip: float = self.phi_lip(c_e_ip=c_e_ip, c_e_mid=c_e_mid, i_app=i_app, temp=temp)
        return phi_lip + (2 * Constants.R * temp / Constants.F) * (1-self.t_c) * np.log(c_e_p / c_e_ip) - \
               i_app * (L_value - self.L_n - self.L_s) - \
               i_app * (L_value-self.L_n-self.L_s)**2 / (2*self.L_p*self.kappa_ep)
