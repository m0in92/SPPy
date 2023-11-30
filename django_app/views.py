"""
Contains the functionality to render the html containing the simulations results. However, index(request) just renders
the homepage.
"""

__all__ = ['index', 'get_simulation_inputs', 'perform_simulation']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by SPPy. All rights reserved."
__status__ = "developement"

from django.shortcuts import render
from django.http import HttpResponse

from django_app.forms import ECMSimulationVariables, SPSimulationVariables

import SPPy
from SPPy.calc_helpers.constants import Constants


def index(request) -> HttpResponse:
    return render(request=request, template_name='index.html', context={})


def ecm(request) -> HttpResponse:
    if request.method == "POST":
        form = ECMSimulationVariables(request.POST)
        if form.is_valid():
            print("Pressed")
    else:
        form = ECMSimulationVariables()

    return render(request=request, template_name='ecm.html', context={'form': form})


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

    return render(request=request, template_name='sp.html', context={'form': form,
                                                                     't_sim': t_sim,
                                                                     'v_sim': v_sim,
                                                                     'soc_p_sim': soc_p_sim,
                                                                     'soc_n_sim': soc_n_sim,
                                                                     'temp_sim': temp_sim})


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
