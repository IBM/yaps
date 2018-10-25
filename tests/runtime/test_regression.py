import pystan
import numpy as np
import yaps
from .utils import compare_fit_objects, global_num_chains,global_num_iterations,global_random_seed


def test_regression():
    stan_code = """
    data {
        int<lower=0> N;
        vector[N] x;
        vector[N] y;
        }
    parameters {
        real alpha;
        real beta;
        real<lower=0> sigma;
    }
    model {
        y ~ normal(alpha + beta * x, sigma);
        }
    """

    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)

    # Add Data
    num_samples = 100
    X = np.arange(num_samples)
    y = np.arange(num_samples)

    data = {'N': num_samples,
            'x': X,
            'y':y}

    # Compile and fit
    sm1 = pystan.StanModel(model_code=str(stan_code))
    fit_stan = sm1.sampling(data=data, iter=global_num_iterations, chains=global_num_chains, seed=global_random_seed)

    # Compile and fit
    sm2 = pystan.StanModel(model_code=str(generated_stan_code))
    fit_generated_stan = sm2.sampling(data=data, iter=global_num_iterations, chains=global_num_chains, seed=global_random_seed)

    compare_fit_objects(fit_stan, fit_generated_stan)

    # if matplotlib is installed (optional, not required), a visual summary and
    # traceplot are available
    #print(fit_stan)
    #import matplotlib.pyplot as plt
    #fit.plot()
    #plt.show()

