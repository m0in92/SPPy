"""
Contains the functionality to render the html containing the simulations results. However, index(request) just renders
the homepage.
"""

__all__ = ['index', 'get_simulation_inputs', 'perform_simulation']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by SPPy. All rights reserved."
__status__ = "developement"

from typing import Optional, Any

from django.shortcuts import render
from django.http import HttpResponse

from django_app.forms import ECMSimulationVariables, SPSimulationVariables

import SPPy
from SPPy.calc_helpers.constants import Constants

from .models import SpModel

def index(request) -> HttpResponse:
    return render(request=request, template_name='index.html',
                  context={'context_package': {}})


def ecm(request) -> HttpResponse:
    t_sim, v_sim, soc_lib, temp_sim = [], [], [], []
    if request.method == "POST":
        form = ECMSimulationVariables(request.POST)
        if form.is_valid():
            t_sim, v_sim, soc_lib, temp_sim = Simulator(battery_model='ECM').get_simulation_results(request=request)
    else:
        form = ECMSimulationVariables()

    return render(request=request, template_name='index.html', context={'context_package': {'form': form,
                                                                                            't_sim': t_sim,
                                                                                            'v_sim': v_sim,
                                                                                            'soc_lib': soc_lib,
                                                                                            'temp_sim': temp_sim}})


def sp(request) -> HttpResponse:
    t_sim: list = []  # list of floats intended to store the time from the simulation
    v_sim: list = []  # list of floats intended to store the voltage from the simulation
    soc_p_sim: list = []  # list of floats intended to store the soc_p from the simulation
    soc_n_sim: list = []  # list of floats intended to store the soc_p from the simulation
    temp_sim: list = []  # list of floats intended to store the soc_p from the simulation
    if request.method == "POST":
        form = SPSimulationVariables(request.POST)
        if form.is_valid():
            simulation_inputs = get_simulation_inputs(request=request)
            sol: SPPy.Solution = perform_simulation(simulation_inputs=simulation_inputs)
            sol.T = sol.T - Constants.T_abs  # Converts the temperature to degrees C
            t_sim, v_sim, soc_p_sim, soc_n_sim, temp_sim = sol.t[::10].tolist(), \
                sol.V[::10].tolist(), \
                sol.x_surf_p[::10].tolist(), sol.x_surf_n[::10].tolist(), \
                sol.T[::10].tolist()
    else:
        form = SPSimulationVariables()

    return render(request=request, template_name='index.html', context={'context_package': {'form': form,
                                                                                            't_sim': t_sim,
                                                                                            'v_sim': v_sim,
                                                                                            'soc_p_sim': soc_p_sim,
                                                                                            'soc_n_sim': soc_n_sim,
                                                                                            'temp_sim': temp_sim}})


def sp_serializer_view_get(request):
    #load sim params on initialization or param change
    return 0


def get_simulation_inputs(request) -> tuple[str, str, float]:
    parameter_name = request.POST.get('parameter_name')
    cycler = request.POST.get('cycler')
    soc_lib_init = request.POST.get('soc_lib_init')
    return parameter_name, cycler, soc_lib_init


def perform_simulation(simulation_inputs: tuple[str, str, float, float]) -> SPPy.Solution:
    # Operating parameters
    I = 1.656
    T = 298.15
    V_min = 3
    SOC_min = 0.1
    SOC_LIB = 0.9

    # Modelling parameters
    parameter_set_name = simulation_inputs[0]
    soc_lib_init = simulation_inputs[2]

    # Setup battery components
    cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name=parameter_set_name,
                                                    soc_lib_init=soc_lib_init,
                                                    temp_init=T)

    # set-up cycler and solver
    dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=False, degradation=False, electrode_SOC_solver='poly')

    # simulate
    sol = solver.solve(cycler_instance=dc)
    return sol


class Simulator:
    """
    Contains the functionality to perform battery cell simulations using SPPy package.
    """
    available_models: list = ['SP', 'ECM']  # inherent battery models

    def __init__(self, battery_model: str):
        """
        Constructor for the simulator class.
        :param battery_model: (str) string representing the battery model.
        """
        if self.check_for_valid_battery_models(battery_model=battery_model):
            self.battery_model: str = battery_model

    @classmethod
    def check_for_valid_battery_models(cls, battery_model: str) -> bool:
        """
        Raise ValueError in case the inputted battery model is not amongst the inherent battery models.
        """
        if battery_model not in Simulator.available_models:
            raise ValueError('battery_model not available.')
        else:
            return True

    def _get_simulation_inputs(self, request) -> Optional[tuple[str, str, float, float]]:
        if self.battery_model == 'ECM':
            parameter_name: str = request.POST.get('parameter_name')
            cycler: str = request.POST.get('cycler')
            soc_lib_init: float = float(request.POST.get('soc_lib_init'))
            temp_amb: float = float(request.POST.get('temp_amb'))
            return parameter_name, cycler, soc_lib_init, temp_amb
        else:
            return None

    def _perform_simulation(self, request) -> SPPy.ECMSolution:
        # Simulation Parameters below
        I = 1.65
        v_min: float = 2.5  # TODO: just use battery cell min v
        soc_min: float = 0

        # Perform Simulation below
        parameter_set_name, cycler, soc_lib_init, temp_amb = self._get_simulation_inputs(request=request)
        b_cell = SPPy.ECMBatteryCell.read_from_parametersets(parameter_set_name=parameter_set_name,
                                                             soc_init=soc_lib_init,
                                                             temp_init=temp_amb)
        dc = SPPy.Discharge(discharge_current=I, v_min=v_min, SOC_LIB_min=soc_min, SOC_LIB=soc_lib_init)
        solver = SPPy.DTSolver(battery_cell_instance=b_cell, isothermal=True)
        sol = solver.solve(cycling_step=dc)
        # sol.array_temp = sol.array_temp - Constants.T_abs
        return sol

    def get_simulation_results(self, request) -> Optional[tuple[Any, Any, Any, Any]]:
        if self.battery_model == 'ECM':
            sol: SPPy.ECMSolution = self._perform_simulation(request=request)
            t_sim, v_sim, soc_lib, temp_sim = sol.array_t[::10].tolist(), \
                sol.array_V[::10].tolist(), \
                sol.array_soc[::10].tolist(), \
                sol.array_temp[::10].tolist()
            return t_sim, v_sim, soc_lib, temp_sim
        else:
            return None
