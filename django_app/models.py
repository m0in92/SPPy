from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from SPPy.battery_components.parameter_set_manager import ParameterSets, ECMParameterSets


class Simulation(models.Model):
    parameter_name = models.CharField(max_length=200)
    battery_cell_model = models.CharField(max_length=200)
    solver_type = models.CharField(max_length=200)
    cycler = models.CharField(max_length=200)


class SpModel(models.Model):
    t_sim = models.JSONField(encoder=None, null=True, blank=True)
    v_sim = models.JSONField(encoder=None, null=True, blank=True)
    soc_p_sim = models.JSONField(encoder=None, null=True, blank=True)
    soc_n_sim = models.JSONField(encoder=None, null=True, blank=True)
    temp_sim = models.JSONField(encoder=None, null=True, blank=True)


class SpSimulationVariablesModel(models.Model):
    """
    Contains the relevant fields required from the user to perform the single particle model simulations.
    """
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ParameterSets.list_parameters_sets()]
    lst_cyclers: list = [('discharge', 'discharge')]

    parameter_name = models.CharField(choices=lst_parameter_name)
    cycler = models.CharField(choices=lst_cyclers)
    soc_lib_init = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)
    parameter_values = models.JSONField(encoder=None)
