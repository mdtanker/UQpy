import itertools
from abc import ABC, abstractmethod
from typing import Union

import numpy as np

from UQpy.utilities import GrassmannPoint
from UQpy.utilities.ValidationTypes import NumpyFloatArray, Numpy2DFloatArray


class Kernel(ABC):
    """
    This is the baseclass for all kernels in :py:mod:`UQpy`.

    This serves a blueprint to show the methods for kernels implemented in the :py:mod:`.kernels` module .
    """
    def __init__(self):
        self.kernel_matrix = None
        """Kernel matrix defining the similarity between the points"""

    def calculate_kernel_matrix(self, points: Union[list, NumpyFloatArray]):
        """
        Using the kernel-specific :py:meth:`.kernel_entry` method, this function assembles the kernel matrix.
        """
        pass

    @abstractmethod
    def kernel_entry(self, xi: Union[Numpy2DFloatArray, GrassmannPoint],
                     xj: Union[Numpy2DFloatArray, GrassmannPoint]):
        """
        Given two points, this method calculates the respective kernel entry. Each concrete kernel implementation must
        override this method and provide its own implementation.

        :param xi: First point.
        :param xj: Second point.
        :return: Float representing the kernel entry.
        """
        pass
