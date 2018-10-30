import numpy as np

global_num_iterations=10
global_num_chains=4
global_random_seed=42

def compare_fit_objects(fit_stan, fit_generated_stan):
    #Check that the number of parameters are equal
    assert len(fit_stan._get_param_names()) == len(fit_generated_stan._get_param_names())
    for param_name in fit_stan._get_param_names():
        param_stan = fit_stan.extract(permuted=True)[param_name]
        param_generated_stan = fit_generated_stan.extract(permuted=True)[param_name]
        if(isinstance(param_stan,  np.ndarray)):
            assert np.all(param_stan == param_generated_stan)
        else:
            assert param_stan == param_generated_stan