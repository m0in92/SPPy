import unittest

from SPPy.battery_components import electrode
from tests.test_config.file_path_variables import TEST_POS_ELEC_DIR # imports the test positive electrode's csv file path.
from parameter_sets.test import funcs # imports the test OCP vs. SOC function and dOCP/dT functions
from SPPy.warnings_and_exceptions import custom_exceptions


class testElectrode(unittest.TestCase):
    L = 7.000000e-05
    A = 5.960000e-02
    max_conc = 51410
    epsilon = 0.49
    kappa = 3.8
    S = 1.1167
    R = 8.5e-6
    T_ref = 298.15
    D_ref = 1e-14
    k_ref = 6.67e-11
    Ea_D = 29000
    Ea_R = 58000
    brugg = 1.5
    T = 298.15
    SOC_init = 0.59
    SOC = SOC_init
    soc_min, soc_max = 0.4956, 0.989011
    electrode_type = 'none'

    elec = electrode.Electrode(L=L, A=A, max_conc=max_conc, epsilon=epsilon, kappa=kappa, S=S, R=R, T_ref=T_ref,
                               D_ref=D_ref, k_ref=k_ref, Ea_D=Ea_D, Ea_R=Ea_R, brugg=brugg, T=T, SOC_init=SOC_init,
                               soc_min=soc_min, soc_max=soc_max,
                               alpha=0.5,
                               func_OCP=funcs.OCP_ref_p, func_dOCPdT=funcs.dOCPdT_p)

    def test_Electrode_constructor(self):
        """
        This test methods ensures that the Electrode object is created correctly, i.e., the csv is read correctly
        and assigned to relevant instance attributes.
        """
        self.assertEqual(self.L, self.elec.L)

    def test_electrode_properties(self):
        self.assertAlmostEqual(172941.17647058822, self.elec.a_s)

    def test_invalid_SOC_init(self):
        """
        This test method checks if the constructor raises an InvalidSOCException when invalid SOC_init is passed.
        """
        T = 298.15
        # Check with a SOC below lower threshold
        SOC_init = -1
        with self.assertRaises(custom_exceptions.InvalidSOCException) as e:
            electrode.Electrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                       kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                       D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                       brugg=self.brugg, T=T,
                                       SOC_init=SOC_init, soc_min=self.soc_min, soc_max=self.soc_max,
                                       alpha=0.5, func_OCP=funcs.OCP_ref_p, func_dOCPdT=13)
        # Check with a SOC above upper threshold
        SOC_init = 1.2
        with self.assertRaises(custom_exceptions.InvalidSOCException) as e:
            electrode.Electrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                brugg=self.brugg, T=T,
                                SOC_init=SOC_init, soc_min=self.soc_min, soc_max=self.soc_max,
                                alpha=0.5, func_OCP=funcs.OCP_ref_p, func_dOCPdT=13)

    def test_SOC_setter(self):
        """
        This test method checks if the SOC attribute of the Electrode object can be changes correctly.
        """
        T = 298.15
        SOC_init = 0.59
        self.assertEqual(self.elec.SOC, SOC_init)
        # Now change the SOC
        new_SOC = 0.71
        self.elec.SOC = new_SOC
        self.assertEqual(self.elec.SOC, new_SOC)
        # Now change it to invalid SOC, i.e, SOC < 0
        new_SOC = -1
        with self.assertRaises(custom_exceptions.InvalidSOCException):
            self.elec.SOC = new_SOC
        # Now change it to another invalid SOC, i.e, SOC > 1
        new_SOC = 1.1
        with self.assertRaises(custom_exceptions.InvalidSOCException):
            self.elec.SOC = new_SOC

    def test_invalid_func_OCP_input(self):
        """
        This test method checks if the constructor raises a TypeError when an invalid function is passed for the
        func_OCP parameter.
        """
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError) as context_manager:
            # Create an instance of Electrode object using a value (instead of a valid function) for func_OCP parameter.
            elec = electrode.Electrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                       kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                       D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                       brugg=self.brugg, T=T,
                                       SOC_init=self.SOC_init,
                                       soc_min=self.soc_min, soc_max=self.soc_max,
                                       alpha=0.5, func_OCP=13, func_dOCPdT=funcs.dOCPdT_p)

    def test_invalid_func_dOCPdT_input(self):
        """
        This test method checks if the constructor raises a TypeError when an invalid function is passed for the
        func_dOCPdT parameter.
        """
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError):
            # Create an instance of the Electrode object using a value (instead of a valid function) for func_dOCPdT
            # parameter.
            elec = electrode.Electrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                       kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                       D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                       brugg=self.brugg, T=T,
                                       SOC_init=self.SOC_init,
                                       soc_min=self.soc_min, soc_max=self.soc_max,
                                       alpha=0.5, func_OCP=funcs.OCP_ref_p, func_dOCPdT=13)
