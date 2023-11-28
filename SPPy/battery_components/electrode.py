""" electrode
Contains classes and functionalities for the electrode related objects
"""

__all__ = ['Electrode', 'PElectrode', 'NElectrode']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved'
__status__ = 'deployed'

from typing import Optional
from dataclasses import dataclass, field
import collections

import numpy as np

from SPPy.calc_helpers import constants
from SPPy.warnings_and_exceptions import custom_exceptions


@dataclass
class Electrode:
    """
    This class is used to create an electrode object. This object is used to store the electrode parameters and provide
    relevant electrode methods. It takes input parameters from the csv file. The electrode parameters are stored as
    attributes of the object.
    """
    L: float  # Electrode Thickness [m]
    A: float  # Electrode Area [m^2]
    kappa: float # Ionic Conductivity [S m^-1]
    epsilon: float  # Volume Fraction
    max_conc: float  # Max. Conc. [mol m^-3]
    R: float # Radius [m]
    S: Optional[float]  # Electro-active Area [m2]
    T_ref: float  # Reference Temperature [K]
    D_ref: float  # Reference Diffusivity [m2/s]
    k_ref: float  # Reference Rate Constant [m2.5 / (mol0.5 s)
    Ea_D: float  # Activation Energy of Diffusion [J / mol]
    Ea_R: float  # Activation Energy of Reaction [J / mol]
    alpha: float  # Anodic Transfer Coefficient
    brugg: float  # Bruggerman Coefficient
    SOC_init: float  # initial SOC
    soc_min: float  # min. electrode soc
    soc_max: float  # max. electrode soc
    func_OCP: collections.abc.Callable[[float], [float]] # electrode open-circuit potential function that takes SOC as
    # its arguments
    func_dOCPdT: collections.abc.Callable[[float], [float]] # the function that represents the change of open-curcuit
    # potential with SOC
    T: float # electrode temperature, K
    electrode_type: str = field(default='none')  # electrode type: none, 'p', or 'n'

    def __post_init__(self):
        """
        Electrode class constructor
        :param file_path: file path of the csv containing the electrode parameters. Please adhere to the csv format
        in the data/param_pos-electrode.csv or data/param_neg-electrode.csv file.
        :param SOC_init: state of charge of the electrode and is between 0 and 1.
        :param T: current electrode temperature.
        :param func_OCP: function that describes the OCP of the electrode.
        :param func_dOCPdT: a function that describes the change of OCP with temperature
        """
        if np.isnan(self.S):
            self.S = 3 * self.epsilon * (self.A * self.L) / self.R
        self.kappa_eff = self.kappa * (self.epsilon ** self.brugg)

        # Check if SOC is within the threshold
        if (self.SOC_init <= 0) or (self.SOC_init >= 1):
            raise custom_exceptions.InvalidSOCException(self.electrode_type)
        self.SOC_ = self.SOC_init

        # Check if inputted func_OCP is a function type.
        if not isinstance(self.func_OCP, collections.abc.Callable):
            raise TypeError("func_OCP argument needs to be of a function type.")
        # Check if inputted func_dOCPdt is a function type.
        if isinstance(self.func_dOCPdT, collections.abc.Callable):
            self.func_dOCPdT = self.func_dOCPdT
        else:
            raise TypeError("func_dOCPdT needs to be a None or Function type")

    @property
    def a_s(self) -> float:
        """
        Specific interfacial area [m2/m3]
        :return: (float) specific interfacial area
        """
        return 3 * self.epsilon / self.R

    @property
    def SOC(self):
        return self.SOC_

    @SOC.setter
    def SOC(self, new_SOC):
        if (new_SOC <= 0) or (new_SOC >= 1):
            raise custom_exceptions.InvalidSOCException(self.electrode_type)
        self.SOC_ = new_SOC

    @property
    def D(self):
        return self.D_ref * np.exp(-1 * self.Ea_D / constants.Constants.R * (1 / self.T - 1 / self.T_ref))

    @property
    def k(self):
        return self.k_ref * np.exp(self.Ea_R / constants.Constants.R * (1 / self.T_ref - 1 / self.T))

    @property
    def dOCPdT(self):
        return self.func_dOCPdT(self.SOC)

    @property
    def OCP(self):
        return self.func_OCP(self.SOC) + self.dOCPdT * (self.T - self.T_ref)

    def i_0(self, c_e):
        return self.k * self.max_conc * (c_e ** 0.5) * ((1 - self.SOC)**0.5) * (self.SOC ** 0.5)


@dataclass
class PElectrode(Electrode):
    """
    This class is used to create a Positive electrode object. This object is used to store the electrode parameters and
    provide relevant electrode methods. It inherits from the Electrode class.
    """
    def __post_init__(self):
        super().__post_init__()
        self.electrode_type = 'p'


@dataclass
class NElectrode(Electrode):
    """
    This class is used to create a Negative electrode object. This object is used to store the electrode parameters and
    provide relevant electrode methods. It inherits from the Electrode class.
    """
    U_s: float = field(default=0.0)  # the OCP of the SEI reaction [V]
    i_s: float = field(default=0.0)  # exchange current density of the SEI reaction [A/m2]
    MW_SEI: float = field(default=0.0)  # SEI film average molecular weight [kg/mol]
    rho_SEI: float = field(default=0.0)  # SEI film density [kg/m3]
    kappa_SEI: float = field(default=0.0)  # SEI conductivity [S/m]

    def __post_init__(self):
        super().__post_init__()
        self.electrode_type = 'n'
