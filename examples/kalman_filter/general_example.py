"""
This is an example of SPKF from Plett's book "Battery Management System. vol 2".

x_{k+1} = f(x_k, u_k, w_k) = sqrt(5+x_k) + w_k
y_k = h(x_k, u_k, v_k) = x_3 ** 3 + v_k

"""

import numpy as np
import scipy.linalg
import matplotlib.pyplot as plt

from SPPy.calc_helpers.kalman_filter import NormalRandomVector, SigmaPointKalmanFilter


# The functions below defines the state and output equations. These will be inputs for the SigmaPointKalmanFilter
# instance parameters.
def state_func(x_k, u_k, w_k):
    return np.sqrt(5 + x_k) + w_k


def output_func(x_k, u_k, v_k):
    return x_k**3 + v_k


# Create NormalRandomVector instances. They will be used as the inputs for the SigmaPointClass class instances.
X: NormalRandomVector = NormalRandomVector(vector_init=np.array([[2]]), cov_init=np.array([[1]]))
W: NormalRandomVector = NormalRandomVector(vector_init=np.array([[0]]), cov_init=np.array([[1]]))
V: NormalRandomVector = NormalRandomVector(vector_init=np.array([[0]]), cov_init=np.array([[1]]))

max_iter: int = 40

# Define the size of variables in the model
Nx: float = 1
Ny: float = 1

# Initialize simulation variables
xhat: float = 2
SigmaX: float = 1
SigmaW: float = 1
SigmaV: float = 2
max_iter: int = 100

# simulate true signals
# -------------- Create true values ----------------------------------------
v_vector: np.ndarray = np.random.normal(loc=0, scale=2, size=(max_iter,))
w_vector: np.ndarray = np.random.normal(loc=0, scale=1, size=(max_iter,))
# x_true_0: float = np.random.normal(loc=2, scale=1)
x_true: np.ndarray = np.zeros(max_iter)                                             # true state array
# x_true[0] = x_true_0
for i in range(max_iter):
    x_true[i] = state_func(x_true[i], 0, w_vector[i])
y_true = np.zeros(max_iter)                                                       # true output array
for i in range(max_iter):
    y_true[i] = output_func(x_true[i], 0, v_vector[i])
u: np.ndarray = np.zeros(max_iter)                                                  # input array
# ------------------------------------------------------------------------

# setup SPKF object
spkf_obj: SigmaPointKalmanFilter = SigmaPointKalmanFilter(x=X, w=W, v=V, y_dim=1,
                                                          state_equation=state_func,
                                                          output_equation=output_func)

# below is the sigma-point Kalman filter
x_calc: np.ndarray = np.zeros(max_iter)
for i in range(max_iter):
    spkf_obj.solve(u=u[i], y_true=y_true[i])
    x_calc[i] = spkf_obj.x.vector
    print(x_calc[i], x_true[i], y_true[i])

# plots
t = np.arange(max_iter)
plt.plot(t, x_true, label="true")
plt.plot(t, x_calc, label="calc.")

plt.xlabel('time [s]')
plt.ylabel('state value [a.u.]')
plt.legend()
plt.show()
