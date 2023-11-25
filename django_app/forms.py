from django import forms

from SPPy.battery_components.parameter_set_manager import ParameterSets


class SimulationVariables(forms.Form):
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ParameterSets.list_parameters_sets()]
    lst_cell_model: list = [('ECM', 'ECM'),
                            ("SPM", 'SPM')]

    parameter_name = forms.ChoiceField(label="Parameter Name", choices=lst_parameter_name)
    battery_cell_model = forms.ChoiceField(label="Battery Cell Model", choices=lst_cell_model)
    solver_type = forms.CharField(max_length=200)
    cycler = forms.CharField(max_length=200)

