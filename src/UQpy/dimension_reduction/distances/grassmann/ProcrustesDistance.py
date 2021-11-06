import numpy as np

from UQpy.dimension_reduction.distances.grassmann.baseclass.RiemannianDistance import (
    RiemannianDistance,
)
from UQpy.dimension_reduction.grassmann_manifold.GrassmannPoint import GrassmannPoint


class ProcrustesDistance(RiemannianDistance):
    """
    A class to calculate the Procrustes (chordal) distance between two  Grassmann points defined as:

    .. math::

        d_{C}(x_i, x_j) = 2[\sum_{l}\sin^2(\Theta_l/2)]^{1/2}

    """
    def compute_distance(self, xi: GrassmannPoint, xj: GrassmannPoint) -> float:
        """
        Compute the Procrustes (chordal) distance between two points on the Grassmann manifold.

        :param numpy.array xi: Orthonormal matrix representing the first subspace.
        :param numpy.array xj: Orthonormal matrix representing the second subspace.
        :rtype: float
        """
        RiemannianDistance.check_rows(xi, xj)

        rank_i = xi.data.shape[1]
        rank_j = xj.data.shape[1]

        r = np.dot(xi.data.T, xj.data)
        (ui, si, vi) = np.linalg.svd(r, full_matrices=True)
        si[np.where(si > 1)] = 1.0
        theta = np.arccos(si)
        sin_sq = np.sin(theta / 2) ** 2
        distance = 2 * np.sqrt(abs(rank_i - rank_j) + np.sum(sin_sq))

        return distance
