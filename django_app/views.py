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
from rest_framework.views import APIView
from rest_framework.response import Response

from django_app.models import EcmSimulationVariablesModel, SpSimulationVariablesModel, EcmSolvedModel, SpSolvedModel
from django_app.serializers import EcmSimulationVariablesModelSerializer, EcmSolvedModelSerializer,\
    SpSolvedModelSerializer, SpSimulationVariablesModelSerializer

import json
import SPPy
from SPPy.calc_helpers.constants import Constants


def index(request) -> HttpResponse:
    return render(request=request, template_name='index.html',
                  context={'context_package': {}})


class EcmParamView(APIView):
    def options(self, request, *args, **kwargs):
        parameter_name_list: list = [name[1] for name in EcmSimulationVariablesModel.lst_parameter_name]
        cycler_list: list = [name[1] for name in EcmSimulationVariablesModel.lst_cycler]
        return Response({'ecm_options': {'parameter_name_list': parameter_name_list,
                                         'cycler_list': cycler_list,
                                         'soc_lib_init': 0,
                                         'temp_amb': 298.0}})

    def get(self, request):
        parameter_name = request.query_params['parameter_name'] if bool(request.query_params) else 'test'
        # a placeholder solution to make django read ECM parameters from a json. said parameters will be served by a DB in the future
        with open('django_app/static/parameter_sets_ecm.json', 'r') as f:
            parameter_sets = json.load(f)
        parameter_chosen = json.dumps(parameter_sets[parameter_name])
        ecm_sim_var_proto = EcmSimulationVariablesModel.objects.create_ecm_sim_var_model(
            parameter_name_arg=parameter_name,
            parameter_values_arg=parameter_chosen)
        ecm_sim_var_serializer = EcmSimulationVariablesModelSerializer(ecm_sim_var_proto)
        return Response(ecm_sim_var_serializer.data)

    def post(self, request):
        t_sim, v_sim, soc_lib, temp_sim = [], [], [], []

        t_sim, v_sim, soc_lib, temp_sim = Simulator(battery_model='ECM').get_simulation_results(request=request)
        t_sim_json = json.dumps(t_sim)
        v_sim_json = json.dumps(v_sim)
        soc_lib_json = json.dumps(soc_lib)
        temp_sim_json = json.dumps(temp_sim)
        ecm_solved_proto = EcmSolvedModel.objects.create_ecm_solved_model(t_sim=t_sim_json,
                                                                          v_sim=v_sim_json,
                                                                          soc_lib=soc_lib_json,
                                                                          temp_sim=temp_sim_json)
        ecm_model_serializer = EcmSolvedModelSerializer(ecm_solved_proto)
        return Response(ecm_model_serializer.data)


class SpParamView(APIView):
    def options(self, request, *args, **kwargs):
        parameter_name_list: list = [name[1] for name in SpSimulationVariablesModel.lst_parameter_name]
        cycler_list: list = [name[1] for name in SpSimulationVariablesModel.lst_cyclers]
        return Response({'sp_options': {'parameter_name_list': parameter_name_list,
                                        'cycler_list': cycler_list,
                                        'soc_lib_init': 0}})

    def get(self, request):
        # the query_params field is the backend contact point for Axios's GET method's param field
        parameter_name = request.query_params['parameter_name'] if bool(request.query_params) else 'test'
        # a placeholder solution to make django read SP parameters from a json. said parameters will be served by a DB in the future
        with open('django_app/static/parameter_sets.json', 'r') as f:
            parameter_sets = json.load(f)
        parameter_chosen = json.dumps(parameter_sets[parameter_name])
        sp_sim_var_proto = SpSimulationVariablesModel.objects.create_sp_sim_var_model(
            parameter_name_arg=parameter_name,
            parameter_values_arg=parameter_chosen)
        sp_sim_var_serializer = SpSimulationVariablesModelSerializer(sp_sim_var_proto)
        return Response(sp_sim_var_serializer.data)

    def post(self, request):
        parameter_name = request.data.get("parameter_name")
        cycler = request.data.get("cycler")
        soc_lib_init = float(request.data.get("soc_lib_init"))
        sol: SPPy.Solution = perform_simulation(simulation_inputs=(parameter_name, cycler, soc_lib_init))
        sol.T = sol.T - Constants.T_abs  # Converts the temperature to degrees C
        t_sim, v_sim, soc_p_sim, soc_n_sim, temp_sim = sol.t[::10].tolist(), \
            sol.V[::10].tolist(), \
            sol.x_surf_p[::10].tolist(), sol.x_surf_n[::10].tolist(), \
            sol.T[::10].tolist()
        t_sim_json = json.dumps(t_sim)
        v_sim_json = json.dumps(v_sim)
        soc_p_sim_json = json.dumps(soc_p_sim)
        soc_n_sim_json = json.dumps(soc_n_sim)
        temp_sim_json = json.dumps(temp_sim)
        sp_solved_proto = SpSolvedModel.objects.create_sp_solved_model(t_sim=t_sim_json,
                                                                       v_sim=v_sim_json,
                                                                       soc_p_sim=soc_p_sim_json,
                                                                       soc_n_sim=soc_n_sim_json,
                                                                       temp_sim=temp_sim_json)
        sp_model_serializer = SpSolvedModelSerializer(sp_solved_proto)
        return Response(sp_model_serializer.data)


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
        # 15-01-2024: modified `request.POST.get()` into `request.data.get()`. check for crashing other functions...
        if self.battery_model == 'ECM':
            parameter_name: str = request.data.get('parameter_name')
            cycler: str = request.data.get('cycler')
            soc_lib_init: float = float(request.data.get('soc_lib_init'))
            temp_amb: float = float(request.data.get('temp_amb'))
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
