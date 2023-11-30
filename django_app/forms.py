"""
This module contains the forms (inherited from Django's Forms) to be used for the django apps.
"""
__all__ = ['ECMSimulationVariables', 'SPSimulationVariables']

__authors__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by SPPy. All Rights Reserved."


from django import forms

from SPPy.battery_components.parameter_set_manager import ParameterSets, ECMParameterSets



class BaseBatteryModelForm(forms.Form):
    lst_cycler: list = [('discharge', 'discharge')]


class ECMSimulationVariables(BaseBatteryModelForm):
    """
    Contains the field ECM simulation's user inputs.
    """
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ECMParameterSets.lst_parameter_names()]
    # lst_cycler: list = [('discharge', 'discharge')]

    parameter_name = forms.ChoiceField(label="Parameter Name", choices=lst_parameter_name)
    cycler = forms.ChoiceField(choices=BaseBatteryModelForm.lst_cycler)
    soc_lib_init = forms.FloatField(label='Initial LIB SOC', min_value=-0.1, max_value=1.1)
    temp_amb = forms.FloatField(label='Ambient Temperature [K]')


class SPSimulationVariables(forms.Form):
    """
    Contains the relevant fields required from the user to perform the single particle model simulations.
    """
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ParameterSets.list_parameters_sets()]
    lst_cyclers: list = [('discharge', 'discharge')]

    parameter_name = forms.ChoiceField(label="Parameter Name", choices=lst_parameter_name)
    cycler = forms.ChoiceField(choices=lst_cyclers)
    soc_lib_init = forms.FloatField(label='Initial LIB SOC', min_value=-0.1, max_value=1.1)


class SPeSimulationVariables(forms.Form):
    pass


class P2DSimulationVariables(forms.Form):
    pass

