""" random_variables
Contains classes and functionalities pertaining to the random vectors.
"""

# __all__ = ['NormalRandomVector']
#
# __author__ = 'Moin Ahmed'
# __copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved.'
# __status__ = 'Development'
#
# from typing import Optional
#
# import numpy as np
# import numpy.typing as npt
#
#
# class NormalRandomVector:
#     """
#     Class for the normally distributed random vector
#     """
#
#     def __init__(self, vector_init: npt.ArrayLike, cov_init: npt.ArrayLike) -> None:
#         """
#         Class constructor
#         :param vector_init: row vector representing the mean
#         :param cov_init: covariance matrix
#         """
#         self._vector = None
#         self._cov = None
#         self.set_vector(vector_new=vector_init)
#         self.set_cov(cov_new=cov_init)
#
#     @classmethod
#     def _check_for_row_vector(cls, row_vector: npt.ArrayLike) -> None:
#         if not isinstance(row_vector, np.ndarray):
#             raise TypeError('row vector needs to be a numpy array and have a single column')
#         else:
#             if len(row_vector.shape) != 2:
#                 raise ValueError('row vector needs to be a nx1 vector')
#             else:
#                 if row_vector.shape[1] != 1:
#                     raise ValueError('row vector needs to have a single column')
#
#     @classmethod
#     def create_unit_normal_rv_sample(cls, vector_size: int) -> npt.ArrayLike:
#         return np.array([np.random.normal(loc=0.0, scale=1.0) for i in range(vector_size)]).reshape(-1, 1)
#
#     # @classmethod
#     # def create_normal_rv_sample(cls, mean: npt.ArrayLike, cov: npt.ArrayLike) -> npt.ArrayLike:
#     #     a = np.linalg.cholesky(cov)
#     #     return mean + a @ cls.create_unit_normal_rv_sample(vector_size=mean.shape[0])
#
#     def get_vector(self) -> Optional[npt.ArrayLike]:
#         return self._vector
#
#     def get_cov(self) -> npt.ArrayLike:
#         return self._cov
#
#     def set_vector(self, vector_new: npt.ArrayLike) -> None:
#         self._check_for_row_vector(row_vector=vector_new)
#         self._vector = vector_new
#
#     def set_cov(self, cov_new: npt.ArrayLike) -> None:
#         self._check_for_matrix(cov_new)
#         self._cov = cov_new
#
#     def _del_vector(self) -> None:
#         self._vector = None
#
#     def _del_cov(self) -> None:
#         self._cov = None
#
#     vector = property(get_vector, set_vector, _del_vector, 'vector containing expected values')
#     cov = property(get_cov, set_cov, _del_cov, 'covariance matrix')
#
#     @property
#     def dim(self) -> Optional[int]:
#         if self._vector is not None:
#             return self._vector.shape[0]
#         else:
#             return None
#
#     def _check_for_matrix(self, matrix) -> None:
#         if not isinstance(matrix, np.ndarray):
#             raise TypeError('matrix needs to be a nxn matrix')
#         else:
#             if len(matrix.shape) != 2:
#                 raise ValueError('matrix needs to have nxn matrix')
#             elif matrix.shape[0] != matrix.shape[1]:
#                 raise ValueError('matrix needs to be a square matrix')
#             elif matrix.shape[0] != self.dim:
#                 raise ValueError('matrix dimension do not matrix with the expected value')
#
#     def __repr__(self):
#         return f'vector {self._vector} and cov {self._cov}'
