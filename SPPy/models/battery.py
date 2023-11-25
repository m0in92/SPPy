__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'

from typing import Union

import numpy as np
import numpy.typing as npt
import scipy

from SPPy.calc_helpers.constants import Constants
from SPPy.warnings_and_exceptions.custom_exceptions import InvalidElectrodeType


class SPM:
    """
    This class contains the methods for calculating the molar lithium flux, cell terminal voltage according to the
    single particle model.
    """

    @classmethod
    def molar_flux_electrode(cls, I: float, S: float, electrode_type: str) -> float:
        """
        Calculates the model lithium-ion flux [mol/m2/s] into the electrodes.
        :param I: (float) Applied current [A]
        :param S: (float) electrode electrochemically active area [m2]
        :param electrode_type: (str) positive electrode ('p') or negative electrode ('n')
        :return: (float) molar flux [mol/m2/s]
        """
        if electrode_type == 'p':
            return I / (Constants.F * S)
        elif electrode_type == 'n':
            return -I / (Constants.F * S)
        else:
            raise InvalidElectrodeType

    @staticmethod
    def flux_to_current(molar_flux: float, S: float, electrode_type: str) -> float:
        """
        Converts molar flux [mol/m2/s] to current [A].
        :param molar_flux: molar lithium-ion flux [mol/m2/s]
        :param S: (float) electrode electrochemically active area [m2]
        :param electrode_type: (str) positive electrode ('p') or negative electrode ('n')
        :return: (float) current [A]
        """
        if electrode_type == 'p':
            return molar_flux * Constants.F * S
        elif electrode_type == 'n':
            return -molar_flux * Constants.F * S
        else:
            raise InvalidElectrodeType

    @staticmethod
    def m(I, k, S, c_max, SOC, c_e) -> float:
        return I / (Constants.F * k * S * c_max * (c_e ** 0.5) * ((1 - SOC) ** 0.5) * (SOC ** 0.5))

    @staticmethod
    def calc_cell_terminal_voltage(OCP_p, OCP_n, m_p, m_n, R_cell, T, I) -> float:
        V = OCP_p - OCP_n
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        V += I * R_cell
        return V

    def __call__(self, OCP_p, OCP_n, R_cell,
                 k_p, S_p, c_smax_p, SOC_p,
                 k_n, S_n, c_smax_n, SOC_n,
                 c_e,
                 T, I_p_i, I_n_i) -> float:
        """
        Calculates the cell terminal voltage.
        :param OCP_p: Open-circuit potential of the positive electrode [V]
        :param OCP_n: Open-circuit potential of the negative electrode [V]
        :param R_cell: Battery cell ohmic resistance [ohms]
        :param k_p: positive electrode rate constant [m2 mol0.5 / s]
        :param S_p:  positive electrode electro-active area [mol/m2]
        :param c_smax_p: positive electrode max. lithium conc. [mol]
        :param SOC_p: positive electrode SOC
        :param k_n: negative electrode rate constant [m2 mol0.5 / s]
        :param S_n: negative electrode electrochemical active area [m2/mol]
        :param c_smax_n: negative electrode max. lithium conc. [mol]
        :param SOC_n: negative electrode SOC
        :param c_e: electrolyte conc. [mol]
        :param T: Battery cell temperature [K]
        :param I_p_i: positive electrode intercalation applied current [A]
        :param I_n_i: negative electrode intercalation applied current [A]
        :return: Battery cell terminal voltage [V]
        """
        m_p = self.m(I=I_p_i, k=k_p, S=S_p, c_max=c_smax_p, SOC=SOC_p, c_e=c_e)
        m_n = self.m(I=I_n_i, k=k_n, S=S_n, c_max=c_smax_n, SOC=SOC_n, c_e=c_e)
        return self.calc_cell_terminal_voltage(OCP_p=OCP_p, OCP_n=OCP_n, m_p=m_p, m_n=m_n, R_cell=R_cell, T=T, I=I_p_i)


class SPMe:
    """
    This class contains the methods to calculate the molar ionic flux in the electrode regions and the cell terminal
    voltage as expressed in the SPMe model [1].

    Reference:
    [1] S. J. Moura, F. B. Argomedo, R. Klein, A. Mirtabatabaei and M. Krstic,
    "Battery State Estimation for a Single Particle Model With Electrolyte Dynamics,"
    in IEEE Transactions on Control Systems Technology, vol. 25, no. 2, pp. 453-468, March 2017,
    doi: 10.1109/TCST.2016.2571663.
    """

    @classmethod
    def molar_flux_electrode(cls, I: float, S: float, electrode_type: str) -> float:
        """
        Returns the area molar flux entering/exiting the electrode surface [mol/m2/s]
        :param I:
        :param S:
        :param electrode_type:
        :return:
        """
        if electrode_type == 'p':
            return I / (Constants.F * S)
        elif electrode_type == 'n':
            return -I / (Constants.F * S)
        else:
            raise InvalidElectrodeType

    @classmethod
    def a_s(cls, epsilon: float, R: float) -> float:
        """
        Calculates the electrode's interfacial surface area [m2/m3]
        :param epsilon: active material volume fraction
        :param R: radius of the electrode particle
        :return: (float) electrode's interfacial surface area [m2/m3]
        """
        return 3 * epsilon / R

    @classmethod
    def i_0(cls, k: float, c_s_max: float, c_e: float, soc_surf: float) -> float:
        """
        Calculates the exchange current density for an electrode.
        :param k: rate constant [m2.5 / mol0.5 / s]
        :param c_s_max: max. lithium-ion electrode conc. [mol/m3]
        :param c_e: lithium-ion conc in the electrolyte [mol/m3]
        :param SOC_surf: state-of-charge of the electrode particle surface
        :return: (float) exchange current density [mol/m2/s]
        """
        return k * c_s_max * (c_e ** 0.5) * ((1 - soc_surf) ** 0.5) * (soc_surf ** 0.5)

    @classmethod
    def eta(cls, temp, j: float, i_0_: float) -> float:
        """
        Returns the overpotential of the electrode surface
        :param temp: electrode temperature
        :param j: molar flux [mol/m2/s]
        :param i_0_: exchange current density [mol/m2/s]
        :return:
        """
        return (2 * Constants.R * temp / Constants.F) * np.arcsinh(j / (2 * i_0_))

    @classmethod
    def calc_terminal_voltage(cls, ocp_p: float, ocp_n: float, eta_p: float, eta_n: float,
                              l_p: float, l_sep: float, l_n: float, battery_cross_area: float,
                              kappa_eff_avg: float, k_f_avg: float, t_c: float,
                              R_p: float, R_n: float,
                              S_n: float, S_p: float,
                              c_e_n: float, c_e_p: float,
                              temp: float, i_app: float):
        k_conc = (2 * Constants.R * temp / Constants.F) * (1 - t_c) * k_f_avg

        term_v = eta_p - eta_n + ocp_p - ocp_n
        term_v -= (R_p / (S_p) + R_n / (S_n)) * i_app
        term_v += (l_p + 2 * l_sep + l_n) * i_app / (2 * kappa_eff_avg * battery_cross_area)
        term_v += k_conc * (np.log(c_e_p) - np.log(c_e_n))
        return term_v


class P2DM:
    """
    Contains class methods that calculate the general equations pertaining to the P2D Model.
    """

    @classmethod
    def a_s(cls, epsilon, r) -> float:
        """
        Calculates the specific interfacial surface area [m] of an solid electrode phase
        :param epsilon: Volume fraction of the active material in the solid electrode phase
        :param r: the radius of the electrode particle [m]
        :return: (float) specific interfacial surface area [m]
        """
        return 3 * epsilon / r

    @classmethod
    def i_0(cls, k: Union[float, npt.ArrayLike],
            c_s_surf: Union[float, npt.ArrayLike], c_s_max: float,
            c_e: Union[float, npt.ArrayLike],
            c_e_0: Union[float, npt.ArrayLike]) -> Union[float, npt.ArrayLike]:
        return Constants.F * k * ((c_s_max - c_s_surf) ** 0.5) * (c_s_surf ** 0.5) * (c_e / c_e_0) ** 0.5

    @classmethod
    def v_n_minus_v_e(cls, array_i_0_n: npt.ArrayLike, array_eta_rel_n: npt.ArrayLike, array_coord_n: npt.ArrayLike,
                      i_app: float, temp: float, a_s_n: float, cell_area: float, L_n: float) -> npt.ArrayLike:
        func_i_0 = scipy.interpolate.interp1d(array_coord_n, array_i_0_n, fill_value='extrapolate')
        func_rel_eta_n = scipy.interpolate.interp1d(array_coord_n, array_eta_rel_n, fill_value='extrapolate')

        def func_integrand1(x) -> float:
            return func_i_0(x) * np.exp(Constants.F * func_rel_eta_n(x) / (2 * Constants.R * temp))

        def func_integrand2(x: float) -> float:
            return func_i_0(x) * np.exp(-Constants.F * func_rel_eta_n(x) / (2 * Constants.R * temp))

        coeff = 2 * Constants.R * temp / Constants.F  # coefficient
        term1 = -i_app / cell_area
        term2 = a_s_n * scipy.integrate.quad(func_integrand1, 0, L_n)[0]
        term3 = a_s_n * scipy.integrate.quad(func_integrand2, 0, L_n)[0]
        return coeff * np.log((term1 + (term1 ** 2 + (4 * term2 * term3)) ** 0.5) / (2 * a_s_n * term2))

    @classmethod
    def v_p_minus_v_e(cls, array_i_0_p: npt.ArrayLike, array_eta_rel_p: npt.ArrayLike, array_coord_p: npt.ArrayLike,
                      i_app: float, temp: float, a_s_p: float, cell_area: float, L_p_0: float, L_p: float):
        func_i_0_p = scipy.interpolate.interp1d(array_coord_p, array_i_0_p, fill_value='extrapolate')
        func_eta_rel_p = scipy.interpolate.interp1d(array_coord_p, array_eta_rel_p, fill_value='extrapolate')

        def integrand1(x: float) -> float:
            return func_i_0_p(x) * np.exp(Constants.F * func_eta_rel_p(x) / (2 * Constants.R * temp))

        def integrand2(x: float) -> float:
            return func_i_0_p(x) * np.exp(-Constants.F * func_eta_rel_p(x) / (2 * Constants.R * temp))

        coeff = 2 * Constants.R * temp / Constants.F
        term1 = -i_app / cell_area
        term2 = a_s_p * scipy.integrate.quad(func=integrand1, a=L_p_0, b=L_p)[0]
        term3 = a_s_p * scipy.integrate.quad(func=integrand2, a=L_p_0, b=L_p)[0]
        return coeff * np.log((term1 + (term1**2 + 4*term2*term3)**0.5) / (2 * a_s_p * term2))

    @classmethod
    def v_p(cls):
        pass

    @classmethod
    def calc_eta_from_rel_eta(cls, rel_eta: npt.ArrayLike, v_terminal: float, v_terminal_e: float) -> npt.ArrayLike:
        return rel_eta + v_terminal - v_terminal_e

    @classmethod
    def calc_j_from_BV(cls, i_0: Union[float, npt.ArrayLike], eta: Union[float, npt.ArrayLike],
                       temp: float) -> Union[float, npt.ArrayLike]:
        exp_term = 0.5 * Constants.F * eta / (Constants.R * temp)
        return (i_0/Constants.F) * (np.exp(exp_term) - np.exp(-exp_term))
