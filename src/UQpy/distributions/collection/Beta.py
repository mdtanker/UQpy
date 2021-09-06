from typing import Union

import scipy.stats as stats
from UQpy.distributions.baseclass import DistributionContinuous1D
from beartype import beartype


class Beta(DistributionContinuous1D):
    """
    Beta distribution having probability density function

    .. math:: f(x|a,b) = \dfrac{ \Gamma(a+b)x^{a-1}(1-x)^{b-1}}{\Gamma(a) \Gamma(b)}

    for :math:`0 \le x \ge 0`, :math:`a > 0, b > 0`. Here :math:` \Gamma(a)` refers to the Gamma function.

    In this standard form `(loc=0, scale=1)`, the distribution is defined over the interval (0, 1). Use `loc` and
    `scale` to shift the distribution to interval `(loc, loc + scale)`. Specifically, this is equivalent to computing
    :math:`f(y|a,b)` where :math:`y=(x-loc)/scale`.

    **Inputs:**

    * **a** (`float`):
        first shape parameter
    * **b** (float):
        second shape parameter
    * **loc** (`float`):
        location parameter
    * **scale** (`float`):
        scale parameter

    The following methods are available for ``Beta``:

    * ``cdf``, ``pdf``, ``log_pdf``, ``icdf``, ``rvs``, ``moments``, ``fit``
    """
    @beartype
    def __init__(self, a: Union[None, float, int], b: Union[None, float, int],
                 loc: Union[None, float, int] = 0., scale: Union[None, float, int] = 1.):
        super().__init__(a=a, b=b, loc=loc, scale=scale, ordered_parameters=('a', 'b', 'loc', 'scale'))
        self._construct_from_scipy(scipy_name=stats.beta)
