import numpy as np
from pycmdstan.model import Model
import pycmdstan
import yaps

global_num_iterations = 10
global_random_seed = 42


def compare_fit_objects(fit_stan, fit_generated_stan):
    # Check that the number of parameters are equal
    assert len(fit_stan.csv) == len(fit_generated_stan.csv)
    for param_name in fit_stan.csv:
        param_stan = fit_stan.csv[param_name]
        param_generated_stan = fit_generated_stan.csv[param_name]
        if(isinstance(param_stan,  np.ndarray)):
            assert np.all(param_stan == param_generated_stan)
        else:
            assert param_stan == param_generated_stan


def compare_models(stan_code, data, **kwargs):
    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)
    # Compile and fit original code
    sm1 = Model(code=str(stan_code))
    fit_stan = sm1.sample(**kwargs,
                          data=data,
                          num_samples=global_num_iterations,
                          random_='seed={}'.format(global_random_seed))
    # Compile and fit generated code
    sm2 = Model(code=str(generated_stan_code))
    fit_generated_stan = sm2.sample(**kwargs,
                                    data=data,
                                    num_samples=global_num_iterations,
                                    random_='seed={}'.format(global_random_seed))
    # Compare results
    compare_fit_objects(fit_stan, fit_generated_stan)
