""" parameters_set
Contains the classes and functionality for the extracting battery cell parameters
"""

__all__ = ['ParameterSets', 'ECMParameterSets', 'PydanticParameterSets']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved'
__status__ = 'deployed'


from typing import Optional, Callable
import importlib

import pandas as pd
from pydantic import BaseModel

from SPPy.config.definations import *


class ParameterSets:
    PARAMETER_SET_DIR = PARAMETER_SET_DIR  # directory to the parameter_sets folder

    def __init__(self, name: str):
        # below checks if the inputted name is available in the parameter sets.
        if not self._check_parameter_set(name):
            raise ValueError(f"{name} not found in the existing parameter_set")

        self.name: str = name  # name of the parameter set

        self.POSITIVE_ELECTRODE_DIR: str = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_pos-electrode.csv')
        self.NEGATIVE_ELECTRODE_DIR: str = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_neg-electrode.csv')
        self.ELECTROLYTE_DIR: str = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_electrolyte.csv')
        self.BATTERY_CELL_DIR: str = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_battery-cell.csv')

        # Positive electrode parameters are extracted below
        df = ParameterSets._parse_csv(file_path=self.POSITIVE_ELECTRODE_DIR)  # Read and parse the csv file.
        self.L_p: float = df['Electrode Thickness [m]']
        self.A_p: float = df['Electrode Area [m^2]']
        self.kappa_p: float = df['Ionic Conductivity [S m^-1]']
        self.epsilon_p: float = df['Volume Fraction']
        self.max_conc_p: float = df['Max. Conc. [mol m^-3]']
        self.R_p: float = df['Radius [m]']
        self.S_p: float = df['Electroactive Area [m^2]']
        self.T_ref_p: float = df['Reference Temperature [K]']
        self.D_ref_p: float = df['Reference Diffusitivity [m^2 s^-1]']
        self.k_ref_p: float = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        self.Ea_D_p: float = df['Activation Energy of Diffusion [J mol^-1]']
        self.Ea_R_p: float = df['Activation Energy of Reaction [J mol^-1]']
        self.alpha_p: float = df['Anodic Transfer Coefficient']
        self.brugg_p: float = df['Bruggerman Coefficient']
        self.soc_min_p: float = df['soc_min']
        self.soc_max_p: float = df['soc_max']

        # Negative electrode parameters are extracted below
        df = ParameterSets._parse_csv(file_path=self.NEGATIVE_ELECTRODE_DIR)  # Read and parse the csv file.
        self.L_n: float = df['Electrode Thickness [m]']
        self.A_n: float = df['Electrode Area [m^2]']
        self.kappa_n: float = df['Ionic Conductivity [S m^-1]']
        self.epsilon_n: float = df['Volume Fraction']
        self.max_conc_n: float = df['Max. Conc. [mol m^-3]']
        self.R_n: float = df['Radius [m]']
        self.S_n: float = df['Electroactive Area [m^2]']
        self.T_ref_n: float = df['Reference Temperature [K]']
        self.D_ref_n: float = df['Reference Diffusitivity [m^2 s^-1]']
        self.k_ref_n: float = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        self.Ea_D_n: float = df['Activation Energy of Diffusion [J mol^-1]']
        self.Ea_R_n: float = df['Activation Energy of Reaction [J mol^-1]']
        self.alpha_n: float = df['Anodic Transfer Coefficient']
        self.brugg_n: float = df['Bruggerman Coefficient']
        self.soc_min_n: float = df['soc_min']
        self.soc_max_n: float = df['soc_max']
        # SEI parameters for the negative electrode are extracted below
        self.U_s: float = df['SEI Reference Overpotential [V]']
        self.i_s: float = df['SEI Exchange Current Density [mol m^-2 s^-1]']
        self.MW_SEI: float = df['SEI Molar Weight [kg mol^-1]']
        self.rho_SEI: float = df['SEI Density [kg m^-3]']
        self.kappa_SEI: float = df['SEI Conductivity [S m^-1]']  # SEI conductivity [S/m]

        # Below extracts electrolyte parameters
        df = ParameterSets._parse_csv(file_path=self.ELECTROLYTE_DIR)
        self.conc_es: float = df['Conc. [mol m^-3]']
        self.L_es: float = df['Thickness [m]']
        self.kappa_es: float = df['Ionic Conductivity [S m^-1]']
        self.epsilon_es: float = df['Volume Fraction']
        self.brugg_es: float = df['Bruggerman Coefficient']

        try:
            self.t_c: Optional[float] = df['Cation Transference No.']  # This parameter is NOT used in the single
            # particle model
        except KeyError as e:
            self.t_c: Optional[float] = None
            print("No value found for t_c. Can only perform single particle model.")

        try:
            self.value_D_e: Optional[float] = df['Diffusivity']  # This parameter is NOT used in the single
            # particle model
        except KeyError as e:
            self.value_D_e: Optional[float] = None
            print("No value found for D_e [m2/s]. Can only perform single particle model.")

        try:
            self.epsilon_en: Optional[float] = df['Volume Fraction N']  # This parameter is NOT used in the
            # single particle model
        except KeyError as e:
            self.epsilon_en: Optional[float] = None
            print("No value found for kappa_en. Can only perform single particle model.")

        try:
            self.epsilon_ep: Optional[float] = df['Volume Fraction P']  # This parameter is NOT used in the
            # single particle model
        except KeyError as e:
            self.epsilon_ep: Optional[float] = None
            print("No value found for kappa_pn. Can only perform single particle model.")

        # Below extracts the battery cell parameters
        df = ParameterSets._parse_csv(file_path=self.BATTERY_CELL_DIR)
        self.rho: float = df['Density [kg m^-3]']
        self.Vol: float = df['Volume [m^3]']
        self.C_p: float = df['Specific Heat [J K^-1 kg^-1]']
        self.h: float = df['Heat Transfer Coefficient [J s^-1 K^-1]']
        self.A: float = df['Surface Area [m^2]']
        self.cap: float = df['Capacity [A hr]']
        self.V_max: float = df['Maximum Potential Cut-off [V]']
        self.V_min: float = df['Minimum Potential Cut-off [V]']

        func_module = importlib.import_module(f'parameter_sets.{self.name}.funcs')  # imports the python module
        # containing the OCP related funcs in the parameter set.
        self.OCP_ref_p_: Callable = func_module.OCP_ref_p
        self.dOCPdT_p_: Callable = func_module.dOCPdT_p
        self.OCP_ref_n_: Callable = func_module.OCP_ref_n
        self.dOCPdT_n_: Callable = func_module.dOCPdT_n

        # containing the electrolyte related functions in the parameter set below.
        warning_msg: str = 'No electrolyte related functions found in the parameter set: '
        try:
            self.func_D_e_ = func_module.func_D_e
        except AttributeError as e:
            print(warning_msg, 'D_e')
            self.func_D_e_ = None
        try:
            self.func_kappa_e_ = func_module.func_kappa_e
        except AttributeError as e:
            print(warning_msg, 'kappa_e')
        try:
            self.func_dlnf_ = func_module.func_dlnf
        except AttributeError as e:
            print(warning_msg, '1+dlnf/flnc_e')

    @classmethod
    def list_parameters_sets(cls):
        """
        Returns the list of available parameter sets.
        :return: (list) list of available parameters sets.
        """
        return os.listdir(cls.PARAMETER_SET_DIR)

    @classmethod
    def _check_parameter_set(cls, name) -> bool:
        """
        Checks if the inputted parameter name is in the parameter set. If not available, it raises an exception.
        """
        flag_name_present: bool = False
        if name in cls.list_parameters_sets():
            flag_name_present = True
        return flag_name_present

    @classmethod
    def _parse_csv(cls, file_path):
        """
        reads the csv file and returns a Pandas DataFrame.
        :param file_path: the absolute or relative file drectory of the csv file.
        :return: the dataframe with the column containing numerical values only.
        """
        return pd.read_csv(file_path, index_col=0)["Value"]


class ECMParameterSets:
    """
    Class to collect ECM parameters from the csv file
    """
    PARAMETER_SET_DIR = PARAMETER_SET_ECM_DIR

    def __init__(self, name: str) -> None:
        self.name = name

        file_path: str = os.path.join(ECMParameterSets.PARAMETER_SET_DIR, self.name, 'param.csv')
        df = self._parse_csv(file_path=file_path)
        self.R0_ref: float = df["R0 ref [ohm]"]  # resistance value of R0 [ohm]
        self.R1_ref: float = df['R1_ref [ohm]']  # resistance value of R1 [ohm]
        self.C1: float = df['C1 [F]']  # capacitance of capacitor in RC circuit [ohm]
        self.temp_ref: float = df['temp_ref [K]']  # reference temperature for R0_ref and R1_ref
        self.Ea_R0: float = df['Ea_R0 [J/mol]']  # activation energy for R0 [J/mol]
        self.Ea_R1: float = df['Ea_R1 [J/mol]']  # activation energy for R1 [J/mol]

        self.rho: float = df['rho [kg/m3]']  # battery density (mostly for thermal modelling), kg/m3
        self.vol: float = df['vol [m3]']  # battery cell volume, m3
        self.c_p: float = df['C_p [J/(Kkg)]']  # specific heat capacity, J / (K kg)
        self.h: float = df['h [J/(SK)]'] # heat transfer coefficient, J / (S K)
        self.area: float = df['area [m2]']  # surface area, m2
        self.cap: float = df['cap [Ahr]']  # capacity, Ah
        self.v_max: float = df['V_max [V]']  # maximum potential
        self.v_min: float = df['V_min [V]']  # minimum potential

        # The parameters below relate the dynamic and instantaneous hysteresis
        self.M_0: Optional[float] = df['M_0 [V]']  # The instantaneous hysteresis co-efficient [V]
        self.M: Optional[float] = df['M [V]']  # SOC-dependent hysteresis co-efficient [V]
        self.gamma: Optional[float] = df['gamma']  # Hysteresis time-constant

        func_module = importlib.import_module(f'parameter_sets_ecm.{self.name}.funcs')  # imports the python module
        self.func_eta: Callable = func_module.func_eta  # func for the Columbic efficiency as a func of SOC and temp
        self.func_ocv: Callable = func_module.func_ocv  # func which outputs the battery OCV from its SOC
        self.func_docvdtemp: Callable = func_module.func_docvdtemp  # function which outputs the change of OCV with
        # respect to temperature from its SOC

    @classmethod
    def lst_parameter_names(cls) -> list:
        """
        List containing the ECM parameter names.
        """
        return os.listdir(ECMParameterSets.PARAMETER_SET_DIR)

    @classmethod
    def _parse_csv(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, index_col=0)['Value']


class PydanticParameterSets(BaseModel):
    """
    This classes uses the pydantic Python package with the intended purpose of enforcing data types.
    """

    # class variables pertaining to the positive electrode
    L_p: float
    A_p: float
    kappa_p: float
    epsilon_p: float
    max_conc_p: float
    R_p: float
    S_p: float
    T_ref_p: float
    D_ref_p: float
    k_ref_p: float
    Ea_D_p: float
    Ea_R_p: float
    alpha_p: float
    brugg_p: float
    soc_min_p: float
    soc_max_p: float

    # class variables pertaining to the negative electrode
    L_n: float              # Electrode Thickness [m]
    A_n: float              # Electrode Area [m^2]
    kappa_n: float          # Ionic Conductivity [S m^-1]
    epsilon_n: float        # Volume Fraction
    max_conc_n: float       # Max. Conc. [mol m^-3]
    R_n: float              # Radius [m]
    S_n: float              # Electroactive Area [m^2]
    T_ref_n: float          # Reference Temperature [K]
    D_ref_n: float          # Reference Diffusitivity [m^2 s^-1]
    k_ref_n: float          # Reference Rate Constant [m^2.5 mol^-0.5 s^-1]
    Ea_D_n: float           # Activation Energy of Diffusion [J mol^-1]
    Ea_R_n: float           # Activation Energy of Reaction [J mol^-1]
    alpha_n: float          # Anodic Transfer Coefficient
    brugg_n: float          # Bruggerman Coefficient
    soc_min_n: float        # soc_min
    soc_max_n: float        # soc_max
    # SEI parameters for the negative electrode are extracted below
    U_s: float         # SEI Reference Overpotential [V]
    i_s: float         # SEI Exchange Current Density [mol m^-2 s^-1]
    MW_SEI: float      # SEI Molar Weight [kg mol^-1]
    rho_SEI: float     # SEI Density [kg m^-3]
    kappa_SEI: float   # SEI Conductivity [S m^-1]

    # class variables pertaining to the electrolyte
    conc_es: float      # Conc. [mol m^-3]
    L_es: float         # Thickness [m]
    kappa_es: float     # Ionic Conductivity [S m^-1]
    epsilon_es: float   # Volume Fraction
    brugg_es: float     # Bruggerman Coefficient

    # class variables pertaining to the battery cell
    rho: float      # Density [kg m^-3]
    Vol: float      # Volume [m^3]
    C_p: float      # Specific Heat [J K^-1 kg^-1]
    h: float        # Heat Transfer Coefficient [J s^-1 K^-1]
    A: float        # Surface Area [m^2]
    cap: float      # Capacity [A hr]
    V_max: float    # Maximum Potential Cut-off [V]
    V_min: float    # Minimum Potential Cut-off [V]

    # Open-circuit potential [V] related functions
    OCP_ref_p_: Callable
    dOCPdT_p_: Callable
    OCP_ref_n_: Callable
    dOCPdT_n_: Callable

    def __init__(self, parameter_set_name: str) -> None:
        param_instance: ParameterSets = ParameterSets(parameter_set_name)

        data: dict = {'L_p': param_instance.L_p,
                      'A_p': param_instance.A_p,
                      'kappa_p': param_instance.kappa_p,
                      'epsilon_p': param_instance.epsilon_p,
                      'max_conc_p': param_instance.max_conc_p,
                      'R_p': param_instance.R_p,
                      'S_p': param_instance.S_p,
                      'T_ref_p': param_instance.T_ref_p,
                      'D_ref_p': param_instance.D_ref_p,
                      'k_ref_p': param_instance.k_ref_p,
                      'Ea_D_p': param_instance.Ea_D_p,
                      'Ea_R_p': param_instance.Ea_R_p,
                      'alpha_p': param_instance.alpha_p,
                      'brugg_p': param_instance.brugg_p,
                      'soc_min_p': param_instance.soc_min_p,
                      'soc_max_p': param_instance.soc_max_p,

                      'L_n': param_instance.L_n,
                      'A_n': param_instance.A_n,
                      'kappa_n': param_instance.kappa_n,
                      'epsilon_n': param_instance.epsilon_n,
                      'max_conc_n': param_instance.max_conc_n,
                      'R_n': param_instance.R_n,
                      'S_n': param_instance.S_n,
                      'T_ref_n': param_instance.T_ref_n,
                      'D_ref_n': param_instance.D_ref_n,
                      'k_ref_n': param_instance.k_ref_n,
                      'Ea_D_n': param_instance.Ea_D_n,
                      'Ea_R_n': param_instance.Ea_R_n,
                      'alpha_n': param_instance.alpha_n,
                      'brugg_n': param_instance.brugg_n,
                      'soc_min_n': param_instance.soc_min_n,
                      'soc_max_n': param_instance.soc_max_n,
                      'U_s': param_instance.U_s,
                      'i_s': param_instance.i_s,
                      'MW_SEI': param_instance.MW_SEI,
                      'rho_SEI': param_instance.rho_SEI,
                      'kappa_SEI': param_instance.kappa_SEI,

                      'conc_es': param_instance.conc_es,
                      'L_es': param_instance.L_es,
                      'kappa_es': param_instance.kappa_es,
                      'epsilon_es': param_instance.epsilon_es,
                      'brugg_es': param_instance.brugg_es,

                      'rho': param_instance.rho,
                      'Vol': param_instance.Vol,
                      'C_p': param_instance.C_p,
                      'h': param_instance.h,
                      'A': param_instance.A,
                      'cap': param_instance.cap,
                      'V_max': param_instance.V_max,
                      'V_min': param_instance.V_min,

                      'OCP_ref_p_': param_instance.OCP_ref_p_,
                      'dOCPdT_p_': param_instance.dOCPdT_p_,
                      'OCP_ref_n_': param_instance.OCP_ref_n_,
                      'dOCPdT_n_': param_instance.dOCPdT_n_
                      }
        super().__init__(**data)

