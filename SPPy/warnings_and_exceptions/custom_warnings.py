__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'


import warnings


# def threshold_potential_warning(V_val):
#     warnings.warn(f"Threshold battery cell potential reached {V_val} V.")

class ThresholdPotentialWarning(Warning):
    def __init__(self, V: flaot):
        self.message = f"Threshold battery cell potential reached {V} V."
        warnings.warn(self.message)


def threshold_SOC_warning():
    warnings.warn("Threshold battery cell SOC reached.")
