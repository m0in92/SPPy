""" electrolyte
Contains the classes and functionality for the electrolyte related object(s).
"""

__all__ = ['Electrolyte']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved'
__status__ = 'deployed'


from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Electrolyte:
    """
    Class for the Electrolyte object and contains the relevant electrolyte parameters.
    """
    L: float  # seperator thickness, m3

    conc: float  # initial electrolyte concentration, mol/m3
    kappa: float  # ionic conductivity, S/m
    brugg: float  # Bruggerman coefficient for electrolyte

    epsilon_n: Optional[float] = None  # electrolyte volume fraction in the negative electrode region
    epsilon_sep: Optional[float] = None  # electrolyte volume fraction in the seperator region
    epsilon_p: Optional[float] = None  # electrolyte volume fraction in the positive electrode region

    t_c: Optional[float] = None  # cationic transference number

    D_e: Optional[float] = None  # electrolyte diffusivity [mol/m3]
    func_D_e: Optional[Callable[[float, float], float]] = None  # function that outputs the electrolyte diffusivity and
    # takes parameters of c_e [mol/m3] and temp [K].
    func_ln_f: Optional[Callable[[float, float], float]] = None  # function representing the (1+dlnf/dlnc_e) that takes
    # the c_e [mol/m3] and temperature [K] parameters.

    def __post_init__(self):
        # Check for types of the input parameters
        if not isinstance(self.conc, float):
            raise "Electrolyte conc. needs to be a float."
        if not isinstance(self.L, float):
            raise "Electrolyte thickness needs to be a float."
        if not isinstance(self.kappa, float):
            raise "Electrolyte conductivity needs to be a float."
        if not isinstance(self.epsilon_sep, float):
            raise "Electrolyte volume fraction needs to be a float."
        if not isinstance(self.brugg, float):
            raise "Electrolyte's bruggerman coefficient needs to be a float."

    @ property
    def kappa_sep_eff(self) -> float:
        """
        Represents the effective electrolyte conductivity [S/m] in the seperator region of the battery cell
        :return: effective electrolyte conductivity [S/m] in the seperator region
        """
        return self.kappa * (self.epsilon_sep ** self.brugg)
