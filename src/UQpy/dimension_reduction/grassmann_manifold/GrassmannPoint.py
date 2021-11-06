from typing import Annotated

from beartype import beartype
from beartype.vale import Is

from UQpy.utilities.ValidationTypes import Numpy2DFloatArrayOrthonormal, Numpy2DFloatArray
import numpy as np


class GrassmannPoint:
    @beartype
    def __init__(self, data: Numpy2DFloatArrayOrthonormal):
        """
        :param data: Orthonormal matrix containing the data of a point on the Grassmann manifold.
        """
        self._data = data

    @property
    def data(self) -> Numpy2DFloatArray:
        """
        The matrix containing the Grassmann point
        """
        return self._data


ListOfGrassmannPoints = Annotated[
    list[GrassmannPoint],
    Is[lambda points: all(point.data.shape[0] == points[0].data.shape[0] for point in points) and len(points) >= 2]]
