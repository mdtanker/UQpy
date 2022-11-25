from UQpy.sampling.mcmc.baseclass.MCMC import *
from abc import ABC


class TemperingMCMC(ABC):
    """
    Parent class to parallel and sequential tempering MCMC algorithms.

    To sample from the target distribution :math:`p(x)`, a sequence of intermediate densities
    :math:`p(x, \beta) \propto q(x, \beta) p_{0}(x)` for values of the parameter :math:`\beta` between 0 and 1,
    where :math:`p_{0}` is a reference distribution (often set as the prior in a Bayesian setting).
    Setting :math:`\beta = 1` equates sampling from the target, while
    :math:`\beta \rightarrow 0` samples from the reference distribution.

    **Inputs:**

    **Methods:**
    """

    def __init__(self, pdf_intermediate=None, log_pdf_intermediate=None, args_pdf_intermediate=(),
                 distribution_reference=None, save_log_pdf=True, random_state=None):
        self.logger = logging.getLogger(__name__)
        # Check a few inputs
        self.save_log_pdf = save_log_pdf
        self.random_state = process_random_state(random_state)

        # Initialize the prior and likelihood
        self.evaluate_log_intermediate = self._preprocess_intermediate(
            log_pdf_=log_pdf_intermediate, pdf_=pdf_intermediate, args=args_pdf_intermediate)
        if not (isinstance(distribution_reference, Distribution) or (distribution_reference is None)):
            raise TypeError('UQpy: if provided, input distribution_reference should be a UQpy.Distribution object.')
        # self.evaluate_log_reference = self._preprocess_reference(dist_=distribution_reference, args=())

        # Initialize the outputs
        self.samples = None
        self.intermediate_samples = None
        if self.save_log_pdf:
            self.log_pdf_values = None

    def run(self, nsamples):
        """ Run the tempering MCMC algorithms to generate nsamples from the target posterior """
        pass

    def evaluate_normalization_constant(self, **kwargs):
        """ Computes the normalization constant :math:`Z_{1}=\int{q_{1}(x) p_{0}(x)dx}` where p0 is the reference pdf
         and q1 is the intermediate density with :math:`\beta=1`, thus q1 p0 is the target pdf."""
        pass

    def _preprocess_reference(self, dist_, **kwargs):
        """
        Preprocess the target pdf inputs.

        Utility function (static method), that transforms the log_pdf, pdf, args inputs into a function that evaluates
        log_pdf_target(x) for a given x. If the target is given as a list of callables (marginal pdfs), the list of
        log margianals is also returned.

        **Inputs:**

        * dist_ (distribution object)

        **Output/Returns:**

        * evaluate_log_pdf (callable): Callable that computes the log of the target density function

        """
        # log_pdf is provided
        if dist_ is None:
            evaluate_log_pdf = None
        elif isinstance(dist_, Distribution):
            evaluate_log_pdf = (lambda x: dist_.log_pdf(x))
        else:
            raise TypeError('UQpy: A UQpy.Distribution object must be provided.')
        return evaluate_log_pdf

    @staticmethod
    def _preprocess_intermediate(log_pdf_, pdf_, args):
        """
        Preprocess the target pdf inputs.

        Utility function (static method), that transforms the log_pdf, pdf, args inputs into a function that evaluates
        log_pdf_target(x, beta) for a given x. If the target is given as a list of callables (marginal pdfs), the list of
        log margianals is also returned.

        **Inputs:**

        * log_pdf_ (callable): Log of the target density function from which to draw random samples. Either
          pdf_target or log_pdf_target must be provided.
        * pdf_ (callable): Target density function from which to draw random samples. Either pdf_target or
          log_pdf_target must be provided.
        * args (tuple): Positional arguments of the pdf target.

        **Output/Returns:**

        * evaluate_log_pdf (callable): Callable that computes the log of the target density function

        """
        # log_pdf is provided
        if log_pdf_ is not None:
            if not callable(log_pdf_):
                raise TypeError('UQpy: log_pdf_intermediate must be a callable')
            if args is None:
                args = ()
            evaluate_log_pdf = (lambda x, temper_param: log_pdf_(x, temper_param, *args))
        elif pdf_ is not None:
            if not callable(pdf_):
                raise TypeError('UQpy: pdf_intermediate must be a callable')
            if args is None:
                args = ()
            evaluate_log_pdf = (lambda x, temper_param: np.log(
                np.maximum(pdf_(x, temper_param, *args), 10 ** (-320) * np.ones((x.shape[0],)))))
        else:
            raise ValueError('UQpy: log_pdf_intermediate or pdf_intermediate must be provided')
        return evaluate_log_pdf

    @staticmethod
    def _target_generator(intermediate_logpdf_, reference_logpdf_, temper_param_):
        return lambda x: (reference_logpdf_(x) + intermediate_logpdf_(x, temper_param_))
