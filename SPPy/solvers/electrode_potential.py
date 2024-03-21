"""
Contains the classes and functionalities foe solving for the solid phase electrode potential
"""

__all__ = ["ElectrodePotentialFVMSolver"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by SPPy. All rights reserved."
__status__ = "Deployed"


import numpy as np
import numpy.typing as npt

from SPPy.warnings_and_exceptions.custom_exceptions import InvalidElectrodeType
from SPPy.calc_helpers import constants
from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates


class ElectrodePotentialFVMSolver:
    """
    This solver solves for the solid phase potential across the electrode. It uses the finite volume method (FVM)
    as indicated by Han et al. [1].

    In their paper, Han et al. defined the flux in terms of A/m2/s. Here, the relevant equations have been modified
    to refer to flux in terms of mol/m2/s.

    [1] Han, S., Tang, Y., & Khaleghi Rahimian, S. (2021). A numerically efficient method of solving the full-order
    pseudo-2-dimensional (P2D) Li-ion cell model. Journal of Power Sources, 490, 229571.
    https://doi.org/10.1016/J.JPOWSOUR.2021.229571Han, S., Tang, Y., & Khaleghi Rahimian, S. (2021).
    """
    def __init__(self, fvm_coords: ElectrolyteFVMCoordinates,
                 electrode_type: str, a_s: float, sigma_eff: float,
                 ref_potential: float = 0.0) -> None:
        """
        Constructor for the class
        :param fvm_coords:
        :param electrode_type: 'n' for the negative electrode and 'p' for positive electrode
        :param a_s: electrode's specific interfacial area [m2/m3]
        :param sigma_eff: effective conductivity [S/m]
        :param ref_potential: Refers to the potential at the negative electrode/Current Collector interface. Usually set
        to zero.
        """
        self.electrode_type: str = electrode_type
        self.a_s: float = a_s
        self.sigma_eff: float = sigma_eff
        self.ref_potential: float = ref_potential

        if electrode_type == 'n':
            self.coords = fvm_coords.array_x_n
        elif electrode_type == 'p':
            self.coords = fvm_coords.array_x_p

        self.dx = self.coords[1] - self.coords[0]  # this assumes that the spatial co-ordinates are equally spaced

    @classmethod
    def _M_phi_n(cls, n: int) -> npt.ArrayLike:
        # create diagonal elements
        diag_elements = -2 * np.ones(n)
        diag_elements[0] = -3
        diag_elements[-1] = -1
        # create upper diagonal elements
        upper_diag_elements = np.ones(n - 1)
        # create lower diagonal elements
        lower_diag_elements = np.ones(n - 1)
        # create matrix
        m_ = np.diag(diag_elements) + np.diag(upper_diag_elements, 1) + np.diag(lower_diag_elements, -1)
        return m_

    @classmethod
    def _M_phi_p(cls, n: int) -> npt.ArrayLike:
        # create diagonal elements
        diag_elements = -2 * np.ones(n)
        diag_elements[0] = -1
        diag_elements[-1] = -3
        # create upper diagonal elements
        upper_diag_elements = np.ones(n - 1)
        # create lower diagonal elements
        lower_diag_elements = np.ones(n - 1)
        # create matrix
        m_ = np.diag(diag_elements) + np.diag(upper_diag_elements, 1) + np.diag(lower_diag_elements, -1)
        return m_

    @property
    def _M_phi_s(self) -> npt.ArrayLike:
        n = self.coords.shape[0]  # the size of the rows and columns of the square matrix
        if self.electrode_type == 'n':
            return ElectrodePotentialFVMSolver._M_phi_n(n=n)
        elif self.electrode_type == 'p':
            return ElectrodePotentialFVMSolver._M_phi_p(n=n)
        else:
            raise InvalidElectrodeType

    def _array_V(self, terminal_potential: float = 0.0) -> npt.ArrayLike:
        array_v_ = np.zeros(self.coords.shape[0])
        if self.electrode_type == 'n':
            array_v_[0] = self.ref_potential
        elif self.electrode_type == 'p':
            array_v_[-1] = terminal_potential
        return array_v_.reshape(-1, 1)

    def _array_j(self, j: npt.ArrayLike) -> npt.ArrayLike:
        """
        returns the column vector for the FVM solver
        :param j: row or column vector containing the molar flux [mol m-2 s-1]
        :return: column vector with values in the units of V
        """
        if j.ndim == 1:
            j = j.reshape(-1, 1)
        return self.a_s * constants.Constants.F * (self.dx ** 2) * j / self.sigma_eff

    def solve_phi_s(self, j: npt.ArrayLike, terminal_potential: float = 0.0) -> npt.ArrayLike:
        vec = self._array_j(j=j) - 2 * self._array_V(terminal_potential=terminal_potential)
        inv_matrix = np.linalg.inv(self._M_phi_s)
        return inv_matrix@vec
