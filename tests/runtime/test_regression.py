import numpy as np
from .utils import compare_models


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

    num_samples = 100
    X = np.arange(num_samples)
    y = np.arange(num_samples)

    data = {'N': num_samples,
            'x': X,
            'y': y}

    compare_models(stan_code, data)
