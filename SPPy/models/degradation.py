"""
Contains the functionalities to conduct battery cell degradation equations.
"""

__all__ = ["ROMSEI"]

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'


import numpy as np

from SPPy.models.battery import SPM
from SPPy.calc_helpers.constants import Constants


class ROMSEI:
    """
    This class contains the equations for the reduced order SEI growth model as mentioned in ref [1], with slight
    modifications.

    Literature Reference:
    1. Randell et al. "Controls oriented reduced order modeling of solid-electrolyte interphase layer growth". 2012.
    Journal of Power Sources. Vol: 209. pgs: 282-288.
    """

    @classmethod
    def calc_j_0_i(cls, k: float, c_s_max: float, c_e: float, soc: float) -> float:
        """
        Calculates the exchange lithium ion flux density [mol/m2/s]
        :param k: rate of reaction at the negative electrode [m2.5/mol-0.5/s]
        :param c_s_max: max. lithium concentration at the negative electrode [mol/m3]
        :param c_e: electrolyte concentration [mol/m3]
        :param soc: negative electrode SOC
        :return: (float) exchange current density [mol/m2/s]
        """
        return k * c_s_max * (c_e ** 0.5) * ((1-soc) ** 0.5) * soc ** 0.5

    @classmethod
    def calc_j_tot(cls, I: float, S: float) -> float:
        return SPM.molar_flux_electrode(I=I, S=S, electrode_type='n')

    @classmethod
    def calc_j_i(cls, j_tot: float, j_s: float) -> float:
        return j_tot - j_s

    @classmethod
    def calc_eta_n(cls, temp: float, j_i: float, j_0_i: float) -> float:
        """
        Calculates and returns the surface over-potential [V] of the intercalation reaction.
        :param temp: Electrode temperature [K]
        :param j_i: intercalation flux [mol/m2/s]
        :param j_0_i: intercalation reaction exchange current [mol/m2/s]
        :return: (float) intercalation reaction surface over-potential [V]
        """
        return (2 * Constants.R * temp / Constants.F) * (np.arcsinh(j_i /(2 * j_0_i)))

    @classmethod
    def calc_eta_s(cls, eta_n: float, ocp_n: float, ocp_s: float) -> float:
        """
        Calculates and returns the side-reaction electrode surface over-potential [V]
        :param eta_n: intercalation reaction over-potential [V]
        :param ocp_n: open-circuit potential of the electrode [V
        :param ocp_s: reference potential of the SEI side reaction [V]
        :return:
        """
        return eta_n + ocp_n - ocp_s

    @classmethod
    def calc_j_s(cls, temp: float, j_0_s: float, eta_s: float) -> float:
        """
        Calculates and returns the side-reaction flux [mol/m2/s]
        :param temp: Electrode temperature [K]
        :param j_0_s: side reaction exchange current density [mol/m2/s]
        :param eta_s: side reaction surface over-potential [V]
        :return: (float) side reaction flux [mol/m2/s]
        """
        return -j_0_s * np.exp(-Constants.F * eta_s / (2 * Constants.R * temp))

    @classmethod
    def flux_to_current(cls, molar_flux: float, S: float) -> float:
        """
        Converts molar flux [mol/m2/s] to current [A].
        :param molar_flux: molar lithium-ion flux [mol/m2/s]
        :param S: (float) electrode electrochemically active area [m2]
        :return: current [A]
        """
        return SPM.flux_to_current(molar_flux=molar_flux, S=S, electrode_type='n')