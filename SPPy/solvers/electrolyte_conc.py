"""
Contains classes for electrolyte solvers.
"""

__all__ = ['ElectrolyteConcFVMSolver']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright by SPPy. All rights reserved."
__status__ = "deployed"


import numpy as np
import numpy.typing as npt
import scipy.interpolate

from SPPy.calc_helpers.matrix_operations import TDMAsolver
from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates


class ElectrolyteConcFVMSolver:
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
    def array_epsilon_e(self) -> npt.ArrayLike:
        """
        Returns an array containing the volume fraction of the electrolyte at each spatial region
        :return:
        """
        array_epsilon_n = self.epsilon_en * np.ones(len(self.co_ords.array_x_n))
        array_epsilon_s = self.epsilon_esep * np.ones(len(self.co_ords.array_x_s))
        array_epsilon_p = self.epsilon_ep * np.ones(len(self.co_ords.array_x_p))
        return np.append(np.append(array_epsilon_n, array_epsilon_s), array_epsilon_p)

    @property
    def array_D_eff(self) -> npt.ArrayLike:
        """
        Returns an array containing the effective electrolyte diffusivity at spatial FVM points.
        :return:
        """
        array_D_eff_n = self.D_e * (self.epsilon_en ** self.brugg) * np.ones(len(self.co_ords.array_x_n))
        array_D_eff_s = self.D_e * (self.epsilon_esep ** self.brugg) * np.ones(len(self.co_ords.array_x_s))
        array_D_eff_p = self.D_e * (self.epsilon_ep ** self.brugg) * np.ones(len(self.co_ords.array_x_p))
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


class ElectrolyteConcROMSolver:
    pass
