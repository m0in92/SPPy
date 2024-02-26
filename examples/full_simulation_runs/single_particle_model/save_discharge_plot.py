"""
This script just demonstrates how to save the plotted image using the relevant Solution's method
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by SPPy. All rights reserved.'
__status__ = 'deployed'


from examples.full_simulation_runs.single_particle_model.discharge_isothermal import *


sol.comprehensive_plot(save_dir="saved_results/isothermal_discharge.png")
