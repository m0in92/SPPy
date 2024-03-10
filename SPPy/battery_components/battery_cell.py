""" battery_cell
contains the class and functionality for the battery cell objects
"""

__all__ = ['BatteryCell', 'ECMBatteryCell', 'ParameterSets']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved.'
__status__ = 'deployed'

import sys
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import numpy.typing as npt
import scipy

from SPPy.calc_helpers import constants
from SPPy.battery_components.parameter_set_manager import ParameterSets, ECMParameterSets
from SPPy.battery_components import electrolyte, electrode

# Below checks for the Python3 version and imports the relevant packages for the type hinting. Note that the keyword
# Self was introduced in Python3.11
PYTHON_MAIN_VERSION = sys.version_info[0]
PYTHON_MINOR_VERSION = sys.version_info[1]
if PYTHON_MINOR_VERSION >= 11:
    from typing import Self
else:
    from typing_extensions import Self


@dataclass
class BatteryCell:
    T_: float  # battery cell temperature, K
    rho: float  # battery density (mostly for thermal modelling), kg/m3
    Vol: float  # battery cell volume, m3
    C_p: float  # specific heat capacity, J / (K kg)
    h: float  # heat transfer coefficient, J / (S K)
    A: float  # surface area, m2
    cap: float  # capacity, Ah
    V_max: float  # maximum potential
    V_min: float  # minimum potential

    elec_p: electrode.PElectrode  # electrode class object
    elec_n: electrode.NElectrode  # electrode class object
    electrolyte: electrolyte.Electrolyte  # electrolyte class object

    def __post_init__(self):
        # self.T_ = self.T
        self.T_amb_ = self.T  # initial condition
        # initialize internal cell resistance
        self.R_cell = (self.elec_p.L / self.elec_p.kappa_eff + self.electrolyte.L / self.electrolyte.kappa_sep_eff + \
                       self.elec_n.L / self.elec_n.kappa_eff) / self.elec_n.A
        self.R_cell_init = self.R_cell

    @property
    def T(self) -> float:
        """
        Represents the lumped battery cell temperature [K]
        :return: Lumped battery cell temperature [K]
        """
        return self.T_

    @T.setter
    def T(self, new_T):
        self.T_ = new_T
        self.elec_p.T = new_T
        self.elec_n.T = new_T

    @property
    def T_amb(self):
        return self.T_amb_

    @classmethod
    def read_from_parametersets(cls, parameter_set_name: str,
                                soc_init_p: float, soc_init_n: float,
                                temp_init: float) -> Self:
        param_set = ParameterSets(name=parameter_set_name)
        rho = param_set.rho
        Vol = param_set.Vol
        C_p = param_set.C_p
        h = param_set.h
        A = param_set.A
        cap = param_set.cap
        V_max = param_set.V_max
        V_min = param_set.V_min
        # initialize electrodes and electrolyte
        # soc_init_p, soc_init_n = BatteryCell._get_electrode_soc_from_lib_soc(soc_lib=soc_lib_init,
        #                                                                      soc_p_min=param_set.soc_min_p,
        #                                                                      soc_p_max=param_set.soc_max_p,
        #                                                                      soc_n_min=param_set.soc_min_n,
        #                                                                      soc_n_max=param_set.soc_max_n)
        obj_elec_p = electrode.PElectrode(L=param_set.L_p, A=param_set.A_p, kappa=param_set.kappa_p,
                                          epsilon=param_set.epsilon_p, S=param_set.S_p, max_conc=param_set.max_conc_p,
                                          R=param_set.R_p, k_ref=param_set.k_ref_p, D_ref=param_set.D_ref_p,
                                          Ea_R=param_set.Ea_R_p, Ea_D=param_set.Ea_D_p, alpha=param_set.alpha_p,
                                          T_ref=param_set.T_ref_p, brugg=param_set.brugg_p,
                                          func_OCP=param_set.OCP_ref_p_, func_dOCPdT=param_set.dOCPdT_p_,
                                          SOC_init=soc_init_p, soc_min=param_set.soc_min_p, soc_max=param_set.soc_max_p,
                                          T=temp_init)
        obj_elec_n = electrode.NElectrode(L=param_set.L_n, A=param_set.A_n, kappa=param_set.kappa_n,
                                          epsilon=param_set.epsilon_n, S=param_set.S_n, max_conc=param_set.max_conc_n,
                                          R=param_set.R_n, k_ref=param_set.k_ref_n, D_ref=param_set.D_ref_n,
                                          Ea_R=param_set.Ea_R_n, Ea_D=param_set.Ea_D_n, alpha=param_set.alpha_n,
                                          T_ref=param_set.T_ref_n,
                                          brugg=param_set.brugg_n,
                                          func_OCP=param_set.OCP_ref_n_, func_dOCPdT=param_set.dOCPdT_n_,
                                          U_s=param_set.U_s, i_s=param_set.i_s, MW_SEI=param_set.MW_SEI,
                                          rho_SEI=param_set.rho_SEI, kappa_SEI=param_set.kappa_SEI,
                                          SOC_init=soc_init_n, soc_min=param_set.soc_min_n, soc_max=param_set.soc_max_n,
                                          T=temp_init)
        obj_electrolyte = electrolyte.Electrolyte(L=param_set.L_es, conc=param_set.conc_es, kappa=param_set.kappa_es,
                                                  epsilon_sep=param_set.epsilon_es, brugg=param_set.brugg_es)

        return cls(T_=temp_init, rho=rho, Vol=Vol, C_p=C_p, h=h, A=A, cap=cap, V_max=V_max, V_min=V_min,
                   elec_p=obj_elec_p, elec_n=obj_elec_n, electrolyte=obj_electrolyte)

    @classmethod
    def _get_electrode_soc_from_lib_soc(cls, soc_lib: float,
                                        soc_p_min: float, soc_p_max: float,
                                        soc_n_min: float, soc_n_max: float) -> tuple[float, float]:
        SOC_LIB_MIN: float = 0.0  # it is assumed that the min SOC_LIB is 0.0
        SOC_LIB_MAX: float = 1.0  # it is assumed that the max SOC_LIB is 1.0

        array_soc_lib: npt.ArrayLike = np.linspace(SOC_LIB_MIN, SOC_LIB_MAX)
        array_soc_p: npt.ArrayLike = np.flip(np.linspace(soc_p_min, soc_p_max))
        array_soc_n: npt.ArrayLike = np.linspace(soc_n_min, soc_n_max)

        # below is the interpolation of soc_lib with the electrode socs
        func_ocp_p: Callable = scipy.interpolate.interp1d(array_soc_lib, array_soc_p)
        func_ocp_n: Callable = scipy.interpolate.interp1d(array_soc_lib, array_soc_n)

        return func_ocp_p(soc_lib), func_ocp_n(soc_lib)


@dataclass
class ECMBatteryCell:
    R0_ref: float  # resistance value of R0 [ohm]
    R1_ref: float  # resistance value of R1 [ohm]
    C1: float  # capacitance of capacitor in RC circuit [ohm]
    temp_ref: float  # reference temperature for R0_ref and R1_ref
    Ea_R0: float  # activation energy for R0 [J/mol]
    Ea_R1: float  # activation energy for R1 [J/mol]

    rho: float  # battery density (mostly for thermal modelling), kg/m3
    vol: float  # battery cell volume, m3
    c_p: float  # specific heat capacity, J / (K kg)
    h: float  # heat transfer coefficient, J / (S K)
    area: float  # surface area, m2
    cap: float  # capacity, Ah
    v_max: float  # maximum potential
    v_min: float  # minimum potential

    soc_init: float  # initial SOC
    temp_init: float  # initial battery cell temperature, K

    func_eta: Callable  # func for the Columbic efficiency as a func of SOC and temp
    func_ocv: Callable  # func which outputs the battery OCV from its SOC
    func_docvdtemp: Callable  # function which outputs the change of OCV with respect to temperature from its SOC

    # The parameters below relate the dynamic and instantaneous hysteresis
    M_0: Optional[float] = None  # The instantaneous hysteresis co-efficient [V]
    M: Optional[float] = None  # SOC-dependent hysteresis co-efficient [V]
    gamma: Optional[float] = None  # Hysteresis time-constant

    @classmethod
    def read_from_parametersets(cls, parameter_set_name: str, soc_init: float, temp_init: float) -> Self:
        param = ECMParameterSets(name=parameter_set_name)
        return cls(R0_ref=param.R0_ref, R1_ref=param.R1_ref, C1=param.C1, temp_ref=param.temp_ref,
                   Ea_R0=param.Ea_R0,Ea_R1=param.Ea_R1,
                   rho=param.rho, vol=param.rho, c_p=param.c_p, h=param.h, area=param.h, cap=param.cap,
                   v_min=param.v_min, v_max=param.v_max,
                   soc_init=soc_init, temp_init=temp_init,
                   func_eta=param.func_eta, func_ocv=param.func_ocv, func_docvdtemp=param.func_docvdtemp,
                   M_0=param.M_0, M=param.M, gamma=param.gamma)

    def __post_init__(self):
        self.temp_ = self.temp_init
        self.soc_ = self.soc_init

    @property
    def temp(self):
        """
        Represents the current temperature of the battery cell [K]
        :return: (float) current battery cell temperature [K]
        """
        return self.temp_

    @temp.setter
    def temp(self, temp_new: float):
        self.temp_ = temp_new

    @property
    def soc(self):
        """
        Represents the current battery cell SOC
        :return: (float) returns the current battery cell SOC
        """
        return self.soc_

    @soc.setter
    def soc(self, soc_new: float):
        """
        Setter function for the battery cell state-of-charge
        :param soc_new:
        :return:
        """
        self.soc_ = soc_new

    @property
    def R0(self):
        return self.R0_ref * np.exp(-1 * self.Ea_R0 / constants.Constants.R * (1 / self.temp - 1 / self.temp_ref))

    @property
    def R1(self):
        return self.R0_ref * np.exp(-1 * self.Ea_R1 / constants.Constants.R * (1 / self.temp - 1 / self.temp_ref))

    @property
    def docpdtemp(self):
        return self.func_docvdtemp(self.soc)

    @property
    def ocv(self):
        return self.func_ocv(self.soc) + self.docpdtemp * (self.temp - self.temp_ref)

    @property
    def eta(self):
        return self.func_eta(self.soc, self.temp)
