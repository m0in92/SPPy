from django.db import models


class Simulation(models.Model):
    parameter_name = models.CharField(max_length=200)
    battery_cell_model = models.CharField(max_length=200)
    solver_type = models.CharField(max_length=200)
    cycler = models.CharField(max_length=200)
