from django import forms

from SPPy.battery_components.parameter_set_manager import ParameterSets


class SimulationVariables(forms.Form):
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ParameterSets.list_parameters_sets()]
    lst_cyclers: list = [('discharge', 'discharge')]

    parameter_name = forms.ChoiceField(label="Parameter Name", choices=lst_parameter_name)
    cycler = forms.ChoiceField(choices=lst_cyclers)
    soc_lib_init = forms.FloatField(label='Initial LIB SOC', min_value=-0.1, max_value=1.1)


