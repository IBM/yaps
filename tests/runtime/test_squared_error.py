import numpy as np
from .utils import compare_models


def test_squared_error():
    stan_code = """
        data {
        int<lower=0> N;
        int<lower=1> K;
        vector[N] y;
        matrix[N,K] x;
        }
        parameters {
        vector[K] beta;
        }
        transformed parameters {
        real<lower=0> squared_error;
        squared_error = dot_self(y - x * beta);
        }
        model {
        target += -squared_error;
        }
        generated quantities {
        real<lower=0> sigma_squared;
        sigma_squared = squared_error / N;
        }
    """

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

    compare_models(stan_code, data)


test_squared_error()
