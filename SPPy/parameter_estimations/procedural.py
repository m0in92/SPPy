from typing import Union, Callable, Optional

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import scipy

import SPPy
from SPPy.calc_helpers.computational_intelligence_algorithms import GA


class OCVData:
    """
    This class finds the stociometric limits of the positive and the negative electrodes using the low C-rate
    battery cycling.
    Optimization is performed whereby the fitted OCV is compared with the experimental results
    """

    SOC_LIB_MIN = 0.0
    SOC_LIB_MAX = 1.0

    array_soc_lib = np.linspace(SOC_LIB_MIN, SOC_LIB_MAX)

    def __init__(self, func_ocp_p: Callable, func_ocp_n: Callable,
                 soc_n_min_1: float, soc_n_min_2: float,
                 soc_n_max_1: float, soc_n_max_2: float,
                 soc_p_min_1: float, soc_p_min_2: float,
                 soc_p_max_1: float, soc_p_max_2: float,
                 charge_or_discharge: str):
        """
        Constructor
        :param func_ocp_p: positive electrode OCP function
        :param func_ocp_n: negative electrode OCP function

        :soc_n_min_1: lower bound for negative electrode minimum SOC
        :soc_n_min_2: upper bound for negative electrode minimum SOC
        :soc_n_max_1: lower bound for negative electrode maximum SOC
        :soc_n_max_2: upper bound for negative electrode maximum SOC

        :soc_p_min_1: lower bound for positive electrode minimum SOC
        :soc_p_min_2: upper bound for positive electrode minimum SOC
        :soc_p_max_1: lower bound for positive electrode maximum SOC
        :soc_p_max_2: upper bound for positive electrode maximum SOC

        :charge_or_discharge: either 'charge' or 'discharge'
        """
        self.func_ocp_p = func_ocp_p
        self.func_ocp_n = func_ocp_n

        self.SOC_N_MIN_1 = soc_n_min_1
        self.SOC_N_MIN_2 = soc_n_min_2
        self.SOC_N_MAX_1 = soc_n_max_1
        self.SOC_N_MAX_2 = soc_n_max_2
        self.SOC_P_MIN_1 = soc_p_min_1
        self.SOC_P_MIN_2 = soc_p_min_2
        self.SOC_P_MAX_1 = soc_p_max_1
        self.SOC_P_MAX_2 = soc_p_max_2

        self.fitted_soc_n_min: Optional[float] = None
        self.fitted_soc_n_max: Optional[float] = None
        self.fitted_soc_p_min: Optional[float] = None
        self.fitted_soc_p_max: Optional[float] = None

        self.cycling_step: str = charge_or_discharge

    @staticmethod
    def _func_interp_ocp_exp(array_cap_exp: npt.ArrayLike, array_v_exp: npt.ArrayLike):
        return scipy.interpolate.interp1d(array_cap_exp, array_v_exp, fill_value="extrapolate")

    @classmethod
    def array_soc(cls, soc_min: float, soc_max: float) -> np.ndarray:
        return np.linspace(soc_min, soc_max)

    def array_ocp_p(self, soc_min: float, soc_max: float) -> np.ndarray:
        array_soc_p = self.array_soc(soc_min=soc_min, soc_max=soc_max)
        if self.cycling_step == 'discharge':
            return self.func_ocp_p(array_soc_p)
        elif self.cycling_step == 'charge':
            return np.flip(self.func_ocp_p(array_soc_p))
        else:
            raise TypeError('Unknown charging step.')

    def array_ocp_n(self, soc_min: float, soc_max: float) -> np.ndarray:
        array_soc_n = self.array_soc(soc_min=soc_min, soc_max=soc_max)
        if self.cycling_step == 'discharge':
            return np.flip(self.func_ocp_n(array_soc_n))
        elif self.cycling_step == 'charge':
            return self.func_ocp_n(array_soc_n)
        else:
            raise TypeError('Unknown charging step.')

    def _func_interp_ocp(self, soc_min: float, soc_max: float, interpolation_type: str) -> Callable:
        if interpolation_type == 'p':
            array_ocp_p_: npt.ArrayLike = self.array_ocp_p(soc_min=soc_min, soc_max=soc_max)
            return scipy.interpolate.interp1d(self.array_soc_lib, array_ocp_p_)
        elif interpolation_type == 'n':
            array_ocp_n_: npt.ArrayLike = self.array_ocp_n(soc_min=soc_min, soc_max=soc_max)
            return scipy.interpolate.interp1d(self.array_soc_lib, array_ocp_n_)

    @classmethod
    def ocv_lib(cls, ocp_p: float, ocp_n: float) -> float:
        return ocp_p - ocp_n

    def mse(self, array_v_exp: npt.ArrayLike, array_v_fit: npt.ArrayLike) -> float:
        return np.mean((array_v_exp - array_v_fit) ** 2)

    def find_optimized_parameters(self, array_cap_exp: npt.ArrayLike, array_v_exp_: npt.ArrayLike) -> np.ndarray:
        """
        Applies the genetic algorithm to find the optimized parameters for the stoiciometric limits.
        :param array_cap_exp: Array containing experimental capacity [Ahr].
        :param array_v_exp_: Array containing experimental voltage [V].
        :return: Array containing optimized parameters [SOC_P_MIN, SOC_P_MAX, SOC_N_MIN, SOC_N_MAX].
        """

        def func_obj(lst_param: list) -> float:
            # extract the params from the parameter set below
            soc_p_min, soc_p_max, soc_n_min, soc_n_max = lst_param[0], lst_param[1], lst_param[2], lst_param[3]

            # calculate the OCV of the LIB below
            array_ocp_p = self._func_interp_ocp(soc_min=soc_p_min, soc_max=soc_p_max,
                                                interpolation_type='p')(self.array_soc_lib)
            array_ocp_n = self._func_interp_ocp(soc_min=soc_n_min, soc_max=soc_n_max,
                                                interpolation_type='n')(self.array_soc_lib)
            array_ocv = self.ocv_lib(ocp_p=array_ocp_p, ocp_n=array_ocp_n)

            # MSE calculation below
            array_v_exp = self._func_interp_ocp_exp(array_cap_exp=array_cap_exp,
                                                    array_v_exp=array_v_exp_)(self.array_soc_lib)
            mse: float = self.mse(array_v_exp=array_v_exp, array_v_fit=array_ocv)
            return mse

        array_bounds: npt.ArrayLike = np.array([[self.SOC_P_MIN_1, self.SOC_P_MIN_2],
                                                [self.SOC_P_MAX_1, self.SOC_P_MAX_2],
                                                [self.SOC_N_MIN_1, self.SOC_N_MIN_2],
                                                [self.SOC_N_MAX_1, self.SOC_N_MAX_2]])
        result: np.ndarray = GA(n_chromosomes=100, bounds=array_bounds, obj_func=func_obj,
                                n_pool=7, n_elite=3, n_generations=10).solve()[0]
        self.fitted_soc_p_min = result[0]
        self.fitted_soc_p_max = result[1]
        self.fitted_soc_n_min = result[2]
        self.fitted_soc_n_max = result[3]
        return result

    @classmethod
    def get_soc(cls, soc_lib: Union[float, npt.ArrayLike],
                soc_p_min: float, soc_p_max: float,
                soc_n_min: float, soc_n_max: float) -> tuple[float, float]:
        """
        Returns a tuple which contains the values of positive and negative electrode SOC from the LIB SOC.
        :param soc_lib: state-of-charge of the lithium-ion battery
        :param soc_p_min: minimum state-of-charge of the positive electrode
        :param soc_p_max: maximum state-of-charge of the negative electrode
        :param soc_n_min: minimum state-of-charge of the positive electrode
        :param soc_n_max: maximum state-of-charge of the negative electode

        :return: (tuple[float, float]) soc of the positive and negative electrode, respectively.
        """
        array_soc_p = np.flip(np.linspace(soc_p_min, soc_p_max))
        array_soc_n = np.linspace(soc_n_min, soc_n_max)
        func_interpolation_soc_p = scipy.interpolate.interp1d(OCVData.array_soc_lib, array_soc_p)
        func_interpolation_soc_n = scipy.interpolate.interp1d(OCVData.array_soc_lib, array_soc_n)
        return func_interpolation_soc_p(soc_lib), func_interpolation_soc_n(soc_lib)

    def plot_fit(self,
                 cap_exp: Optional[npt.ArrayLike] = None,
                 v_exp: Optional[npt.ArrayLike] = None) -> None:
        array_ocp_p = self._func_interp_ocp(soc_min=self.fitted_soc_p_min, soc_max=self.fitted_soc_p_max,
                                            interpolation_type='p')(self.array_soc_lib)
        array_ocp_n = self._func_interp_ocp(soc_min=self.fitted_soc_n_min, soc_max=self.fitted_soc_n_max,
                                            interpolation_type='n')(self.array_soc_lib)
        array_ocv = self.ocv_lib(ocp_p=array_ocp_p, ocp_n=array_ocp_n)

        fig = plt.figure()

        ax1 = fig.add_subplot(111)
        ax1.plot(self.array_soc_lib, array_ocp_p, '--', label=r'${OCP_p}$')
        ax1.plot(self.array_soc_lib, array_ocp_n, '--', label=r'${OCP_n}$')
        ax1.plot(self.array_soc_lib, array_ocv, label=r'$OCV_{LIB}^{fit}$')

        if cap_exp is not None and v_exp is not None:
            ax1.plot(cap_exp, v_exp, label=r'$OCV_{LIB}^{exp}$')

            # MSE calculation below
            array_v_exp = self._func_interp_ocp_exp(array_cap_exp=cap_exp, array_v_exp=v_exp)(self.array_soc_lib)
            mse: float = self.mse(array_v_exp=array_v_exp, array_v_fit=array_ocv)
            ax1.set_title(f'MSE: {mse}')

        ax1.set_xlabel('Cap. [Ahr]')
        ax1.set_ylabel('V [V]')
        ax1.legend()
        plt.show()


class DriveCycleData:
    def __init__(self, b_cell: SPPy.BatteryCell, sol_exp: SPPy.Solution):
        self.b_cell = b_cell

    def func_obj_isothermal(self, lst_params):
        # Modify the battery cell parameters below
        self.b_cell.elec_n.SOC_init = lst_params[0]
        self.b_cell.elec_p.SOC_init = lst_params[1]
        self.b_cell.elec_n.D_ref = lst_params[2]
        self.b_cell.elec_p.D_ref = lst_params[3]
        self.b_cell.elec_n.R = lst_params[4]
        self.b_cell.elec_p.R = lst_params[5]
        self.b_cell.elec_n.k_ref = lst_params[6]
        self.b_cell.elec_p.k_ref = lst_params[7]
        self.b_cell.R_cell = lst_params[8]

        # set up solver and cycler
        cycler = SPPy.CustomCycler(t_array=0, I_array=0, SOC_LIB=1.0)
        solver = SPPy.SPPySolver(b_cell=self.b_cell, N=5, isothermal=True, degradation=False,
                                 electrode_SOC_solver='poly')

    def ga(self):
        pass
