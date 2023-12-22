from django.db import models
import json


class SpSimulationVariablesModelManager(models.Manager):
    def create_sp_sim_var_model(self, parameter_name_arg='test', cycler_arg='discharge', soc_lib_init_arg=float(0.0),
                                parameter_values_arg=None):
        def is_json(myjson):
            try:
                json.loads(myjson)
            except ValueError as e:
                return False
            return True

        output = self.create(parameter_name=parameter_name_arg,
                             cycler=cycler_arg,
                             soc_lib_init=soc_lib_init_arg,
                             parameter_values=parameter_values_arg if is_json(parameter_values_arg) else {})

        return output


class SpSolvedModelManager(models.Manager):
    def create_sp_solved_model(self,t_sim,v_sim,soc_p_sim,soc_n_sim,temp_sim):
        output = self.create(t_sim=t_sim, v_sim=v_sim, soc_p_sim=soc_p_sim, soc_n_sim=soc_n_sim, temp_sim=temp_sim)
        return output
