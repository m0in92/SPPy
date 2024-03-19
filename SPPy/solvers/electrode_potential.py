import numpy as np
import numpy.typing as npt

from SPPy.warnings_and_exceptions.custom_exceptions import InvalidElectrodeType
from SPPy.calc_helpers import constants
from SPPy.solvers.co_ordinates import FVMCoordinates


class ElectrodePotentialFVMSolver:
    def __init__(self, fvm_coords: FVMCoordinates,
                 electrode_type: str, a_s: float, sigma_eff: float,
                 ref_potential: float = 0.0) -> None:
        self.electrode_type = electrode_type
        self.a_s = a_s
        self.sigma_eff = sigma_eff
        self.ref_potential = ref_potential  # usually set to zero. Refers to the potential at the negative electrode/CC
        # interface.

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
