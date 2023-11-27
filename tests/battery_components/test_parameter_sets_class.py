import unittest
import os

from SPPy.battery_components.battery_cell import ParameterSets


class TestParameterSets(unittest.TestCase):
    def test_constructor_with_valid_name(self):
        params = ParameterSets(name='test')
        self.assertEqual('test', params.name)
        self.assertEqual(os.path.basename(os.path.join('..', '..', 'parameter_sets', 'test', 'param_electrolyte.csv')),
                         os.path.basename(params.ELECTROLYTE_DIR))

        # Below test for the positive electrode parameter extraction
        self.assertEqual(0.0596, params.A_p)
        self.assertEqual(7e-5, params.L_p)
        self.assertEqual(3.8, params.kappa_p)
        self.assertEqual(0.49, params.epsilon_p)
        self.assertEqual(1.1167, params.S_p)
        self.assertEqual(51410, params.max_conc_p)
        self.assertEqual(8.5e-6, params.R_p)
        self.assertEqual(6.67e-11, params.k_ref_p)
        self.assertEqual(1e-14, params.D_ref_p)
        self.assertEqual(5.8e4, params.Ea_R_p)
        self.assertEqual(2.9e4, params.Ea_D_p)
        self.assertEqual(0.5, params.alpha_p)
        self.assertEqual(298.15, params.T_ref_p)
        self.assertEqual(1.5, params.brugg_p)
        self.assertEqual(0.4956, params.soc_min_p)
        self.assertEqual(0.989011, params.soc_max_p)

        # Below tests for the negative electrode parameter extraction
        self.assertEqual(0.0596, params.A_n)
        self.assertEqual(7.35e-5, params.L_n)
        self.assertEqual(100, params.kappa_n)
        self.assertEqual(0.59, params.epsilon_n)
        self.assertEqual(0.7824, params.S_n)
        self.assertEqual(31833, params.max_conc_n)
        self.assertEqual(12.5e-6, params.R_n)
        self.assertEqual(1.76e-11, params.k_ref_n)
        self.assertEqual(3.9e-14, params.D_ref_n)
        self.assertEqual(2e4, params.Ea_R_n)
        self.assertEqual(3.5e4, params.Ea_D_n)
        self.assertEqual(0.5, params.alpha_n)
        self.assertEqual(298.15, params.T_ref_n)
        self.assertEqual(1.5, params.brugg_n)
        self.assertEqual(0.01890232, params.soc_min_n)
        self.assertEqual(0.7568, params.soc_max_n)

        # Below test for the electrolyte parameters
        self.assertEqual(1000, params.conc_es)
        self.assertEqual(2e-5, params.L_es)
        self.assertEqual(0.2875, params.kappa_es)
        self.assertEqual(0.724, params.epsilon_es)
        self.assertEqual(1.5, params.brugg_es)

        # Below tests for the battery cell parameters
        self.assertEqual(1626, params.rho)
        self.assertEqual(3.38e-5, params.Vol)
        self.assertEqual(750, params.C_p)
        self.assertEqual(1, params.h)
        self.assertEqual(1.65, params.cap)
        self.assertEqual(4.2, params.V_max)
        self.assertEqual(2.5, params.V_min)

    def test_constructor_with_invalid_name(self):
        with self.assertRaises(ValueError) as context:
            ParameterSets('non-sense')

    def test_list_parameter_sets_methods(self):
        self.assertTrue(self.check_for_parameter_sets('test'))

    def test_check_parameter_sets(self):
        # a parameter set that is present is tested below
        self.assertTrue(ParameterSets._check_parameter_set(name='test'))

        # a parameter set that is not present is tested below
        self.assertFalse(ParameterSets._check_parameter_set(name='non_sense'))

    def check_for_parameter_sets(self, *args):
        for parameter_set_name in args:
            if parameter_set_name not in ParameterSets.list_parameters_sets():
                return False
        return True
