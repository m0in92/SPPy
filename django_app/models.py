from django.db import models


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
    temp_sim = models.JSONField(encoder=None, null=True, blank=True,)
    #more to come
