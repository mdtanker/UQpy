from UQpy.inference import *
from UQpy.RunModel import RunModel
from UQpy.inference.inference_models.ComputationalModel import ComputationalModel
from UQpy.sampling.mcmc import MetropolisHastings
from UQpy.distributions.collection.Normal import Normal
from UQpy.distributions.collection.JointIndependent import JointIndependent
import shutil


def test_models():
    data_ex1 = np.loadtxt('data_ex1a.txt')

    runmodel4 = RunModel(model_script='pfn.py', model_object_name='model_linear', vec=False, var_names=['theta_0'])
    runmodel5 = RunModel(model_script='pfn1.py', model_object_name='model_quadratic', vec=False,
                         var_names=['theta_0', 'theta_1'])
    runmodel6 = RunModel(model_script='pfn2.py', model_object_name='model_cubic', vec=False,
                         var_names=['theta_0', 'theta_1', 'theta_2'])

    prior1 = Normal()
    prior2 = JointIndependent(marginals=[Normal(), Normal()])
    prior3 = JointIndependent(marginals=[Normal(), Normal(), Normal()])

    model_n_params = [1, 2, 3]
    model1 = ComputationalModel(parameters_number=1, runmodel_object=runmodel4, prior=prior1,
                                error_covariance=np.ones(50), name='model_linear')
    model2 = ComputationalModel(parameters_number=2, runmodel_object=runmodel5, prior=prior2,
                                error_covariance=np.ones(50), name='model_quadratic')
    model3 = ComputationalModel(parameters_number=3, runmodel_object=runmodel6, prior=prior3,
                                error_covariance=np.ones(50), name='model_cubic')

    proposals = [Normal(0, 10),
                 JointIndependent([Normal(0, 1), Normal(0, 1)]),
                 JointIndependent([Normal(0, 1), Normal(0, 2), Normal(0.025)])]

    # sampling =
    mh1 = MetropolisHastings.create_for_inference(inference_model=model1, data=data_ex1, jump=1, burn_length=500,
                                                  proposal=proposals[0], random_state=0, seed=[0.])
    mh2 = MetropolisHastings.create_for_inference(inference_model=model2, data=data_ex1, jump=1, burn_length=500,
                                                  proposal=proposals[1], random_state=0, seed=[0., 0.])
    mh3 = MetropolisHastings.create_for_inference(inference_model=model3, data=data_ex1, jump=1, burn_length=500,
                                                  proposal=proposals[2], random_state=0, seed=[0., 0., 0.])

    selection = BayesModelSelection(candidate_models=[model1, model2, model3],
                                    data=data_ex1,
                                    sampling_class=[mh1, mh2, mh3],
                                    prior_probabilities=[1. / 3., 1. / 3., 1. / 3.],
                                    samples_number=[2000, 2000, 2000])

    selection.sort_models()
    assert selection.probabilities[0] == 1.0
    assert selection.probabilities[1] == 0.0
    assert selection.probabilities[2] == 0.0

    assert selection.candidate_models[0].name == 'model_quadratic'
    assert selection.candidate_models[1].name == 'model_cubic'
    assert selection.candidate_models[2].name == 'model_linear'

    shutil.rmtree(runmodel4.model_dir)
    shutil.rmtree(runmodel5.model_dir)
    shutil.rmtree(runmodel6.model_dir)
