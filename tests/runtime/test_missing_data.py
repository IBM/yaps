import numpy as np
from .utils import compare_models


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

    num_samples = 6
    X = np.array([5, 6, 1, 0, 9, 10])

    data = {'N_obs': num_samples,
            'N_mis': 2,
            'y_obs': X}

    compare_models(stan_code, data)


if __name__ == "__main__":
    test_missing_data()
