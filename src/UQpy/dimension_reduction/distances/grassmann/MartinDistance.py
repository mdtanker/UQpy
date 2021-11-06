import numpy as np
import sys
from UQpy.dimension_reduction.distances.grassmann.baseclass.RiemannianDistance import (
    RiemannianDistance,
)
from UQpy.dimension_reduction.grassmann_manifold.GrassmannPoint import GrassmannPoint


class MartinDistance(RiemannianDistance):
    """
    A class to calculate the Martin distance between two  Grassmann points defined as:

    .. math::

        d_{M}(x_i, x_j) = [\log\prod_{l}1/\cos^2(\Theta_l)]^{1/2}

    """
    def compute_distance(self, xi: GrassmannPoint, xj: GrassmannPoint) -> float:
        """
        Compute the Martin distance between two points on the Grassmann manifold.

        :param numpy.array xi: Orthonormal matrix representing the first subspace.
        :param numpy.array xj: Orthonormal matrix representing the second subspace.
        :rtype: float
        """
        RiemannianDistance.check_rows(xi, xj)

        r = np.dot(xi.data.T, xj.data)
        (ui, si, vi) = np.linalg.svd(r, full_matrices=True)
        si[np.where(si > 1)] = 1.0
        theta = np.arccos(si)
        cos_sq = np.cos(theta) ** 2
        float_min = sys.float_info.min
        index = np.where(cos_sq < float_min)
        cos_sq[index] = float_min
        recp = np.reciprocal(cos_sq)
        distance = np.sqrt(np.log(np.prod(recp)))

        return distance
