""" parameters_set
Contains the classes and functionality for the extracting battery cell parameters
"""

__all__ = ['ParameterSets', 'ECMParameterSets']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights reserved'
__status__ = 'deployed'


from typing import Optional, Callable
import importlib

import pandas as pd

from SPPy.config.definations import *


class ParameterSets:
    PARAMETER_SET_DIR = PARAMETER_SET_DIR  # directory to the parameter_sets folder

    def __init__(self, name: str):
        # below checks if the inputted name is available in the parameter sets.
        if not self._check_parameter_set(name):
            raise ValueError(f"{name} not found in the existing parameter_set")

        self.name = name  # name of the parameter set

        self.POSITIVE_ELECTRODE_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_pos-electrode.csv')
        self.NEGATIVE_ELECTRODE_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_neg-electrode.csv')
        self.ELECTROLYTE_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_electrolyte.csv')
        self.BATTERY_CELL_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_battery-cell.csv')

        # Positive electrode parameters are extracted below
        df = ParameterSets._parse_csv(file_path=self.POSITIVE_ELECTRODE_DIR)  # Read and parse the csv file.
        self.L_p = df['Electrode Thickness [m]']
        self.A_p = df['Electrode Area [m^2]']
        self.kappa_p = df['Ionic Conductivity [S m^-1]']
        self.epsilon_p = df['Volume Fraction']
        self.max_conc_p = df['Max. Conc. [mol m^-3]']
        self.R_p = df['Radius [m]']
        self.S_p = df['Electroactive Area [m^2]']
        self.T_ref_p = df['Reference Temperature [K]']
        self.D_ref_p = df['Reference Diffusitivity [m^2 s^-1]']
        self.k_ref_p = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        self.Ea_D_p = df['Activation Energy of Diffusion [J mol^-1]']
        self.Ea_R_p = df['Activation Energy of Reaction [J mol^-1]']
        self.alpha_p = df['Anodic Transfer Coefficient']
        self.brugg_p = df['Bruggerman Coefficient']
        self.soc_min_p = df['soc_min']
        self.soc_max_p = df['soc_max']

        # Negative electrode parameters are extracted below
        df = ParameterSets._parse_csv(file_path=self.NEGATIVE_ELECTRODE_DIR)  # Read and parse the csv file.
        self.L_n = df['Electrode Thickness [m]']
        self.A_n = df['Electrode Area [m^2]']
        self.kappa_n = df['Ionic Conductivity [S m^-1]']
        self.epsilon_n = df['Volume Fraction']
        self.max_conc_n = df['Max. Conc. [mol m^-3]']
        self.R_n = df['Radius [m]']
        self.S_n = df['Electroactive Area [m^2]']
        self.T_ref_n = df['Reference Temperature [K]']
        self.D_ref_n = df['Reference Diffusitivity [m^2 s^-1]']
        self.k_ref_n = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        self.Ea_D_n = df['Activation Energy of Diffusion [J mol^-1]']
        self.Ea_R_n = df['Activation Energy of Reaction [J mol^-1]']
        self.alpha_n = df['Anodic Transfer Coefficient']
        self.brugg_n = df['Bruggerman Coefficient']
        self.soc_min_n = df['soc_min']
        self.soc_max_n = df['soc_max']
        # SEI parameters for the negative electrode are extracted below
        self.U_s = df['SEI Reference Overpotential [V]']
        self.i_s = df['SEI Exchange Current Density [mol m^-2 s^-1]']
        self.MW_SEI = df['SEI Molar Weight [kg mol^-1]']
        self.rho_SEI = df['SEI Density [kg m^-3]']
        self.kappa_SEI = df['SEI Conductivity [S m^-1]']  # SEI conductivity [S/m]

        # Below extracts electrolyte parameters
        df = ParameterSets._parse_csv(file_path=self.ELECTROLYTE_DIR)
        self.conc_es = df['Conc. [mol m^-3]']
        self.L_es = df['Thickness [m]']
        self.kappa_es = df['Ionic Conductivity [S m^-1]']
        self.epsilon_es = df['Volume Fraction']
        self.brugg_es = df['Bruggerman Coefficient']

        # Below extracts the battery cell parameters
        df = ParameterSets._parse_csv(file_path=self.BATTERY_CELL_DIR)
        self.rho = df['Density [kg m^-3]']
        self.Vol = df['Volume [m^3]']
        self.C_p = df['Specific Heat [J K^-1 kg^-1]']
        self.h = df['Heat Transfer Coefficient [J s^-1 K^-1]']
        self.A = df['Surface Area [m^2]']
        self.cap = df['Capacity [A hr]']
        self.V_max = df['Maximum Potential Cut-off [V]']
        self.V_min = df['Minimum Potential Cut-off [V]']

        func_module = importlib.import_module(f'parameter_sets.{self.name}.funcs')  # imports the python module
        # containing the OCP related funcs in the parameter set.
        self.OCP_ref_p_ = func_module.OCP_ref_p
        self.dOCPdT_p_ = func_module.dOCPdT_p
        self.OCP_ref_n_ = func_module.OCP_ref_n
        self.dOCPdT_n_ = func_module.dOCPdT_n

        # containing the electrolyte related fuctions in the parameter set below.
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

