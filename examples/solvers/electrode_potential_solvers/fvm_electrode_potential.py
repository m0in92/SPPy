"""
This script demonstrates the example usage of the solid phase electrode potential using the finite volume method (FVM).
"""

from SPPy.solvers.co_ordinates import ElectrolyteFVMCoordinates
from SPPy.solvers.electrode_potential import ElectrodePotentialFVMSolver


L_n: float = 8e-5
L_s: float = 2.5e-5
L_p: float = 8.8e-5

a_s_p: float = 7.28e3
a_s_n: float = 5.78e3

electrode_type_p: str = 'p'

coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
