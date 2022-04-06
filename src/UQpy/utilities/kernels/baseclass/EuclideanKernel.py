import itertools
from abc import ABC, abstractmethod
from typing import Union
import scipy.spatial.distance as sd
import numpy as np

from UQpy.utilities import GrassmannPoint
from UQpy.utilities.ValidationTypes import NumpyFloatArray, Numpy2DFloatArray
from UQpy.utilities.kernels.baseclass.Kernel import Kernel


class EuclideanKernel(Kernel, ABC):
    """This is a blueprint for Euclidean kernels implemented in the :py:mod:`kernels` module ."""

    def __init__(self):
        super().__init__()

    def calculate_kernel_matrix(self, points: Numpy2DFloatArray):
        """
        Using the kernel-specific :py:meth:`.kernel_entry` method, this function assembles the kernel matrix.

        :param points: Set of data points in the Euclidean space

        """
        distance_pairs = None
        if len(np.shape(points)) == 2:
            distance_pairs = sd.pdist(points, "sqeuclidean")

        elif len(np.shape(points)) == 3:
            nargs = len(points)
            indices = range(nargs)
            pairs = list(itertools.combinations(indices, 2))
            distance_pairs = []
            for id_pair in range(np.shape(pairs)[0]):
                i = pairs[id_pair][0]
                j = pairs[id_pair][1]

                xi = points[i]
                xj = points[j]

                distance_pairs.append(self.kernel_entry(xi, xj))

        self.kernel_matrix = self.kernel_function(distance_pairs)

    @abstractmethod
    def kernel_function(self, distance_pairs):
        pass
