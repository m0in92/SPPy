from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from bokeh.plotting import figure
from bokeh.embed import components

from django_app.forms import SimulationVariables

import SPPy


def index(request) -> HttpResponse:
    if request.method == "POST":
        form = SimulationVariables(request.POST)
        if form.is_valid():
            HttpResponseRedirect('/result/')
    else:
        form = SimulationVariables()

    return render(request=request, template_name='input_simulation_variables.html', context={'form': form})


def result(request) -> HttpResponse:
    simulation_inputs = get_simulation_inputs(request=request)
    sol = perform_simulation(simulation_inputs=simulation_inputs)
    plot = figure(title='Voltage Profile', x_axis_label='t [s]', y_axis_label='V [V]')
    plot.line(sol.t, sol.V, line_width=5)

    script, div = components(plot)

    return render(request=request, template_name='result.html', context={'script': script, 'div': div})


def get_simulation_inputs(request) -> tuple[str, str, str, str]:
    parameter_name = request.POST.get('parameter_name')
    battery_cell_model = request.POST.get('battery_cell_model')
    solver_type = request.POST.get('solver_type')
    cycler = request.POST.get('cycler')
    return (parameter_name, battery_cell_model, solver_type, cycler)


def perform_simulation(simulation_inputs: tuple[str, str, str, str]) -> SPPy.Solution:
    # Operating parameters
    I = 1.656
    T = 298.15
    V_min = 3
    SOC_min = 0.1
    SOC_LIB = 0.9

    # Modelling parameters
    SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

    # Setup battery components
    cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', SOC_init_p=SOC_init_p,
                                                    SOC_init_n=SOC_init_n,
                                                    temp_init=T)

    # set-up cycler and solver
    dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

    # simulate
    sol = solver.solve(cycler_instance=dc)
    return sol
