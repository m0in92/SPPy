from typing import Callable

import numpy as np


def func_eta(soc: float, temp: float) -> float:
    return 1.0

# the functions below were estimated from the create_and_save_OCV.py module
func_ocv: Callable = np.poly1d(np.array([7.83002260e+03, -4.72721395e+04, 1.25237092e+05, -1.91403553e+05,
                                         1.86656077e+05, -1.21342077e+05, 5.33553293e+04, -1.57665852e+04,
                                         3.04748964e+03, -3.65636105e+02, 2.50281588e+01, 2.93438431e+00]))

func_docvdtemp: Callable = np.poly1d(np.array([-1.62911207e+01, 9.66871309e+01, -2.50145828e+02, 3.70280039e+02,
                                              -3.46021781e+02, 2.12461660e+02, -8.64646004e+01, 2.29561374e+01,
                                              -3.80515739e+00, 3.58298325e-01, -1.40044753e-02, -6.86713653e-04]))
