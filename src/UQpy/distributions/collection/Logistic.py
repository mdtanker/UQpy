from typing import Union

import scipy.stats as stats
from beartype import beartype

from UQpy.distributions.baseclass import DistributionContinuous1D


class Logistic(DistributionContinuous1D):
    """
    Logistic distribution having probability density function

    .. math:: f(x) = \dfrac{\exp(-x)}{(1+\exp(-x))^2}

    In this standard form `(loc=0, scale=1)`. Use `loc` and `scale` to shift and scale the distribution. Specifically,
    this is equivalent to computing :math:`f(y)` where :math:`y=(x-loc)/scale`.

    **Inputs:**

    * **loc** (`float`):
        location parameter
    * **scale** (`float`):
        scale parameter

    The following methods are available for ``Logistic``:

    * ``cdf``, ``pdf``, ``log_pdf``, ``icdf``, ``rvs``, ``moments``, ``fit``.
    """
    @beartype
    def __init__(self, loc: Union[None, float, int] = 0., scale: Union[None, float, int] = 1.):
        super().__init__(loc=loc, scale=scale, ordered_parameters=('loc', 'scale'))
        self._construct_from_scipy(scipy_name=stats.logistic)

