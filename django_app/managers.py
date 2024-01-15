from django.db import models
import json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


class EcmSimulationVariablesModelManager(models.Manager):
    def create_ecm_sim_var_model(self, parameter_name_arg, cycler_arg='discharge', soc_lib_init_arg=float(0.0),
                                 temp_amb_arg=float(298.0), parameter_values_arg=None):
        output = self.create(parameter_name=parameter_name_arg,
                             cycler=cycler_arg,
                             soc_lib_init=soc_lib_init_arg,
                             temp_amb=temp_amb_arg,
                             parameter_values=parameter_values_arg if is_json(parameter_values_arg) else {})
        return output


class EcmSolvedModelManager(models.Manager):
    def create_ecm_solved_model(self, t_sim, v_sim, soc_lib, temp_sim):
        output = self.create(t_sim=t_sim, v_sim=v_sim, soc_lib=soc_lib, temp_sim=temp_sim)
        return output


class SpSimulationVariablesModelManager(models.Manager):
    def create_sp_sim_var_model(self, parameter_name_arg='test', cycler_arg='discharge', soc_lib_init_arg=float(0.0),
                                parameter_values_arg=None):

        output = self.create(parameter_name=parameter_name_arg,
                             cycler=cycler_arg,
                             soc_lib_init=soc_lib_init_arg,
                             parameter_values=parameter_values_arg if is_json(parameter_values_arg) else {})

        return output


class SpSolvedModelManager(models.Manager):
    def create_sp_solved_model(self, t_sim, v_sim, soc_p_sim, soc_n_sim, temp_sim):
        output = self.create(t_sim=t_sim, v_sim=v_sim, soc_p_sim=soc_p_sim, soc_n_sim=soc_n_sim, temp_sim=temp_sim)
        return output
