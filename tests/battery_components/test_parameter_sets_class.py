from typing import Callable

import numpy as np
import unittest
import os

from SPPy.battery_components.battery_cell import ParameterSets
from SPPy.battery_components.parameter_set_manager import PydanticParameterSets
from SPPy.battery_components.parameter_set_manager import ECMParameterSets


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
        self.assertEqual(0.38, params.t_c)

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


class TestECMParameterSet(unittest.TestCase):
    instance_test: ECMParameterSets = ECMParameterSets('test')

    def test_file_path(self):
        """
        Ensures PARAMETER_SET_DIR is set to two parents above.
        """
        self.assertTrue(os.path.join('.', '.', 'parameter_sets_ecm'), self.instance_test.PARAMETER_SET_DIR)

    def test_constructor(self):
        # Check for the instance field types
        self.assertTrue(isinstance(self.instance_test.R0_ref, np.float64))
        self.assertTrue(isinstance(self.instance_test.R1_ref, np.float64))
        self.assertTrue(isinstance(self.instance_test.C1, np.float64))
        self.assertTrue(isinstance(self.instance_test.temp_ref, np.float64))
        self.assertTrue(isinstance(self.instance_test.Ea_R0, np.float64))
        self.assertTrue(isinstance(self.instance_test.Ea_R1, np.float64))

        self.assertTrue(isinstance(self.instance_test.rho, np.float64))
        self.assertTrue(isinstance(self.instance_test.vol, np.float64))
        self.assertTrue(isinstance(self.instance_test.c_p, np.float64))
        self.assertTrue(isinstance(self.instance_test.h, np.float64))
        self.assertTrue(isinstance(self.instance_test.area, np.float64))
        self.assertTrue(isinstance(self.instance_test.cap, np.float64))
        self.assertTrue(isinstance(self.instance_test.v_max, np.float64))
        self.assertTrue(isinstance(self.instance_test.v_min, np.float64))

        self.assertTrue(np.isnan(self.instance_test.M_0))
        self.assertTrue(np.isnan(self.instance_test.M))
        self.assertTrue(np.isnan(self.instance_test.gamma))

        self.assertTrue(isinstance(self.instance_test.func_eta, Callable))
        self.assertTrue(isinstance(self.instance_test.func_ocv, Callable))
        self.assertTrue(isinstance(self.instance_test.func_docvdtemp, Callable))

        # Check for the instance values
        self.assertEqual('test', self.instance_test.name)
        self.assertEqual(0.005, self.instance_test.R0_ref)
        self.assertTrue(0.001, self.instance_test.R1_ref)
        self.assertTrue(0.03, self.instance_test.C1)
        self.assertTrue(298.15, self.instance_test.temp_ref)
        self.assertTrue(400, self.instance_test.Ea_R0)
        self.assertTrue(400, self.instance_test.Ea_R1)

        self.assertTrue(1626, self.instance_test.rho)
        self.assertTrue(3.38e-5, self.instance_test.vol)
        self.assertTrue(750, self.instance_test.c_p)
        self.assertTrue(0.085, self.instance_test.h)
        self.assertTrue(1, self.instance_test.area)
        self.assertTrue(1.65, self.instance_test.cap)
        self.assertTrue(4.2, self.instance_test.v_max)
        self.assertTrue(2.5, self.instance_test.v_min)

        self.assertEqual(1.0, self.instance_test.func_eta(0.5, 298.15))
        self.assertEqual(3.7913774209371964, self.instance_test.func_ocv(0.5))
        self.assertEqual(-0.0002942358440153894, self.instance_test.func_docvdtemp(0.5))

    def test_list_parameter_names(self):
        self.assertTrue('test' in self.instance_test.lst_parameter_names())


class TestPydanticParameterSet(unittest.TestCase):
    def test_constructor(self):
        parameter_set_name: str = "test"
        pyd_parameterset_instance: PydanticParameterSets = PydanticParameterSets(parameter_set_name=parameter_set_name)

        # Testing for the positive electrode parameters
        self.assertEqual(7e-5, pyd_parameterset_instance.L_p)
        self.assertEqual(0.0596, pyd_parameterset_instance.A_p)
        self.assertEqual(3.8, pyd_parameterset_instance.kappa_p)
        self.assertEqual(0.49, pyd_parameterset_instance.epsilon_p)
        self.assertEqual(8.5e-6, pyd_parameterset_instance.R_p)
        self.assertEqual(1.1167, pyd_parameterset_instance.S_p)

        self.assertEqual(298.15, pyd_parameterset_instance.T_ref_p)
        self.assertEqual(1e-14, pyd_parameterset_instance.D_ref_p)
        self.assertEqual(6.67e-11, pyd_parameterset_instance.k_ref_p)

        self.assertEqual(0.5, pyd_parameterset_instance.alpha_p)
        self.assertEqual(1.5, pyd_parameterset_instance.brugg_p)

        self.assertEqual(0.4956, pyd_parameterset_instance.soc_min_p)
        self.assertEqual(0.989011, pyd_parameterset_instance.soc_max_p)

        # Testing for the negative electrode parameters
        self.assertEqual(7.35e-5, pyd_parameterset_instance.L_n)
        self.assertEqual(0.0596, pyd_parameterset_instance.A_n)
        self.assertEqual(100, pyd_parameterset_instance.kappa_n)
        self.assertEqual(0.59, pyd_parameterset_instance.epsilon_n)
        self.assertEqual(1.25e-5, pyd_parameterset_instance.R_n)
        self.assertEqual(0.7824, pyd_parameterset_instance.S_n)

        self.assertEqual(298.15, pyd_parameterset_instance.T_ref_n)
        self.assertEqual(3.9e-14, pyd_parameterset_instance.D_ref_n)
        self.assertEqual(1.76e-11, pyd_parameterset_instance.k_ref_n)

        self.assertEqual(0.5, pyd_parameterset_instance.alpha_n)
        self.assertEqual(1.5, pyd_parameterset_instance.brugg_n)

        self.assertEqual(0.01890232, pyd_parameterset_instance.soc_min_n)
        self.assertEqual(0.7568, pyd_parameterset_instance.soc_max_n)

        # Below test for the electrolyte parameters
        self.assertEqual(1000, pyd_parameterset_instance.conc_es)
        self.assertEqual(2e-5, pyd_parameterset_instance.L_es)
        self.assertEqual(0.2875, pyd_parameterset_instance.kappa_es)
        self.assertEqual(0.724, pyd_parameterset_instance.epsilon_es)
        self.assertEqual(1.5, pyd_parameterset_instance.brugg_es)

        # Below tests for the battery cell parameters
        self.assertEqual(1626, pyd_parameterset_instance.rho)
        self.assertEqual(3.38e-5, pyd_parameterset_instance.Vol)
        self.assertEqual(750, pyd_parameterset_instance.C_p)
        self.assertEqual(1, pyd_parameterset_instance.h)
        self.assertEqual(1.65, pyd_parameterset_instance.cap)
        self.assertEqual(4.2, pyd_parameterset_instance.V_max)
        self.assertEqual(2.5, pyd_parameterset_instance.V_min)

        # Below are the tests for the positive and negative electrode ocp functions
        self.assertEqual(4.176505962016067, pyd_parameterset_instance.OCP_ref_p_(0.4956))
        self.assertEqual(-3.493449781653898e-05, pyd_parameterset_instance.dOCPdT_p_(0.5))
        self.assertAlmostEqual(0.09051278679435444, pyd_parameterset_instance.OCP_ref_n_(0.5), places=3)
        self.assertAlmostEqual(-0.00011021528491435903, pyd_parameterset_instance.dOCPdT_n_(0.5))





