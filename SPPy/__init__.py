"""
Package header for the SPPy namespace
Provides the continuum scale battery cell simulations.
"""

__all__ = ['battery_components', 'calc_helpers', 'config', 'cycler', 'general_OCP', 'models',
           'parameter_estimations', 'solvers', 'sol_and_visualization', 'warnings_and_exceptions']

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'

from SPPy.battery_components.electrode import NElectrode, PElectrode
from SPPy.battery_components.electrolyte import Electrolyte
from SPPy.battery_components.battery_cell import BatteryCell, ECMBatteryCell

from SPPy.solvers.battery_solver import SPPySolver, EnhancedSPSolver
from SPPy.solvers.ecm_solvers import DTSolver, ESCDTSolver, KFDTSolver

from SPPy.cycler.cc import CC, CCCV, CCNoFirstRest, DischargeRestCharge, DischargeRestChargeRest
from SPPy.cycler.charge import Charge, ChargeRest
from SPPy.cycler.discharge import Discharge, DischargeRest, CustomDischarge
from SPPy.cycler.custom import CustomCycler, HPPCCycler

from SPPy.sol_and_visualization.solution import Solution, ECMSolution
from SPPy.sol_and_visualization.plots import Plots

from SPPy.parameter_estimations.procedural import OCVData

from SPPy.calc_helpers.computational_intelligence_algorithms import GA


