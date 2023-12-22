from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from SPPy.battery_components.parameter_set_manager import ParameterSets, ECMParameterSets
from .managers import *

class Simulation(models.Model):
    parameter_name = models.CharField(max_length=200)
    battery_cell_model = models.CharField(max_length=200)
    solver_type = models.CharField(max_length=200)
    cycler = models.CharField(max_length=200)


class SpSolvedModel(models.Model):
    t_sim = models.JSONField(encoder=None, null=True, blank=True)
    v_sim = models.JSONField(encoder=None, null=True, blank=True)
    soc_p_sim = models.JSONField(encoder=None, null=True, blank=True)
    soc_n_sim = models.JSONField(encoder=None, null=True, blank=True)
    temp_sim = models.JSONField(encoder=None, null=True, blank=True)

    objects = SpSolvedModelManager()


class SpSimulationVariablesModel(models.Model):
    """
    Contains the relevant fields required from the user to perform the single particle model simulations.
    """
    lst_parameter_name: list = [(param_set_name, param_set_name)
                                for param_set_name in ParameterSets.list_parameters_sets()]
    lst_cyclers: list = [('discharge', 'discharge')]

    parameter_name = models.CharField(max_length=16, choices=lst_parameter_name, default='test')
    cycler = models.CharField(max_length=9, choices=lst_cyclers, default='discharge')
    soc_lib_init = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0.0)
    parameter_values = models.JSONField(encoder=None)

    objects = SpSimulationVariablesModelManager()
