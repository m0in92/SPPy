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
    def calc_c_n(self, k_n: float, c_nmax: float, c_e: float, SOC_surf_n: float):
        """
        Calculates the exchange lithium ion flux density [mol/m2/s]
        :param k_n: rate of reaction at the negative electrode [m2.5/mol-0.5/s]
        :param c_nmax: max. lithium concentration at the negative electrode [mol/m3]
        :param c_e: electrolyte concentration [mol/m3]
        :param SOC_surf_n: negative electrode SOC
        :return: (float) exchange current density [mol/m2/s]
        """
        return k_n * c_nmax * (c_e ** 0.5) * ((1-SOC_surf_n) ** 0.5) * (SOC_surf_n) ** 0.5

    def calc_j_tot(self, I: float, S: float):
        return SPM.molar_flux_electrode(I=I, S=S, electrode_type='n')

    def calc_j_i(self, j_tot: float, j_s: float):
        return j_tot - j_s

    def calc_eta_n(self, temp: float, j_i: float, c_n: float):
        return (2 * Constants.R * temp / Constants.F) * (np.arcsinh(j_i /(2 * c_n)))

    def calc_eta_s(self, eta_n: float, OCP_n: float, OCP_s: float):
        return eta_n + OCP_n + OCP_s  # TODO: this expression is incorrent. Needs another view

    def calc_j_s(self, temp: float, i_s: float, eta_s: float):
        return -i_s * np.exp(-Constants.F * eta_s / (2 * Constants.R * temp))

    def flux_to_current(self, molar_flux: float, S: float):
        """
        Converts molar flux [mol/m2/s] to current [A].
        :param molar_flux: molar lithium-ion flux [mol/m2/s]
        :param S: (float) electrode electrochemically active area [m2]
        :return: current [A]
        """
        return SPM.flux_to_current(molar_flux=molar_flux, S=S, electrode_type='n')