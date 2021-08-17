import scipy.stats as stats
from beartype import beartype

from UQpy.distributions.baseclass import DistributionContinuous1D


class Pareto(DistributionContinuous1D):
    """
    Pareto distribution having probability density function

    .. math:: f(x|b) = \dfrac{b}{x^{b+1}}

    for :math:`x\ge 1, b>0`.

    In this standard form `(loc=0, scale=1)`. Use `loc` and `scale` to shift and scale the distribution. Specifically,
    this is equivalent to computing :math:`f(y)` where :math:`y=(x-loc)/scale`.

    **Inputs:**

    * **b** (`float`):
        shape parameter
    * **loc** (`float`):
        location parameter
    * **scale** (`float`):
        scale parameter

    The following methods are available for ``Pareto``:

    * ``cdf``, ``pdf``, ``log_pdf``, ``icdf``, ``rvs``, ``moments``, ``fit``.
    """
    @beartype
    def __init__(self, shape_parameter: float, location: float = 0., scale: float = 1.):
        super().__init__(b=shape_parameter, loc=location, scale=scale,
                         ordered_parameters=('shape_parameter', 'location', 'scale'))
        self._construct_from_scipy(scipy_name=stats.pareto)
