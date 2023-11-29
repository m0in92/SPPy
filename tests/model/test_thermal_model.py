import unittest

import SPPy
from SPPy.models.thermal import Lumped


class TestLumped(unittest.TestCase):
    T = 298.15
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', soc_lib_init=1.0,
                                                         # SOC_init_p=SOC_init_p,
                                                         # SOC_init_n=SOC_init_n,
                                                         temp_init=T)
    t_model = Lumped(b_cell=test_cell)

    def test_reversible_heat_loss(self):
        I = -1.656
        T = 298.15
        self.assertAlmostEqual(0.017761327872963178, self.t_model.reversible_heat(I=I, T=T))

    def test_irreversible_heat_loss(self):
        V = self.test_cell.elec_p.OCP - self.test_cell.elec_n.OCP
        I = -1.656
        T = 298.15
        self.assertEqual(0.0, self.t_model.irreversible_heat(I=I, V=V))
        V = 3.9
        self.assertEqual(0.33428490122165927, self.t_model.irreversible_heat(I, V))

    def test_heat_balance(self):
        self.assertEqual(0.0, self.t_model.heat_flux(298.15))
        self.assertEqual(1.2750000000000001, self.t_model.heat_flux(313.15))
