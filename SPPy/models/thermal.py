__all__ = ["Lumped", "ECMLumped"]

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'


from typing import Callable

from SPPy.battery_components.battery_cell import BatteryCell


class Lumped:
    def __init__(self, b_cell: BatteryCell):
        # check for input arguments
        if not isinstance(b_cell, BatteryCell):
            raise TypeError("b_cell input argument needs to be a BatteryCell object.")
        # Assign class atributes
        self.b_cell = b_cell

    def reversible_heat(self, I: float, T: float) -> float:
        return I * T * (self.b_cell.elec_p.dOCPdT - self.b_cell.elec_n.dOCPdT)

    def irreversible_heat(self, I: float, V: float) -> float:
        return I * (V - (self.b_cell.elec_p.OCP - self.b_cell.elec_n.OCP))

    def heat_flux(self, T: float) -> float:
        return self.b_cell.h * self.b_cell.A * (T - self.b_cell.T_amb)

    def heat_balance(self, V: float, I: float) -> Callable:
        def func_heat_balance(T: float, t: float) -> float:
            main_coeff = 1 / (self.b_cell.rho * self.b_cell.Vol * self.b_cell.C_p)
            return main_coeff * (self.reversible_heat(I=I, T=T) + self.irreversible_heat(I=I, V=V) - self.heat_flux(T=T))
        return func_heat_balance


class ECMLumped:
    def reversible_heat(self, I: float, T: float, dOCVdT: float) -> float:
        return I * T * dOCVdT

    def irreversible_heat(self, I: float, V: float, OCV: float) -> float:
        return I * (V - OCV)

    def heat_flux(self, T: float, h: float, A: float, T_amb: float):
        return h * A * (T - T_amb)

    def heat_balance(self, V: float, I: float, rho: float, Vol: float, C_p: float,
                     OCV: float, dOCVdT: float, h: float, A: float, T_amb: float) -> Callable:
        def func_heat_balance(T: float, t: float) -> float:
            main_coeff: float = 1 / (rho * Vol * C_p)
            return main_coeff * (self.reversible_heat(I=I, T=T, dOCVdT=dOCVdT) + \
                                 self.irreversible_heat(I=I, V=V, OCV=OCV) - \
                                 self.heat_flux(T=T, h=h, A=A, T_amb=T_amb))
        return func_heat_balance
