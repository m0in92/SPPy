from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.layouts import row, gridplot

from django_app.forms import SimulationVariables

import SPPy
from SPPy.calc_helpers.constants import Constants


def index(request) -> HttpResponse:
    t_sim: list = []  # list of floats intended to store the time from the simulation
    v_sim: list = []  # list of floats intended to store the voltage from the simulation
    soc_p_sim: list = []   # list of floats intended to store the soc_p from the simulation
    soc_n_sim: list = []  # list of floats intended to store the soc_p from the simulation
    temp_sim: list = []  # list of floats intended to store the soc_p from the simulation
    if request.method == "POST":
        form = SimulationVariables(request.POST)
        if form.is_valid():
            simulation_inputs = get_simulation_inputs(request=request)
            sol: SPPy.Solution = perform_simulation(simulation_inputs=simulation_inputs)
            sol.T = sol.T - Constants.T_abs  # Converts the temperature to degrees C
            t_sim, v_sim, soc_p_sim, soc_n_sim, temp_sim = sol.t[::10].tolist(), \
                                                 sol.V[::10].tolist(), \
                                                 sol.x_surf_p[::10].tolist(), sol.x_surf_n[::10].tolist(), sol.T[::10].tolist()
    else:
        form = SimulationVariables()

    return render(request=request, template_name='sim_sp.html', context={'form': form,
                                                                        't_sim': t_sim,
                                                                        'v_sim': v_sim,
                                                                        'soc_p_sim': soc_p_sim,
                                                                        'soc_n_sim': soc_n_sim,
                                                                        'temp_sim': temp_sim})


# def result(request) -> HttpResponse:
#     FIG_HEIGHT = 300  # in px
#     FIG_WIDTH = 300  # in px
#
#     simulation_inputs = get_simulation_inputs(request=request)
#     sol = perform_simulation(simulation_inputs=simulation_inputs)
#
#     # plot V vs. t
#     p1 = figure(title='Voltage Profile', x_axis_label='t [s]', y_axis_label='V [V]', height=FIG_HEIGHT)
#     p1.line(sol.t, sol.V, line_width=5)
#
#     # plot cap vs. t
#     p2 = figure(title='Voltage Profile', x_axis_label='cap [Ahr]', y_axis_label='V [V]', height=FIG_HEIGHT)
#     p2.line(sol.cap, sol.V, line_width=5)
#
#     # plot soc_p vs. t
#     p3 = figure(title='Positive Electrode SOC', x_axis_label='t [s]', y_axis_label='SOC', height=FIG_HEIGHT)
#     p3.line(sol.t, sol.x_surf_p, line_width=5)
#
#     # plot soc_n vs. t
#     p4 = figure(title='Negative Electrode SOC', x_axis_label='t [s]', y_axis_label='SOC', height=FIG_HEIGHT)
#     p4.line(sol.t, sol.x_surf_n, line_width=5)
#
#     script, div = components(gridplot([[p1, p2], [p3, p4]]))
#     return render(request=request, template_name='result.html', context={'script': script, 'div': div})


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
