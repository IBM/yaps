import pystan
import numpy as np
import yaps
from .utils import compare_fit_objects, global_num_chains,global_num_iterations,global_random_seed


def test_regression_matrix():
    stan_code = """
    data {
        int<lower=0> N;
        int<lower=0> K;
        matrix[N, K] x;
        vector[N] y;
    }
    parameters {
        real alpha;
        vector[K] beta;
        real<lower =0> sigma;
    }
    model {
        y ~ normal(x * beta + alpha, sigma);
    }
    """

    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)

    # Add Data
    num_samples = 100
    num_features = 2
    #X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    X = np.random.randint(5, size=(100, 2))
    # y = 1 * x_0 + 2 * x_1 + 3
    y = np.dot(X, np.array([1, 2])) + 3

    data = {'N': num_samples,
            'K': num_features,
            'x': X,
            'y': y}

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

test_regression_matrix()
