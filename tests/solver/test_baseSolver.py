import unittest
import numpy as np

import SPPy
from SPPy.solvers.base import BaseSolver


class TestBaseSolver(unittest.TestCase):

    def test_constructor(self):
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        t = np.arange(0, 4000, 0.1)
        I = -1.656 * np.ones(len(t))
        test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test',
                                                             soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                             temp_init=T)
