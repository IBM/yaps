import pystan
import numpy as np
import yaps
from .utils import compare_fit_objects, global_num_chains,global_num_iterations,global_random_seed


def test_missing_data():
    stan_code = """
        data {
        int<lower=0> N_obs;
        int<lower=0> N_mis;
        real y_obs[N_obs];
        }
        parameters {
        real mu;
        real<lower=0> sigma;
        real y_mis[N_mis];
        }
        model {
        y_obs ~ normal(mu, sigma);
        y_mis ~ normal(mu, sigma);
        }
    """

    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)

    # Add Data
    num_samples = 6
    X = np.array([5, 6, 1, 0, 9, 10])

    data = {'N_obs': num_samples,
            'N_mis': 2,
            'y_obs': X}

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

if __name__ == "__main__":
    test_missing_data()
