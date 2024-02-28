__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'

import numpy as np

from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.degradation import ROMSEI


class ROMSEISolver(ROMSEI):
    def __init__(self, b_cell: BatteryCell, thickness_SEI_init: float = 0.0):
        """
        This class stores and solves for parameters related to the SEI degradation. The degradations are calculated
        ONLY during charge cycles, i.e. when the applied current > 0.
        :param b_cell: BatteryCell instance
        :param thickness_SEI_init: initial SEI thickness
        """
        if not isinstance(b_cell, BatteryCell):
            raise TypeError("b_cell needs to be BatteryCell Type.")
        self.k_n = b_cell.elec_n.k  # rate of reaction at the negative electrode [m2.5/mol0.5/s]
        self.c_e = b_cell.electrolyte.conc  # electrolyte conc. [mol/m3]
        self.S_n = b_cell.elec_n.S  # electrode electrochemical area [mol/m2]
        self.c_nmax = b_cell.elec_n.max_conc  # electrode max. Li. conc. [mol/m3]
        self.U_s = b_cell.elec_n.U_s  # SEI reference potential [V]
        self.i_s = b_cell.elec_n.i_s  # SEI exchange current density [mol/m2/s]
        self.A = b_cell.elec_n.A  # electrode area [m2]

        self.MW_SEI = b_cell.elec_n.MW_SEI  # SEI molar weight [kg/m3]
        self.rho = b_cell.elec_n.rho_SEI  # SEI density [kg/m3]
        self.kappa = b_cell.elec_n.kappa_SEI  # SEI conductivity [S/m]

        self.L = thickness_SEI_init  # initial SEI thickness [m]
        self.J_tot = 0  # total lithium-ion flux [mol/m2/s], initialized to zero
        self.J_i = 0  # intercalation lithium-ion flux [mol/m2/s] initialized to zero
        self.J_s = 0  # SEI side reaction flux [mol/m2/s], initialized to zero
        self.cumulative_J_s = 0  # cumulative SEI side reaction flux [mol/m2], initialized to zero.

    def solve_current(self, soc: float, ocp: float, temp: float, I: float, rel_tol: float = 1e-12,
                      max_iter_no: int = 10) -> tuple[float, float]:
        """
        Returns the currents consumed for intercalation and side reactions.
        :param SOC_n:
        :param OCP_n:
        :param temp:
        :param I:
        :param iter_no:
        :return: tuple containing the intercalation current [A] and side-reaction current [A]
        """
        J_s = self.J_s = 0
        J_tot = self.J_tot = self.J_i = self.calc_j_tot(I=I, S=self.S_n)
        if I > 0:
            j_0_i: float = self.calc_j_0_i(k=self.k_n, c_s_max=self.c_nmax,
                                           c_e=self.c_e, soc=soc)
            rel_error = 1
            iter = 0
            while rel_error > rel_tol:
                J_i: float = self.calc_j_i(j_tot=J_tot, j_s=J_s)
                eta_n: float = self.calc_eta_n(temp=temp, j_i=J_i, j_0_i=j_0_i)
                eta_s: float = self.calc_eta_s(eta_n=eta_n, ocp_n=ocp, ocp_s=self.U_s)
                J_s_prev: float = J_s
                J_s: float = self.calc_j_s(temp=temp, j_0_s=self.i_s, eta_s=eta_s)

                rel_error = np.abs((J_s - J_s_prev) / J_s)
                iter += 1
                if iter > max_iter_no:
                    break
            I_i: float = self.flux_to_current(molar_flux=J_i, S=self.S_n)
            I_s: float = self.flux_to_current(molar_flux=J_s, S=self.S_n)
            self.J_i = J_i
            self.J_s = J_s
            self.cumulative_J_s += self.J_s  # update the cumulative side reaction flux [mol/m2].
            return I_i, I_s
        else:
            return I, 0  # in case of discharge, there is no side reaction current.

    def solve_delta_L(self, J_s, dt):
        return -(self.MW_SEI * J_s / self.rho) * dt

    def update_L(self, J_s, dt):
        self.L += self.solve_delta_L(J_s=J_s, dt=dt)

    def solve_delta_R_SEI_(self, J_s, dt):
        """
        Calculates the change in the SEI resistance [ohm m2]
        :param J_s:
        :param dt:
        :return:
        """
        return self.solve_delta_L(J_s=J_s, dt=dt) / self.kappa

    def solve_delta_R_SEI(self, J_s, dt):
        return self.solve_delta_R_SEI_(J_s=J_s, dt=dt) / self.A

    @property
    def R_SEI_(self):
        """
        The resistance of the SEI layer [ohm m2]
        :return:
        """
        return self.L / self.kappa

    @property
    def R_SEI(self):
        """
        SEI film resistance [ohm]
        :return: (float) SEI film resistance [ohm]
        """
        return self.R_SEI_ / self.A

    def __call__(self, SOC_n: float, OCP_n: float, temp: float, I: float, dt: float,
                 rel_tol: float = 1e-6, max_iter_no: int = 10):
        I_i, I_s = self.solve_current(SOC_n=SOC_n, OCP_n=OCP_n, temp=temp, I=I, rel_tol=rel_tol)
        delta_R_SEI = self.solve_delta_R_SEI(J_s=self.J_s, dt=dt)
        self.update_L(J_s=self.J_s, dt=dt)
        return I_i, I_s, delta_R_SEI

    def __repr__(self):
        return f"SEI with resistance {self.R_SEI}"
