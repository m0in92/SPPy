import unittest
import numpy as np

import SPPy


class TestSPPySolverBasic(unittest.TestCase):
    """
    Basic test to ensure its basic functionalities.
    """
    T = 298.15
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    t = np.arange(0, 4000, 0.1)
    I = -1.656 * np.ones(len(t))
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', SOC_init_p=SOC_init_p,
                                                         SOC_init_n=SOC_init_n, temp_init=T)
    test_solver = SPPy.SPPySolver(b_cell=test_cell, N=N, isothermal=True, degradation=False)
    def test_constructor(self):
        self.assertEqual(self.N, self.test_solver.N)
        self.assertEqual(self.test_cell, self.test_solver.b_cell)
        self.assertTrue(self.test_solver.bool_isothermal)
        self.assertFalse(self.test_solver.bool_degradation)

    def test_invalid_constructor_arguments(self):
        with self.assertRaises(TypeError):
            SPPy.SPPySolver(b_cell=self.test_cell, N=self.N, isothermal=13, degradation=False)
        with self.assertRaises(TypeError):
            SPPy.SPPySolver(b_cell=self.test_cell, N=self.N, isothermal=True, degradation=13)

class TestSPPySolverMethods(unittest.TestCase):
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    I = 1.656
    T = 298.15
    V_min = 4.0
    SOC_min = 0.1
    SOC_LIB = 0.9
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', SOC_init_p=SOC_init_p,
                                                         SOC_init_n=SOC_init_n, temp_init=T)

    def test_solve(self):
        dc = SPPy.Discharge(discharge_current=self.I, v_min=self.V_min, SOC_LIB_min=self.SOC_min, SOC_LIB=self.SOC_LIB)
        test_solver = SPPy.SPPySolver(b_cell=self.test_cell, N=self.N, isothermal=True, degradation=False)

        with self.assertRaises(TypeError) as context:
            test_solver.solve(cycler_instance=0)


class TestSPPySolverIsothermal(unittest.TestCase):
    """
    Test the values of the simulation in a isothermal simulation. The test are conducted in a single discharge step
    cycle.
    """
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    I = 1.656
    T = 298.15
    V_min = 4.0
    SOC_min = 0.1
    SOC_LIB = 0.9
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', SOC_init_p=SOC_init_p,
                                                         SOC_init_n=SOC_init_n, temp_init=T)
    test_solver = SPPy.SPPySolver(b_cell=test_cell, N=N, isothermal=True, degradation=False)
    dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    sol = test_solver.solve(cycler_instance=dc)

    def test_terminal_potential(self):
        """
        Test the battery cell terminal voltage.
        """
        self.assertEqual(4.017944458468085, self.sol.V[0])
        self.assertEqual(4.0178735493136415, self.sol.V[1])
        self.assertEqual(4.01780271676398, self.sol.V[2])
        self.assertEqual(4.017731960073281, self.sol.V[3])
        self.assertEqual(4.017661278502599, self.sol.V[4])

    def test_cell_temperature(self):
        """
        Test the battery cell temperatures.
        """
        self.assertEqual(298.15, self.sol.T[0])
        self.assertEqual(298.15, self.sol.T[1])
        self.assertEqual(298.15, self.sol.T[2])
        self.assertEqual(298.15, self.sol.T[3])
        self.assertEqual(298.15, self.sol.T[4])

    def test_poly_solver(self):
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        I = 1.656
        V_min = 3.5
        SOC_min = 0.1
        SOC_LIB = 0.9
        T = 298.15
        test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', SOC_init_p=SOC_init_p,
                                                             SOC_init_n=SOC_init_n, temp_init=T)
        dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
        test_solver = SPPy.SPPySolver(b_cell=self.test_cell, N=self.N, isothermal=True, degradation=False,
                                      electrode_SOC_solver="poly", type='two')
        sol = test_solver.solve(cycler_instance=dc)
        self.assertEqual(3.925178151483124, sol.V[0])
        print(sol.V)

class TestSppySolverNonIsothermal(unittest.TestCase):
    """
    Test the values of the simulation in a non-isothermal simulation. The test are conducted in a single discharge step
    cycle.
    """
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    I = 1.656
    T = 298.15
    V_min = 4.0
    SOC_min = 0.1
    SOC_LIB = 0.9
    test_cell = SPPy.BatteryCell.read_from_parametersets(parameter_set_name='test', SOC_init_p=SOC_init_p,
                                                         SOC_init_n=SOC_init_n, temp_init=T)
    test_solver = SPPy.SPPySolver(b_cell=test_cell, N=N, isothermal=False, degradation=False)
    dc = SPPy.Discharge(discharge_current=I, v_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    sol = test_solver.solve(cycler_instance=dc)

    def test_terminal_potential(self):
        """
        Test the battery cell terminal voltage.
        """
        self.assertEqual(4.017944458468085, self.sol.V[0])
        self.assertEqual(4.017873715136176, self.sol.V[1])
        self.assertEqual(4.017803045441758, self.sol.V[2])
        self.assertEqual(4.017732448639317, self.sol.V[3])
        self.assertEqual(4.017661923990237, self.sol.V[4])

    def test_cell_temperature(self):
        """
        Test the battery cell temperatures.
        """
        self.assertEqual(298.15007654854116, self.sol.T[0])
        self.assertEqual(298.15015162076287, self.sol.T[1])
        self.assertEqual(298.1502252195381, self.sol.T[2])
        self.assertEqual(298.1502973477614, self.sol.T[3])
        self.assertEqual(298.1503680083491, self.sol.T[4])

