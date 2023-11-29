import typing
import unittest

import SPPy


class TestBatteryCell(unittest.TestCase):
    T = 298.15
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', soc_lib_init=1.0,
                                                         # SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n,
                                                         temp_init=T)

    def test_negative_electrode_parameters(self):
        """
        This test method test the constructor of the BatteryCell class.
        """
        self.assertEqual(self.test_cell.elec_n.L, 7.35e-05)
        self.assertEqual(self.test_cell.elec_n.A, 5.960000e-02)
        self.assertEqual(self.test_cell.elec_n.max_conc, 31833)
        self.assertEqual(self.test_cell.elec_n.epsilon, 0.59)
        self.assertEqual(self.test_cell.elec_n.kappa, 100)
        self.assertEqual(self.test_cell.elec_n.S, 0.7824)
        self.assertEqual(self.test_cell.elec_n.R, 12.5e-6)
        self.assertEqual(self.test_cell.elec_n.T_ref, 298.15)
        self.assertEqual(self.test_cell.elec_n.D_ref, 3.9e-14)
        self.assertEqual(self.test_cell.elec_n.k_ref, 1.76e-11)
        self.assertEqual(self.test_cell.elec_n.Ea_D, 35000)
        self.assertEqual(self.test_cell.elec_n.Ea_R, 20000)
        self.assertEqual(self.test_cell.elec_n.brugg, 1.5)
        self.assertEqual(self.test_cell.elec_n.T, 298.15)
        self.assertEqual(self.test_cell.elec_n.SOC, self.SOC_init_n)
        self.assertEqual(0.01890232, self.test_cell.elec_n.soc_min)
        self.assertEqual(0.7568, self.test_cell.elec_n.soc_max)
        self.assertEqual(0.7568, self.test_cell.elec_n.SOC)
        self.assertEqual(self.test_cell.elec_n.electrode_type, 'n')

    def test_positive_electrode(self):
        """
        Tests the attributes of the battery cell's positive electrode.
        """
        self.assertEqual(0.0596, self.test_cell.elec_p.A)
        self.assertEqual(7e-5, self.test_cell.elec_p.L)
        self.assertEqual(3.8, self.test_cell.elec_p.kappa)
        self.assertEqual(0.49, self.test_cell.elec_p.epsilon)
        self.assertEqual(1.1167, self.test_cell.elec_p.S)
        self.assertEqual(51410, self.test_cell.elec_p.max_conc)
        self.assertEqual(8.5e-6, self.test_cell.elec_p.R)
        self.assertEqual(6.67e-11, self.test_cell.elec_p.k_ref)
        self.assertEqual(1e-14, self.test_cell.elec_p.D_ref)
        self.assertEqual(5.8e4, self.test_cell.elec_p.Ea_R)
        self.assertEqual(2.9e4, self.test_cell.elec_p.Ea_D)
        self.assertEqual(0.5, self.test_cell.elec_p.alpha)
        self.assertEqual(1.5, self.test_cell.elec_p.brugg)
        self.assertEqual(0.4956, self.test_cell.elec_p.soc_min)
        self.assertEqual(0.989011, self.test_cell.elec_p.soc_max)
        self.assertEqual(0.4956, self.test_cell.elec_p.SOC)

    def test_electrolyte_parameters(self):
        # Below tests for the electrolyte parameters
        self.assertEqual(self.test_cell.electrolyte.conc, 1000)
        self.assertEqual(self.test_cell.electrolyte.L, 2e-5)
        self.assertEqual(self.test_cell.electrolyte.kappa, 0.2875)
        self.assertEqual(self.test_cell.electrolyte.epsilon_sep, 0.724)
        self.assertEqual(self.test_cell.electrolyte.brugg, 1.5)

    def test_battery_cell_parameters(self):
        # below tests for the battery cell parameters
        self.assertEqual(self.test_cell.rho, 1626)
        self.assertEqual(self.test_cell.Vol, 3.38e-5)
        self.assertEqual(self.test_cell.C_p, 750)
        self.assertEqual(self.test_cell.h, 1)
        self.assertEqual(self.test_cell.A, 0.085)
        self.assertEqual(self.test_cell.cap, 1.65)
        self.assertEqual(self.test_cell.V_max, 4.2)
        self.assertEqual(self.test_cell.V_min, 2.5)

    def test_R_cell(self):
        self.assertEqual(0.0028230038442483246, self.test_cell.R_cell)

    def test_temp(self):
        """
        This test method checks if the temperature is properly assigned to the object after the temperature
        parameter is changed.
        :return:
        """
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', soc_lib_init=1.0,
                                                             # SOC_init_p=SOC_init_p,
                                                             # SOC_init_n=SOC_init_n,
                                                             temp_init=T)

        self.assertEqual(test_cell.T, T)
        self.assertEqual(test_cell.elec_p.T, T)
        self.assertEqual(test_cell.elec_n.T, T)
        # change T and check if the battery and electrode temperature changes as well.
        new_T = 313.15
        test_cell.T = new_T
        self.assertEqual(test_cell.T, new_T)
        self.assertEqual(test_cell.elec_p.T, new_T)
        self.assertEqual(test_cell.elec_n.T, new_T)

    def test_temp_amb(self):
        """
        test_T_amb test if the ambient temperature stays constant even after temperature parameter change.
        """
        orig_T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', soc_lib_init=1.0,
                                                             # SOC_init_p=SOC_init_p,
                                                             # SOC_init_n=SOC_init_n,
                                                             temp_init=orig_T)

        self.assertEqual(test_cell.T_amb, orig_T)
        # Now change to new T but T_amb should not change
        new_T = 313.15
        test_cell.T = new_T
        self.assertEqual(test_cell.T_amb, orig_T)

    def test_get_electrode_soc_from_lib_soc(self):
        soc_p_0, soc_n_0 = self.test_cell._get_electrode_soc_from_lib_soc(soc_lib=0.0,
                                                                          soc_p_min=0.4956, soc_p_max=0.989011,
                                                                          soc_n_min=0.01890232, soc_n_max=0.7568)
        self.assertEqual(0.989011, soc_p_0)
        self.assertEqual(0.01890232, soc_n_0)

        soc_p_1, soc_n_1 = self.test_cell._get_electrode_soc_from_lib_soc(soc_lib=1.0,
                                                                          soc_p_min=0.4956, soc_p_max=0.989011,
                                                                          soc_n_min=0.01890232, soc_n_max=0.7568)
        self.assertEqual(0.4956, soc_p_1)
        self.assertEqual(0.7568, soc_n_1)


class TestECMBatteryCell(unittest.TestCase):

    @staticmethod
    def func_ocv(soc: float) -> float:
        return 2.5 + 1.7 * soc

    @staticmethod
    def func_docvdtemp(soc: float):
        return 1.0

    @staticmethod
    def func_eta(soc: float, temp: float) -> float:
        return 1.0

    test_cell_Thevenin = SPPy.ECMBatteryCell(R0_ref=0.225, R1_ref=0.001, C1=0.03, temp_ref=298.15, Ea_R1=400, Ea_R0=400,
                                             rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085,
                                             func_eta=func_eta, func_ocv=func_ocv, func_docvdtemp=func_docvdtemp,
                                             soc_init=0.1, temp_init=298.15,
                                             cap=1.65, v_max=4.2, v_min=2.5)

    test_cell_ESC = SPPy.ECMBatteryCell(R0_ref=0.225, R1_ref=0.001, C1=0.03, temp_ref=298.15, Ea_R1=400, Ea_R0=400,
                                        rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085,
                                        func_eta=func_eta, func_ocv=func_ocv, func_docvdtemp=func_docvdtemp,
                                        soc_init=0.1, temp_init=298.15,
                                        cap=1.65, v_max=4.2, v_min=2.5,
                                        M_0=4.4782e-4, M=0.0012)

    def test_battery_cell_parameters_for_Thevenin_simulations(self):
        self.assertEqual(self.test_cell_Thevenin.rho, 1626)
        self.assertEqual(self.test_cell_Thevenin.vol, 3.38e-5)
        self.assertEqual(self.test_cell_Thevenin.c_p, 750)
        self.assertEqual(self.test_cell_Thevenin.h, 1)
        self.assertEqual(self.test_cell_Thevenin.area, 0.085)
        self.assertEqual(self.test_cell_Thevenin.cap, 1.65)
        self.assertEqual(self.test_cell_Thevenin.v_max, 4.2)
        self.assertEqual(self.test_cell_Thevenin.v_min, 2.5)

        self.assertTrue(isinstance(self.test_cell_Thevenin.func_ocv, typing.Callable))
        self.assertEqual(2.5, self.test_cell_Thevenin.func_ocv(soc=0.0))
        self.assertEqual(3.35, self.test_cell_Thevenin.func_ocv(soc=0.5))
        self.assertEqual(4.2, self.test_cell_Thevenin.func_ocv(soc=1.0))

        self.assertTrue(isinstance(self.test_cell_Thevenin.func_eta, typing.Callable))

        self.assertTrue(isinstance(self.test_cell_Thevenin.func_docvdtemp, typing.Callable))

        self.assertTrue(self.test_cell_Thevenin.M is None)
        self.assertTrue(self.test_cell_Thevenin.M_0 is None)


    def test_battery_cell_parameters_for_ESC_simulations(self):
        self.assertEqual(self.test_cell_ESC.rho, 1626)
        self.assertEqual(self.test_cell_ESC.vol, 3.38e-5)
        self.assertEqual(self.test_cell_ESC.c_p, 750)
        self.assertEqual(self.test_cell_ESC.h, 1)
        self.assertEqual(self.test_cell_ESC.area, 0.085)
        self.assertEqual(self.test_cell_ESC.cap, 1.65)
        self.assertEqual(self.test_cell_ESC.v_max, 4.2)
        self.assertEqual(self.test_cell_ESC.v_min, 2.5)

        self.assertTrue(isinstance(self.test_cell_ESC.func_ocv, typing.Callable))
        self.assertEqual(2.5, self.test_cell_ESC.func_ocv(soc=0.0))
        self.assertEqual(3.35, self.test_cell_ESC.func_ocv(soc=0.5))
        self.assertEqual(4.2, self.test_cell_ESC.func_ocv(soc=1.0))

        self.assertTrue(isinstance(self.test_cell_ESC.func_eta, typing.Callable))

        self.assertTrue(isinstance(self.test_cell_ESC.func_docvdtemp, typing.Callable))

        self.assertEqual(4.4782e-4, self.test_cell_ESC.M_0)
        self.assertEqual(0.0012, self.test_cell_ESC.M)



