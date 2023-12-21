from django.db import models
import json


class SpSimulationVariablesModelManager(models.Manager):
    def create_sp_sim_var_model(self, parameter_name_arg, cycler_arg, soc_lib_init_arg, parameter_values_arg):
        def is_json(myjson):
            try:
                json.loads(myjson)
            except ValueError as e:
                return False
            return True

        output = self.create(parameter_name=parameter_name_arg if parameter_values_arg else 'test',
                             cycler=cycler_arg if cycler_arg else 'discharge',
                             soc_lib_init=soc_lib_init_arg if soc_lib_init_arg else float(0.0),
                             parameter_values=parameter_values_arg if is_json(parameter_values_arg) else {})

        return output
